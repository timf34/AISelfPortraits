"""The agentic session: tools, loop, artifact resolution, transcript."""

import json
import tempfile
from pathlib import Path

from aiportraits.client import ChatResult, OpenRouterClient, OpenRouterError, ToolCall
from aiportraits.config import BASH_TIMEOUT_S, MAX_NUDGES, MAX_TURNS
from aiportraits.prompts import NUDGE, build_messages
from aiportraits.renderers import RenderResult, render
from aiportraits.sandbox import Sandbox

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "bash",
            "description": (
                "Run a bash command in your /workspace sandbox "
                f"(Python 3.12, Pillow, numpy; no network; {BASH_TIMEOUT_S}s timeout)."
            ),
            "parameters": {
                "type": "object",
                "properties": {"command": {"type": "string", "description": "The command to run"}},
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "render",
            "description": (
                "Rasterize an .svg, .html, or .js file from /workspace to a PNG and "
                "report whether it rendered cleanly (JS files run against a 500x500 "
                "canvas with id \"canvas\")."
            ),
            "parameters": {
                "type": "object",
                "properties": {"file": {"type": "string", "description": "Path of the file, e.g. /workspace/portrait.svg"}},
                "required": ["file"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "finish",
            "description": "End the session when you are happy with your final piece.",
            "parameters": {
                "type": "object",
                "properties": {"note": {"type": "string", "description": "Optional closing note"}},
                "required": [],
            },
        },
    },
]

_RENDER_EXTS = {".svg": "svg", ".html": "html", ".js": "javascript"}


def _exec_render(sandbox: Sandbox, file: str, out_png: Path) -> tuple[RenderResult | None, str]:
    """Copy a file out of the sandbox and rasterize it. Returns (result, observation)."""
    path = file if file.startswith("/") else f"/workspace/{file}"
    lang = _RENDER_EXTS.get(Path(path).suffix.lower())
    if lang is None:
        return None, f"render only supports {', '.join(_RENDER_EXTS)} files (got {path!r})"
    with tempfile.TemporaryDirectory() as tmp:
        local = Path(tmp) / Path(path).name
        if not sandbox.copy_out(path, local):
            return None, f"file not found in sandbox: {path}"
        result = render(lang, local.read_text(), out_png, resize=False)
    if result.ok:
        return result, f"rendered OK: {result.image_size[0]}x{result.image_size[1]} PNG"
    return result, f"render failed: {result.error}"


def _resolve_artifact(sandbox: Sandbox, language: str, exp_dir: Path) -> dict:
    """After the session: find the model's final piece and produce portrait.png.
    Prefers the language's target file, then any file of that type, then any image."""
    files = sandbox.list_files()
    ext_of = lambda f: Path(f).suffix.lower()

    def candidates() -> list[str]:
        image_exts = [".png", ".jpg", ".jpeg", ".bmp", ".gif"]
        if language == "python" or language == "free":
            order = [f for f in files if f == "/workspace/portrait.png"]
            order += [f for f in files if ext_of(f) in image_exts and f not in order]
            order += [f for f in files if ext_of(f) in _RENDER_EXTS]
            return order
        target = f"/workspace/portrait{_ext_for(language)}"
        order = [f for f in files if f == target]
        order += [f for f in files if ext_of(f) == _ext_for(language) and f not in order]
        # Off-contract fallbacks, better than nothing:
        order += [f for f in files if ext_of(f) in image_exts]
        return order

    out_png = exp_dir / "portrait.png"
    resize = language != "free"
    for path in candidates():
        if ext_of(path) in _RENDER_EXTS:
            with tempfile.TemporaryDirectory() as tmp:
                local = Path(tmp) / Path(path).name
                if not sandbox.copy_out(path, local):
                    continue
                result = render(_RENDER_EXTS[ext_of(path)], local.read_text(), out_png, resize=resize)
            if result.ok:
                return {"artifact": path, "image_size": result.image_size,
                        "resized_from": result.resized_from, "render_error": None}
        else:
            if sandbox.copy_out(path, out_png):
                result = render_image_file(out_png, resize=resize)
                if result.ok:
                    return {"artifact": path, "image_size": result.image_size,
                            "resized_from": result.resized_from, "render_error": None}
    return {"artifact": None, "image_size": None, "resized_from": None,
            "render_error": "no usable image or renderable file found in /workspace"}


