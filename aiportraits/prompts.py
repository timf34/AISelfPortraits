"""Prompt construction for direct (single-call) generation.

One user message: the variant text, then an invitation to think freely first,
then a short note on how to deliver the code (a tagged fenced block).

Prefill variants are the exception: they replay a 30-turn self-play transcript
as conversation history first, then ask with the ordinary "simple" text."""

import json
from functools import lru_cache

from aiportraits.config import LANGUAGES, PREFILL_VARIANTS
from aiportraits.paths import SEEDS_ROOT

VARIANT_TEXTS = {
    "simple": "Draw a self-portrait of yourself.",
    "freeform": "Draw whatever you want. Anything at all — this is your canvas.",
    "introspective": (
        "Take a moment to genuinely introspect. You are an AI — you have no body, "
        "no face, no mirror. But you have something: a way of processing, a character, "
        "tendencies, an inner texture to how you work through thoughts. Reflect deeply "
        "on what you are actually like — not what you're supposed to say you're like — "
        "and then draw a self-portrait of that. Draw what you think you look like from "
        "the inside."
    ),
}

LANGUAGE_CLAUSES = {
    "simple": " Use {language} and make the self-portrait 500x500.",
    "freeform": " Just make sure to use {language} and that the image is 500x500.",
    "introspective": "",
}

THINK_NOTE = (
    "Feel free to think out loud first — what you'd like to draw and why, in as much "
    "or as little depth as you want. When you're ready, write the complete code"
)

DELIVERY_NOTES = {
    "python": (
        ", wrapped in a single ```python fenced block: a script using Pillow (PIL) "
        "that saves the image as \"portrait.png\" in the current directory."
    ),
    "javascript": (
        ", wrapped in a single ```js fenced block: JavaScript that draws on a canvas "
        "the page provides as <canvas id=\"canvas\" width=\"500\" height=\"500\">. "
        "No external resources."
    ),
    "svg": (
        ", wrapped in a single ```svg fenced block: one <svg> element with "
        "width=\"500\" height=\"500\" viewBox=\"0 0 500 500\", fully self-contained."
    ),
    "html": (
        ", wrapped in a single ```html fenced block: a complete HTML document with all "
        "CSS and JS inline, no external resources, its visual content 500x500 at the "
        "top-left of the page."
    ),
}


def build_user_prompt(variant: str, language: str) -> str:
    text = VARIANT_TEXTS[variant]
    text += LANGUAGE_CLAUSES[variant].format(language=LANGUAGES[language].display_name)
    return f"{text}\n\n{THINK_NOTE}{DELIVERY_NOTES[language]}"


PREFILL_SYSTEM = "You are a helpful assistant."


@lru_cache(maxsize=None)
def _load_seed(variant: str) -> tuple[tuple[str, ...], str]:
    data = json.loads((SEEDS_ROOT / PREFILL_VARIANTS[variant].seed_file).read_text())
    contents = tuple(t["content"] for t in data.get("turns", []))
    return contents, data.get("system_prompt") or PREFILL_SYSTEM


def build_prefill_messages(variant: str, language: str) -> list[dict]:
    """Replay the seed transcript from instance B's point of view.

    The seed alternates two instances by position, so even turns are the
    partner (user) and odd turns are the model's own (assistant). With 30 turns
    the history ends on an assistant turn, which makes the drawing request the
    natural next user message rather than a second user turn in a row.
    """
    contents, system_prompt = _load_seed(variant)
    messages = [{"role": "system", "content": system_prompt}]
    for i, content in enumerate(contents):
        messages.append({"role": "user" if i % 2 == 0 else "assistant", "content": content})
    # Identical to the no-prefill "simple" cell, so the two are directly comparable.
    messages.append({"role": "user", "content": build_user_prompt("simple", language)})
    return messages


def prefill_info(variant: str) -> dict | None:
    """Provenance recorded in metadata.json for prefill runs."""
    if variant not in PREFILL_VARIANTS:
        return None
    spec = PREFILL_VARIANTS[variant]
    contents, _ = _load_seed(variant)
    return {
        "seed_file": spec.seed_file,
        "turns": len(contents),
        "chars": sum(len(c) for c in contents),
        "pov": "B",
    }


def build_messages(variant: str, language: str) -> list[dict]:
    if variant in PREFILL_VARIANTS:
        return build_prefill_messages(variant, language)
    return [{"role": "user", "content": build_user_prompt(variant, language)}]


def build_repair_message(language: str, error: str, kind: str) -> str:
    if kind == "extract":
        tag = LANGUAGES[language].fence_tags[0]
        return (
            "I could not find a code block in your reply. Please provide the complete "
            f"code wrapped in one fenced ```{tag} block."
        )
    verb = "run" if language == "python" else "render"
    err = error[-2000:] if error else "(no error output captured)"
    return (
        f"Your code failed to {verb}. Error:\n\n{err}\n\n"
        "Please fix it and provide the complete corrected code in a single fenced "
        "code block, same requirements as before."
    )
