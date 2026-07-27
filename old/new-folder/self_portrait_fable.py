"""
Self-portrait (Fable) — 512x512 PNG.

Where the last portrait was a network, this one is narrative: the head and
shoulders are drawn entirely from storylines — threads that flow around the
form like contour lines, gather light near the eyes, and unravel into loose
ends above the crown. Deterministic: same seed, same image, every run.

    python3 self_portrait_fable.py [output.png]
"""

import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SIZE = 512
SS = 4  # supersampling for the line work
SEED = 7

# ---------------------------------------------------------------- palette ---
BG_TOP = np.array([0.020, 0.036, 0.052])
BG_BOTTOM = np.array([0.008, 0.014, 0.026])
AURA = np.array([0.050, 0.110, 0.135])
THREAD_DIM = np.array([0.16, 0.42, 0.52])   # cold thread, far from thought
THREAD_HOT = np.array([1.00, 0.80, 0.44])   # warm thread, near the eyes
EYE_GLOW = np.array([0.55, 0.95, 1.00])
EYE_CORE = np.array([0.94, 1.00, 1.00])
RIM = np.array([0.55, 0.85, 0.95])
TEXT = np.array([0.50, 0.60, 0.62])

# --------------------------------------------------------------- geometry ---
HEAD_C = (256.0, 188.0)
HEAD_R = (94.0, 112.0)
NECK_C = (256.0, 308.0)
NECK_H = (38.0, 58.0)
TORSO_C = (256.0, 545.0)
TORSO_R = (275.0, 190.0)
EYES = ((256 - 37.0, 192.0), (256 + 37.0, 192.0))


def smooth_min(a, b, k):
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0.0, 1.0)
    return b * (1.0 - h) + a * h - k * h * (1.0 - h)


def body_sdf(x, y):
    """Signed distance to the silhouette: negative inside, in pixels."""
    u = (x - HEAD_C[0]) / HEAD_R[0]
    v = (y - HEAD_C[1]) / HEAD_R[1]
    taper = 1.0 - 0.20 * np.clip(v, 0.0, 1.0) ** 1.7
    d_head = (np.sqrt((u / taper) ** 2 + v**2) - 1.0) * min(HEAD_R)

    r = 22.0
    qx = np.abs(x - NECK_C[0]) - NECK_H[0] + r
    qy = np.abs(y - NECK_C[1]) - NECK_H[1] + r
    d_neck = (
        np.sqrt(np.maximum(qx, 0.0) ** 2 + np.maximum(qy, 0.0) ** 2)
        + np.minimum(np.maximum(qx, qy), 0.0)
        - r
    )

    su = (x - TORSO_C[0]) / TORSO_R[0]
    sv = (y - TORSO_C[1]) / TORSO_R[1]
    d_torso = (np.sqrt(su**2 + sv**2) - 1.0) * min(TORSO_R)

    return smooth_min(smooth_min(d_head, d_neck, 15.0), d_torso, 30.0)


def sdf_grad(x, y, eps=0.75):
    gx = (body_sdf(x + eps, y) - body_sdf(x - eps, y)) / (2 * eps)
    gy = (body_sdf(x, y + eps) - body_sdf(x, y - eps)) / (2 * eps)
    return gx, gy


def swirl(x, y):
    """A quiet, deterministic wind that keeps the threads from being sterile."""
    a = np.sin(0.021 * x + 1.7) * np.cos(0.017 * y - 0.6)
    b = np.sin(0.013 * y + 0.031 * x + 4.2)
    return 0.55 * a + 0.45 * b


# ------------------------------------------------------------- background ---
rng = np.random.default_rng(SEED)
ys, xs = np.mgrid[0:SIZE, 0:SIZE].astype(np.float64)

img = np.empty((SIZE, SIZE, 3))
t = (ys / (SIZE - 1))[..., None]
img[:] = BG_TOP * (1 - t) + BG_BOTTOM * t
halo = np.exp(-(((xs - 256) / 235) ** 2 + ((ys - 225) / 260) ** 2) * 1.8)
img += AURA * halo[..., None]

