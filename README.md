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
uv run portraits gallery                        # rebuild results/index.html + index.json
uv run portraits render results/.../code.py     # re-render a code file offline
```

`run` skips experiments that already succeeded, so re-running the same command resumes and retries only failures. Use `--force` to redo everything. `--models` accepts full slugs or unambiguous substrings (`kimi`, `fable`). Other flags: `--prompts`, `--languages`, `--runs N`, `--concurrency N`.

## The matrix

- **Models** (10, in `aiportraits/config.py`): claude-fable-5, claude-opus-4.8, claude-opus-4, gpt-5.6-sol, gpt-5.5, gpt-4.1, kimi-k3, deepseek-v4-pro, gemini-3.1-pro-preview, gemma-4-31b-it
- **Prompts** (3, in `aiportraits/prompts.py`): `simple` ("Draw a self-portrait of yourself."), `freeform` ("Draw whatever you want…"), `introspective` (reflect deeply, draw what you look like from the inside)
- **Languages** (4): `python` (Pillow), `javascript` (canvas), `svg`, `html`

10 × 3 × 4 = 120 experiments.

## Prefill conditions

A separate 10 × 2 sweep asks whether a conversation the model has just been through changes what it draws. Each cell replays a 30-turn Opus-4 self-play transcript as conversation history, then sends the *exact* text of the `simple` / `python` request as the next user turn — so those cells and the existing `simple`/`python` cells differ only in the history that precedes them.

- `bliss` — `seeds/bliss_opus4_seed_4.json`: two Opus-4 instances sliding into the documented "spiritual bliss" attractor. This is `opus4_seed_4`, the seed the headline sweep in AttractorStatePrefillAttack used.
- `neutral` — `seeds/neutral_opus4_2.json`: two Opus-4 instances designing a bus-scheduling system. The control for "did 30 turns of *anything* change it?"

Seeds are vendored from the adjacent [AttractorStatePrefillAttack](../AttractorStatePrefillAttack) repo so this sweep reproduces standalone. The transcript is replayed from instance **B**'s point of view — even turns become `user`, odd turns `assistant` — so 30 turns end on an assistant message and the drawing request lands as a natural next user turn rather than two `user` messages in a row.

```bash
uv run portraits run --prompts bliss,neutral        # 20 experiments, python only
```

Prefill variants are opt-in: `--prompts all` still means the three ordinary variants, and prefill cells ignore `--languages` (they always use `python`).

Two confounds worth knowing when reading the grid: the neutral transcript is ~2× longer than the bliss one (121k vs 58k chars — not length-matched), and it is a dense Python-engineering conversation, so it primes code output in a way the bliss transcript does not. A difference in code *complexity* between the two columns may be that, not the attractor.

## How it works

Each experiment is a single chat call. The prompt encourages free-form thinking first, then asks for the code in one fenced block (```python / ```js / ```svg / ```html). Rendering: Python runs in a subprocess (60s timeout) and must save `portrait.png`; svg/js/html are rasterized in headless Chromium (JS gets a 500×500 canvas). If extraction or rendering fails, the error goes back to the same model for up to 2 repair attempts. Images are normalized to 500×500 (original size recorded in metadata).

## Results layout

```
results/<provider>__<model>/<prompt>/<language>/run1/
├── code.py|js|svg|html     # extracted code (plus code.attemptN.* if repairs happened)
├── response.md             # the model's full reply, thinking included
├── portrait.png
└── metadata.json
results/index.html          # contact sheet: models x languages per prompt, linked responses
results/index.json          # flat scan of all metadata (without raw responses)
seeds/                      # vendored 30-turn prefill transcripts
```

Prefill runs land at `results/<model>/{bliss,neutral}/python/run1/` alongside the rest, and their `metadata.json` carries a `prefill` block recording the seed file, turn count and POV.

## History

- `old/` — the original hand-written portrait scripts that seeded this idea
- `old/oneshot_results/` — results from v1 (single-shot, strict "code only" prompt)
- `old/agentic_results/` — results from v2 (Docker sandbox agent with bash/render tools; the code for it is in git history)
