"""Rebuild results/index.json and results/gallery.html from a filesystem scan."""

import html
import json
from pathlib import Path

from aiportraits.config import LANGUAGES, MODELS, PROMPT_VARIANTS
from aiportraits.paths import RESULTS_ROOT, safe_model_name


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
        "</style></head><body>",
        "<h1>AI Self-Portraits</h1>",
        f"<p>{ok}/{total} experiments ok</p>",
    ]

    for prompt in PROMPT_VARIANTS:
        parts.append(f"<h2>{prompt}</h2><table><tr><th></th>")
        parts.extend(f"<th>{lang}</th>" for lang in LANGUAGES)
        parts.append("</tr>")
        for model in MODELS:
            parts.append(f"<tr><th class='rowh'>{html.escape(model)}</th>")
            for lang in LANGUAGES:
                rel = f"{safe_model_name(model)}/{prompt}/{lang}/run1"
                entry = entries.get(rel)
                if entry is None:
                    cell = "<div class='missing'>not run</div>"
                elif entry.get("status") == "ok" and entry.get("has_image"):
                    cap = f"attempts: {entry.get('final_attempt', '?')}"
                    if lang == "free" and entry.get("detected_language"):
                        cap += f" · chose {entry['detected_language']}"
                    if entry.get("resized_from"):
                        cap += f" · resized from {entry['resized_from']}"
                    cap += f" · <a href='{rel}/response.md'>response</a>"
                    cell = (
                        f"<a href='{rel}/portrait.png'><img src='{rel}/portrait.png' loading='lazy'></a>"
                        f"<div class='cap'>{cap}</div>"
                    )
                else:
                    err = ""
                    for attempt in reversed(entry.get("attempts", [])):
                        err = (attempt.get("render") or {}).get("error") or attempt.get("api_error") or err
                        if err:
                            break
                    cell = (
                        f"<div class='fail'>{html.escape(entry.get('status', '?'))}\n"
                        f"{html.escape((err or '')[:300])}</div>"
                    )
                parts.append(f"<td>{cell}</td>")
            parts.append("</tr>")
        parts.append("</table>")

    parts.append("</body></html>")
    out = root / "gallery.html"
    out.write_text("\n".join(parts))
    return out
