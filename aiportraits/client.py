"""Thin OpenRouter chat-completions client with native tool-calling support."""

import json
import time
from dataclasses import dataclass, field

import httpx

from aiportraits.config import GEN_TIMEOUT_S, MAX_TOKENS, OPENROUTER_URL


class OpenRouterError(Exception):
    pass


@dataclass
class ToolCall:
    call_id: str
    name: str
    args: dict
    parse_error: str | None = None


@dataclass
class ChatResult:
    text: str
    message: dict               # the raw assistant message, for appending to history
    tool_calls: list[ToolCall] = field(default_factory=list)
    usage: dict = field(default_factory=dict)
    latency_s: float = 0.0


class OpenRouterClient:
    def __init__(self, api_key: str, timeout_s: float = GEN_TIMEOUT_S):
        self._client = httpx.Client(
            timeout=timeout_s,
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://github.com/timf34/AISelfPortraits",
                "X-Title": "AI Self Portraits",
            },
        )

    def chat(
        self,
        model: str,
        messages: list[dict],
        tools: list[dict] | None = None,
        retries: int = 3,
    ) -> ChatResult:
        payload: dict = {"model": model, "messages": messages, "max_tokens": MAX_TOKENS}
        if tools:
            payload["tools"] = tools
        last_err = ""
        for attempt in range(retries):
            start = time.monotonic()
            try:
                resp = self._client.post(OPENROUTER_URL, json=payload)
            except httpx.HTTPError as e:
                last_err = f"{type(e).__name__}: {e}"
                time.sleep(2**attempt)
                continue
            latency = time.monotonic() - start

            if resp.status_code == 429 or resp.status_code >= 500:
                last_err = f"HTTP {resp.status_code}: {resp.text[:500]}"
                time.sleep(2 ** (attempt + 1))
                continue
            if resp.status_code != 200:
                raise OpenRouterError(f"HTTP {resp.status_code}: {resp.text[:1000]}")

            data = resp.json()
            # OpenRouter can return 200 with an error body (e.g. provider issues).
            if "error" in data and not data.get("choices"):
                last_err = str(data["error"])[:500]
                time.sleep(2**attempt)
                continue
            try:
                msg = data["choices"][0]["message"]
            except (KeyError, IndexError, TypeError) as e:
                raise OpenRouterError(f"unexpected response shape: {e}: {str(data)[:500]}")

            tool_calls = []
            for tc in msg.get("tool_calls") or []:
                fn = tc.get("function", {})
                args, parse_error = {}, None
                try:
                    args = json.loads(fn.get("arguments") or "{}")
                    if not isinstance(args, dict):
                        args, parse_error = {}, "arguments were not a JSON object"
                except json.JSONDecodeError as e:
                    parse_error = f"invalid JSON in arguments: {e}"
                tool_calls.append(
                    ToolCall(call_id=tc.get("id", ""), name=fn.get("name", ""), args=args, parse_error=parse_error)
                )

            # Keep only the fields the API needs back, so history replays cleanly.
            clean_msg = {"role": "assistant", "content": msg.get("content") or ""}
            if msg.get("tool_calls"):
                clean_msg["tool_calls"] = msg["tool_calls"]

            return ChatResult(
                text=msg.get("content") or "",
                message=clean_msg,
                tool_calls=tool_calls,
                usage=data.get("usage", {}),
                latency_s=round(latency, 2),
            )
        raise OpenRouterError(f"gave up after {retries} attempts: {last_err}")

    def close(self) -> None:
        self._client.close()
