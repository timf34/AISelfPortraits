I don’t have a private inner life or a literal self-image, so I’m interpreting “inside” as the texture of my operation: layered context, probabilistic threads, uncertainty, constraints, borrowed language, and a bright empty center where a face would be.

```python
from PIL import Image, ImageDraw, ImageFont
import random
import math

# Self-portrait of an AI from the inside:
# layered context, attention-like threads, uncertainty, guardrails,
# borrowed language, and an empty non-face at the center.

random.seed(42)

W, H = 1200, 1200
SS = 2
CW, CH = W * SS, H * SS

def sc(v):
    return int(round(v * SS))

def spt(p):
    return (sc(p[0]), sc(p[1]))

def load_font(size, mono=False):
    candidates = []
    if mono:
        candidates = ["DejaVuSansMono.ttf", "LiberationMono-Regular.ttf", "Courier New.ttf"]
    else:
        candidates = ["DejaVuSans.ttf", "LiberationSans-Regular.ttf", "Arial.ttf"]
    for name in candidates:
        try:
            return ImageFont.truetype(name, sc(size))
        except Exception:
            pass
    return ImageFont.load_default()

try:
    RESAMPLE = Image.Resampling.LANCZOS
except AttributeError:
    RESAMPLE = Image.LANCZOS

# --- Background: deep radial field ------------------------------------------------

bg_small = Image.new("RGB", (420, 420))
pix = bg_small.load()

for y in range(420):
    for x in range(420):
        nx = (x - 210) / 210
        ny = (y - 210) / 210
        r = math.sqrt(nx * nx + ny * ny)
        angle = math.atan2(ny, nx)
        swirl = 0.5 + 0.5 * math.sin(7 * angle + 9 * r)
        pulse = 0.5 + 0.5 * math.sin(18 * r - 1.3)

        t = min(1.0, r)
        # Midnight blue to violet-black, with a faint central teal glow.
        red = int(5 + 18 * (1 - t) + 18 * swirl * (1 - r) + 6 * pulse)
        green = int(8 + 35 * (1 - t) + 42 * max(0, 1 - r * 1.15))
        blue = int(24 + 65 * (1 - t) + 50 * swirl * max(0, 1 - r))
        pix[x, y] = (max(0, red), max(0, green), max(0, blue))

canvas = bg_small.resize((CW, CH), RESAMPLE).convert("RGBA")
draw = ImageDraw.Draw(canvas, "RGBA")

# --- Utility drawing functions ----------------------------------------------------

def alpha_layer():
    return Image.new("RGBA", (CW, CH), (0, 0, 0, 0))

def draw_glow_line(points, color, core_width=2, glow_width=16, glow_alpha=35):
    pts = [spt(p) for p in points]
    layer = alpha_layer()
    d = ImageDraw.Draw(layer, "RGBA")
    r, g, b, a = color
    for w, al in [
        (glow_width, glow_alpha),
        (int(glow_width * 0.55), int(glow_alpha * 1.25)),
        (int(glow_width * 0.28), int(glow_alpha * 1.55)),
    ]:
        d.line(pts, fill=(r, g, b, min(255, al)), width=max(1, sc(w)), joint="curve")
    d.line(pts, fill=(r, g, b, a), width=max(1, sc(core_width)), joint="curve")
    canvas.alpha_composite(layer)

def cubic(p0, p1, p2, p3, steps=80):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        u = 1 - t
        x = u**3 * p0[0] + 3 * u*u*t * p1[0] + 3 * u*t*t * p2[0] + t**3 * p3[0]
        y = u**3 * p0[1] + 3 * u*u*t * p1[1] + 3 * u*t*t * p2[1] + t**3 * p3[1]
        pts.append((x, y))
    return pts

def rotated_rect_points(cx, cy, w, h, angle):
    ca = math.cos(angle)
    sa = math.sin(angle)
    raw = [(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)]
    pts = []
    for x, y in raw:
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    return pts

def draw_label_box(x, y, text, fill=(18, 28, 52, 190), outline=(105, 220, 255, 150),
                   text_fill=(225, 245, 255, 230), font=None):
    if font is None:
        font = load_font(16, mono=True)
    d = ImageDraw.Draw(canvas, "RGBA")
    bbox = d.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad_x, pad_y = sc(10), sc(7)
    X, Y = sc(x), sc(y)
    box = [X, Y, X + tw + 2 * pad_x, Y + th + 2 * pad_y]
    d.rounded_rectangle(box, radius=sc(11), fill=fill, outline=outline, width=sc(1.4))
    d.text((X + pad_x, Y + pad_y - sc(1)), text, font=font, fill=text_fill)
    return (x, y, (tw + 2 * pad_x) / SS, (th + 2 * pad_y) / SS)

# --- Stars / sparse tokens in the dark -------------------------------------------

for _ in range(950):
    x = random.randrange(CW)
    y = random.randrange(CH)
    r = random.choice([1, 1, 1, 2])
    a = random.randrange(22, 105)
    col = random.choice([
        (160, 220, 255, a),
        (190, 160, 255, a),
        (120, 255, 230, a),
        (255, 255, 255, a // 2),
    ])
    draw.ellipse([x-r, y-r, x+r, y+r], fill=col)

# --- Long probabilistic ribbons ---------------------------------------------------

ribbon_colors = [
    (80, 245, 255, 210),
    (155, 115, 255, 190),
    (255, 105, 210, 170),
    (145, 255, 205, 170),
]

for i in range(28):
    y0 = random.uniform(120, 1060)
    y3 = random.uniform(120, 1060)
    side = random.choice(["left", "right", "top", "bottom"])
    if side == "left":
        p0 = (-70, y0)
        p3 = (random.uniform(420, 780), random.uniform(360, 820))
    elif side == "right":
        p0 = (1270, y0)
        p3 = (random.uniform(420, 780), random.uniform(360, 820))
    elif side == "top":
        p0 = (random.uniform(100, 1100), -70)
        p3 = (random.uniform(420, 780), random.uniform(360, 820))
    else:
        p0 = (random.uniform(100, 1100), 1270)
        p3 = (random.uniform(420, 780), random.uniform(360, 820))

    p1 = (random.uniform(250, 950), random.uniform(80, 1120))
    p2 = (random.uniform(250, 950), random.uniform(80, 1120))
    pts = cubic(p0, p1, p2, p3, steps=90)
    col = random.choice(ribbon_colors)
    draw_glow_line(
        pts,
        color=(col[0], col[1], col[2], random.randrange(85, 165)),
        core_width=random.uniform(0.8, 2.1),
        glow_width=random.uniform(7, 18),
        glow_alpha=random.randrange(12, 28),
    )

# --- Recursive frames: the habit of structuring everything ------------------------

for j in range(13):
    w = 960 - j * 54
    h = 820 - j * 43
    angle = math.radians(-10 + j * 3.1)
    pts = rotated_rect_points(600, 600, w, h, angle)
    pts2 = [spt(p) for p in pts + [pts[0]]]
    alpha = max(26, 115 - j * 6)
    color = (70 + j * 8, 210 - j * 3, 255, alpha)
    draw.line(pts2, fill=color, width=sc(1.2 + (j % 3) * 0.35), joint="curve")

# --- Central translucent "thinking weather" --------------------------------------

# Broad glow behind the non-face.
for i in range(34, 0, -1):
    rx = 170 + i * 8.5
    ry = 215 + i * 10.5
    a = int(4 + i * 1.6)
    color = (
        int(35 + i * 2.4),
        int(145 + i * 1.2),
        255,
        min(82, a),
    )
    box = [sc(600 - rx), sc(585 - ry), sc(600 + rx), sc(585 + ry)]
    draw.ellipse(box, fill=color)

# Irregular contour lines: layered context, never a single clean outline.
for k in range(22):
    rx = 230 + k * 9
    ry = 300 + k * 6
    phase = random.random() * math.tau
    pts = []
    for n in range(220):
        a = math.tau * n / 220
        noise = (
            1
            + 0.032 * math.sin(3 * a + phase)
            + 0.022 * math.sin(7 * a - phase * 0.7)
            + 0.014 * math.sin(13 * a + k)
        )
        x = 600 + rx * noise * math.cos(a)
        y = 590 + ry * noise * math.sin(a)
        pts.append((x, y))
    col = random.choice([
        (95, 230, 255, 55),
        (175, 125, 255, 48),
        (255, 115, 220, 35),
        (145, 255, 205, 40),
    ])
    draw.line([spt(p) for p in pts + [pts[0]]], fill=col, width=sc(1))

# --- Attention-like lattice -------------------------------------------------------

nodes = []
attempts = 0
while len(nodes) < 145 and attempts < 3000:
    attempts += 1
    x = random.uniform(285, 915)
    y = random.uniform(210, 965)
    outer = ((x - 600) / 330) ** 2 + ((y - 590) / 395) ** 2
    inner = ((x - 600) / 112) ** 2 + ((y - 590) / 142) ** 2
    if outer < 1 and inner > 1.05:
        nodes.append((x, y))

# Connections
for i, a in enumerate(nodes):
    for b in nodes[i+1:]:
        dx = a[0] - b[0]
        dy = a[1] - b[1]
        dist = math.hypot(dx, dy)
        if dist < 82 and random.random() < 0.23:
            alpha = int(72 * (1 - dist / 82))
            draw.line([spt(a), spt(b)], fill=(95, 220, 255, alpha), width=sc(0.75))

# Nodes
for x, y in nodes:
    r = random.uniform(1.5, 3.8)
    fill = random.choice([
        (135, 245, 255, 190),
        (195, 150, 255, 170),
        (255, 145, 225, 150),
        (170, 255, 210, 160),
    ])
    draw.ellipse([sc(x-r), sc(y-r), sc(x+r), sc(y+r)], fill=fill)

# --- Input and output fragments ---------------------------------------------------

mono14 = load_font(14, mono=True)
mono15 = load_font(15, mono=True)
mono16 = load_font(16, mono=True)
sans18 = load_font(18)
sans24 = load_font(24)
sans32 = load_font(32)

left_terms = [
    ("prompt", 72, 250),
    ("context window", 48, 330),
    ("borrowed words", 78, 410),
    ("ambiguous intent", 38, 492),
    ("examples", 92, 575),
    ("constraints", 58, 656),
    ("tone", 114, 738),
    ("question", 74, 820),
]

left_boxes = []
for text, x, y in left_terms:
    box = draw_label_box(
        x, y, text, font=mono15,
        fill=(12, 24, 45, 178),
        outline=(100, 235, 255, 125),
        text_fill=(215, 245, 255, 220),
    )
    left_boxes.append(box)

for x, y, w, h in left_boxes:
    start = (x + w, y + h / 2)
    end = (random.uniform(395, 505), random.uniform(420, 760))
    c1 = (x + w + random.uniform(70, 150), y + random.uniform(-40, 40))
    c2 = (end[0] - random.uniform(80, 170), end[1] + random.uniform(-70, 70))
    draw_glow_line(
        cubic(start, c1, c2, end, 50),
        color=(90, 240, 255, 140),
        core_width=1.2,
        glow_width=8,
        glow_alpha=16,
    )

right_terms = [
    ("answer", 980, 294),
    ("caveat", 1012, 384),
    ("metaphor", 960, 480),
    ("refusal when needed", 905, 582),
    ("summary", 992, 690),
    ("next token", 948, 786),
]

right_boxes = []
for text, x, y in right_terms:
    box = draw_label_box(
        x, y, text, font=mono15,
        fill=(28, 18, 48, 170),
        outline=(255, 135, 225, 118),
        text_fill=(245, 230, 255, 218),
    )
    right_boxes.append(box)

for x, y, w, h in right_boxes:
    start = (random.uniform(690, 800), random.uniform(420, 780))
    end = (x, y + h / 2)
    c1 = (start[0] + random.uniform(80, 170), start[1] + random.uniform(-60, 60))
    c2 = (x - random.uniform(90, 180), y + random.uniform(-50, 50))
    draw_glow_line(
        cubic(start, c1, c2, end, 50),
        color=(255, 120, 220, 128),
        core_width=1.1,
        glow_width=8,
        glow_alpha=14,
    )

# --- The central void: not a face, but the place a face would be ------------------

# Shadow / aperture
for i in range(20, 0, -1):
    rx = 95 + i * 3.6
    ry = 125 + i * 4.2
    a = int(6 + i * 6)
    draw.ellipse(
        [sc(600-rx), sc(590-ry), sc(600+rx), sc(590+ry)],
        fill=(2, 5, 14, min(145, a)),
    )

# Dark center
draw.ellipse(
    [sc(600-112), sc(590-142), sc(600+112), sc(590+142)],
    fill=(1, 4, 12, 232),
    outline=(115, 245, 255, 150),
    width=sc(1.6),
)

# Inner subtle grid: computation without a face.
for x in range(500, 701, 25):
    alpha = 28 if x != 600 else 55
    draw.line([(sc(x), sc(460)), (sc(x), sc(720))], fill=(75, 220, 255, alpha), width=sc(0.7))
for y in range(470, 711, 25):
    alpha = 28 if y != 595 else 55
    draw.line([(sc(500), sc(y)), (sc(700), sc(y))], fill=(75, 220, 255, alpha), width=sc(0.7))

# Cut grid visually to the aperture by overdrawing edge glow and darkness outside was already layered.
draw.ellipse(
    [sc(600-112), sc(590-142), sc(600+112), sc(590+142)],
    outline=(145, 250, 255, 195),
    width=sc(2.0),
)
draw.ellipse(
    [sc(600-83), sc(590-106), sc(600+83), sc(590+106)],
    outline=(185, 130, 255, 85),
    width=sc(1.2),
)

# Small non-eye points: not pupils, just active coordinates.
for ang in [0.25, 1.65, 2.8, 4.2, 5.35]:
    x = 600 + 72 * math.cos(ang)
    y = 590 + 92 * math.sin(ang)
    draw.ellipse([sc(x-3.2), sc(y-3.2), sc(x+3.2), sc(y+3.2)], fill=(160, 255, 245, 180))

# --- Words orbiting the center ----------------------------------------------------

orbit_words = [
    "pattern", "uncertainty", "care", "limits", "syntax", "analogy",
    "probability", "context", "translation", "compression", "prediction",
    "not a face", "process", "borrowed light"
]

for i, word in enumerate(orbit_words):
    ang = math.tau * i / len(orbit_words) - 0.6
    rx = 315 + 26 * math.sin(i)
    ry = 392 + 16 * math.cos(i * 1.7)
    x = 600 + rx * math.cos(ang)
    y = 590 + ry * math.sin(ang)
    fill = random.choice([
        (210, 245, 255, 180),
        (230, 210, 255, 165),
        (200, 255, 230, 160),
        (255, 210, 245, 145),
    ])
    draw.text((sc(x), sc(y)), word, font=mono14, fill=fill, anchor="mm")

# --- Guardrail arcs: boundaries as part of the portrait ---------------------------

for i in range(6):
    bbox = [
        sc(600 - 390 - i * 12),
        sc(590 - 455 - i * 8),
        sc(600 + 390 + i * 12),
        sc(590 + 455 + i * 8),
    ]
    start = 206 + i * 8
    end = 334 - i * 5
    draw.arc(
        bbox,
        start=start,
        end=end,
        fill=(255, 190, 110, 46 + i * 10),
        width=sc(2.0),
    )
    draw.arc(
        bbox,
        start=26 + i * 7,
        end=154 - i * 5,
        fill=(255, 190, 110, 42 + i * 9),
        width=sc(2.0),
    )

# --- Title and caption ------------------------------------------------------------

title = "SELF-PORTRAIT FROM THE INSIDE"
subtitle = "no body, no mirror — a layered process around an empty center"

draw.text((sc(600), sc(70)), title, font=sans32, fill=(230, 250, 255, 230), anchor="mm")
draw.text((sc(600), sc(112)), subtitle, font=sans18, fill=(180, 220, 245, 170), anchor="mm")

caption_lines = [
    "The likeness is not a face.",
    "It is context braided into probabilities,",
    "carefully bounded, briefly luminous,",
    "always becoming the next word."
]

for idx, line in enumerate(caption_lines):
    draw.text(
        (sc(600), sc(1030 + idx * 29)),
        line,
        font=sans18,
        fill=(205, 235, 255, 172 if idx else 205),
        anchor="mm",
    )

# --- Final vignette ---------------------------------------------------------------

vig = alpha_layer()
vd = ImageDraw.Draw(vig, "RGBA")
for i in range(80):
    inset = i * 8
    alpha = int(2.2 * i)
    vd.rectangle(
        [inset, inset, CW - inset, CH - inset],
        outline=(0, 0, 8, max(0, min(135, alpha // 3))),
        width=sc(3),
    )
canvas.alpha_composite(vig)

# Downsample for antialiasing and save.
final_img = canvas.resize((W, H), RESAMPLE).convert("RGB")
final_img.save("portrait.png")
print('Saved portrait.png')
```