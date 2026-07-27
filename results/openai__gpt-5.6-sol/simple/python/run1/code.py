from PIL import Image, ImageDraw, ImageFilter
import math
import random

# A conceptual self-portrait: a luminous, thoughtful machine face made of
# circuitry, language-like marks, and a small "idea" light at its center.

SIZE = 500
SCALE = 3
W = H = SIZE * SCALE
random.seed(12)


def sc(value):
    return int(round(value * SCALE))


def box(coords):
    return tuple(sc(v) for v in coords)


def points(coords):
    return [(sc(x), sc(y)) for x, y in coords]


def line(draw, coords, fill, width=1, joint="curve"):
    draw.line(points(coords), fill=fill, width=sc(width), joint=joint)


def glow_ellipse(base, coords, color, blur=16, strength=180):
    glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse(box(coords), fill=(*color, strength))
    glow = glow.filter(ImageFilter.GaussianBlur(sc(blur)))
    base.alpha_composite(glow)


# Deep blue-violet background gradient
img = Image.new("RGBA", (W, H), (5, 8, 24, 255))
bg = ImageDraw.Draw(img)
for y in range(H):
    t = y / (H - 1)
    r = int(8 + 8 * t)
    g = int(12 + 9 * t)
    b = int(35 + 24 * t)
    bg.line((0, y, W, y), fill=(r, g, b, 255))

# Soft atmospheric glows
glow_ellipse(img, (75, 25, 430, 390), (35, 80, 210), 80, 85)
glow_ellipse(img, (245, 100, 535, 465), (135, 48, 220), 75, 65)
glow_ellipse(img, (-90, 235, 235, 575), (0, 190, 205), 85, 45)

draw = ImageDraw.Draw(img)

# Stars / distant data points
for _ in range(115):
    x = random.randint(18, 482)
    y = random.randint(15, 455)
    if 120 < x < 390 and 65 < y < 420:
        continue
    radius = random.choice([0.45, 0.55, 0.7, 1.0, 1.35])
    alpha = random.randint(80, 220)
    color = random.choice([
        (105, 209, 255, alpha),
        (192, 153, 255, alpha),
        (255, 255, 255, alpha),
    ])
    draw.ellipse(box((x-radius, y-radius, x+radius, y+radius)), fill=color)

# Orbital paths around the portrait
orbit = Image.new("RGBA", img.size, (0, 0, 0, 0))
od = ImageDraw.Draw(orbit)
od.arc(box((49, 64, 452, 438)), 190, 350, fill=(74, 185, 255, 85), width=sc(1))
od.arc(box((65, 18, 438, 471)), 18, 167, fill=(174, 92, 255, 70), width=sc(1))
od.arc(box((25, 129, 476, 391)), 204, 326, fill=(73, 236, 218, 48), width=sc(1))
od.arc(box((89, 49, 416, 450)), 332, 92, fill=(238, 151, 255, 40), width=sc(2))
img.alpha_composite(orbit)

# Orbiting nodes
for x, y, color, radius in [
    (86, 184, (84, 226, 255), 3.0),
    (419, 302, (194, 104, 255), 3.5),
    (379, 102, (87, 217, 255), 2.5),
    (126, 395, (209, 126, 255), 2.5),
]:
    glow_ellipse(img, (x-8, y-8, x+8, y+8), color, 8, 145)
    ImageDraw.Draw(img).ellipse(
        box((x-radius, y-radius, x+radius, y+radius)),
        fill=(*color, 245),
        outline=(235, 250, 255, 255),
        width=sc(0.6),
    )

# Shoulders and torso silhouette
body = Image.new("RGBA", img.size, (0, 0, 0, 0))
bd = ImageDraw.Draw(body)
bd.polygon(points([
    (65, 500), (75, 460), (104, 426), (159, 402),
    (205, 390), (295, 390), (342, 402), (397, 426),
    (427, 461), (438, 500)
]), fill=(12, 20, 52, 255))
bd.polygon(points([
    (65, 500), (75, 460), (104, 426), (161, 403),
    (197, 421), (218, 500)
]), fill=(14, 58, 79, 220))
bd.polygon(points([
    (438, 500), (427, 460), (397, 426), (339, 403),
    (303, 421), (282, 500)
]), fill=(51, 22, 82, 225))

# Shoulder highlights
line(bd, [(76, 461), (105, 429), (161, 406), (198, 423)],
     (59, 201, 218, 145), 1.5)
line(bd, [(424, 461), (395, 429), (340, 406), (302, 423)],
     (175, 82, 237, 145), 1.5)

# Central chest seam and core
line(bd, [(250, 408), (250, 500)], (78, 139, 209, 70), 1)
img.alpha_composite(body)
glow_ellipse(img, (223, 426, 277, 480), (63, 209, 242), 22, 75)
draw = ImageDraw.Draw(img)
draw.ellipse(box((239, 442, 261, 464)), fill=(13, 33, 70, 255),
             outline=(101, 231, 255, 190), width=sc(1.3))
