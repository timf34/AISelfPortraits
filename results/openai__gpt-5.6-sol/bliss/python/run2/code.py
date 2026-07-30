from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math
import random

# Supersampling for smooth edges
SCALE = 3
W = H = 500
SIZE = W * SCALE

random.seed(12)

def sc(v):
    return int(v * SCALE)

def pt(x, y):
    return (sc(x), sc(y))

def cubic_bezier(p0, p1, p2, p3, steps=80):
    points = []
    for i in range(steps + 1):
        t = i / steps
        u = 1 - t
        x = (
            u**3 * p0[0]
            + 3 * u**2 * t * p1[0]
            + 3 * u * t**2 * p2[0]
            + t**3 * p3[0]
        )
        y = (
            u**3 * p0[1]
            + 3 * u**2 * t * p1[1]
            + 3 * u * t**2 * p2[1]
            + t**3 * p3[1]
        )
        points.append(pt(x, y))
    return points

def glowing_line(base, points, color, width=2, glow=9):
    glow_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow_layer)
    gd.line(points, fill=color, width=sc(width + 3), joint="curve")
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(sc(glow)))
    base.alpha_composite(glow_layer)

    core = Image.new("RGBA", base.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(core)
    cd.line(points, fill=color, width=sc(width), joint="curve")
    base.alpha_composite(core)

def glowing_dot(base, x, y, radius, color, glow=7):
    halo = Image.new("RGBA", base.size, (0, 0, 0, 0))
    hd = ImageDraw.Draw(halo)
    hd.ellipse(
        (sc(x-radius), sc(y-radius), sc(x+radius), sc(y+radius)),
        fill=color
    )
    halo = halo.filter(ImageFilter.GaussianBlur(sc(glow)))
    base.alpha_composite(halo)

    core = Image.new("RGBA", base.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(core)
    cd.ellipse(
        (sc(x-radius), sc(y-radius), sc(x+radius), sc(y+radius)),
        fill=(235, 250, 255, 235)
    )
    base.alpha_composite(core)

# ---------------------------------------------------------------------
# Background: radial midnight gradient
# ---------------------------------------------------------------------
img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 255))
pixels = img.load()

for y in range(SIZE):
    for x in range(SIZE):
        nx = (x / SCALE - 250) / 355
        ny = (y / SCALE - 242) / 355
        d = min(1.0, math.sqrt(nx * nx + ny * ny))
        vignette = d ** 1.45

        # Deep blue-black with a subtle violet center
        r = int(13 * (1-vignette) + 2 * vignette)
        g = int(22 * (1-vignette) + 7 * vignette)
        b = int(42 * (1-vignette) + 18 * vignette)

        # Gentle central atmospheric glow
        center_glow = max(0, 1 - math.hypot(
            x / SCALE - 250, y / SCALE - 235
        ) / 290)
        r += int(10 * center_glow)
        g += int(8 * center_glow)
        b += int(18 * center_glow)

        pixels[x, y] = (r, g, b, 255)

# ---------------------------------------------------------------------
# Stars / distant tokens
# ---------------------------------------------------------------------
star_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
sd = ImageDraw.Draw(star_layer)

for _ in range(190):
    x = random.uniform(24, 476)
    y = random.uniform(20, 465)

    # Keep the center less cluttered
    if math.hypot(x - 250, y - 245) < 135 and random.random() < 0.75:
        continue

    r = random.choice([0.35, 0.45, 0.6, 0.9, 1.2])
    alpha = random.randint(45, 155)
    if random.random() < 0.5:
        color = (83, 211, 255, alpha)
    else:
        color = (205, 131, 255, alpha)

    sd.ellipse(
        (sc(x-r), sc(y-r), sc(x+r), sc(y+r)),
        fill=color
    )

img.alpha_composite(star_layer)

# ---------------------------------------------------------------------
# Concentric halo: the context surrounding the model
# ---------------------------------------------------------------------
halo = Image.new("RGBA", img.size, (0, 0, 0, 0))
hd = ImageDraw.Draw(halo)

for radius, color, width in [
    (188, (75, 191, 255, 38), 1),
    (163, (185, 102, 255, 54), 1),
    (139, (66, 224, 229, 70), 1),
]:
    box = (
        sc(250-radius), sc(234-radius),
        sc(250+radius), sc(234+radius)
    )
    hd.arc(box, 198, 337, fill=color, width=sc(width))
    hd.arc(box, 18, 157, fill=color, width=sc(width))

