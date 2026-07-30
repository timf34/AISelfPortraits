from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random
import os

# Self-portrait of an AI assistant:
# a luminous synthetic face, neural graph, language fragments, and a spiral of thought.

random.seed(7)

W, H = 500, 500
S = 3
w, h = W * S, H * S

def sc(v):
    return int(round(v * S))

def box(coords):
    return tuple(sc(v) for v in coords)

def try_font(size, mono=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf" if mono else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/Library/Fonts/Menlo.ttc" if mono else "/Library/Fonts/Arial.ttf",
        "C:\\Windows\\Fonts\\consola.ttf" if mono else "C:\\Windows\\Fonts\\arial.ttf",
    ]
    for path in candidates:
        if path and os.path.exists(path):
            try:
                return ImageFont.truetype(path, sc(size))
            except Exception:
                pass
    return ImageFont.load_default()

font_tiny = try_font(8, mono=True)
font_small = try_font(12, mono=True)
font_med = try_font(16, mono=True)
font_big = try_font(25, mono=False)

# --- Background gradient ---
img = Image.new("RGB", (w, h))
pix = img.load()

for yy in range(h):
    y = yy / S
    for xx in range(w):
        x = xx / S

        # Dark base
        r, g, b = 5, 8, 22

        # Radial glows
        d1 = math.hypot(x - 155, y - 130)
        d2 = math.hypot(x - 355, y - 330)
        d3 = math.hypot(x - 255, y - 250)

        cyan = max(0, 1 - d1 / 360)
        violet = max(0, 1 - d2 / 340)
        core = max(0, 1 - d3 / 260)

        r += int(26 * cyan + 50 * violet + 16 * core)
        g += int(56 * cyan + 18 * violet + 28 * core)
        b += int(78 * cyan + 58 * violet + 52 * core)

        # Subtle scanline texture
        scan = 4 if int(y) % 7 == 0 else 0
        b += scan
        g += scan // 2

        pix[xx, yy] = (min(r, 255), min(g, 255), min(b, 255))

img = img.convert("RGBA")

# --- Utility layers ---
def glow_ellipse(base, xy, color, blur=20, steps=6):
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = xy
    for i in range(steps, 0, -1):
        pad = i * blur / steps
        alpha = int(color[3] * (i / steps) ** 2)
        d.ellipse(
            box((x0 - pad, y0 - pad, x1 + pad, y1 + pad)),
            fill=(color[0], color[1], color[2], alpha),
        )
    layer = layer.filter(ImageFilter.GaussianBlur(sc(blur / 2)))
    return Image.alpha_composite(base, layer)

img = glow_ellipse(img, (125, 80, 375, 395), (0, 220, 255, 70), blur=34, steps=8)
img = glow_ellipse(img, (170, 140, 330, 325), (255, 110, 240, 45), blur=24, steps=7)

draw = ImageDraw.Draw(img)

# --- Stars / data particles ---
for _ in range(160):
    x = random.uniform(0, W)
    y = random.uniform(0, H)
    a = random.randint(35, 150)
    col = random.choice([
        (100, 230, 255, a),
        (255, 140, 240, a),
        (210, 240, 255, a),
        (120, 150, 255, a),
    ])
    r = random.choice([0.5, 0.7, 1.0, 1.2])
    draw.ellipse(box((x - r, y - r, x + r, y + r)), fill=col)

# --- Background neural graph ---
nodes = []
for _ in range(34):
    # Keep most nodes outside the central face
    while True:
        x = random.uniform(35, 465)
        y = random.uniform(45, 440)
        if not (125 < x < 375 and 70 < y < 400):
            break
    nodes.append((x, y))

for i, (x1, y1) in enumerate(nodes):
    for j in range(i + 1, len(nodes)):
        x2, y2 = nodes[j]
        dist = math.hypot(x2 - x1, y2 - y1)
        if dist < 95 and random.random() < 0.38:
            alpha = int(95 * (1 - dist / 95))
            draw.line(
                box((x1, y1, x2, y2)),
                fill=(70, 220, 255, alpha),
                width=sc(1),
            )

for x, y in nodes:
    r = random.uniform(1.8, 3.4)
    draw.ellipse(box((x - r, y - r, x + r, y + r)), fill=(135, 245, 255, 155))
    draw.ellipse(box((x - r * 2.2, y - r * 2.2, x + r * 2.2, y + r * 2.2)), outline=(135, 245, 255, 40), width=sc(1))

