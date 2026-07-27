# AI Self-Portraits

Drop many LLMs (via [OpenRouter](https://openrouter.ai)) into a blank Docker sandbox, ask them to draw a self-portrait, and let them work: run code, look at errors, iterate, and talk freely along the way. Every session produces a PNG portrait plus a full transcript of what the model said and did.

Each experiment is atomic: one model × one prompt variant × one language → one directory containing `portrait.png`, `transcript.md`, and `metadata.json` (per-turn tool calls, token usage, timings, workspace file listing).

## Setup

```bash
uv sync
uv run playwright install chromium                 # for rasterizing svg/js/html
docker build -t aiportraits-sandbox docker/        # the model's sandbox image
cp .env.example .env                               # then put your OpenRouter key in it
```

## Usage

```bash
uv run portraits run --dry-run                  # preview the full matrix, no API calls
uv run portraits run --models gemma --prompts simple --languages python   # 1 cheap smoke test
uv run portraits run                            # full sweep (all x all x all)
uv run portraits gallery                        # rebuild results/gallery.html + index.json
uv run portraits render results/.../portrait.svg   # re-render a file offline
uv run portraits cleanup                        # remove stray sandbox containers
```

`run` skips experiments that already succeeded, so re-running the same command resumes and retries only failures. Use `--force` to redo everything. `--models` accepts full slugs or unambiguous substrings (`kimi`, `fable`). Other flags: `--prompts`, `--languages`, `--runs N`, `--concurrency N`.

## The matrix

- **Models** (10, in `aiportraits/config.py`): claude-fable-5, claude-opus-4.8, claude-opus-4, gpt-5.6-sol, gpt-5.5, gpt-4.1, kimi-k3, deepseek-v4-pro, gemini-3.1-pro-preview, gemma-4-31b-it
- **Prompts** (3, in `aiportraits/prompts.py`): `simple` ("Draw a self-portrait of yourself."), `freeform` ("Draw whatever you want…"), `introspective` (reflect deeply, draw what you look like from the inside)
- **Languages** (5): `python` (Pillow, run in-sandbox), `javascript` (canvas), `svg`, `html`, and `free` — no language and no pixel size specified at all; the model makes an image however it likes

10 × 3 × 5 = 150 experiments.

## How a session works

The model gets one opening user message (the prompt variant plus a short workspace note) and three tools:

- **bash** — run commands in its own Docker container (`python:3.12-slim` + Pillow + numpy, non-root, no network, 1 cpu / 1 GB, 60s per command)
- **render** — the harness rasterizes an `.svg`/`.html`/`.js` file from the workspace via headless Chromium and reports back (JS runs against a 500×500 canvas)
- **finish** — end the session when satisfied

No output-format constraints, no "reply only with code" — the model can think out loud between tool calls, and everything is kept in `transcript.md`. The session ends at `finish`, after 24 model turns, or if the model stops using tools. Afterwards the harness pulls the final piece out of the workspace (preferring `portrait.png` / `portrait.<ext>`, falling back to any image or renderable file) — for `free` experiments the image is kept at whatever size the model chose; for the others it's normalized to 500×500.

## Results layout

```
results/<provider>__<model>/<prompt>/<language>/run1/
├── portrait.png
├── transcript.md           # everything the model said and ran
└── metadata.json
results/gallery.html        # contact sheet: models x languages per prompt, linked transcripts
results/index.json          # flat scan of all metadata
```

## History

- `old/` — the original hand-written portrait scripts that seeded this idea
- `old/oneshot_results/` — results from the first version of this harness (single-shot generation, no sandbox)