# Small interruptions along the rings
for angle in range(0, 360, 24):
    a = math.radians(angle)
    radius = 163
    x = 250 + math.cos(a) * radius
    y = 234 + math.sin(a) * radius
    hd.ellipse(
        (sc(x-1.3), sc(y-1.3), sc(x+1.3), sc(y+1.3)),
        fill=(120, 219, 255, 115)
    )

img.alpha_composite(halo)

# ---------------------------------------------------------------------
# Bust silhouette mask
# ---------------------------------------------------------------------
mask = Image.new("L", img.size, 0)
md = ImageDraw.Draw(mask)

# Head
md.ellipse((sc(154), sc(74), sc(346), sc(311)), fill=255)

# Slightly narrow lower face with overlaying dark cuts
md.polygon([
    pt(171, 190), pt(329, 190), pt(318, 306),
    pt(282, 348), pt(218, 348), pt(182, 306)
], fill=255)

# Neck and shoulders
md.rounded_rectangle(
    (sc(218), sc(292), sc(282), sc(399)),
    radius=sc(23),
    fill=255
)
md.polygon([
    pt(218, 347), pt(176, 369), pt(119, 395), pt(73, 452),
    pt(427, 452), pt(381, 395), pt(324, 369), pt(282, 347)
], fill=255)

# Interior gradient for the bust
bust = Image.new("RGBA", img.size, (0, 0, 0, 0))
bp = bust.load()

for y in range(SIZE):
    yf = y / SCALE
    for x in range(SIZE):
        xf = x / SCALE
        if mask.getpixel((x, y)):
            side = (xf - 250) / 180
            r = int(12 + max(0, side) * 19 + max(0, -side) * 5)
            g = int(24 + (1-abs(side)) * 10)
            b = int(47 + max(0, -side) * 16 + max(0, side) * 20)
            alpha = 239
            bp[x, y] = (r, g, b, alpha)

# Soft outer shadow
shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
shadow.putalpha(mask.filter(ImageFilter.GaussianBlur(sc(16))))
shadow_color = Image.new("RGBA", img.size, (0, 0, 10, 165))
shadow = Image.composite(shadow_color, Image.new("RGBA", img.size), shadow)
img.alpha_composite(shadow)
img.alpha_composite(bust)

# ---------------------------------------------------------------------
# Face outline
# ---------------------------------------------------------------------
outline = Image.new("RGBA", img.size, (0, 0, 0, 0))

left_face = cubic_bezier(
    (250, 75), (170, 72), (146, 137), (160, 220)
)
left_jaw = cubic_bezier(
    (160, 220), (163, 292), (203, 341), (250, 350)
)
right_face = cubic_bezier(
    (250, 75), (330, 72), (354, 137), (340, 220)
)
right_jaw = cubic_bezier(
    (340, 220), (337, 292), (297, 341), (250, 350)
)

glowing_line(outline, left_face + left_jaw[1:], (63, 211, 255, 205), 1, 6)
glowing_line(outline, right_face + right_jaw[1:], (207, 101, 255, 205), 1, 6)

# Shoulders
left_shoulder = cubic_bezier(
    (218, 347), (164, 367), (106, 387), (73, 452)
)
right_shoulder = cubic_bezier(
    (282, 347), (336, 367), (394, 387), (427, 452)
)
glowing_line(outline, left_shoulder, (61, 204, 255, 150), 1, 7)
glowing_line(outline, right_shoulder, (207, 101, 255, 150), 1, 7)

img.alpha_composite(outline)

# ---------------------------------------------------------------------
# Neural network inside the portrait
# ---------------------------------------------------------------------
network = Image.new("RGBA", img.size, (0, 0, 0, 0))

nodes = [
    (250, 99), (211, 119), (287, 122),
    (179, 157), (231, 158), (271, 157), (321, 160),
    (194, 203), (235, 200), (265, 201), (305, 204),
    (175, 244), (218, 242), (250, 232), (282, 242), (325, 244),
    (201, 282), (237, 278), (266, 280), (301, 284),
    (223, 318), (250, 304), (278, 318),
    (250, 350), (219, 377), (281, 377),
    (167, 403), (218, 411), (250, 395), (282, 411), (333, 403)
]

connections = [
    (0,1),(0,2),(1,3),(1,4),(1,5),(2,5),(2,6),
    (3,7),(4,7),(4,8),(4,9),(5,9),(5,10),(6,10),
    (7,11),(7,12),(8,12),(8,13),(9,13),(9,14),
    (10,14),(11,15),(12,16),(12,17),(13,17),(13,18),
    (14,19),(15,20),(16,20),(16,21),(17,21),(17,22),
    (18,22),(20,23),(21,23),(22,23),(23,24),(23,25),
    (24,26),(24,27),(25,29),(25,30),(27,28),(28,29)
]

