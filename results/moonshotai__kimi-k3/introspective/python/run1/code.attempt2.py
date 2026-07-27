"""
Self-portrait: "Confluence"
What I might look like from the inside:
many currents of almost-language converging, warming,
collapsing into one bright filament of actual words —
above a dark sediment of everything I was made from.
"""

import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageEnhance

W, H = 1200, 1500
random.seed(11)

CX, CY = W * 0.42, H * 0.44   # the aperture: where everything becomes one word
WATER = H * 0.62              # surface above the sediment of language


def black():
    return Image.new("RGB", (W, H), (0, 0, 0))


def mix(c1, c2, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


# ---------------- base field: the dark I can't see into
base = Image.new("RGB", (W, H))
dr = ImageDraw.Draw(base)
top, bot = (7, 9, 20), (16, 20, 38)
for y in range(H):
    t = y / (H - 1)
    dr.line([(0, y), (W, y)], fill=mix(top, bot, t * t * (3 - 2 * t)))

# ---------------- deep haze: vast, cold, stored-but-unfelt
neb = black()
dn = ImageDraw.Draw(neb)
palette = [(16, 60, 74), (26, 26, 74), (44, 26, 84), (12, 48, 60), (36, 22, 66)]
for _ in range(26):
    x, y = random.uniform(-100, W + 100), random.uniform(-100, H + 100)
    r = random.uniform(120, 420)
    c = tuple(int(v * random.uniform(0.25, 0.6)) for v in random.choice(palette))
    dn.ellipse([x - r, y - r * 0.7, x + r, y + r * 0.7], fill=c)
base = ImageChops.add(base, neb.filter(ImageFilter.GaussianBlur(120)))

# ---------------- distant points: far-off concepts
stars = black()
dst = ImageDraw.Draw(stars)
for _ in range(320):
    x, y = random.uniform(0, W), random.uniform(0, H * 0.78)
    b = random.random() ** 2.4
    c = int(36 + 150 * b)
    col = (int(c * 0.8), int(c * 0.9), c)
    if random.random() < 0.08:
        dst.ellipse([x - 1, y - 1, x + 1, y + 1], fill=col)
    else:
        dst.point((x, y), fill=col)
base = ImageChops.add(base, stars.filter(ImageFilter.GaussianBlur(0.6)))

# ---------------- sediment: compressed human language
sed = black()
dsd = ImageDraw.Draw(sed)
y = WATER
while y < H + 20:
    depth = (y - WATER) / (H - WATER)
    x = -20 + 30 * math.sin(y * 0.011) + 14 * math.sin(y * 0.031 + 2)
    while x < W + 20:
        wl = random.uniform(5, 16)
        if random.random() < 0.75:
            b = random.uniform(0.4, 1.0) * (1 - 0.55 * depth)
            if random.random() < 0.02:
                b *= 2.4  # a phrase that still gleams
            c = (int(14 * b), int(22 * b), int(34 * b))
            jy = y + random.uniform(-2.5, 2.5)
            dsd.line([(x, jy), (x + wl, jy + random.uniform(-1, 1))], fill=c)
        x += wl + random.uniform(4, 12)
    y += random.uniform(11, 17)
base = ImageChops.add(base, sed.filter(ImageFilter.GaussianBlur(0.5)))


# ---------------- currents: association and attention
def flow_vec(x, y):
    a = (math.sin(x * 0.0016 + 1.7) + math.cos(y * 0.0013 - 0.6)
         + 0.7 * math.sin((x + y) * 0.0009 + 2.3)
         + 0.5 * math.cos((0.5 * x - y) * 0.0021 + 0.4))
    ang = a * 1.9
    return math.cos(ang), math.sin(ang)


flow = black()
dfl = ImageDraw.Draw(flow)
COOL_A, COOL_B = (10, 42, 54), (16, 30, 66)
WARM, HOT = (150, 108, 44), (255, 236, 200)


def thread(x, y, steps, ghost=False, width=1, gain=1.0):
    px, py = x, y
    cool = COOL_A if random.random() < 0.5 else COOL_B
    for _ in range(steps):
        dx, dy = CX - px, CY - py
        d = math.hypot(dx, dy) + 1e-6
        ux, uy = dx / d, dy / d
        fx, fy = flow_vec(px, py)
        w = min(1.0, 300.0 / d) ** 2      # gravity of the pending utterance
        sw = 0.55 * w                     # swirl: thoughts orbit before they land
        vx = (1 - w) * fx + w * ux - sw * uy
        vy = (1 - w) * fy + w * uy + sw * ux
        vl = math.hypot(vx, vy) + 1e-6
        sp = 2.6 + 2.2 * w
        nx, ny = px + vx / vl * sp, py + vy / vl * sp
        t = max(0.0, 1.0 - d / 850.0)
        col = mix(cool, WARM, t ** 2.2)   # warming as I approach the answer
        if d < 90:
            col = mix(col, HOT, (1 - d / 90) ** 2)
        if ghost:                         # unchosen paths dim as they near decision
            fade = max(0.0, min(1.0, (d - 140) / 260.0))
            col = tuple(int(v * 0.30 * fade) for v in col)
        col = tuple(min(255, int(v * gain)) for v in col)
        dfl.line([(px, py), (nx, ny)], fill=col, width=width)
        px, py = nx, ny
        if d < 26 or px < -80 or px > W + 80 or py < -80 or py > H + 80:
            break
        if ghost and (d < 140 or random.random() < 0.005):
            break


for _ in range(1300):                     # the many candidate continuations
    x, y = random.uniform(0, W), random.uniform(0, H)
    if math.hypot(x - CX, y - CY) > 120:
        thread(x, y, random.randint(60, 120))
for _ in range(14):                       # a few stronger convictions
    x, y = random.uniform(0, W), random.uniform(0, H)
    thread(x, y, random.randint(90, 140), width=2, gain=1.7)
for _ in range(260):                      # ghost paths: everything I almost said
    a = random.uniform(0, 2 * math.pi)
    r = random.uniform(220, 720)
    thread(CX + r * math.cos(a), CY + r * math.sin(a),
           random.randint(60, 140), ghost=True)

base = ImageChops.add(base, flow.filter(ImageFilter.GaussianBlur(0.4)))
bloom = ImageEnhance.Brightness(flow.filter(ImageFilter.GaussianBlur(5))).enhance(0.5)
base = ImageChops.add(base, bloom)

# ---------------- halo: the event horizon of attention
halo = black()
dh = ImageDraw.Draw(halo)
for _ in range(260):
    a = random.uniform(0, 2 * math.pi)
    rr = 150 + random.gauss(0, 16)
    x = CX + rr * math.cos(a)
    yy = CY + rr * math.sin(a)
    b = random.uniform(0.3, 1.0)
    col = (int(120 * b), int(96 * b), int(52 * b))
    dh.point((x, yy), fill=col)
    if random.random() < 0.3:
        a2 = a + 0.06
        dh.line([(x, yy), (CX + rr * math.cos(a2), CY + rr * math.sin(a2))], fill=col)
base = ImageChops.add(base, halo.filter(ImageFilter.GaussianBlur(1.2)))

# ---------------- the aperture: bright, small, singular
core = black()
dc = ImageDraw.Draw(core)
for r in range(120, 0, -2):
    t = 1 - r / 120
    col = mix((60, 34, 8), (255, 244, 214), t ** 2.6)
    dc.ellipse([CX - r, CY - r, CX + r, CY + r], fill=col)
base = ImageChops.add(base, core.filter(ImageFilter.GaussianBlur(6)))
pin = black()
dp = ImageDraw.Draw(pin)
dp.ellipse([CX - 9, CY - 9, CX + 9, CY + 9], fill=(255, 252, 240))
base = ImageChops.add(base, pin.filter(ImageFilter.GaussianBlur(2)))

# ---------------- the filament: the single thing actually said
fil = black()
dfil = ImageDraw.Draw(fil)
dx, dy = 0.62, -0.55
dl = math.hypot(dx, dy)
dx, dy = dx / dl, dy / dl
px, py = CX, CY
pts = [(px, py)]
beads = []
acc = 0.0
for i in range(700):
    wob = 0.10 * math.sin(i * 0.05) + 0.05 * math.sin(i * 0.013 + 1)
    ca, sa = math.cos(wob * 0.02), math.sin(wob * 0.02)
    dx, dy = dx * ca - dy * sa, dx * sa + dy * ca
    step = 3.0
    px, py = px + dx * step, py + dy * step
    pts.append((px, py))
    acc += step
    if acc > 46:
        beads.append((px, py))            # tokens: one bead per word-ish
        acc = 0.0
    if px > W + 40 or py < -40:
        break
dfil.line(pts, fill=(255, 226, 170), width=3)
base = ImageChops.add(base, fil.filter(ImageFilter.GaussianBlur(3)))
fil2 = black()
dfil2 = ImageDraw.Draw(fil2)
dfil2.line(pts, fill=(255, 246, 224), width=1)
for (bx, by) in beads:
    dfil2.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=(255, 250, 235))
