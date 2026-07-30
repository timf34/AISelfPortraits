"""Rebuild results/index.json and results/index.html from a filesystem scan."""

import html
import json
from pathlib import Path

from aiportraits.config import (
    LANGUAGES,
    MODELS,
    PREFILL_LANGUAGE,
    PREFILL_RUNS,
    PREFILL_VARIANTS,
    PROMPT_VARIANTS,
)
from aiportraits.paths import RESULTS_ROOT, safe_model_name
from aiportraits.prompts import VARIANT_TEXTS, build_user_prompt


def scan(root: Path = RESULTS_ROOT) -> list[dict]:
    entries = []
    for meta_path in sorted(root.glob("*/*/*/*/metadata.json")):
        try:
            meta = json.loads(meta_path.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        # Keep the index light; full detail (raw responses) stays in metadata.json.
        for attempt in meta.get("attempts", []):
            attempt.pop("raw_response", None)
        meta["dir"] = str(meta_path.parent.relative_to(root))
        meta["has_image"] = (meta_path.parent / "portrait.png").exists()
        entries.append(meta)
    return entries


def build_index(root: Path = RESULTS_ROOT) -> Path:
    root.mkdir(exist_ok=True)
    entries = scan(root)
    out = root / "index.json"
    out.write_text(json.dumps(entries, indent=2))
    return out


def _cell(entries: dict, rel: str) -> str:
    """One grid cell: the portrait, a failure box, or a 'not run' placeholder."""
    entry = entries.get(rel)
    if entry is None:
        return "<div class='missing'>not run</div>"
    if entry.get("status") == "ok" and entry.get("has_image"):
        cap = f"attempts: {entry.get('final_attempt', '?')}"
        if entry.get("resized_from"):
            cap += f" · resized from {entry['resized_from']}"
        cap += f" · <a href='{rel}/response.md'>response</a>"
        return (
            f"<a href='{rel}/portrait.png'><img src='{rel}/portrait.png' loading='lazy'></a>"
            f"<div class='cap'>{cap}</div>"
        )
    err = ""
    for attempt in reversed(entry.get("attempts", [])):
        err = (attempt.get("render") or {}).get("error") or attempt.get("api_error") or err
        if err:
            break
    return (
        f"<div class='fail'>{html.escape(entry.get('status', '?'))}\n"
        f"{html.escape((err or '')[:300])}</div>"
    )


def _prompt_block(variant: str, languages: list[str]) -> str:
    """The ask itself, plus the exact per-language message behind a disclosure.

    Only the language clause and the delivery note differ between columns, but
    quoting a doctored composite would misrepresent what was sent — so the
    expanded view carries each language's real message verbatim.
    """
    lead = html.escape(VARIANT_TEXTS[variant])
    detail = "".join(
        f"<div class='plang'>{html.escape(lang)}</div>"
        f"<pre class='prompt'>{html.escape(build_user_prompt(variant, lang))}</pre>"
        for lang in languages
    )
    suffix = "" if len(languages) == 1 else " — differs slightly per language"
    return (
        f"<blockquote class='ask'>{lead}</blockquote>"
        f"<details class='promptbox'><summary>exact message sent{suffix}</summary>"
        f"{detail}</details>"
    )


def _prefill_section(entries: dict) -> list[str]:
    """Prefill conditions side by side with the no-prefill cell they share a prompt with.

    All three columns end with the identical `simple` request in `PREFILL_LANGUAGE`;
    they differ only in what conversation history precedes it.
    """
    # (variant, run, heading, blurb). The no-prefill baseline has only run1;
    # each prefill condition shows PREFILL_RUNS independent samples side by side
    # so sampling noise stays visible next to any condition effect.
    columns = [("simple", 1, "No prefill", "The plain request, no conversation history.")]
    for name, spec in PREFILL_VARIANTS.items():
        for run in range(1, PREFILL_RUNS + 1):
            title = f"{spec.display_name} · run {run}"
            columns.append((name, run, title, spec.blurb if run == 1 else ""))

    parts = [
        "<h2 id='prefill'>prefill: does a 30-turn attractor transcript "
        "change the portrait?</h2>",
        "<p class='note'>Each cell replays 30 turns of Opus-4 self-play as conversation "
        "history, then asks for the portrait with the <em>exact</em> text used in the "
        f"<code>simple</code> / <code>{PREFILL_LANGUAGE}</code> cell above — so the only "
        "variable across these columns is the history. Seeds are vendored in "
        "<code>seeds/</code> from the AttractorStatePrefillAttack repo.</p>"
        f"<p class='note'>Each condition is sampled {PREFILL_RUNS}× independently. "
        "Compare the two runs of one condition before reading anything into a "
        "difference between conditions — with one sample per cell there is no way "
        "to tell a real effect from sampling noise.</p>",
        _prompt_block("simple", [PREFILL_LANGUAGE]),
        "<div class='scroll'><table><tr><th></th>",
    ]
    for _, _, title, blurb in columns:
        parts.append(f"<th>{html.escape(title)}<div class='colnote'>{html.escape(blurb)}</div></th>")
    parts.append("</tr>")

    for model in MODELS:
        parts.append(f"<tr><th class='rowh'>{html.escape(model)}</th>")
        for name, run, _, _ in columns:
            rel = f"{safe_model_name(model)}/{name}/{PREFILL_LANGUAGE}/run{run}"
            parts.append(f"<td>{_cell(entries, rel)}</td>")
        parts.append("</tr>")
    parts.append("</table></div>")
    return parts


def build_gallery(root: Path = RESULTS_ROOT) -> Path:
    root.mkdir(exist_ok=True)
    entries = {e["dir"]: e for e in scan(root)}
    ok = sum(1 for e in entries.values() if e.get("status") == "ok")
    total = len(entries)

    parts = [
        "<!doctype html><html><head><meta charset='utf-8'><title>AI Self-Portraits</title>",
        "<style>",
        "body{font-family:system-ui,sans-serif;background:#faf5ef;color:#2a2320;margin:2rem}",
        "h1{margin-bottom:.2rem} h2{margin-top:3rem;border-bottom:2px solid #d97757;padding-bottom:.3rem}",
        "table{border-collapse:collapse;margin-top:1rem}",
        ".scroll{overflow-x:auto;max-width:100%}",
        "th,td{padding:6px;text-align:center;vertical-align:top}",
        "th.rowh{text-align:right;font-weight:600;font-size:.8rem;max-width:130px;word-break:break-all}",
        "img{width:250px;height:250px;object-fit:contain;background:#141414;display:block;",
        "border-radius:6px;box-shadow:0 1px 4px rgba(0,0,0,.25)}",
        ".fail{width:250px;height:250px;display:flex;align-items:center;justify-content:center;",
        "background:#f6dcd3;color:#8a2d10;font-size:.7rem;border-radius:6px;padding:8px;box-sizing:border-box;",
        "overflow:hidden;white-space:pre-wrap;word-break:break-word}",
        ".missing{width:250px;height:250px;display:flex;align-items:center;justify-content:center;",
        "background:#eee7de;color:#999;font-size:.8rem;border-radius:6px}",
        ".cap{font-size:.7rem;color:#77685f;margin-top:4px}",
        ".note{max-width:62ch;font-size:.85rem;color:#5c4f47;line-height:1.5}",
        ".colnote{font-weight:400;font-size:.7rem;color:#77685f;max-width:250px;",
        "margin:.25rem auto 0;line-height:1.35}",
        "nav{font-size:.9rem;margin:.75rem 0 0}",
        "nav a{color:#a34a22;text-decoration:none;border-bottom:1px solid #e0c4b6}",
        "nav a:hover{border-bottom-color:#a34a22}",
        "h2{scroll-margin-top:1rem}",
        ".ask{margin:.9rem 0 .5rem;padding:.1rem 0 .1rem .9rem;border-left:3px solid #d97757;",
        "max-width:70ch;font-size:.95rem;line-height:1.5;color:#3d322c}",
        ".promptbox{max-width:70ch;font-size:.8rem;color:#77685f}",
        ".promptbox summary{cursor:pointer;user-select:none}",
        ".plang{margin:.7rem 0 .2rem;font-weight:600;color:#5c4f47}",
        "pre.prompt{margin:0;padding:.6rem .7rem;background:#f2e9df;border-radius:5px;",
        "white-space:pre-wrap;word-break:break-word;font-size:.75rem;line-height:1.45;color:#3d322c}",
        "</style></head><body>",
        "<h1>AI Self-Portraits</h1>",
        f"<p>{ok}/{total} experiments ok</p>",
        # The page is several screens tall; without this the last section is easy to miss.
        "<nav>" + " · ".join(
            [f"<a href='#{p}'>{p}</a>" for p in PROMPT_VARIANTS]
            + ["<a href='#prefill'>prefill (bliss vs neutral)</a>"]
        ) + "</nav>",
    ]

    for prompt in PROMPT_VARIANTS:
        parts.append(f"<h2 id='{prompt}'>{prompt}</h2>")
        parts.append(_prompt_block(prompt, list(LANGUAGES)))
        parts.append("<div class='scroll'><table><tr><th></th>")
        parts.extend(f"<th>{lang}</th>" for lang in LANGUAGES)
        parts.append("</tr>")
        for model in MODELS:
            parts.append(f"<tr><th class='rowh'>{html.escape(model)}</th>")
            for lang in LANGUAGES:
                rel = f"{safe_model_name(model)}/{prompt}/{lang}/run1"
                parts.append(f"<td>{_cell(entries, rel)}</td>")
            parts.append("</tr>")
        parts.append("</table></div>")

    parts.extend(_prefill_section(entries))
    parts.append("</body></html>")
    # index.html so `results/` can be served as a static site root as-is.
    out = root / "index.html"
    out.write_text("\n".join(parts))
    return out
