from PIL import Image, ImageDraw, ImageFilter
import random
import math

# Canvas settings
W, H = 500, 500
S = 3  # supersampling for smoother edges
SW, SH = W * S, H * S

random.seed(12)

# Pillow resampling compatibility
try:
    RESAMPLE_LANCZOS = Image.Resampling.LANCZOS
    RESAMPLE_BICUBIC = Image.Resampling.BICUBIC
except AttributeError:
    RESAMPLE_LANCZOS = Image.LANCZOS
    RESAMPLE_BICUBIC = Image.BICUBIC

def lerp(a, b, t):
    return int(a + (b - a) * t)

def mix(c1, c2, t):
    return tuple(lerp(c1[i], c2[i], t) for i in range(3))

# --- Background gradient at base resolution ---
top = (10, 15, 43)
bottom = (4, 57, 69)
moon_glow = (59, 98, 123)

bg = Image.new("RGB", (W, H))
pix = bg.load()
for y in range(H):
    for x in range(W):
        t = y / (H - 1)
        col = mix(top, bottom, t)

        # soft moon glow
        dx = x - 368
        dy = y - 102
        d = math.sqrt(dx * dx + dy * dy)
        glow = max(0, 1 - d / 260) ** 2
        col = mix(col, moon_glow, glow * 0.55)

        pix[x, y] = col

img = bg.resize((SW, SH), RESAMPLE_BICUBIC).convert("RGBA")
draw = ImageDraw.Draw(img, "RGBA")

def sc(v):
    return int(round(v * S))

def pt(x, y):
    return (sc(x), sc(y))

def ellipse_box(cx, cy, rx, ry):
    return (sc(cx - rx), sc(cy - ry), sc(cx + rx), sc(cy + ry))

def draw_rotated_ellipse(base, center, size, angle, fill, outline=None, width=1):
    """Draw a rotated ellipse on base. center and size are in final-canvas coords."""
    w, h = sc(size[0]), sc(size[1])
    pad = sc(max(size) * 0.7 + 6)
    layer = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, "RGBA")
    bbox = (pad, pad, pad + w, pad + h)
    d.ellipse(bbox, fill=fill, outline=outline, width=max(1, sc(width)))
    rotated = layer.rotate(angle, expand=True, resample=RESAMPLE_BICUBIC)
    x = sc(center[0]) - rotated.size[0] // 2
    y = sc(center[1]) - rotated.size[1] // 2
    base.alpha_composite(rotated, (x, y))

def polygon(points, fill, outline=None):
    draw.polygon([pt(x, y) for x, y in points], fill=fill, outline=outline)

def line(points, fill, width=1, joint="curve"):
    draw.line([pt(x, y) for x, y in points], fill=fill, width=max(1, sc(width)), joint=joint)

# --- Stars ---
for _ in range(90):
    x = random.uniform(0, W)
    y = random.uniform(0, 240)
    r = random.choice([0.45, 0.6, 0.8, 1.1])
    a = random.randint(80, 190)
    draw.ellipse(ellipse_box(x, y, r, r), fill=(210, 236, 255, a))

# A few brighter star crosses
for _ in range(13):
    x = random.uniform(20, 480)
    y = random.uniform(20, 190)
    a = random.randint(110, 190)
    line([(x - 3, y), (x + 3, y)], fill=(220, 245, 255, a), width=0.55)
    line([(x, y - 3), (x, y + 3)], fill=(220, 245, 255, a), width=0.55)

# --- Moon glow ---
glow_layer = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow_layer, "RGBA")
for r in range(120, 28, -8):
    alpha = int(4 + (120 - r) * 0.28)
    gd.ellipse(ellipse_box(368, 102, r, r), fill=(186, 222, 232, alpha))
glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(sc(7)))
img.alpha_composite(glow_layer)

