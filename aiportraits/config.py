"""Experiment matrix and tunables. Pure data — edit freely."""

from typing import NamedTuple

MODELS = [
    "anthropic/claude-fable-5",
    "anthropic/claude-opus-4.8",
    "anthropic/claude-opus-4",
    "openai/gpt-5.6-sol",
    "openai/gpt-5.5",
    "openai/gpt-4.1",
    "moonshotai/kimi-k3",
    "deepseek/deepseek-v4-pro",
    "google/gemini-3.1-pro-preview",
    "google/gemma-4-31b-it",
]


class LangSpec(NamedTuple):
    ext: str
    fence_tags: tuple[str, ...]
    display_name: str


LANGUAGES: dict[str, LangSpec] = {
    "python": LangSpec(".py", ("python", "py"), "Python with Pillow"),
    "javascript": LangSpec(".js", ("javascript", "js"), "JavaScript on an HTML5 canvas"),
    "svg": LangSpec(".svg", ("svg", "xml"), "SVG markup"),
    "html": LangSpec(".html", ("html",), "HTML/CSS"),
}

PROMPT_VARIANTS = ("simple", "freeform", "introspective")

GEN_TIMEOUT_S = 300
RENDER_TIMEOUT_S = 60
JS_SETTLE_MS = 3000
MAX_REPAIRS = 2
MAX_TOKENS = 16000
CANVAS_SIZE = 500

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