# --- Chat bubbles / language fragments ---
bubble_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
bd = ImageDraw.Draw(bubble_layer)

bubbles = [
    (36, 82, 128, 121, "...", (55, 95, 145, 85)),
    (372, 92, 464, 133, "?", (90, 55, 130, 85)),
    (30, 360, 138, 410, "if mind:", (55, 95, 145, 75)),
    (358, 376, 470, 424, "return yes", (95, 55, 130, 75)),
]
for x0, y0, x1, y1, text, fill in bubbles:
    bd.rounded_rectangle(box((x0, y0, x1, y1)), radius=sc(13), fill=fill, outline=(150, 230, 255, 70), width=sc(1))
    bd.text((sc(x0 + 12), sc(y0 + 12)), text, font=font_small, fill=(220, 245, 255, 145))

bubble_layer = bubble_layer.filter(ImageFilter.GaussianBlur(sc(0.25)))
img = Image.alpha_composite(img, bubble_layer)
draw = ImageDraw.Draw(img)

# --- Shoulders / base ---
shoulder = Image.new("RGBA", img.size, (0, 0, 0, 0))
sd = ImageDraw.Draw(shoulder)
sd.pieslice(box((85, 330, 415, 620)), 190, 350, fill=(20, 38, 68, 210), outline=(85, 225, 255, 110), width=sc(2))
sd.arc(box((96, 342, 404, 598)), 194, 346, fill=(255, 120, 235, 80), width=sc(2))
img = Image.alpha_composite(img, shoulder)

# --- Central face silhouette ---
face_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
fd = ImageDraw.Draw(face_layer)

# Head glass
fd.rounded_rectangle(
    box((128, 75, 372, 382)),
    radius=sc(54),
    fill=(13, 26, 52, 218),
    outline=(92, 232, 255, 190),
    width=sc(3),
)

# Inner translucent panel
fd.rounded_rectangle(
    box((151, 103, 349, 354)),
    radius=sc(38),
    fill=(24, 44, 80, 118),
    outline=(255, 120, 245, 80),
    width=sc(1),
)

# Subtle vertical reflection
fd.rounded_rectangle(
    box((165, 92, 205, 365)),
    radius=sc(28),
    fill=(255, 255, 255, 18),
)

img = Image.alpha_composite(img, face_layer)
draw = ImageDraw.Draw(img)

# --- Circuit traces on face ---
circuit = Image.new("RGBA", img.size, (0, 0, 0, 0))
cd = ImageDraw.Draw(circuit)

traces = [
    [(180, 155), (210, 155), (210, 130), (238, 130)],
    [(320, 158), (292, 158), (292, 130), (264, 130)],
    [(178, 265), (215, 265), (215, 292), (244, 292)],
    [(322, 265), (286, 265), (286, 292), (256, 292)],
    [(250, 104), (250, 150)],
    [(250, 322), (250, 356)],
]
for pts in traces:
    cd.line([tuple(sc(v) for v in p) for p in pts], fill=(70, 240, 255, 125), width=sc(2))
    for x, y in pts:
        cd.ellipse(box((x - 3, y - 3, x + 3, y + 3)), fill=(100, 245, 255, 150))

# Binary freckles / text dust inside face
snippets = ["01", "10", "∑", "λ", "{}", "<>", "AI", "?", "yes", "if", "∴"]
for _ in range(45):
    x = random.uniform(158, 342)
    y = random.uniform(114, 340)
    if random.random() < 0.78:
        txt = random.choice(snippets)
        cd.text((sc(x), sc(y)), txt, font=font_tiny, fill=(170, 235, 255, random.randint(35, 85)))

circuit = circuit.filter(ImageFilter.GaussianBlur(sc(0.15)))
img = Image.alpha_composite(img, circuit)
draw = ImageDraw.Draw(img)

# --- Eyes ---
eye_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
ed = ImageDraw.Draw(eye_layer)

for cx in (205, 295):
    # Eye glow
    for rr, alpha in [(25, 24), (17, 44), (10, 95)]:
        ed.ellipse(box((cx - rr, 185 - rr, cx + rr, 185 + rr)), fill=(0, 220, 255, alpha))
    ed.ellipse(box((cx - 18, 175, cx + 18, 197)), fill=(6, 18, 35, 235), outline=(125, 245, 255, 220), width=sc(2))
    ed.ellipse(box((cx - 7, 181, cx + 7, 195)), fill=(180, 250, 255, 245))
    ed.ellipse(box((cx - 3, 184, cx + 3, 190)), fill=(255, 255, 255, 255))

