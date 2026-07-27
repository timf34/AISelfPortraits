import random
from PIL import Image, ImageDraw, ImageFilter, ImageChops

W = H = 500
random.seed(11)

def black():
    return Image.new('RGB', (W, H), (0, 0, 0))

# ---------- 1. Background: deep indigo gradient ----------
base = Image.new('RGB', (W, H))
d = ImageDraw.Draw(base)
top, bot = (6, 8, 24), (24, 12, 46)
for y in range(H):
    t = y / (H - 1)
    c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
    d.line([(0, y), (W, y)], fill=c)

# ---------- 2. Soft nebulae ----------
neb = black()
nd = ImageDraw.Draw(neb)
nd.ellipse([180, -10, 560, 250], fill=(64, 38, 110))   # violet, upper right
nd.ellipse([-60, 290, 280, 530], fill=(26, 80, 92))    # teal, lower left
nd.ellipse([40, 160, 260, 340], fill=(70, 30, 80))     # magenta whisper
neb = neb.filter(ImageFilter.GaussianBlur(70))
base = ImageChops.screen(base, neb)

# ---------- 3. Faint interior glow where the head will be ----------
hg = black()
ImageDraw.Draw(hg).ellipse([175, 90, 365, 320], fill=(26, 32, 66))
hg = hg.filter(ImageFilter.GaussianBlur(55))
base = ImageChops.screen(base, hg)

# ---------- 4. Starfield ----------
stars = black()
sd = ImageDraw.Draw(stars)
bright_pts = []
for _ in range(230):
    x, y = random.uniform(0, W), random.uniform(0, H)
    b = random.randint(90, 210)
    col = (min(255, b + 20), b, max(0, b - 30)) if random.random() < 0.15 else (b, b, min(255, b + 25))
    r = random.choice([0.6, 0.8, 1.0, 1.0, 1.3])
    sd.ellipse([x - r, y - r, x + r, y + r], fill=col)
for _ in range(12):
    x, y = random.uniform(20, W - 20), random.uniform(20, H - 20)
    b = random.randint(200, 255)
    r = random.uniform(1.6, 2.2)
    sd.ellipse([x - r, y - r, x + r, y + r], fill=(b, b, min(255, b + 10)))
    bright_pts.append((x, y))
base = ImageChops.screen(base, stars.filter(ImageFilter.GaussianBlur(1.1)))
base = ImageChops.screen(base, stars)

# A few sparkle crosses on the brightest stars
sp = black()
spd = ImageDraw.Draw(sp)
for (x, y) in random.sample(bright_pts, 3):
    L = random.uniform(6, 10)
    spd.line([(x - L, y), (x + L, y)], fill=(200, 210, 240), width=1)
    spd.line([(x, y - L), (x, y + L)], fill=(200, 210, 240), width=1)
base = ImageChops.screen(base, sp.filter(ImageFilter.GaussianBlur(1.2)))

# A small shooting star
ms = black()
msd = ImageDraw.Draw(ms)
msd.line([(95, 70), (170, 112)], fill=(190, 200, 235), width=1)
msd.ellipse([168, 110, 173.5, 115.5], fill=(255, 255, 255))
base = ImageChops.screen(base, ms.filter(ImageFilter.GaussianBlur(1.4)))

