import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from aiportraits.config import (
    LANGUAGES,
    MODELS,
    PREFILL_LANGUAGE,
    PREFILL_VARIANTS,
    PROMPT_VARIANTS,
)

ALL_PROMPTS = list(PROMPT_VARIANTS) + list(PREFILL_VARIANTS)


def _resolve_models(arg: str) -> list[str]:
    if arg == "all":
        return list(MODELS)
    out = []
    for token in arg.split(","):
        token = token.strip()
        if not token:
            continue
        if token in MODELS:
            out.append(token)
            continue
        matches = [m for m in MODELS if token.lower() in m.lower()]
        if len(matches) == 1:
            out.append(matches[0])
        elif not matches:
            sys.exit(f"error: no configured model matches '{token}' (see aiportraits/config.py)")
        else:
            sys.exit(f"error: '{token}' is ambiguous: {', '.join(matches)}")
    return out


def _resolve_list(arg: str, valid: list[str], kind: str) -> list[str]:
    if arg == "all":
        return list(valid)
    out = []
    for token in arg.split(","):
        token = token.strip()
        if token not in valid:
            sys.exit(f"error: unknown {kind} '{token}' (valid: {', '.join(valid)})")
        out.append(token)
    return out


def cmd_run(args) -> None:
    from aiportraits.client import OpenRouterClient
    from aiportraits.runner import Experiment, existing_status, run_all

    models = _resolve_models(args.models)
    # "all" means the three ordinary variants; prefill conditions are opt-in by name.
    prompts = _resolve_list(args.prompts, ALL_PROMPTS, "prompt") \
        if args.prompts != "all" else list(PROMPT_VARIANTS)
    languages = _resolve_list(args.languages, list(LANGUAGES), "language")

    experiments = [
        Experiment(model=m, prompt=p, language=l, run=r)
        for m in models
        for p in prompts
        # Prefill conditions are single-language; don't fan them across the grid.
        for l in ([PREFILL_LANGUAGE] if p in PREFILL_VARIANTS else languages)
        for r in range(1, args.runs + 1)
    ]
    experiments = list(dict.fromkeys(experiments))

    to_run, skipped = [], []
    for exp in experiments:
        if not args.force and existing_status(exp) == "ok":
            skipped.append(exp)
        else:
            to_run.append(exp)

    print(f"matrix: {len(models)} models x prompts[{','.join(prompts)}] "
          f"x {args.runs} run(s) = {len(experiments)} experiments")
    print(f"to run: {len(to_run)}   skipped (already ok): {len(skipped)}")

    if args.dry_run:
        for exp in to_run:
            print(f"  would run: {exp.label}")
        return
    if not to_run:
        print("nothing to do (use --force to re-run)")
        return

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        sys.exit("error: OPENROUTER_API_KEY not set (put it in .env — see .env.example)")

    client = OpenRouterClient(api_key)
    try:
        run_all(client, to_run, concurrency=args.concurrency)
    finally:
        client.close()


def cmd_gallery(args) -> None:
    from aiportraits.gallery import build_gallery, build_index

    index = build_index()
    gallery = build_gallery()
    print(f"wrote {index}")
    print(f"wrote {gallery}")


def cmd_render(args) -> None:
    from aiportraits.renderers import render, shutdown_browsers

    path = Path(args.code_file)
    ext_to_lang = {spec.ext: lang for lang, spec in LANGUAGES.items() if spec.ext}
    language = args.language or ext_to_lang.get(path.suffix)
    if language is None:
        sys.exit(f"error: cannot infer language from '{path.suffix}', pass --language")

    out = Path(args.output) if args.output else path.with_suffix(".png")
    try:
        result = render(language, path.read_text(), out)
    finally:
        shutdown_browsers()
    if result.ok:
        print(f"ok: {out} {result.image_size}"
              + (f" (resized from {result.resized_from})" if result.resized_from else "")
              + (" [blank]" if result.blank else ""))
    else:
        sys.exit(f"render failed: {result.error}")


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(prog="portraits", description="AI self-portrait experiments")
    sub = parser.add_subparsers(dest="command", required=True)

    p_run = sub.add_parser("run", help="run experiments")
    p_run.add_argument("--models", default="all", help="comma-separated slugs or substrings (default: all)")
    p_run.add_argument(
        "--prompts",
        default="all",
        help=f"comma-separated from {','.join(ALL_PROMPTS)} "
             f"('all' = {','.join(PROMPT_VARIANTS)}; prefill conditions are opt-in)",
    )
    p_run.add_argument("--languages", default="all", help=f"comma-separated from {','.join(LANGUAGES)}")
    p_run.add_argument("--runs", type=int, default=1)
    p_run.add_argument("--concurrency", type=int, default=4)
    p_run.add_argument("--force", action="store_true", help="re-run even if already ok")
    p_run.add_argument("--dry-run", action="store_true", help="print the matrix and exit")
    p_run.set_defaults(func=cmd_run)

    p_gal = sub.add_parser("gallery", help="rebuild results/index.json and results/index.html")
    p_gal.set_defaults(func=cmd_gallery)

    p_ren = sub.add_parser("render", help="render a code file to PNG (offline, for debugging)")
    p_ren.add_argument("code_file")
    p_ren.add_argument("-o", "--output")
    p_ren.add_argument("--language", choices=[l for l in LANGUAGES if l != "free"])
    p_ren.set_defaults(func=cmd_render)

    args = parser.parse_args()
    args.func(args)