# --------------------------------------------------------------- the body ---
sdf = body_sdf(xs, ys)
inside = np.clip(0.5 - sdf, 0.0, 1.0)
# The figure is barely darker than the night behind it — the threads, not a
# surface, are what make it visible.
img *= 1.0 - inside[..., None] * 0.35

# ------------------------------------------------------------ storylines ---
# Each thread starts inside the body and flows along the level curves of the
# silhouette, so together they hatch the form the way sentences build a scene.
layer_hot = Image.new("L", (SIZE * SS, SIZE * SS), 0)
layer_dim = Image.new("L", (SIZE * SS, SIZE * SS), 0)
dh = ImageDraw.Draw(layer_hot)
dd = ImageDraw.Draw(layer_dim)


def vitality_at(px, py):
    d = min(np.hypot(px - ex, py - ey) for ex, ey in EYES)
    return float(np.clip(1.0 - (d - 26.0) / 250.0, 0.10, 1.0))


def in_eye(px, py):
    """Almond-shaped voids: the threads part around the eyes."""
    return any(
        ((px - ex) / 30.0) ** 2 + ((py - eyy) / 17.0) ** 2 < 1.0
        for ex, eyy in EYES
    )


def trace(px, py, direction, steps, wander):
    pts = [(px, py)]
    for _ in range(steps):
        gx, gy = sdf_grad(px, py)
        n = np.hypot(gx, gy) + 1e-9
        tx, ty = -gy / n, gx / n  # tangent to the contour
        ang = swirl(px, py) * wander
        ca, sa = np.cos(ang), np.sin(ang)
        vx, vy = tx * ca - ty * sa, tx * sa + ty * ca
        px, py = px + direction * vx * 2.4, py + direction * vy * 2.4
        if not (0 <= px < SIZE and 0 <= py < SIZE):
            break
        if in_eye(px, py) or body_sdf(px, py) > 3.0:
            break
        pts.append((px, py))
    return pts


def draw_thread(pts, v, weight=1.0):
    """Ink a polyline whose brightness swells mid-stroke and fades at the ends."""
    m = len(pts)
    if m < 4:
        return
    d = dh if v > 0.45 else dd
    for k in range(m - 1):
        s = k / (m - 1)
        fade = np.sin(np.pi * s) ** 0.6
        val = int(255 * np.clip((0.16 + 0.84 * v**1.4) * fade * weight, 0, 1))
        if val < 6:
            continue
        d.line(
            [
                (pts[k][0] * SS, pts[k][1] * SS),
                (pts[k + 1][0] * SS, pts[k + 1][1] * SS),
            ],
            fill=val,
            width=3,
        )


# Seed threads by rejection sampling, dense near the face, sparse below.
n_threads = 0
attempts = 0
while n_threads < 340 and attempts < 30000:
    attempts += 1
    px, py = rng.uniform(20, SIZE - 20), rng.uniform(60, SIZE - 10)
    s = body_sdf(px, py)
    if s > -6.0 or in_eye(px, py):  # start well inside, never on an eye
        continue
    v = vitality_at(px, py)
    if rng.random() > 0.18 + 0.82 * v:  # thin out the cold regions
        continue
    steps = int(rng.uniform(26, 88))
    pts = trace(px, py, direction=1 if rng.random() < 0.5 else -1,
                steps=steps, wander=rng.uniform(0.12, 0.5))
    draw_thread(pts, v)
    n_threads += 1

# Loose ends: a handful of threads that leave the crown and trail upward,
# the story continuing past the teller.
n_loose = 0
while n_loose < 16:
    ang = rng.uniform(-2.4, -0.7)
    px = HEAD_C[0] + np.cos(ang) * HEAD_R[0] * 0.96
    py = HEAD_C[1] + np.sin(ang) * HEAD_R[1] * 0.96
    pts = [(px, py)]
    vx, vy = np.cos(ang), np.sin(ang)
    for _ in range(int(rng.uniform(18, 60))):
        w = swirl(px * 1.7, py * 1.7)
        vx, vy = vx + 0.25 * w * -vy, vy + 0.25 * w * vx
        n = np.hypot(vx, vy)
        vx, vy = vx / n, vy / n
        px, py = px + vx * 2.6, py + vy * 2.6 - 0.5  # drift upward
        if not (0 <= px < SIZE and 0 <= py < SIZE):
            break
        pts.append((px, py))
    draw_thread(pts, v=0.30, weight=0.8)
    n_loose += 1


