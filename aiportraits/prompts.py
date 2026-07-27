"""Prompt construction for the agentic sandbox mode.

One user message opens the session: the variant text, then a short workspace
note. No output-format constraints — the model is free to talk and iterate."""

from aiportraits.config import LANGUAGES

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

# Appended to simple/freeform variants when a language is specified.
LANGUAGE_CLAUSES = {
    "simple": " Use {language} and make the self-portrait 500x500.",
    "freeform": " Just make sure to use {language} and that the image is 500x500.",
    "introspective": "",
}

WORKSPACE_NOTE = (
    "You have your own Linux sandbox at /workspace — Python 3.12 with Pillow and "
    "numpy, no network. Use the bash tool to run commands. Take your time, think "
    "out loud, iterate as much as you like. Call finish when you're happy with it."
)

LANGUAGE_NOTES = {
    "python": "Save your final image as /workspace/portrait.png.",
    "javascript": (
        "Write your final JavaScript to /workspace/portrait.js. It will run in a page "
        "that provides <canvas id=\"canvas\" width=\"500\" height=\"500\">. Use the render "
        "tool to rasterize it and check for errors."
    ),
    "svg": (
        "Write your final SVG markup to /workspace/portrait.svg. Use the render tool "
        "to rasterize it and check for errors."
    ),
    "html": (
        "Write your final self-contained HTML document to /workspace/portrait.html. "
        "Use the render tool to rasterize it and check for errors."
    ),
    "free": (
        "Leave your final piece in /workspace as an image file, or as an .svg/.html/.js "
        "file — the render tool can rasterize those."
    ),
}


def build_user_prompt(variant: str, language: str) -> str:
    text = VARIANT_TEXTS[variant]
    if language != "free":
        text += LANGUAGE_CLAUSES[variant].format(language=LANGUAGES[language].display_name)
    return f"{text}\n\n{WORKSPACE_NOTE} {LANGUAGE_NOTES[language]}"


def build_messages(variant: str, language: str) -> list[dict]:
    return [{"role": "user", "content": build_user_prompt(variant, language)}]


NUDGE = "(You can keep going with the tools, or call finish if you're done.)"