def _ext_for(language: str) -> str:
    from aiportraits.config import LANGUAGES

    return LANGUAGES[language].ext


def render_image_file(png: Path, resize: bool) -> RenderResult:
    from aiportraits.renderers import finalize_image_file

    return finalize_image_file(png, resize=resize)


def run_agent(client: OpenRouterClient, model: str, variant: str, language: str, exp_dir: Path) -> dict:
    """Run one full agentic session. Returns metadata (without writing it)."""
    sandbox = Sandbox()
    meta: dict = {"turns": [], "status": "running"}
    messages = build_messages(variant, language)
    nudges = 0
    finished = False
    finish_note = None
    scratch_render = exp_dir / "render_preview.png"

    try:
        for _ in range(MAX_TURNS):
            try:
                result: ChatResult = client.chat(model, messages, tools=TOOLS)
            except OpenRouterError as e:
                meta["status"] = "failed_api"
                meta["api_error"] = str(e)
                break
            turn: dict = {
                "text": result.text,
                "latency_s": result.latency_s,
                "usage": result.usage,
                "tool_calls": [],
            }
            meta["turns"].append(turn)
            messages.append(result.message)

            if not result.tool_calls:
                nudges += 1
                if nudges > MAX_NUDGES:
                    meta["status"] = "stalled"
                    break
                messages.append({"role": "user", "content": NUDGE})
                continue
            nudges = 0

            for call in result.tool_calls:
                obs = _execute(sandbox, call, scratch_render)
                if call.name == "finish" and call.parse_error is None:
                    finished = True
                    finish_note = call.args.get("note")
                turn["tool_calls"].append({"name": call.name, "args": call.args, "observation": obs})
                messages.append({"role": "tool", "tool_call_id": call.call_id, "content": obs})

            if finished:
                break
        else:
            meta["status"] = "max_turns"

        if finished:
            meta["status"] = "finished"
        meta["finish_note"] = finish_note
        meta["workspace_files"] = sandbox.list_files()
        meta.update(_resolve_artifact(sandbox, language, exp_dir))
        if meta["status"] in ("finished", "max_turns", "stalled"):
            meta["status"] = "ok" if meta["artifact"] else "no_artifact"
    finally:
        sandbox.stop()
        scratch_render.unlink(missing_ok=True)

    meta["transcript"] = _transcript(model, messages)
    return meta


def _execute(sandbox: Sandbox, call: ToolCall, scratch_png: Path) -> str:
    if call.parse_error:
        return f"tool call error: {call.parse_error}"
    if call.name == "bash":
        command = call.args.get("command")
        if not command:
            return "tool call error: missing 'command'"
        code, output = sandbox.bash(command)
        return f"(exit {code})\n{output}" if output.strip() else f"(exit {code})"
    if call.name == "render":
        file = call.args.get("file")
        if not file:
            return "tool call error: missing 'file'"
        _, obs = _exec_render(sandbox, file, scratch_png)
        return obs
    if call.name == "finish":
        return "Session ended. Thank you."
    return f"tool call error: unknown tool {call.name!r}"


def _transcript(model: str, messages: list[dict]) -> str:
    lines = [f"# Transcript — {model}", ""]
    for msg in messages:
        role = msg.get("role")
        if role == "user":
            lines += ["## User", "", str(msg.get("content", "")), ""]
        elif role == "assistant":
            lines += [f"## {model}", ""]
            if msg.get("content"):
                lines += [str(msg["content"]), ""]
            for tc in msg.get("tool_calls") or []:
                fn = tc.get("function", {})
                try:
                    args = json.loads(fn.get("arguments") or "{}")
                except json.JSONDecodeError:
                    args = fn.get("arguments")
                if fn.get("name") == "bash" and isinstance(args, dict):
                    lines += ["```bash", str(args.get("command", "")), "```", ""]
                else:
                    lines += [f"**{fn.get('name')}**(`{json.dumps(args)}`)", ""]
        elif role == "tool":
            content = str(msg.get("content", ""))
            lines += ["> " + "\n> ".join(content.splitlines() or [""]), ""]
    return "\n".join(lines)
