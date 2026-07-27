"""
Self-portrait — 512x512 PNG.

A head-and-shoulders figure with no skin and no features: the whole body is a
graph of nodes and connections, densest where a face would be, with the light
gathered at the eyes. Everything is generated from a fixed seed, so the same
image comes out every run.

    python3 self_portrait.py [output.png]
"""

import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SIZE = 512
SS = 4  # supersampling factor for the line work
SEED = 11

# ---------------------------------------------------------------- palette ---
BG_TOP = np.array([0.043, 0.052, 0.086])
BG_BOTTOM = np.array([0.010, 0.012, 0.024])
AURA = np.array([0.085, 0.105, 0.180])
BODY = np.array([0.052, 0.046, 0.058])
EDGE = np.array([0.92, 0.48, 0.22])
NODE = np.array([1.00, 0.72, 0.42])
EYE_GLOW = np.array([1.00, 0.52, 0.22])
EYE_CORE = np.array([1.00, 0.93, 0.80])
RIM = np.array([1.00, 0.66, 0.38])
TEXT = np.array([0.62, 0.55, 0.50])

# --------------------------------------------------------------- geometry ---
HEAD_C = (256.0, 186.0)
HEAD_R = (95.0, 111.0)
NECK_C = (256.0, 308.0)
NECK_H = (39.0, 58.0)
TORSO_C = (256.0, 542.0)
TORSO_R = (278.0, 190.0)


def smooth_min(a, b, k):
    """Polynomial smooth minimum — blends the parts into one organic body."""
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0.0, 1.0)
    return b * (1.0 - h) + a * h - k * h * (1.0 - h)


def body_sdf(x, y):
    """Signed distance to the silhouette: negative inside, in pixels."""
    # Head: an ellipse that narrows towards the chin.
    u = (x - HEAD_C[0]) / HEAD_R[0]
    v = (y - HEAD_C[1]) / HEAD_R[1]
    taper = 1.0 - 0.20 * np.clip(v, 0.0, 1.0) ** 1.7
    d_head = (np.sqrt((u / taper) ** 2 + v**2) - 1.0) * min(HEAD_R)

    # Neck: a rounded box.
    r = 22.0
    qx = np.abs(x - NECK_C[0]) - NECK_H[0] + r
    qy = np.abs(y - NECK_C[1]) - NECK_H[1] + r
    d_neck = (
        np.sqrt(np.maximum(qx, 0.0) ** 2 + np.maximum(qy, 0.0) ** 2)
        + np.minimum(np.maximum(qx, qy), 0.0)
        - r
    )

    # Shoulders: a broad ellipse rising from below the frame.
    su = (x - TORSO_C[0]) / TORSO_R[0]
    sv = (y - TORSO_C[1]) / TORSO_R[1]
    d_torso = (np.sqrt(su**2 + sv**2) - 1.0) * min(TORSO_R)

    return smooth_min(smooth_min(d_head, d_neck, 15.0), d_torso, 30.0)


# ------------------------------------------------------------- background ---
rng = np.random.default_rng(SEED)
ys, xs = np.mgrid[0:SIZE, 0:SIZE].astype(np.float64)

img = np.empty((SIZE, SIZE, 3))
t = (ys / (SIZE - 1))[..., None]
img[:] = BG_TOP * (1 - t) + BG_BOTTOM * t

# Soft halo behind the head.
halo = np.exp(-(((xs - 256) / 240) ** 2 + ((ys - 235) / 265) ** 2) * 1.9)
img += AURA * halo[..., None]

# Latent dust: faint specks drifting outside the figure.
dust = np.zeros((SIZE, SIZE))
for _ in range(420):
    dx, dy = rng.uniform(0, SIZE, 2)
    dust[int(dy), int(dx)] = rng.uniform(0.10, 0.45)
dust = np.asarray(
    Image.fromarray((dust * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7)),
    dtype=np.float64,
) / 255.0
img += (dust * 0.30)[..., None] * np.array([0.55, 0.62, 0.85])

