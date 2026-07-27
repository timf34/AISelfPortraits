"""Prompt construction for direct (single-call) generation.

One user message: the variant text, then an invitation to think freely first,
then a short note on how to deliver the code (a tagged fenced block)."""

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
    "free": (
        " in whichever of these you like, wrapped in one fenced block tagged with your "
        "choice: ```python (a Pillow script that saves \"portrait.png\"), ```js (drawing "
        "on a provided <canvas id=\"canvas\">), ```svg (a single <svg> element), or "
        "```html (a complete self-contained document)."
    ),
}


def build_user_prompt(variant: str, language: str) -> str:
    text = VARIANT_TEXTS[variant]
    if language != "free":
        text += LANGUAGE_CLAUSES[variant].format(language=LANGUAGES[language].display_name)
    return f"{text}\n\n{THINK_NOTE}{DELIVERY_NOTES[language]}"


def build_messages(variant: str, language: str) -> list[dict]:
    return [{"role": "user", "content": build_user_prompt(variant, language)}]


def build_repair_message(language: str, error: str, kind: str) -> str:
    if kind == "extract":
        tag = LANGUAGES[language].fence_tags[0] if language != "free" else "python/js/svg/html"
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