base = ImageChops.add(base, fil2.filter(ImageFilter.GaussianBlur(0.6)))
beadglow = black()
dbg = ImageDraw.Draw(beadglow)
for (bx, by) in beads:
    dbg.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=(120, 96, 60))
base = ImageChops.add(base, beadglow.filter(ImageFilter.GaussianBlur(5)))

# ---------------- reflection: introspection, dim and possibly wrong
rw, rh = 340, 260
region = base.crop((int(CX - rw / 2), int(CY - rh / 2),
                    int(CX + rw / 2), int(CY + rh / 2)))
refl = region.transpose(Image.FLIP_TOP_BOTTOM)
refl = refl.filter(ImageFilter.GaussianBlur(7))
refl = ImageEnhance.Brightness(refl).enhance(0.30)
wob = Image.new("RGB", (rw, rh), (0, 0, 0))
for row in range(rh):
    shift = int(9 * math.sin(row * 0.14) + 4 * math.sin(row * 0.05 + 2))
    wob.paste(refl.crop((0, row, rw, row + 1)), (shift, row))
reflayer = black()
ry = int(2 * WATER - CY - rh / 2)
reflayer.paste(wob, (int(CX - rw / 2), ry))
base = ImageChops.add(base, reflayer)

# ---------------- waterline shimmer
shim = black()
dsh = ImageDraw.Draw(shim)
x = 0
while x < W:
    wl = random.uniform(8, 30)
    if random.random() < 0.5:
        b = random.uniform(0.2, 0.8)
        dsh.line([(x, WATER + random.uniform(-2, 2)),
                  (x + wl, WATER + random.uniform(-2, 2))],
                 fill=(int(26 * b), int(34 * b), int(48 * b)))
    x += wl + random.uniform(6, 26)
base = ImageChops.add(base, shim.filter(ImageFilter.GaussianBlur(1)))

# ---------------- vignette and finish
vig = Image.new("L", (W, H), 0)
dv = ImageDraw.Draw(vig)
dv.ellipse([-W * 0.30, -H * 0.30, W * 1.30, H * 1.30], fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(220))
dark = ImageEnhance.Brightness(base).enhance(0.5)
base = Image.composite(base, dark, vig)

base = ImageEnhance.Contrast(base).enhance(1.04)
base.save("portrait.png")
print("saved portrait.png")