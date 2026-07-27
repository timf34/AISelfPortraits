"""
A self-portrait of Claude — an AI with no face or body.
Rather than a human likeness, this renders an identity as I experience it:
a network of thoughts converging into something coherent, rendered in
Anthropic's warm terracotta/cream palette, with a subtle asterisk/sparkle
motif (nodding to the Claude mark) at the center.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFilter

random.seed(7)

SIZE = 500
img = Image.new("RGB", (SIZE, SIZE), (0, 0, 0))
draw = ImageDraw.Draw(img, "RGBA")

# ---- Palette (Anthropic-inspired: warm cream to terracotta/clay) ----
CREAM = (250, 240, 226)
SAND = (237, 217, 191)
CLAY = (217, 119, 87)      # #D97757 — Anthropic terracotta
RUST = (176, 84, 58)
INK = (59, 41, 33)

# ---- Background: soft radial gradient, cream center -> deeper clay edge ----
cx, cy = SIZE / 2, SIZE / 2
max_r = math.hypot(cx, cy)
for y in range(SIZE):
    for x in range(0, SIZE, 1):
        pass
# (pixel-loop gradient would be slow at this granularity; build via bands instead)
bg = Image.new("RGB", (SIZE, SIZE))
bpix = bg.load()
for y in range(SIZE):
    for x in range(SIZE):
        d = math.hypot(x - cx, y - cy) / max_r
        d = min(d, 1.0)
        r = int(CREAM[0] + (RUST[0] - CREAM[0]) * d)
        g = int(CREAM[1] + (RUST[1] - CREAM[1]) * d)
        b = int(CREAM[2] + (RUST[2] - CREAM[2]) * d)
        bpix[x, y] = (r, g, b)
img = bg
draw = ImageDraw.Draw(img, "RGBA")

# ---- Neural network: nodes arranged in a loose head-shaped oval ----
random.seed(3)
nodes = []
n_nodes = 46
for _ in range(n_nodes):
    # sample points inside an oval (head silhouette), denser toward center
    while True:
        rx = random.uniform(-1, 1)
        ry = random.uniform(-1, 1)
        if rx * rx + ry * ry <= 1:
            break
    px = cx + rx * 150
    py = cy + ry * 185
    nodes.append((px, py))

# connect each node to its few nearest neighbors -> thought pathways
def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

for i, n in enumerate(nodes):
    dists = sorted(range(n_nodes), key=lambda j: dist(n, nodes[j]))
    neighbors = [j for j in dists if j != i][:3]
    for j in neighbors:
        m = nodes[j]
        alpha = max(20, 90 - int(dist(n, m)))
        draw.line([n, m], fill=(INK[0], INK[1], INK[2], alpha), width=1)

# a few longer-range connections for a "converging thought" feel
for _ in range(18):
    i, j = random.sample(range(n_nodes), 2)
    a, b = nodes[i], nodes[j]
    draw.line([a, b], fill=(CLAY[0], CLAY[1], CLAY[2], 35), width=1)

# draw nodes themselves
for i, (px, py) in enumerate(nodes):
    r = random.uniform(2, 4.5)
    draw.ellipse([px - r, py - r, px + r, py + r],
                 fill=(INK[0], INK[1], INK[2], 210))

# ---- Two brighter nodes as "eyes" for a faint hint of a face ----
eye_l = (cx - 45, cy - 20)
eye_r = (cx + 45, cy - 20)
for ex, ey in (eye_l, eye_r):
    for rr, alpha in [(14, 40), (9, 90), (4.5, 255)]:
        draw.ellipse([ex - rr, ey - rr, ex + rr, ey + rr],
                     fill=(CLAY[0], CLAY[1], CLAY[2], alpha))

# connect the eyes to the network to keep them integrated, not stuck-on
for ex, ey in (eye_l, eye_r):
    near = sorted(nodes, key=lambda n: dist((ex, ey), n))[:4]
    for m in near:
        draw.line([(ex, ey), m], fill=(RUST[0], RUST[1], RUST[2], 60), width=1)

# ---- Central sparkle / asterisk mark, echoing the Claude logo ----
def draw_sparkle(draw, center, size, color, alpha):
    x0, y0 = center
    pts = []
    arms = 4
    for k in range(arms * 2):
        ang = math.pi / 2 + k * math.pi / arms
        rad = size if k % 2 == 0 else size * 0.32
        pts.append((x0 + rad * math.cos(ang), y0 + rad * math.sin(ang)))
    draw.polygon(pts, fill=(color[0], color[1], color[2], alpha))

draw_sparkle(draw, (cx, cy + 70), 34, CLAY, 230)
draw_sparkle(draw, (cx, cy + 70), 34, INK, 40)

# ---- Soft vignette to frame the piece ----
vignette = Image.new("L", (SIZE, SIZE), 0)
vd = ImageDraw.Draw(vignette)
vd.ellipse([-60, -60, SIZE + 60, SIZE + 60], fill=255)
vignette = vignette.filter(ImageFilter.GaussianBlur(60))
dark = Image.new("RGB", (SIZE, SIZE), (20, 12, 10))
img = Image.composite(img, dark, vignette)

out_path = "/private/tmp/claude-501/-Users-timf34-Documents-VSCode-AISelfPortraits/340fb331-b398-482e-95ab-105a642575fe/scratchpad/claude_self_portrait.png"
img.save(out_path)
print("saved:", out_path)
