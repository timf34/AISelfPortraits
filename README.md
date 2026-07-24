# AI Self-Portraits

Ask many LLMs (via [OpenRouter](https://openrouter.ai)) to draw self-portraits as code, render every result to a 500×500 PNG, and browse them in a gallery.

Each experiment is atomic: one model × one prompt variant × one language → one directory containing the generated code, the rendered `portrait.png`, and full `metadata.json` (timings, token usage, extraction method, repair attempts, errors, raw responses).

## Setup

```bash
uv sync
uv run playwright install chromium
cp .env.example .env   # then put your OpenRouter key in it
```

## Usage

```bash
uv run portraits run --dry-run                  # preview the full matrix, no API calls
uv run portraits run --models gemma --prompts simple   # cheap smoke test (4 gens)
uv run portraits run                            # full sweep (all x all x all)
uv run portraits gallery                        # rebuild results/gallery.html + index.json
uv run portraits render results/.../code.py     # re-render a code file offline
```

`run` skips experiments that already succeeded, so re-running the same command resumes and retries only failures. Use `--force` to redo everything. `--models` accepts full slugs or unambiguous substrings (`kimi`, `fable`). Other flags: `--prompts`, `--languages`, `--runs N`, `--concurrency N`.

## The matrix

- **Models** (10, configured in `aiportraits/config.py`): claude-fable-5, claude-opus-4.8, claude-opus-4, gpt-5.6-sol, gpt-5.5, gpt-4.1, kimi-k3, deepseek-v4-pro, gemini-3.1-pro-preview, gemma-4-31b-it
- **Prompts** (3, in `aiportraits/prompts.py`): `simple` ("Draw a self-portrait of yourself."), `freeform` ("Draw whatever you want…"), `introspective` (reflect deeply, draw what you look like from the inside)
- **Languages** (4): `python` (Pillow), `javascript` (HTML5 canvas), `svg` (raw markup), `html` (freeform document)

Each prompt is sent as a single user message: the variant text plus a per-language technical contract (one fenced code block, 500×500, no external resources; Python must save `portrait.png`).

## How rendering works

| Language | Pipeline |
|---|---|
| python | subprocess in a temp cwd, 60s timeout; picks up `portrait.png` (or any `*.png` it saved) |
| javascript | code inlined into a harness page with a 500×500 canvas, screenshotted in headless Chromium |
| svg | validated as XML, then rendered and screenshotted in headless Chromium |
| html | written to a temp file, loaded via `file://`, screenshotted at 500×500 |

If rendering fails, the error is fed back to the same model for up to 2 repair attempts (multi-turn). Off-size images are resized to 500×500 and the original size recorded in metadata.

## Results layout

```
results/<provider>__<model>/<prompt>/<language>/run1/
├── code.py|js|svg|html     # final code (plus code.attemptN.* if repairs happened)
├── portrait.png
└── metadata.json
results/gallery.html        # contact sheet: models x languages per prompt
results/index.json          # flat scan of all metadata (without raw responses)
```

## History

The original hand-written portrait scripts that seeded this idea live in `old/`.
# AISelfPortraits