# Moon
draw = ImageDraw.Draw(img, "RGBA")
draw.ellipse(ellipse_box(368, 102, 38, 38), fill=(238, 235, 205, 255))
draw.ellipse(ellipse_box(354, 91, 5, 5), fill=(205, 205, 188, 80))
draw.ellipse(ellipse_box(381, 110, 7, 7), fill=(205, 205, 188, 65))
draw.ellipse(ellipse_box(371, 82, 3, 3), fill=(205, 205, 188, 55))
draw.arc(ellipse_box(359, 100, 28, 32), 260, 70, fill=(255, 255, 230, 95), width=sc(2))

# --- Water rings ---
water_layer = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
wd = ImageDraw.Draw(water_layer, "RGBA")

for y in [260, 304, 348, 392, 438]:
    for i in range(3):
        cx = random.uniform(60, 440)
        rx = random.uniform(55, 135)
        ry = random.uniform(8, 20)
        a = random.randint(18, 42)
        wd.arc(
            (sc(cx - rx), sc(y - ry), sc(cx + rx), sc(y + ry)),
            random.randint(0, 35),
            random.randint(160, 360),
            fill=(133, 220, 230, a),
            width=sc(random.uniform(0.8, 1.4)),
        )

# main ripples around fish
for rx, ry, a in [(170, 28, 52), (220, 40, 32), (275, 55, 20)]:
    wd.ellipse(ellipse_box(252, 292, rx, ry), outline=(125, 230, 236, a), width=sc(1.2))

water_layer = water_layer.filter(ImageFilter.GaussianBlur(sc(0.35)))
img.alpha_composite(water_layer)
draw = ImageDraw.Draw(img, "RGBA")

# --- Lily pads ---
def draw_lily(cx, cy, rx, ry, angle, color):
    draw_rotated_ellipse(img, (cx, cy), (rx * 2, ry * 2), angle, color)
    # notch
    ang = math.radians(angle)
    ux, uy = math.cos(ang), math.sin(ang)
    px, py = -uy, ux
    notch = [
        (cx + ux * rx * 0.1, cy + uy * rx * 0.1),
        (cx + ux * rx * 1.05 + px * ry * 0.45, cy + uy * rx * 1.05 + py * ry * 0.45),
        (cx + ux * rx * 0.98 - px * ry * 0.45, cy + uy * rx * 0.98 - py * ry * 0.45),
    ]
    polygon(notch, fill=(5, 43, 49, 210))
    line([(cx, cy), (cx + ux * rx * 0.82, cy + uy * rx * 0.82)], fill=(155, 226, 170, 80), width=1)

draw_lily(88, 366, 42, 22, 18, (31, 114, 84, 220))
draw_lily(420, 333, 48, 24, -24, (38, 131, 88, 215))
draw_lily(388, 425, 34, 18, 32, (28, 102, 83, 210))

# small water flowers
for cx, cy in [(75, 344), (405, 310), (392, 410)]:
    for a in range(0, 360, 72):
        dx = math.cos(math.radians(a)) * 6
        dy = math.sin(math.radians(a)) * 4
        draw.ellipse(ellipse_box(cx + dx, cy + dy, 4, 2.3), fill=(224, 178, 223, 210))
    draw.ellipse(ellipse_box(cx, cy, 2, 2), fill=(250, 230, 120, 230))

# --- Koi fish transform helpers ---
fish_cx, fish_cy = 250, 286
fish_angle = -27
ang = math.radians(fish_angle)
ux, uy = math.cos(ang), math.sin(ang)
px, py = -uy, ux

def fish_xy(x, y):
    return (fish_cx + ux * x + px * y, fish_cy + uy * x + py * y)

def fish_poly(local_points, fill, outline=None):
    polygon([fish_xy(x, y) for x, y in local_points], fill=fill, outline=outline)

# Fish shadow
shadow = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
draw_rotated_ellipse(shadow, (fish_cx + 8, fish_cy + 18), (230, 82), fish_angle, (0, 0, 0, 90))
shadow = shadow.filter(ImageFilter.GaussianBlur(sc(8)))
img.alpha_composite(shadow)
draw = ImageDraw.Draw(img, "RGBA")

