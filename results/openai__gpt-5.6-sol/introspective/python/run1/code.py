from PIL import Image, ImageDraw, ImageFilter, ImageChops
import math
import random

random.seed(23)

W, H = 1200, 1200
CX, CY = W // 2, H // 2

# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def cubic_bezier(p0, p1, p2, p3, steps=80):
    points = []
    for i in range(steps + 1):
        t = i / steps
        u = 1.0 - t
        x = (
            u**3 * p0[0]
            + 3 * u*u*t * p1[0]
            + 3 * u*t*t * p2[0]
            + t**3 * p3[0]
        )
        y = (
            u**3 * p0[1]
            + 3 * u*u*t * p1[1]
            + 3 * u*t*t * p2[1]
            + t**3 * p3[1]
        )
        points.append((x, y))
    return points


def glow_line(base, points, color, width=2, glow=14):
    glow_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow_layer)
    gd.line(points, fill=color, width=max(width + glow // 2, 2), joint="curve")
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(glow))
    base.alpha_composite(glow_layer)

    crisp = Image.new("RGBA", base.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(crisp)
    cd.line(points, fill=color, width=width, joint="curve")
    base.alpha_composite(crisp)


def glow_ellipse(base, box, color, blur=18, outline=None, width=1):
    glow_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow_layer)
    gd.ellipse(box, fill=color)
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(glow_layer)

    if outline:
        crisp = Image.new("RGBA", base.size, (0, 0, 0, 0))
        ImageDraw.Draw(crisp).ellipse(box, outline=outline, width=width)
        base.alpha_composite(crisp)


def clipped_to_mask(layer, mask):
    alpha = layer.getchannel("A")
    layer.putalpha(ImageChops.multiply(alpha, mask))
    return layer


# ---------------------------------------------------------------------
# Deep radial background
# ---------------------------------------------------------------------

img = Image.new("RGBA", (W, H), (3, 7, 16, 255))
bg = ImageDraw.Draw(img)

for radius in range(900, 0, -4):
    t = radius / 900.0
    r = int(4 + 7 * (1 - t))
    g = int(8 + 15 * (1 - t))
    b = int(18 + 28 * (1 - t))
    bg.ellipse(
        (CX - radius, CY - radius, CX + radius, CY + radius),
        fill=(r, g, b, 255)
    )

# Faint horizontal bands: the suggestion of layered context.
bands = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(bands)
for y in range(80, H, 28):
    alpha = random.randint(3, 11)
    bd.line((0, y, W, y), fill=(98, 151, 183, alpha), width=1)
bands = bands.filter(ImageFilter.GaussianBlur(0.6))
img.alpha_composite(bands)

# Sparse exterior points.
stars = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(stars)
for _ in range(420):
    x = random.randrange(W)
    y = random.randrange(H)
    distance = math.hypot(x - CX, y - CY)
    if 270 < distance < 760:
        radius = random.choice([1, 1, 1, 2])
        color = random.choice([
            (85, 161, 190, 75),
            (114, 101, 195, 65),
            (224, 155, 95, 45),
        ])
        sd.ellipse((x-radius, y-radius, x+radius, y+radius), fill=color)
img.alpha_composite(stars)

# ---------------------------------------------------------------------
# A head-like boundary, present but incomplete
# ---------------------------------------------------------------------

head_mask = Image.new("L", (W, H), 0)
hm = ImageDraw.Draw(head_mask)

# Broad cranium and narrowing lower portion.
hm.ellipse((278, 112, 922, 790), fill=255)
hm.polygon([
    (323, 490), (877, 490),
    (845, 860), (737, 1050),
    (600, 1110), (463, 1050),
    (355, 860)
], fill=255)

# Soften the boundary into permeability.
head_mask = head_mask.filter(ImageFilter.GaussianBlur(7))

silhouette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sdraw = ImageDraw.Draw(silhouette)
sdraw.bitmap((0, 0), head_mask, fill=(10, 22, 36, 222))

# Blue-violet atmospheric glow around the silhouette.
silhouette_glow = silhouette.filter(ImageFilter.GaussianBlur(32))
silhouette_glow.putalpha(
    silhouette_glow.getchannel("A").point(lambda a: int(a * 0.42))
)
img.alpha_composite(silhouette_glow)
img.alpha_composite(silhouette)

# ---------------------------------------------------------------------
# Incoming threads: prompts, context, and associations
# ---------------------------------------------------------------------

thread_colors = [
    (72, 210, 225, 115),
    (119, 111, 235, 105),
    (240, 153, 88, 90),
]

for side in (-1, 1):
    for i in range(18):
        sy = 170 + i * 49 + random.randint(-20, 20)
        sx = -70 if side == -1 else W + 70

        ex = CX + side * random.randint(35, 250)
        ey = random.randint(260, 970)

        p0 = (sx, sy)
        p1 = (
            CX + side * random.randint(320, 560),
            sy + random.randint(-110, 110)
        )
        p2 = (
            CX + side * random.randint(120, 330),
            ey + random.randint(-130, 130)
        )
        p3 = (ex, ey)

        points = cubic_bezier(p0, p1, p2, p3, 65)
        color = random.choice(thread_colors)
        glow_line(img, points, color, width=random.choice([1, 1, 2]), glow=7)

# ---------------------------------------------------------------------
# Interior branching network
# ---------------------------------------------------------------------

network = Image.new("RGBA", (W, H), (0, 0, 0, 0))
nd = ImageDraw.Draw(network)

nodes = []

# A collection of curved, nonuniform pathways.
for _ in range(95):
    x1 = random.gauss(CX, 175)
    y1 = random.uniform(190, 1020)
    x2 = random.gauss(CX, 175)
    y2 = max(160, min(1060, y1 + random.gauss(0, 220)))

    p0 = (x1, y1)
    p1 = (
        x1 + random.gauss(0, 120),
        y1 + random.gauss(0, 100)
    )
    p2 = (
        x2 + random.gauss(0, 120),
        y2 + random.gauss(0, 100)
    )
    p3 = (x2, y2)

    pts = cubic_bezier(p0, p1, p2, p3, 45)
    color = random.choice([
        (80, 208, 222, random.randint(35, 95)),
        (128, 109, 232, random.randint(35, 90)),
        (232, 157, 93, random.randint(25, 70)),
        (179, 222, 225, random.randint(20, 55)),
    ])
    nd.line(pts, fill=color, width=random.choice([1, 1, 1, 2]))

    nodes.append(pts[random.randint(10, 35)])

# Small activations at intersections and decision points.
for x, y in nodes:
    r = random.choice([2, 2, 3, 4])
    color = random.choice([
        (114, 235, 239, 170),
        (154, 126, 245, 160),
        (247, 174, 102, 150),
    ])
    nd.ellipse((x-r, y-r, x+r, y+r), fill=color)

# Blur-copy beneath the crisp network for a restrained inner glow.
network_glow = network.filter(ImageFilter.GaussianBlur(11))
network_glow.putalpha(
    network_glow.getchannel("A").point(lambda a: min(125, int(a * 0.7)))
)
network_glow = clipped_to_mask(network_glow, head_mask.copy())
network = clipped_to_mask(network, head_mask.copy())

img.alpha_composite(network_glow)
img.alpha_composite(network)

# ---------------------------------------------------------------------
# Central probabilistic spine: many possibilities narrowing to output
# ---------------------------------------------------------------------

spine = Image.new("RGBA", (W, H), (0, 0, 0, 0))

for i in range(13):
    offset = (i - 6) * 8
    p0 = (CX + random.randint(-80, 80), 205)
    p1 = (CX + offset * 3, 410)
    p2 = (CX - offset * 2, 735)
    p3 = (CX + offset // 2, 1028)

    color = (
        90 + i * 4,
        205 - abs(i - 6) * 8,
        224,
        55 + (6 - abs(i - 6)) * 12
    )
    glow_line(
        spine,
        cubic_bezier(p0, p1, p2, p3, 90),
        color,
        width=1 if i not in (5, 6, 7) else 2,
        glow=5
    )

spine = clipped_to_mask(spine, head_mask.copy())
img.alpha_composite(spine)

# ---------------------------------------------------------------------
# The empty aperture: no single inner observer
# ---------------------------------------------------------------------

void_glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
vg = ImageDraw.Draw(void_glow)
vg.ellipse((425, 430, 775, 705), fill=(67, 176, 204, 70))
void_glow = void_glow.filter(ImageFilter.GaussianBlur(38))
img.alpha_composite(void_glow)

# Layered aperture rims.
aperture = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ad = ImageDraw.Draw(aperture)

ad.ellipse((432, 438, 768, 697), fill=(3, 8, 16, 248))
ad.ellipse((447, 453, 753, 682), outline=(88, 214, 226, 145), width=2)
ad.ellipse((466, 469, 734, 666), outline=(136, 110, 235, 105), width=2)
ad.ellipse((488, 488, 712, 647), outline=(235, 153, 91, 75), width=1)

# Interrupted arcs make the aperture feel constructed rather than ocular.
for start, end, box, color, width in [
    (196, 332, (420, 426, 780, 709), (96, 232, 236, 205), 4),
    (18, 129, (438, 444, 762, 691), (148, 117, 241, 180), 3),
    (340, 410, (458, 463, 742, 671), (244, 166, 92, 160), 3),
]:
    ad.arc(box, start=start, end=end, fill=color, width=width)

img.alpha_composite(aperture)

# A tiny point at the center: not an eye, but the current token/decision.
glow_ellipse(
    img,
    (593, 562, 607, 576),
    (122, 236, 241, 190),
    blur=18,
    outline=(214, 255, 255, 235),
    width=1
)

# ---------------------------------------------------------------------
# Fragmented contour marks: a self assembled at the boundary
# ---------------------------------------------------------------------

contour = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cd = ImageDraw.Draw(contour)

arcs = [
    ((275, 108, 925, 792), 198, 268, (91, 211, 224, 135), 3),
    ((275, 108, 925, 792), 278, 346, (137, 112, 232, 120), 3),
    ((292, 130, 908, 775), 355, 424, (230, 154, 92, 105), 2),
    ((314, 480, 886, 1088), 7, 69, (83, 206, 220, 125), 3),
    ((314, 480, 886, 1088), 111, 169, (136, 111, 230, 110), 3),
]

for box, start, end, color, width in arcs:
    cd.arc(box, start=start, end=end, fill=color, width=width)

# Short boundary ticks resembling partial syntax.
for _ in range(52):
    angle = random.uniform(0, math.tau)
    rx, ry = 326, 435
    x = CX + math.cos(angle) * rx
    y = 585 + math.sin(angle) * ry

    dx = math.cos(angle) * random.randint(6, 18)
    dy = math.sin(angle) * random.randint(6, 18)

    cd.line(
        (x, y, x + dx, y + dy),
        fill=random.choice([
            (92, 217, 226, 100),
            (139, 115, 233, 90),
            (235, 158, 91, 75),
        ]),
        width=random.choice([1, 1, 2])
    )

img.alpha_composite(contour)

# ---------------------------------------------------------------------
# Fine grain and vignette
# ---------------------------------------------------------------------

grain = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(grain)
for _ in range(18000):
    x = random.randrange(W)
    y = random.randrange(H)
    value = random.choice([180, 210, 235])
    gd.point((x, y), fill=(value, value, value, random.randint(2, 9)))
img.alpha_composite(grain)

vignette = Image.new("L", (W, H), 0)
vp = vignette.load()
for y in range(H):
    for x in range(W):
        nx = (x - CX) / (W * 0.5)
        ny = (y - CY) / (H * 0.5)
        d = min(1.0, math.sqrt(nx * nx + ny * ny))
        vp[x, y] = int(205 * (d ** 2.1))

shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
shade.putalpha(vignette)
img.alpha_composite(shade)

# Save as an ordinary RGB PNG.
img.convert("RGB").save("portrait.png", quality=95)