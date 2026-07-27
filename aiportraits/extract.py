"""Pull code out of a model response.

Responses are expected to contain free-form thinking plus one tagged fenced
code block. For the "free" language the fence tag tells us which renderer to
use."""

import re

from aiportraits.config import LANGUAGES

_FENCE_RE = re.compile(r"```([^\n`]*)\n(.*?)```", re.DOTALL)

_TAG_TO_LANGUAGE = {
    tag: lang for lang, spec in LANGUAGES.items() for tag in spec.fence_tags
}


def extract_code(text: str, language: str) -> tuple[str | None, str | None, str]:
    """Return (code, detected_language, method).

    For a fixed language, detected_language == language. For "free", it is
    inferred from the fence tag. method: fence_lang | fence_any | bare | none."""
    blocks = [
        ((m.group(1).strip().lower().split() or [""])[0], m.group(2))
        for m in _FENCE_RE.finditer(text)
    ]

    if language == "free":
        tagged = [(t, c) for t, c in blocks if t in _TAG_TO_LANGUAGE]
        if tagged:
            tag, code = max(tagged, key=lambda tc: len(tc[1]))
            return code.strip(), _TAG_TO_LANGUAGE[tag], "fence_lang"
        if blocks:
            _, code = max(blocks, key=lambda tc: len(tc[1]))
            lang = _guess_language(code)
            if lang:
                return code.strip(), lang, "fence_any"
        lang = _guess_language(text)
        if lang in ("svg", "html"):
            return _bare_markup(text, lang), lang, "bare"
        return None, None, "none"

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


def _guess_language(code: str) -> str | None:
    stripped = code.strip().lower()
    if stripped.startswith(("<svg", "<?xml")):
        return "svg"
    if stripped.startswith(("<!doctype", "<html")):
        return "html"
    if re.search(r"^\s*(import|from)\s+\w+", code, re.MULTILINE):
        return "python"
    if "getelementbyid" in stripped or "getcontext" in stripped:
        return "javascript"
    return None