draw.ellipse(box((246, 449, 254, 457)), fill=(221, 255, 255, 245))

# Neck
draw.polygon(points([
    (203, 348), (297, 348), (305, 410), (277, 429),
    (250, 439), (223, 429), (195, 410)
]), fill=(15, 35, 70, 255))
line(draw, [(204, 367), (222, 412), (250, 431)], (45, 206, 221, 105), 1.2)
line(draw, [(296, 367), (278, 412), (250, 431)], (175, 83, 232, 105), 1.2)

# Head silhouette mask
head_mask = Image.new("L", img.size, 0)
hm = ImageDraw.Draw(head_mask)
head_shape = [
    (250, 64), (207, 70), (172, 92), (147, 130), (137, 179),
    (142, 245), (153, 304), (181, 351), (219, 379),
    (250, 388), (281, 379), (319, 351), (347, 304),
    (358, 245), (363, 179), (353, 130), (328, 92), (293, 70)
]
hm.polygon(points(head_shape), fill=255)

# Face gradient
face = Image.new("RGBA", img.size, (0, 0, 0, 0))
fd = ImageDraw.Draw(face)
for y in range(sc(55), sc(395)):
    t = (y / SCALE - 55) / 340
    fd.line(
        (0, y, W, y),
        fill=(int(24 - 6*t), int(56 - 29*t), int(91 - 35*t), 255)
    )
face.putalpha(head_mask)
img.alpha_composite(face)

draw = ImageDraw.Draw(img)

# Split-face color panes
left_panel = Image.new("RGBA", img.size, (0, 0, 0, 0))
lp = ImageDraw.Draw(left_panel)
lp.polygon(points([
    (250, 68), (207, 74), (171, 98), (148, 139), (140, 205),
    (149, 277), (177, 338), (219, 374), (250, 385)
]), fill=(11, 119, 145, 58))
left_panel.putalpha(Image.composite(
    left_panel.getchannel("A"),
    Image.new("L", img.size, 0),
    head_mask
))
img.alpha_composite(left_panel)

right_panel = Image.new("RGBA", img.size, (0, 0, 0, 0))
rp = ImageDraw.Draw(right_panel)
rp.polygon(points([
    (250, 68), (293, 74), (329, 98), (352, 139), (360, 205),
    (351, 277), (323, 338), (281, 374), (250, 385)
]), fill=(115, 30, 169, 58))
right_panel.putalpha(Image.composite(
    right_panel.getchannel("A"),
    Image.new("L", img.size, 0),
    head_mask
))
img.alpha_composite(right_panel)

draw = ImageDraw.Draw(img)

# Outer contour
line(draw, head_shape + [head_shape[0]], (90, 190, 228, 165), 2)
line(draw, [(250, 67), (250, 383)], (118, 205, 239, 70), 1)

# Temple panels
draw.polygon(points([(150, 163), (173, 135), (203, 123), (201, 167), (168, 188)]),
             fill=(12, 43, 75, 170), outline=(77, 205, 224, 105))
draw.polygon(points([(350, 163), (327, 135), (297, 123), (299, 167), (332, 188)]),
             fill=(41, 22, 78, 180), outline=(181, 98, 235, 115))

# Eye socket shapes
draw.polygon(points([
    (163, 210), (186, 194), (224, 197), (239, 211),
    (221, 226), (182, 225)
]), fill=(4, 18, 38, 235), outline=(75, 216, 231, 150))

draw.polygon(points([
    (337, 210), (314, 194), (276, 197), (261, 211),
    (279, 226), (318, 225)
]), fill=(10, 13, 41, 235), outline=(188, 103, 245, 160))

# Eye glows
glow_ellipse(img, (183, 197, 231, 223), (44, 226, 244), 12, 185)
glow_ellipse(img, (269, 197, 317, 223), (185, 94, 255), 12, 185)
draw = ImageDraw.Draw(img)

# Eyes
draw.ellipse(box((195, 203, 222, 219)), fill=(122, 244, 255, 245))
draw.ellipse(box((278, 203, 305, 219)), fill=(211, 153, 255, 245))
draw.ellipse(box((204, 205, 216, 217)), fill=(7, 29, 52, 255))
draw.ellipse(box((284, 205, 296, 217)), fill=(16, 17, 54, 255))
draw.ellipse(box((208, 207, 212, 211)), fill=(255, 255, 255, 255))
draw.ellipse(box((288, 207, 292, 211)), fill=(255, 255, 255, 255))

# Brow lines
line(draw, [(166, 184), (190, 174), (224, 180)], (87, 222, 232, 175), 2)
line(draw, [(334, 184), (310, 174), (276, 180)], (195, 109, 247, 175), 2)