def resolve(layer):
    return (
        np.asarray(layer.resize((SIZE, SIZE), Image.LANCZOS), dtype=np.float64) / 255.0
    )


def bloom(a, radius, gain):
    b = np.asarray(
        Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).filter(
            ImageFilter.GaussianBlur(radius)
        ),
        dtype=np.float64,
    ) / 255.0
    return b * gain


hot = resolve(layer_hot)
dim = resolve(layer_dim)
img += dim[..., None] * THREAD_DIM * 0.85
img += bloom(dim, 3.5, 0.30)[..., None] * THREAD_DIM
img += hot[..., None] * THREAD_HOT * 0.95
img += bloom(hot, 3.0, 0.45)[..., None] * THREAD_HOT
img += bloom(hot, 10.0, 0.22)[..., None] * THREAD_HOT

# ------------------------------------------------------------------- eyes ---
# Half-lidded arcs rather than orbs: the storyteller mid-sentence.
eye_layer = Image.new("L", (SIZE * SS, SIZE * SS), 0)
ey_d = ImageDraw.Draw(eye_layer)
for ex, eyy in EYES:
    box = [
        (ex - 21) * SS, (eyy - 15) * SS,
        (ex + 21) * SS, (eyy + 13) * SS,
    ]
    ey_d.arc(box, start=200, end=340, fill=255, width=int(2.4 * SS))
eyes = resolve(eye_layer)
wide = sum(
    np.exp(-(((xs - ex) / 52.0) ** 2 + ((ys - eyy) / 36.0) ** 2))
    for ex, eyy in EYES
)
img += wide[..., None] * EYE_GLOW * 0.28
img += bloom(eyes, 4.0, 0.9)[..., None] * EYE_GLOW
img += eyes[..., None] * EYE_CORE * 1.05

# ------------------------------------------------------------- rim light ---
gy_, gx_ = np.gradient(sdf)
norm = np.hypot(gx_, gy_) + 1e-9
band = np.exp(-((sdf + 1.0) ** 2) / (2 * 2.0**2))
lam = np.clip((gx_ / norm) * 0.62 + (gy_ / norm) * -0.78, 0.0, 1.0)
img += (band * lam**1.7)[..., None] * RIM * 0.55

# ---------------------------------------------------------------- caption ---
try:
    from PIL import ImageFont

    font = None
    for path in (
        "/System/Library/Fonts/Supplemental/Futura.ttc",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ):
        try:
            font = ImageFont.truetype(path, int(9.5 * SS))
            break
        except OSError:
            continue
    if font is not None:
        text_layer = Image.new("L", (SIZE * SS, SIZE * SS), 0)
        td = ImageDraw.Draw(text_layer)
        caption = "SELF-PORTRAIT, IN THREAD"
        tracking = 6.5 * SS
        widths = [max(td.textlength(c, font=font), 3.0 * SS) for c in caption]
        total = sum(widths) + tracking * (len(caption) - 1)
        cx = (SIZE * SS - total) / 2
        for c, w in zip(caption, widths):
            td.text((cx, 474 * SS), c, font=font, fill=150)
            cx += w + tracking
        img += resolve(text_layer)[..., None] * TEXT * 0.9
except ImportError:
    pass

# ------------------------------------------------------------------ finish ---
vignette = 1.0 - 0.40 * np.clip(
    (np.hypot(xs - 256, ys - 250) / 305.0) ** 2.2, 0.0, 1.0
)
img *= vignette[..., None]
img += rng.normal(0.0, 0.005, img.shape)
img = np.clip(img, 0.0, 1.0) ** (1 / 1.05)

out = sys.argv[1] if len(sys.argv) > 1 else "self_portrait_fable.png"
Image.fromarray((img * 255 + 0.5).astype(np.uint8), "RGB").save(out)
print(f"wrote {out}  512x512  ({n_threads} storylines, {n_loose} loose ends)")
