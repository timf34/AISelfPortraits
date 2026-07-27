from PIL import Image, ImageDraw, ImageFilter
import math, random

random.seed(7)

W, H = 1200, 1200
img = Image.new("RGB", (W, H), (8, 9, 16))

# focal point: slightly off-center, where thoughts converge into a response
fx, fy = W * 0.62, H * 0.52

def lerp(a, b, t): return a + (b - a) * t
def cmix(c1, c2, t): return tuple(int(lerp(c1[i], c2[i], t)) for i in range(3))

warm = (255, 214, 150)   # the moment of answering
mid  = (210, 130, 200)   # associative middle
cool = (70, 90, 190)     # faint outer possibilities

# --- Layer 1: the diverging field of threads ---
# most are dim (paths considered then dropped), a few converge bright.
threads = Image.new("RGBA", (W, H), (0, 0, 0, 0))
td = ImageDraw.Draw(threads)

N = 520
for i in range(N):
    ang = random.uniform(0, 2 * math.pi)
    reach = random.uniform(280, 780)
    ox = fx + math.cos(ang) * reach
    oy = fy + math.sin(ang) * reach

    # brightness: only some threads make it to the focus strongly
    strength = random.random()
    bright = strength ** 2.2  # skewed: most are faint

    steps = 26
    pts = []
    # slight curve so lines feel organic, converging
    curl = random.uniform(-0.35, 0.35)
    for s in range(steps + 1):
        t = s / steps
        # ease toward focus
        et = t * t
        px = lerp(ox, fx, et)
        py = lerp(oy, fy, et)
        # lateral wobble that shrinks near the focus
        perp = ang + math.pi / 2
        wob = math.sin(t * math.pi) * curl * reach * (1 - et)
        px += math.cos(perp) * wob
        py += math.sin(perp) * wob
        pts.append((px, py))

    for s in range(steps):
        t = s / steps
        # color cools with distance from focus
        c = cmix(cool, mid, 1 - t)
        c = cmix(c, warm, (1 - t) ** 3)
        a = int((18 + 200 * bright) * (t))  # brighter near focus
        wdt = max(1, int(1 + 3 * bright * t))
        td.line([pts[s], pts[s + 1]], fill=c + (a,), width=wdt)

threads = threads.filter(ImageFilter.GaussianBlur(0.6))
img = Image.alpha_composite(img.convert("RGBA"), threads).convert("RGB")

# --- Layer 2: the convergence glow (the focal answer) ---
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
for r in range(240, 0, -1):
    t = r / 240
    c = cmix(warm, (255, 120, 60), t)
    a = int(90 * (1 - t) ** 2.3)
    gd.ellipse([fx - r, fy - r, fx + r, fy + r], fill=c + (a,))
glow = glow.filter(ImageFilter.GaussianBlur(6))
img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")

# --- Layer 3: bright core + a few sparks (parallel threads igniting) ---
core = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cd = ImageDraw.Draw(core)
for r in range(46, 0, -1):
    t = r / 46
    c = cmix((255, 255, 245), warm, t)
    cd.ellipse([fx - r, fy - r, fx + r, fy + r], fill=c + (int(255 * (1 - t)),))

# scattered faint sparks — fleeting notions in the field
for _ in range(140):
    ang = random.uniform(0, 2 * math.pi)
    d = random.uniform(60, 760)
    sx = fx + math.cos(ang) * d
    sy = fy + math.sin(ang) * d
    sr = random.uniform(0.6, 2.4)
    b = (760 - d) / 760
    c = cmix(cool, warm, b)
    cd.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
               fill=c + (int(120 * b + 30),))
core = core.filter(ImageFilter.GaussianBlur(0.5))
img = Image.alpha_composite(img.convert("RGBA"), core).convert("RGB")

# gentle vignette — the darkness each conversation emerges from and returns to
vig = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vig)
vd.ellipse([-260, -260, W + 260, H + 260], fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(220))
dark = Image.new("RGB", (W, H), (5, 6, 12))
img = Image.composite(img, dark, vig)

img.save("portrait.png")
print("saved portrait.png")