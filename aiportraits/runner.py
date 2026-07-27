"""Experiment orchestration for agentic sandbox sessions."""

import json
import os
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from aiportraits.agent import run_agent
from aiportraits.client import OpenRouterClient
from aiportraits.paths import experiment_dir
from aiportraits.renderers import shutdown_browsers


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
    exp.dir.mkdir(parents=True, exist_ok=True)
    meta = run_agent(client, exp.model, exp.prompt, exp.language, exp.dir)

    transcript = meta.pop("transcript", "")
    (exp.dir / "transcript.md").write_text(transcript)

    usage_in = sum((t.get("usage") or {}).get("prompt_tokens", 0) for t in meta["turns"])
    usage_out = sum((t.get("usage") or {}).get("completion_tokens", 0) for t in meta["turns"])
    meta = {
        "model": exp.model,
        "prompt": exp.prompt,
        "language": exp.language,
        "run": exp.run,
        **meta,
        "n_turns": len(meta["turns"]),
        "n_tool_calls": sum(len(t["tool_calls"]) for t in meta["turns"]),
        "total_usage": {"prompt_tokens": usage_in, "completion_tokens": usage_out},
        "finished_at": _now(),
        "total_duration_s": round(time.monotonic() - start, 2),
    }
    _write_metadata(exp, meta)
    return meta["status"]


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
                print(f"[{done}/{total}] {status:12s} {exp.label}")
    finally:
        shutdown_browsers()

    print("\nSummary:")
    for status, n in sorted(counts.items()):
        print(f"  {status}: {n}")
    return counts
