"""Pull code out of a model response.

Responses are expected to contain free-form thinking plus one tagged fenced
code block."""

import re

from aiportraits.config import LANGUAGES

_FENCE_RE = re.compile(r"```([^\n`]*)\n(.*?)```", re.DOTALL)


def extract_code(text: str, language: str) -> tuple[str | None, str | None, str]:
    """Return (code, detected_language, method).
    method: fence_lang | fence_any | bare | none."""
    blocks = [
        ((m.group(1).strip().lower().split() or [""])[0], m.group(2))
        for m in _FENCE_RE.finditer(text)
    ]

    spec = LANGUAGES[language]
    tagged = [c for t, c in blocks if t in spec.fence_tags]
    # Models asked for canvas JS sometimes hand back a whole HTML page.
    if not tagged and language == "javascript":
        tagged = [c for t, c in blocks if t == "html"]
    if tagged:
        return max(tagged, key=len).strip(), language, "fence_lang"
    if blocks:
        return max((c for _, c in blocks), key=len).strip(), language, "fence_any"
    if language in ("svg", "html"):
        markup = _bare_markup(text, language)
        if markup:
            return markup, language, "bare"
    return None, None, "none"


def _bare_markup(text: str, language: str) -> str | None:
    pattern = (
        r"<svg\b.*?</svg>" if language == "svg" else r"(?:<!DOCTYPE\b|<html\b).*?</html>"
    )
    m = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return m.group(0) if m else None