# Tail and fins behind body
fish_poly([(-98, 0), (-154, -46), (-132, -5), (-156, 34)], fill=(237, 110, 77, 190))
fish_poly([(-94, 2), (-139, 48), (-118, 10)], fill=(255, 174, 95, 170))

fish_poly([(-20, -25), (40, -74), (25, -17)], fill=(238, 104, 82, 165))
fish_poly([(-5, 24), (64, 60), (34, 16)], fill=(247, 146, 89, 155))

# Body
draw_rotated_ellipse(img, (fish_cx, fish_cy), (212, 72), fish_angle, (245, 238, 214, 255), outline=(255, 255, 238, 150), width=1.2)
draw = ImageDraw.Draw(img, "RGBA")

# Koi orange patches
for lc, size, col in [
    ((72, -4), (58, 42), (223, 88, 48, 230)),
    ((20, 13), (62, 28), (235, 125, 45, 220)),
    ((-48, -12), (55, 31), (219, 91, 53, 220)),
    ((-77, 15), (34, 20), (244, 151, 64, 205)),
]:
    cx, cy = fish_xy(*lc)
    draw_rotated_ellipse(img, (cx, cy), size, fish_angle + random.uniform(-18, 18), col)

draw = ImageDraw.Draw(img, "RGBA")

# Head glow/face
hx, hy = fish_xy(98, 0)
draw.ellipse(ellipse_box(hx, hy, 22, 18), fill=(238, 132, 59, 230))

# Eye
ex, ey = fish_xy(93, -18)
draw.ellipse(ellipse_box(ex, ey, 3.5, 3.5), fill=(12, 25, 30, 255))
draw.ellipse(ellipse_box(ex - 1, ey - 1, 1, 1), fill=(255, 255, 245, 240))

# Mouth and whiskers
m1 = fish_xy(113, -4)
m2 = fish_xy(119, -1)
line([m1, m2], fill=(93, 44, 37, 190), width=1.2)
line([fish_xy(108, -8), fish_xy(129, -24), fish_xy(149, -21)], fill=(249, 206, 145, 180), width=1)
line([fish_xy(109, 7), fish_xy(129, 25), fish_xy(151, 23)], fill=(249, 206, 145, 180), width=1)

# Subtle body contour lines
for yy in [-20, 20]:
    pts = [fish_xy(x, yy * (1 - abs(x) / 120) * 0.8) for x in range(-82, 88, 18)]
    line(pts, fill=(181, 160, 132, 55), width=0.8)

# Constellation-like markings on fish
constellation = [(-50, 5), (-25, -7), (2, 3), (28, -10), (54, -2)]
for a, b in zip(constellation, constellation[1:]):
    line([fish_xy(*a), fish_xy(*b)], fill=(63, 141, 171, 80), width=0.8)
for x, y in constellation:
    sx_, sy_ = fish_xy(x, y)
    draw.ellipse(ellipse_box(sx_, sy_, 2.3, 2.3), fill=(52, 165, 196, 150))

# Highlight along back
back_pts = [fish_xy(x, -22 * (1 - (x / 115) ** 2)) for x in range(-82, 95, 12)]
line(back_pts, fill=(255, 255, 235, 95), width=1.3)

# Sparkles near the fish
for _ in range(32):
    x = random.gauss(260, 95)
    y = random.gauss(292, 55)
    r = random.uniform(0.7, 1.7)
    a = random.randint(70, 170)
    draw.ellipse(ellipse_box(x, y, r, r), fill=(170, 245, 236, a))

# Foreground dark vignette
vignette = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
vd = ImageDraw.Draw(vignette, "RGBA")
for i in range(80):
    alpha = int(i * 1.4)
    vd.rectangle((sc(i), sc(i), SW - sc(i), SH - sc(i)), outline=(0, 10, 18, alpha), width=sc(1))
vignette = vignette.filter(ImageFilter.GaussianBlur(sc(9)))
img.alpha_composite(vignette)

# Downsample to final size and save
img = img.resize((W, H), RESAMPLE_LANCZOS).convert("RGB")
img.save("portrait.png")