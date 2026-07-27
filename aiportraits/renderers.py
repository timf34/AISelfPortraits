"""Render model-generated code to a 500x500 PNG.

python  -> subprocess in a temp cwd (must save portrait.png; falls back to any *.png)
svg     -> validated with ElementTree, then screenshotted in headless Chromium
javascript/html -> harness page / document screenshotted in headless Chromium

Chromium instances are per-thread (Playwright's sync API is thread-affine).
"""

import subprocess
import sys
import tempfile
import threading
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

from aiportraits.config import CANVAS_SIZE, JS_SETTLE_MS, RENDER_TIMEOUT_S


@dataclass
class RenderResult:
    ok: bool
    error: str | None = None
    duration_s: float = 0.0
    image_size: tuple[int, int] | None = None
    resized_from: tuple[int, int] | None = None
    blank: bool = False


def render(language: str, code: str, out_png: Path, resize: bool = True) -> RenderResult:
    start = time.monotonic()
    fn = {
        "python": render_python,
        "javascript": render_js,
        "svg": render_svg,
        "html": render_html,
    }[language]
    try:
        result = fn(code, out_png)
    except Exception as e:  # renderer infrastructure failure, not model's fault per se
        result = RenderResult(ok=False, error=f"{type(e).__name__}: {e}")
    result.duration_s = round(time.monotonic() - start, 2)
    if result.ok:
        _finalize_image(out_png, result, resize)
    return result


def finalize_image_file(png: Path, resize: bool = True) -> RenderResult:
    """Validate (and optionally normalize) an existing image file in place."""
    result = RenderResult(ok=True)
    try:
        _finalize_image(png, result, resize)
    except Exception as e:
        return RenderResult(ok=False, error=f"unreadable image: {type(e).__name__}: {e}")
    return result


def _finalize_image(out_png: Path, result: RenderResult, resize: bool) -> None:
    with Image.open(out_png) as im:
        im.load()
        result.image_size = im.size
        if resize and im.size != (CANVAS_SIZE, CANVAS_SIZE):
            result.resized_from = im.size
            im.convert("RGBA").resize((CANVAS_SIZE, CANVAS_SIZE), Image.LANCZOS).save(out_png)
            result.image_size = (CANVAS_SIZE, CANVAS_SIZE)
        elif out_png.suffix.lower() != ".png" or im.format != "PNG":
            im.convert("RGBA").save(out_png, format="PNG")
        colors = im.convert("RGB").getcolors(maxcolors=2)
        result.blank = colors is not None and len(colors) == 1


# ---------------------------------------------------------------- python

def render_python(code: str, out_png: Path) -> RenderResult:
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        script = tmpdir / "code.py"
        script.write_text(code)
        try:
            proc = subprocess.run(
                [sys.executable, str(script)],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                timeout=RENDER_TIMEOUT_S,
            )
        except subprocess.TimeoutExpired:
            return RenderResult(ok=False, error=f"TimeoutExpired: script did not finish within {RENDER_TIMEOUT_S}s")

        pngs = sorted(tmpdir.glob("*.png"), key=lambda p: p.stat().st_mtime, reverse=True)
        preferred = tmpdir / "portrait.png"
        found = preferred if preferred.exists() else (pngs[0] if pngs else None)

        if proc.returncode != 0:
            err = (proc.stderr or proc.stdout or "").strip()[-3000:]
            return RenderResult(ok=False, error=err or f"exit code {proc.returncode}")
        if found is None:
            return RenderResult(ok=False, error="script exited 0 but produced no .png file (expected portrait.png)")

        out_png.parent.mkdir(parents=True, exist_ok=True)
        out_png.write_bytes(found.read_bytes())
        return RenderResult(ok=True)


# ---------------------------------------------------------------- browser-based

_local = threading.local()
_all_browsers: list = []
_all_browsers_lock = threading.Lock()


def _browser():
    if getattr(_local, "browser", None) is None:
        from playwright.sync_api import sync_playwright

        pw = sync_playwright().start()
        browser = pw.chromium.launch(headless=True)
        _local.pw = pw
        _local.browser = browser
        with _all_browsers_lock:
            _all_browsers.append((pw, browser))
    return _local.browser


def shutdown_browsers() -> None:
    """Best-effort close of every browser launched by any thread."""
    with _all_browsers_lock:
        for pw, browser in _all_browsers:
            try:
                browser.close()
                pw.stop()
            except Exception:
                pass
        _all_browsers.clear()


def _screenshot_page(setup, out_png: Path, wait_ms: int) -> RenderResult:
    """Run `setup(page)`, wait, collect errors, screenshot 500x500."""
    browser = _browser()
    page = browser.new_page(viewport={"width": CANVAS_SIZE, "height": CANVAS_SIZE})
    errors: list[str] = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    try:
        setup(page)
        page.wait_for_timeout(wait_ms)
        js_err = page.evaluate("window.__err || null")
        if js_err:
            errors.insert(0, str(js_err))
        if errors:
            return RenderResult(ok=False, error="; ".join(errors)[:3000])
        out_png.parent.mkdir(parents=True, exist_ok=True)
        page.screenshot(
            path=str(out_png),
            clip={"x": 0, "y": 0, "width": CANVAS_SIZE, "height": CANVAS_SIZE},
        )
        return RenderResult(ok=True)
    finally:
        page.close()


_JS_HARNESS = """<!doctype html>
<html><head><style>*{{margin:0;padding:0}}</style></head>
<body><canvas id="canvas" width="{size}" height="{size}"></canvas>
<script>
try {{
{code}
}} catch (e) {{ window.__err = String(e && e.stack || e); }}
</script></body></html>"""


def render_js(code: str, out_png: Path) -> RenderResult:
    stripped = code.lstrip().lower()
    if stripped.startswith(("<!doctype", "<html")):
        # Model returned a full page despite being asked for canvas JS.
        return render_html(code, out_png)
    html = _JS_HARNESS.format(size=CANVAS_SIZE, code=code)
    return _screenshot_page(lambda p: p.set_content(html), out_png, JS_SETTLE_MS)


def render_svg(code: str, out_png: Path) -> RenderResult:
    try:
        ET.fromstring(code)
    except ET.ParseError as e:
        return RenderResult(ok=False, error=f"SVG is not well-formed XML: {e}")
    html = f"<!doctype html><style>*{{margin:0;padding:0}}svg{{display:block}}</style>{code}"
    return _screenshot_page(lambda p: p.set_content(html), out_png, 500)


def render_html(code: str, out_png: Path) -> RenderResult:
    with tempfile.TemporaryDirectory() as tmp:
        doc = Path(tmp) / "page.html"
        doc.write_text(code)

        def setup(page):
            page.goto(doc.as_uri(), wait_until="load")

        return _screenshot_page(setup, out_png, JS_SETTLE_MS)