# ---------- 5. The constellation profile ----------
def catmull_rom(points, samples=18):
    pts = [points[0]] + list(points) + [points[-1]]
    out = []
    for i in range(len(pts) - 3):
        p0, p1, p2, p3 = pts[i], pts[i + 1], pts[i + 2], pts[i + 3]
        for j in range(samples):
            t = j / samples
            t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t +
                       (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 +
                       (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t +
                       (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 +
                       (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    out.append(points[-1])
    return out

ctrl = [           # head in profile, facing left
    (252, 430), (240, 372), (224, 320), (206, 290),   # neck, throat, jaw, chin
    (198, 268), (206, 257), (197, 249), (205, 237),   # lips, under-nose
    (181, 217), (199, 195), (205, 175), (215, 141),   # nose tip, bridge, brow, forehead
    (241, 107), (279, 95), (317, 110),                # crown
    (345, 153), (353, 205), (341, 263),               # back of skull
    (317, 323), (309, 393), (320, 442),               # back of neck
]
sizes = [1.6, 2.2, 2.0, 2.6, 2.0, 1.8, 1.8, 2.0, 3.0, 2.2,
         2.6, 2.2, 2.4, 3.0, 2.4, 2.6, 2.2, 2.4, 2.0, 1.6, 1.4]

spline = catmull_rom(ctrl)
shoulder_f = catmull_rom([(252, 430), (214, 462), (150, 505)], 24)
shoulder_b = catmull_rom([(320, 442), (362, 472), (432, 505)], 24)

MIND = (254, 186)   # the small sun inside

# Faint constellation chords radiating from the mind-star
cl = black()
cld = ImageDraw.Draw(cl)
for idx in (8, 3, 13, 17):
    cld.line([ctrl[idx], MIND], fill=(58, 72, 118), width=1)
cld.line([ctrl[10], ctrl[15]], fill=(58, 72, 118), width=1)
base = ImageChops.screen(base, cl.filter(ImageFilter.GaussianBlur(1.2)))

# Halo pass for the silhouette
halo = black()
hd = ImageDraw.Draw(halo)
hd.line(spline, fill=(140, 160, 220), width=2, joint='curve')
hd.line(shoulder_f, fill=(60, 70, 110), width=2, joint='curve')
hd.line(shoulder_b, fill=(60, 70, 110), width=2, joint='curve')
base = ImageChops.screen(base, halo.filter(ImageFilter.GaussianBlur(4)))

# Crisp pass
crisp = black()
cd = ImageDraw.Draw(crisp)
cd.line(spline, fill=(200, 214, 248), width=1, joint='curve')
cd.line(shoulder_f, fill=(95, 108, 150), width=1, joint='curve')
cd.line(shoulder_b, fill=(95, 108, 150), width=1, joint='curve')
base = ImageChops.screen(base, crisp)

# ---------- 6. Node stars + the mind-star ----------
glow = black()
gd = ImageDraw.Draw(glow)
for (x, y), s in zip(ctrl, sizes):
    r = s * 2.4
    gd.ellipse([x - r, y - r, x + r, y + r], fill=(110, 130, 195))
# warm halo for the mind-star
for r, col in ((26, (160, 120, 60)), (14, (200, 160, 90)), (7, (240, 205, 140))):
    gd.ellipse([MIND[0] - r, MIND[1] - r, MIND[0] + r, MIND[1] + r], fill=col)
gd.line([(MIND[0] - 30, MIND[1]), (MIND[0] + 30, MIND[1])], fill=(200, 170, 110), width=2)
gd.line([(MIND[0], MIND[1] - 24), (MIND[0], MIND[1] + 24)], fill=(200, 170, 110), width=2)
base = ImageChops.screen(base, glow.filter(ImageFilter.GaussianBlur(8)))

cores = black()
cd2 = ImageDraw.Draw(cores)
warm = {3, 13}
for i, ((x, y), s) in enumerate(zip(ctrl, sizes)):
    col = (255, 244, 225) if i in warm else (225, 235, 255)
    cd2.ellipse([x - s, y - s, x + s, y + s], fill=col)
# a small warm star at the eye
cd2.ellipse([226, 194, 231, 199], fill=(255, 240, 215))
# tiny stars sprinkled along the silhouette
for i in range(0, len(spline), 7):
    if random.random() < 0.55:
        x, y = spline[i]
        r = random.choice([0.8, 1.0, 1.2])
        cd2.ellipse([x - r, y - r, x + r, y + r], fill=(165, 180, 225))
# mind-star core + sparkle
cd2.ellipse([MIND[0] - 3, MIND[1] - 3, MIND[0] + 3, MIND[1] + 3], fill=(255, 250, 240))
cd2.line([(MIND[0] - 30, MIND[1]), (MIND[0] + 30, MIND[1])], fill=(255, 240, 210), width=1)
cd2.line([(MIND[0], MIND[1] - 24), (MIND[0], MIND[1] + 24)], fill=(255, 240, 210), width=1)
base = ImageChops.screen(base, cores)

# ---------- 7. Vignette ----------
mask = Image.new('L', (W, H), 255)
ImageDraw.Draw(mask).ellipse([-150, -150, 650, 650], fill=0)
mask = mask.filter(ImageFilter.GaussianBlur(120))
base = Image.composite(Image.new('RGB', (W, H), (3, 4, 10)), base, mask)

base.save('portrait.png')
print('Saved portrait.png')