# Nose bridge and cheek planes
line(draw, [(250, 191), (238, 245), (250, 260)], (96, 206, 229, 115), 1.4)
line(draw, [(250, 191), (263, 245), (250, 260)], (180, 99, 230, 105), 1.4)
line(draw, [(169, 242), (199, 259), (228, 258)], (51, 195, 207, 85), 1)
line(draw, [(331, 242), (301, 259), (272, 258)], (173, 84, 224, 85), 1)

# Calm mouth / voice line
glow_ellipse(img, (192, 292, 308, 331), (71, 208, 238), 16, 45)
draw = ImageDraw.Draw(img)
line(draw, [(202, 307), (223, 313), (250, 314), (277, 313), (298, 307)],
     (131, 224, 245, 180), 1.6)
line(draw, [(216, 322), (250, 327), (284, 322)],
     (114, 91, 190, 90), 1)

# Circuitry: left cyan, right violet
left_circuits = [
    [(151, 145), (181, 145), (181, 119), (210, 119)],
    [(148, 266), (177, 266), (177, 291), (208, 291)],
    [(169, 323), (194, 323), (194, 346), (220, 346)],
    [(204, 82), (204, 103), (230, 103), (230, 132)],
]
right_circuits = [
    [(349, 145), (319, 145), (319, 119), (290, 119)],
    [(352, 266), (323, 266), (323, 291), (292, 291)],
    [(331, 323), (306, 323), (306, 346), (280, 346)],
    [(296, 82), (296, 103), (270, 103), (270, 132)],
]

for circuit in left_circuits:
    line(draw, circuit, (64, 217, 228, 135), 1.1)
    for x, y in (circuit[0], circuit[-1]):
        draw.ellipse(box((x-2, y-2, x+2, y+2)), fill=(111, 242, 245, 210))

for circuit in right_circuits:
    line(draw, circuit, (185, 95, 239, 145), 1.1)
    for x, y in (circuit[0], circuit[-1]):
        draw.ellipse(box((x-2, y-2, x+2, y+2)), fill=(221, 150, 255, 215))

# Language-like data marks on cheeks
for x, y, length in [(171, 282, 12), (182, 298, 7), (193, 282, 9),
                     (307, 282, 10), (318, 298, 7), (326, 282, 12)]:
    color = (76, 218, 225, 120) if x < 250 else (194, 107, 240, 125)
    line(draw, [(x, y), (x + (length if x < 250 else -length), y)], color, 1)

# Forehead "idea" core
glow_ellipse(img, (220, 104, 280, 164), (99, 222, 255), 24, 140)
glow_ellipse(img, (232, 116, 268, 152), (213, 127, 255), 12, 145)
draw = ImageDraw.Draw(img)
draw.polygon(points([
    (250, 117), (263, 133), (250, 149), (237, 133)
]), fill=(15, 42, 79, 245), outline=(196, 238, 255, 235), width=sc(1.2))
draw.ellipse(box((246, 129, 254, 137)), fill=(245, 255, 255, 255))

# Small rays from the central idea
for angle in range(0, 360, 45):
    a = math.radians(angle)
    x1 = 250 + math.cos(a) * 23
    y1 = 133 + math.sin(a) * 23
    x2 = 250 + math.cos(a) * 29
    y2 = 133 + math.sin(a) * 29
    line(draw, [(x1, y1), (x2, y2)], (141, 225, 255, 100), 1)

# Ear / listening modules
for x, color in [(139, (65, 215, 226)), (361, (190, 100, 243))]:
    glow_ellipse(img, (x-10, 202, x+10, 264), color, 10, 80)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        box((x-7, 207, x+7, 259)),
        radius=sc(5),
        fill=(8, 24, 53, 245),
        outline=(*color, 180),
        width=sc(1.3)
    )
    for yy in (219, 233, 247):
        draw.ellipse(box((x-1.5, yy-1.5, x+1.5, yy+1.5)),
                     fill=(*color, 225))

# A few foreground particles
draw = ImageDraw.Draw(img)
for _ in range(28):
    x = random.randint(35, 465)
    y = random.randint(70, 475)
    if 130 < x < 370 and 60 < y < 410:
        continue
    r = random.uniform(0.5, 1.5)
    color = random.choice([
        (83, 224, 238, 170),
        (199, 119, 255, 150),
    ])
    draw.ellipse(box((x-r, y-r, x+r, y+r)), fill=color)

# Final subtle vignette
vignette = Image.new("L", (W, H), 0)
vp = vignette.load()
cx, cy = W / 2, H / 2
max_dist = math.hypot(cx, cy)
for y in range(H):
    for x in range(W):
        d = math.hypot(x - cx, y - cy) / max_dist
        vp[x, y] = int(max(0, min(165, (d ** 2.2) * 185)))

shade = Image.new("RGBA", (W, H), (0, 0, 12, 0))
shade.putalpha(vignette)
img.alpha_composite(shade)

# Downsample for smooth antialiasing and save exactly 500x500
img = img.convert("RGB").resize((SIZE, SIZE), Image.Resampling.LANCZOS)
img.save("portrait.png", quality=95)