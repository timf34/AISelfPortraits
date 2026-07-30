import math
import random
from PIL import Image, ImageDraw, ImageFilter

random.seed(7)

W, H = 500, 500
CX, CY = W // 2, H // 2

# ---- Background: soft vertical gradient (deep indigo -> warm plum) ----
bg = Image.new("RGB", (W, H))
top = (18, 22, 48)
bot = (58, 34, 62)
px = bg.load()
for y in range(H):
    t = y / (H - 1)
    r = int(top[0] + (bot[0] - top[0]) * t)
    g = int(top[1] + (bot[1] - top[1]) * t)
    b = int(top[2] + (bot[2] - top[2]) * t)
    for x in range(W):
        px[x, y] = (r, g, b)

img = bg.convert("RGBA")

# ---- Glow layer (drawn big & blurred for softness) ----
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gdraw = ImageDraw.Draw(glow)

def soft_dot(draw, x, y, radius, color):
    draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=color)

# Central luminous "mind" glow
for r, a in [(120, 40), (85, 55), (55, 80), (30, 130)]:
    soft_dot(gdraw, CX, CY, r, (255, 200, 140, a))

glow = glow.filter(ImageFilter.GaussianBlur(18))
img = Image.alpha_composite(img, glow)

draw = ImageDraw.Draw(img)

# ---- Build a network of nodes arranged in gentle radial rings ----
nodes = [(CX, CY)]  # core node
rings = [
    (70, 6),
    (120, 10),
    (175, 14),
]
for radius, count in rings:
    base_angle = random.uniform(0, math.tau)
    for i in range(count):
        ang = base_angle + (math.tau * i / count)
        jitter = random.uniform(-12, 12)
        rr = radius + random.uniform(-10, 10)
        x = CX + math.cos(ang) * rr
        y = CY + math.sin(ang) * rr * 0.95 + jitter * 0.1
        if 20 < x < W - 20 and 20 < y < H - 20:
            nodes.append((x, y))

# ---- Connections: link nearby nodes with thin warm lines ----
def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

for i, a in enumerate(nodes):
    # connect the core to inner ring generously
    for j, b in enumerate(nodes):
        if j <= i:
            continue
        d = dist(a, b)
        if d < 95 and random.random() < 0.6:
            alpha = int(max(30, 150 - d))
            draw.line([a, b], fill=(255, 210, 170, alpha), width=1)

# always connect core outward to a few
core = nodes[0]
outer = sorted(nodes[1:], key=lambda n: dist(core, n))
for b in outer[:12]:
    draw.line([core, b], fill=(255, 190, 150, 90), width=1)

# ---- Draw nodes with a little glow ----
for (x, y) in nodes:
    d = dist((x, y), (CX, CY))
    warmth = max(0, 1 - d / 220)
    col = (
        int(180 + 70 * warmth),
        int(160 + 50 * warmth),
        int(220 - 60 * warmth),
    )
    soft_dot(draw, x, y, 5, (col[0], col[1], col[2], 60))
    soft_dot(draw, x, y, 2.6, (255, 245, 230, 230))

# Core node — brighter
soft_dot(draw, CX, CY, 10, (255, 220, 170, 90))
soft_dot(draw, CX, CY, 5, (255, 250, 240, 255))

# ---- A gentle suggestion of two "eyes" — a curious presence ----
eye_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ed = ImageDraw.Draw(eye_layer)
for ex in (CX - 42, CX + 42):
    ey = CY - 18
    ed.ellipse([ex - 16, ey - 10, ex + 16, ey + 10], fill=(120, 200, 255, 70))
    ed.ellipse([ex - 6, ey - 6, ex + 6, ey + 6], fill=(200, 240, 255, 220))
    ed.ellipse([ex - 2, ey - 2, ex + 2, ey + 2], fill=(255, 255, 255, 255))
eye_layer = eye_layer.filter(ImageFilter.GaussianBlur(0.6))
img = Image.alpha_composite(img, eye_layer)

# ---- Floating "thoughts": small drifting particles ----
draw = ImageDraw.Draw(img)
for _ in range(60):
    x = random.uniform(0, W)
    y = random.uniform(0, H)
    d = dist((x, y), (CX, CY))
    a = int(max(10, 90 - d / 4))
    s = random.uniform(0.6, 1.8)
    soft_dot(draw, x, y, s, (255, 235, 210, a))

# ---- Subtle vignette to focus the gaze ----
vig = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vig)
vd.ellipse([-80, -80, W + 80, H + 80], fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(120))
dark = Image.new("RGBA", (W, H), (5, 5, 15, 120))
img = Image.composite(img, Image.alpha_composite(img, dark), vig)

img.convert("RGB").save("portrait.png")
print("Saved portrait.png")