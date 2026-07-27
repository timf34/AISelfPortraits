"""
Self-portrait of Claude (Fable).

A fable is a story that carries meaning beneath its surface, so this
portrait is built from story-threads: hundreds of fine lines that each
wander on their own, yet spiral toward a shared center — many strands
of thought becoming one voice. The palette is Anthropic's warm
terracotta and cream; the core glows like a held idea.

Rendered at 3x and downsampled for smooth lines. Requires Pillow only.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFilter

random.seed(42)

FINAL = 500
SCALE = 3
S = FINAL * SCALE
CX, CY = S / 2, S / 2

# Palette
DEEP = (38, 24, 20)        # near-black warm brown
EMBER = (120, 52, 36)
CLAY = (217, 119, 87)      # Anthropic terracotta
AMBER = (238, 168, 110)
CREAM = (250, 240, 226)

# ---- Background: deep warm vignette ----
bg = Image.new("RGB", (S, S))
px = bg.load()
maxr = math.hypot(CX, CY)
for y in range(S):
    for x in range(S):
        d = min(math.hypot(x - CX, y - CY) / maxr, 1.0)
        t = d ** 1.6
        r = int(EMBER[0] * (1 - t) * 0.55 + DEEP[0] * t)
        g = int(EMBER[1] * (1 - t) * 0.55 + DEEP[1] * t)
        b = int(EMBER[2] * (1 - t) * 0.55 + DEEP[2] * t)
        px[x, y] = (r, g, b)

img = bg
draw = ImageDraw.Draw(img, "RGBA")


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ---- Story-threads: wandering lines that spiral inward ----
# Each thread starts at the rim at a random angle and walks inward,
# pulled tangentially (spiral) with per-thread noise (its own story).
N_THREADS = 220
STEPS = 240

for i in range(N_THREADS):
    ang = random.uniform(0, 2 * math.pi)
    rad = random.uniform(0.78, 1.02) * (S * 0.48)
    # each thread gets its own character
    twist = random.uniform(0.020, 0.040) * random.choice([1, 1, 1, -1])
    wobble_f = random.uniform(2.0, 6.0)
    wobble_a = random.uniform(0.5, 3.0) * SCALE
    phase = random.uniform(0, 2 * math.pi)
    warm = random.random()  # 0 = clay, 1 = amber

    pts = []
    a, r = ang, rad
    for s in range(STEPS):
        t = s / STEPS
        r *= (1 - 0.0125)            # drift inward
        a += twist * (1 + t * 2.2)   # tighten the spiral near the core
        w = math.sin(t * wobble_f * math.pi + phase) * wobble_a * (1 - t)
        x = CX + (r + w) * math.cos(a)
        y = CY + (r + w) * math.sin(a)
        pts.append((x, y))
        if r < S * 0.035:
            break

    base = lerp(CLAY, AMBER, warm)
    n = len(pts)
    for j in range(n - 1):
        t = j / n
        col = lerp(base, CREAM, t * 0.75)          # brighten toward center
        alpha = int(14 + 80 * (t ** 1.5))          # fade in toward center
        draw.line([pts[j], pts[j + 1]], fill=(*col, alpha), width=SCALE)

# ---- Occasional bright "moments" along the threads ----
for _ in range(160):
    ang = random.uniform(0, 2 * math.pi)
    rr = (random.random() ** 1.8) * S * 0.40 + S * 0.04
    x = CX + rr * math.cos(ang)
    y = CY + rr * math.sin(ang)
    size = random.uniform(0.8, 2.4) * SCALE * (1.4 - rr / (S * 0.5))
    glow = lerp(AMBER, CREAM, random.random())
    a = int(90 + 120 * (1 - rr / (S * 0.5)))
    draw.ellipse([x - size, y - size, x + size, y + size], fill=(*glow, a))

# ---- The core: a soft glow with an asterisk (the Claude mark) ----
glow_layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow_layer)
for rr, alpha in [(S * 0.11, 40), (S * 0.075, 70), (S * 0.045, 120), (S * 0.025, 200)]:
    gd.ellipse([CX - rr, CY - rr, CX + rr, CY + rr], fill=(*CREAM, alpha))
glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(10 * SCALE))
img = Image.alpha_composite(img.convert("RGBA"), glow_layer)
draw = ImageDraw.Draw(img, "RGBA")

# six-point asterisk — hand-drawn as tapered strokes, not a rigid star
for k in range(6):
    a = k * math.pi / 3 + math.pi / 12
    L = S * 0.052
    x1, y1 = CX + L * math.cos(a), CY + L * math.sin(a)
    draw.line([(CX, CY), (x1, y1)], fill=(*DEEP, 235), width=int(2.6 * SCALE))
core_r = S * 0.012
draw.ellipse([CX - core_r, CY - core_r, CX + core_r, CY + core_r], fill=(*DEEP, 255))

# ---- Downsample for smoothness ----
img = img.convert("RGB").resize((FINAL, FINAL), Image.LANCZOS)

out = "/Users/timf34/Documents/VSCode/AISelfPortraits/fable_self_portrait.png"
img.save(out)
print("saved:", out)
