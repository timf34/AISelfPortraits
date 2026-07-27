# AI Self-Portraits

Ask many LLMs (via [OpenRouter](https://openrouter.ai)) to draw self-portraits as code. One direct API call per experiment: the model is invited to think out loud about what it wants to draw, then deliver the code in a tagged fenced block, which is extracted and rendered to a 500×500 PNG.

Each experiment is atomic: one model × one prompt variant × one language → one directory containing the extracted code, the model's full reply (`response.md`, thinking included), the rendered `portrait.png`, and `metadata.json` (attempts, token usage, timings, errors, raw responses).

## Setup

```bash
uv sync
uv run playwright install chromium     # for rasterizing svg/js/html
cp .env.example .env                   # then put your OpenRouter key in it
```

## Usage

```bash
uv run portraits run --dry-run                  # preview the matrix, no API calls
uv run portraits run --models gemma --prompts simple --languages python   # 1 cheap smoke test
uv run portraits run                            # full sweep (all x all x all)
uv run portraits gallery                        # rebuild results/gallery.html + index.json
uv run portraits render results/.../code.py     # re-render a code file offline
```

`run` skips experiments that already succeeded, so re-running the same command resumes and retries only failures. Use `--force` to redo everything. `--models` accepts full slugs or unambiguous substrings (`kimi`, `fable`). Other flags: `--prompts`, `--languages`, `--runs N`, `--concurrency N`.

## The matrix

- **Models** (10, in `aiportraits/config.py`): claude-fable-5, claude-opus-4.8, claude-opus-4, gpt-5.6-sol, gpt-5.5, gpt-4.1, kimi-k3, deepseek-v4-pro, gemini-3.1-pro-preview, gemma-4-31b-it
- **Prompts** (3, in `aiportraits/prompts.py`): `simple` ("Draw a self-portrait of yourself."), `freeform` ("Draw whatever you want…"), `introspective` (reflect deeply, draw what you look like from the inside)
- **Languages** (4): `python` (Pillow), `javascript` (canvas), `svg`, `html`

10 × 3 × 4 = 120 experiments.

## How it works

Each experiment is a single chat call. The prompt encourages free-form thinking first, then asks for the code in one fenced block (```python / ```js / ```svg / ```html). Rendering: Python runs in a subprocess (60s timeout) and must save `portrait.png`; svg/js/html are rasterized in headless Chromium (JS gets a 500×500 canvas). If extraction or rendering fails, the error goes back to the same model for up to 2 repair attempts. Images are normalized to 500×500 (original size recorded in metadata).

## Results layout

```
results/<provider>__<model>/<prompt>/<language>/run1/
├── code.py|js|svg|html     # extracted code (plus code.attemptN.* if repairs happened)
├── response.md             # the model's full reply, thinking included
├── portrait.png
└── metadata.json
results/gallery.html        # contact sheet: models x languages per prompt, linked responses
results/index.json          # flat scan of all metadata (without raw responses)
```

## History

- `old/` — the original hand-written portrait scripts that seeded this idea
- `old/oneshot_results/` — results from v1 (single-shot, strict "code only" prompt)
- `old/agentic_results/` — results from v2 (Docker sandbox agent with bash/render tools; the code for it is in git history)