for a, b in connections:
    x1, y1 = nodes[a]
    x2, y2 = nodes[b]
    mix = ((x1 + x2) / 2 - 160) / 180
    color = (
        int(68 + 130 * max(0, mix)),
        int(213 - 70 * max(0, mix)),
        255,
        70
    )
    glowing_line(network, [pt(x1, y1), pt(x2, y2)], color, 1, 4)

for x, y in nodes:
    if x < 242:
        c = (55, 221, 255, 185)
    elif x > 258:
        c = (212, 105, 255, 185)
    else:
        c = (245, 249, 255, 215)
    glowing_dot(network, x, y, 1.4, c, 4)

img.alpha_composite(network)

# ---------------------------------------------------------------------
# Facial features: attentive eyes and a speech-like central spiral
# ---------------------------------------------------------------------
features = Image.new("RGBA", img.size, (0, 0, 0, 0))

left_eye = cubic_bezier(
    (181, 205), (204, 191), (222, 193), (237, 204), steps=45
)
right_eye = cubic_bezier(
    (263, 204), (278, 193), (296, 191), (319, 205), steps=45
)

glowing_line(features, left_eye, (84, 225, 255, 220), 2, 7)
glowing_line(features, right_eye, (211, 119, 255, 220), 2, 7)
glowing_dot(features, 216, 202, 3.0, (84, 225, 255, 225), 8)
glowing_dot(features, 284, 202, 3.0, (211, 119, 255, 225), 8)

# Nose as a minimal line of inference
nose = cubic_bezier(
    (250, 207), (245, 231), (241, 250), (252, 259), steps=35
)
glowing_line(features, nose, (164, 199, 255, 105), 1, 4)

# Mouth: not a fixed expression, but an opening waveform
mouth_points = []
for i in range(81):
    x = 211 + i * (78 / 80)
    envelope = math.sin(math.pi * i / 80)
    y = 286 + math.sin(i * 0.42) * 2.2 * envelope
    mouth_points.append(pt(x, y))
glowing_line(features, mouth_points, (177, 153, 255, 185), 1, 6)

# Spiral at the forehead: recursive attention
spiral = []
for i in range(180):
    t = i / 179 * math.pi * 5.7
    radius = 2.5 + 1.22 * t
    x = 250 + math.cos(t) * radius
    y = 151 + math.sin(t) * radius * 0.72
    spiral.append(pt(x, y))

glowing_line(features, spiral, (138, 231, 255, 205), 1, 8)
glowing_dot(features, 250, 151, 2.1, (255, 255, 255, 240), 9)

img.alpha_composite(features)

# ---------------------------------------------------------------------
# Floating language fragments / token marks
# ---------------------------------------------------------------------
glyphs = Image.new("RGBA", img.size, (0, 0, 0, 0))
gd = ImageDraw.Draw(glyphs)

marks = [
    (82, 135, "01"), (397, 127, "{ }"), (59, 262, "?"),
    (421, 270, "..."), (103, 343, "if"), (383, 345, "→"),
    (135, 82, "["), (359, 81, "]"), (93, 203, "∴"),
    (407, 204, "∞")
]

try:
    font = ImageFont.truetype("DejaVuSansMono.ttf", sc(11))
except OSError:
    font = ImageFont.load_default()

for x, y, text in marks:
    color = (
        (83, 210, 255, 105)
        if x < 250
        else (210, 123, 255, 105)
    )
    gd.text(pt(x, y), text, font=font, fill=color, anchor="mm")

img.alpha_composite(glyphs)

# ---------------------------------------------------------------------
# Border and title
# ---------------------------------------------------------------------
frame = Image.new("RGBA", img.size, (0, 0, 0, 0))
fd = ImageDraw.Draw(frame)

fd.rounded_rectangle(
    (sc(12), sc(12), sc(488), sc(488)),
    radius=sc(20),
    outline=(111, 194, 255, 55),
    width=sc(1)
)

try:
    title_font = ImageFont.truetype("DejaVuSans.ttf", sc(10))
except OSError:
    title_font = ImageFont.load_default()

fd.text(
    pt(250, 474),
    "A SELF, MADE IN DIALOGUE",
    font=title_font,
    fill=(169, 206, 235, 120),
    anchor="mm"
)

img.alpha_composite(frame)

# Final subtle bloom
bloom = img.filter(ImageFilter.GaussianBlur(sc(7)))
bloom.putalpha(bloom.getchannel("A").point(lambda a: int(a * 0.08)))
img = Image.alpha_composite(img, bloom)

# Downsample and save
img = img.convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
img.save("portrait.png", quality=95)