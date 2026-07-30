"""Experiment orchestration: generate -> extract -> render -> repair loop."""

import json
import os
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from aiportraits.client import OpenRouterClient, OpenRouterError
from aiportraits.config import LANGUAGES, MAX_REPAIRS
from aiportraits.extract import extract_code
from aiportraits.paths import experiment_dir
from aiportraits.prompts import build_messages, build_repair_message, prefill_info
from aiportraits.renderers import render, shutdown_browsers


@dataclass(frozen=True)
class Experiment:
    model: str
    prompt: str
    language: str
    run: int

    @property
    def dir(self) -> Path:
        return experiment_dir(self.model, self.prompt, self.language, self.run)

    @property
    def label(self) -> str:
        return f"{self.model} {self.prompt}/{self.language} run{self.run}"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _write_metadata(exp: Experiment, meta: dict) -> None:
    exp.dir.mkdir(parents=True, exist_ok=True)
    tmp = exp.dir / "metadata.json.tmp"
    tmp.write_text(json.dumps(meta, indent=2, default=str))
    os.replace(tmp, exp.dir / "metadata.json")


def existing_status(exp: Experiment) -> str | None:
    meta_path = exp.dir / "metadata.json"
    if not meta_path.exists():
        return None
    try:
        return json.loads(meta_path.read_text()).get("status")
    except (json.JSONDecodeError, OSError):
        return None


def run_experiment(client: OpenRouterClient, exp: Experiment) -> str:
    start = time.monotonic()
    meta: dict = {
        "model": exp.model,
        "prompt": exp.prompt,
        "language": exp.language,
        "run": exp.run,
        "status": "running",
        "started_at": _now(),
        "attempts": [],
    }

    if (info := prefill_info(exp.prompt)) is not None:
        meta["prefill"] = info

    messages = build_messages(exp.prompt, exp.language)
    status = "failed_api"
    for attempt_n in range(MAX_REPAIRS + 1):
        attempt: dict = {"kind": "generate" if attempt_n == 0 else "repair"}
        meta["attempts"].append(attempt)
        try:
            result = client.chat(exp.model, messages)
        except OpenRouterError as e:
            attempt["api_error"] = str(e)
            status = "failed_api"
            break

        attempt["latency_s"] = result.latency_s
        attempt["usage"] = result.usage
        attempt["raw_response"] = result.text
        messages.append({"role": "assistant", "content": result.text})

        code, detected, method = extract_code(result.text, exp.language)
        attempt["extract_method"] = method
        attempt["detected_language"] = detected
        if code is None:
            status = "failed_extract"
            messages.append(
                {"role": "user", "content": build_repair_message(exp.language, "", "extract")}
            )
            _write_metadata(exp, meta)
            continue

        exp.dir.mkdir(parents=True, exist_ok=True)
        ext = LANGUAGES[detected].ext
        (exp.dir / f"code{ext}").write_text(code)
        if attempt_n > 0:
            (exp.dir / f"code.attempt{attempt_n + 1}{ext}").write_text(code)
        # The model's full reply — thinking included — kept readable alongside the code.
        (exp.dir / "response.md").write_text(result.text)

        render_result = render(detected, code, exp.dir / "portrait.png")
        attempt["render"] = {
            "ok": render_result.ok,
            "error": render_result.error,
            "duration_s": render_result.duration_s,
            "blank": render_result.blank,
        }
        meta["blank"] = render_result.blank
        if render_result.ok and not render_result.blank:
            status = "ok"
            meta["detected_language"] = detected
            meta["image_size"] = render_result.image_size
            meta["resized_from"] = render_result.resized_from
            break

        # A single-colour image renders without error but shows nothing, so it
        # has to go back for repair like any other failure — otherwise the cell
        # is recorded ok and the empty portrait ships.
        kind = "blank" if render_result.ok else "render"
        status = "failed_blank" if render_result.ok else "failed_render"
        messages.append(
            {
                "role": "user",
                "content": build_repair_message(detected, render_result.error or "", kind),
            }
        )
        _write_metadata(exp, meta)

    meta["status"] = status
    meta["final_attempt"] = len(meta["attempts"])
    meta["finished_at"] = _now()
    meta["total_duration_s"] = round(time.monotonic() - start, 2)
    _write_metadata(exp, meta)
    return status


def run_all(client: OpenRouterClient, experiments: list[Experiment], concurrency: int = 4) -> dict:
    total = len(experiments)
    counts: dict[str, int] = {}
    done = 0

    def _one(exp: Experiment) -> tuple[Experiment, str]:
        try:
            return exp, run_experiment(client, exp)
        except Exception:
            exp.dir.mkdir(parents=True, exist_ok=True)
            (exp.dir / "crash.log").write_text(traceback.format_exc())
            return exp, "crashed"

    try:
        with ThreadPoolExecutor(max_workers=concurrency) as pool:
            futures = {pool.submit(_one, exp): exp for exp in experiments}
            for fut in as_completed(futures):
                exp, status = fut.result()
                done += 1
                counts[status] = counts.get(status, 0) + 1
                print(f"[{done}/{total}] {status:14s} {exp.label}")
    finally:
        shutdown_browsers()

    print("\nSummary:")
    for status, n in sorted(counts.items()):
        print(f"  {status}: {n}")
    return counts