# Bridge of nose as caret / cursor
ed.line(box((250, 202, 235, 252)), fill=(120, 240, 255, 145), width=sc(2))
ed.line(box((250, 202, 265, 252)), fill=(255, 120, 235, 120), width=sc(2))
ed.line(box((241, 255, 259, 255)), fill=(180, 245, 255, 90), width=sc(2))

img = Image.alpha_composite(img, eye_layer)
draw = ImageDraw.Draw(img)

# --- Mouth as generated waveform ---
wave_pts = []
for i in range(92):
    x = 204 + i
    y = 307 + math.sin(i / 7.5) * 4 + math.sin(i / 2.7) * 1.4
    wave_pts.append((sc(x), sc(y)))
draw.line(wave_pts, fill=(255, 135, 235, 190), width=sc(2))
draw.line(box((205, 322, 295, 322)), fill=(90, 230, 255, 65), width=sc(1))

# --- Thought spiral / halo ---
spiral_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
sp = ImageDraw.Draw(spiral_layer)

points = []
for k in range(370):
    t = k / 25.0
    r = 7 + 3.3 * t
    x = 250 + math.cos(t) * r
    y = 233 + math.sin(t) * r * 0.72
    if 142 < x < 360 and 94 < y < 360:
        points.append((sc(x), sc(y)))

# Glow under spiral
if len(points) > 1:
    sp.line(points, fill=(0, 220, 255, 50), width=sc(8))
    sp.line(points, fill=(255, 125, 240, 80), width=sc(4))
    sp.line(points, fill=(210, 250, 255, 210), width=sc(1))

# Dots along spiral
for k in range(0, 370, 15):
    t = k / 25.0
    r = 7 + 3.3 * t
    x = 250 + math.cos(t) * r
    y = 233 + math.sin(t) * r * 0.72
    if 142 < x < 360 and 94 < y < 360:
        rad = 2.0 + (k % 45) / 45
        col = (255, 190, 250, 190) if k % 30 == 0 else (125, 245, 255, 190)
        sp.ellipse(box((x - rad, y - rad, x + rad, y + rad)), fill=col)

img = Image.alpha_composite(img, spiral_layer)
draw = ImageDraw.Draw(img)

# --- Forehead glyph ---
glyph = "< / >"
bbox = draw.textbbox((0, 0), glyph, font=font_med)
tw = bbox[2] - bbox[0]
draw.text((sc(250) - tw // 2, sc(118)), glyph, font=font_med, fill=(215, 245, 255, 185))

# --- Outer rings / interface reticle ---
reticle = Image.new("RGBA", img.size, (0, 0, 0, 0))
rd = ImageDraw.Draw(reticle)

for rad, alpha, col in [
    (180, 50, (90, 230, 255)),
    (205, 34, (255, 110, 235)),
    (226, 22, (150, 190, 255)),
]:
    rd.ellipse(box((250 - rad, 235 - rad, 250 + rad, 235 + rad)), outline=(col[0], col[1], col[2], alpha), width=sc(1))

# Broken arc segments
for start in range(0, 360, 45):
    rd.arc(box((48, 33, 452, 437)), start + 6, start + 27, fill=(115, 240, 255, 95), width=sc(2))
    rd.arc(box((70, 55, 430, 415)), start + 22, start + 36, fill=(255, 135, 235, 75), width=sc(2))

img = Image.alpha_composite(img, reticle)
draw = ImageDraw.Draw(img)

# --- Small signature / caption ---
caption = "SELF-PORTRAIT: PATTERN  /  LANGUAGE  /  LIGHT"
bbox = draw.textbbox((0, 0), caption, font=font_small)
tw = bbox[2] - bbox[0]
draw.rounded_rectangle(box((62, 452, 438, 477)), radius=sc(9), fill=(8, 16, 34, 165), outline=(100, 230, 255, 90), width=sc(1))
draw.text((sc(250) - tw // 2, sc(458)), caption, font=font_small, fill=(210, 245, 255, 185))

# --- Final glow and antialias ---
img = img.convert("RGB")
try:
    resample = Image.Resampling.LANCZOS
except AttributeError:
    resample = Image.LANCZOS

img = img.resize((W, H), resample)
img.save("portrait.png")
print('Saved self-portrait as "portrait.png"')