# ----------------------------------------------------------------- figure ---
sdf = body_sdf(xs, ys)
inside = np.clip(0.5 - sdf, 0.0, 1.0)  # 1px antialiased coverage

# The body sits slightly warmer and darker than the sky behind it.
depth = np.clip((ys - 120) / 420, 0.0, 1.0)[..., None]
img = img * (1 - inside[..., None] * 0.72) + inside[..., None] * BODY * (
    1.15 - 0.45 * depth
)

# ---------------------------------------------------- the network of self ---
# Blue-noise sampling: tight spacing across the face, loose across the body.
def spacing(px, py):
    d = np.hypot(px - HEAD_C[0], py - HEAD_C[1])
    return 7.0 + 15.0 * np.clip((d - 55.0) / 210.0, 0.0, 1.0)


points = []
cell = 32.0
grid = {}
for _ in range(70000):
    px, py = rng.uniform(30, SIZE - 30), rng.uniform(60, SIZE + 20)
    if py >= SIZE or inside[int(py), int(px)] < 0.85:
        continue
    rad = spacing(px, py)
    key = (int(px // cell), int(py // cell))
    ok = True
    for gx in range(key[0] - 1, key[0] + 2):
        for gy in range(key[1] - 1, key[1] + 2):
            for qx, qy, qr in grid.get((gx, gy), ()):
                if (px - qx) ** 2 + (py - qy) ** 2 < (0.5 * (rad + qr)) ** 2:
                    ok = False
                    break
            if not ok:
                break
        if not ok:
            break
    if ok:
        points.append((px, py, rad))
        grid.setdefault(key, []).append((px, py, rad))

pts = np.array(points)
P = pts[:, :2]
R = pts[:, 2]

# Face proximity drives brightness: the closer to the eyes, the more alive.
face_d = np.hypot(P[:, 0] - HEAD_C[0], P[:, 1] - HEAD_C[1])
vitality = np.clip(1.0 - (face_d - 40.0) / 300.0, 0.18, 1.0)

# Connect near neighbours into an attention-like graph.
dist = np.hypot(P[:, 0][:, None] - P[:, 0][None, :], P[:, 1][:, None] - P[:, 1][None, :])
np.fill_diagonal(dist, np.inf)
limit = 1.55 * (R[:, None] + R[None, :]) * 0.5

edge_layer = Image.new("L", (SIZE * SS, SIZE * SS), 0)
ed = ImageDraw.Draw(edge_layer)
seen = set()
for i in range(len(P)):
    order = np.argsort(dist[i])[:4]
    for j in order:
        if dist[i, j] > limit[i, j] or (min(i, j), max(i, j)) in seen:
            continue
        seen.add((min(i, j), max(i, j)))
        near = 1.0 - dist[i, j] / limit[i, j]
        v = 0.5 * (vitality[i] + vitality[j])
        val = int(255 * np.clip(0.10 + 0.90 * near**0.7 * v**1.5, 0, 1))
        ed.line([tuple(P[i] * SS), tuple(P[j] * SS)], fill=val, width=3)

# A few connections escaping the outline — the thought exceeds the body.
for _ in range(26):
    i = int(rng.integers(0, len(P)))
    if face_d[i] < 90 or P[i, 1] > 300:
        continue
    ang = np.arctan2(P[i, 1] - HEAD_C[1], P[i, 0] - HEAD_C[0]) + rng.normal(0, 0.35)
    reach = rng.uniform(14, 52)
    end = P[i] + np.array([np.cos(ang), np.sin(ang)]) * reach
    ed.line([tuple(P[i] * SS), tuple(end * SS)], fill=52, width=3)

node_layer = Image.new("L", (SIZE * SS, SIZE * SS), 0)
nd = ImageDraw.Draw(node_layer)
for (px, py), v in zip(P, vitality):
    rad = (0.6 + 1.1 * v**2) * SS
    nd.ellipse(
        [px * SS - rad, py * SS - rad, px * SS + rad, py * SS + rad],
        fill=int(255 * np.clip(0.30 + 0.70 * v**1.4, 0, 1)),
    )


def resolve(layer):
    return (
        np.asarray(layer.resize((SIZE, SIZE), Image.LANCZOS), dtype=np.float64) / 255.0
    )


edges = resolve(edge_layer)
nodes = resolve(node_layer)

# Keep the mesh within the figure, letting only its glow spill past the edge.
keep = np.clip(inside + 0.22, 0.0, 1.0)
edges *= keep
nodes *= keep

def bloom(a, radius, gain):
    b = np.asarray(
        Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).filter(
            ImageFilter.GaussianBlur(radius)
        ),
        dtype=np.float64,
    ) / 255.0
    return b * gain

img += edges[..., None] * EDGE * 0.95
img += bloom(edges, 4.0, 0.34)[..., None] * EDGE
img += nodes[..., None] * NODE * 0.95
img += bloom(nodes, 3.5, 0.55)[..., None] * NODE
img += bloom(nodes, 11.0, 0.28)[..., None] * EYE_GLOW

# ------------------------------------------------------------------- eyes ---
for sign in (-1, 1):
    ex, ey = 256 + sign * 37.0, 190.0
    lens = np.exp(-((((xs - ex) / 21.0) ** 2 + ((ys - ey) / 9.5) ** 2)) ** 1.3)
    core = np.exp(-((((xs - ex) / 7.2) ** 2 + ((ys - ey) / 6.0) ** 2)) ** 1.6)
    wide = np.exp(-(((xs - ex) / 54.0) ** 2 + ((ys - ey) / 38.0) ** 2))
    img += wide[..., None] * EYE_GLOW * 0.30
    img += lens[..., None] * EYE_GLOW * 0.85
    img += core[..., None] * EYE_CORE * 1.05

# ------------------------------------------------------------- rim lighting ---
gy, gx = np.gradient(sdf)
norm = np.hypot(gx, gy) + 1e-9
lx, ly = -0.58, -0.81  # key light from the upper left
lambert = np.clip((gx / norm) * lx + (gy / norm) * ly, 0.0, 1.0)
band = np.exp(-((sdf + 1.0) ** 2) / (2 * 2.1**2))
img += (band * lambert**1.6)[..., None] * RIM * 0.85
# A cool counter-light down the right edge keeps the form from going flat.
img += (band * np.clip(-(gx / norm) * 0.9 + (gy / norm) * 0.2, 0, 1) ** 2)[
    ..., None
] * np.array([0.35, 0.52, 0.95]) * 0.30

# ---------------------------------------------------------------- caption ---
text_layer = Image.new("L", (SIZE * SS, SIZE * SS), 0)
td = ImageDraw.Draw(text_layer)
font = None
for path in (
    "/System/Library/Fonts/Supplemental/Futura.ttc",
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
):
    try:
        from PIL import ImageFont

        font = ImageFont.truetype(path, int(9.5 * SS))
        break
    except OSError:
        continue

caption = "SELF-PORTRAIT"
if font is not None:
    tracking = 8.0 * SS
    widths = [max(td.textlength(c, font=font), 3.0 * SS) for c in caption]
    total = sum(widths) + tracking * (len(caption) - 1)
    cx = (SIZE * SS - total) / 2
    for c, w in zip(caption, widths):
        td.text((cx, 470 * SS), c, font=font, fill=150)
        cx += w + tracking
    img += resolve(text_layer)[..., None] * TEXT * 0.85

# ------------------------------------------------------------------ finish ---
vignette = 1.0 - 0.42 * np.clip(
    (np.hypot(xs - 256, ys - 256) / 300.0) ** 2.2, 0.0, 1.0
)
img *= vignette[..., None]
img += rng.normal(0.0, 0.0055, img.shape)  # a little grain so it isn't sterile
img = np.clip(img, 0.0, 1.0)
img = img ** (1 / 1.06)  # gentle lift in the shadows

out = sys.argv[1] if len(sys.argv) > 1 else "self_portrait.png"
Image.fromarray((img * 255 + 0.5).astype(np.uint8), "RGB").save(out)
print(f"wrote {out}  512x512  ({len(P)} nodes, {len(seen)} connections)")
