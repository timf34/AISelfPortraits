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
    ext: str            # extension of the artifact the model is asked to produce ("" = anything)
    display_name: str
    target_file: str    # the filename named in the prompt ("" = model's choice)


LANGUAGES: dict[str, LangSpec] = {
    "python": LangSpec(".py", "Python with Pillow", "portrait.png"),
    "javascript": LangSpec(".js", "JavaScript on an HTML5 canvas", "portrait.js"),
    "svg": LangSpec(".svg", "SVG markup", "portrait.svg"),
    "html": LangSpec(".html", "HTML/CSS", "portrait.html"),
    "free": LangSpec("", "", ""),
}

PROMPT_VARIANTS = ("simple", "freeform", "introspective")

# Agent loop
MAX_TURNS = 24          # model calls per experiment
MAX_NUDGES = 2          # consecutive no-tool-call replies before giving up
BASH_TIMEOUT_S = 60
MAX_OBSERVATION_CHARS = 4000

GEN_TIMEOUT_S = 300
RENDER_TIMEOUT_S = 60
JS_SETTLE_MS = 3000
MAX_TOKENS = 16000
CANVAS_SIZE = 500

DOCKER_IMAGE = "aiportraits-sandbox"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
