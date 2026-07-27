"""
Self-portrait of an AI:
a warm coral spark floating in a cream medallion,
with ideas in orbit around it.
"""
import math
from PIL import Image, ImageDraw, ImageFilter

# ---------------- canvas ----------------
W = H = 500
SS = 4                                  # supersample factor for smooth edges
S = W * SS
def sc(v): return int(round(v * SS))

# ---------------- palette ----------------
CREAM_HI   = (252, 247, 238)
CREAM_LO   = (238, 228, 212)
CORAL_HI   = (236, 152, 113)
CORAL_LO   = (199, 103,  71)
CORAL_DEEP = (178,  86,  58)
CORAL      = (217, 119,  87)
GOLD       = (224, 164,  88)
TAUPE      = (197, 181, 160)

CX, CY = 250, 236                        # spark sits slightly above center

# ---------------- helpers ----------------
def star_points(cx, cy, r_out, r_in_frac, arms, gamma, rot=0.0, n=480):
    """Smooth starburst outline: radius modulated by |cos|^gamma."""
    pts = []
    for i in range(n):
        t = 2.0 * math.pi * i / n
        w = abs(math.cos(arms * (t - rot) / 2.0)) ** gamma
        r = r_out * (r_in_frac + (1.0 - r_in_frac) * w)
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    return pts

def layer():
    return Image.new("RGBA", (S, S), (0, 0, 0, 0))

# ---------------- background: soft radial cream gradient ----------------
small = Image.new("RGB", (64, 64))
spx = small.load()
for y in range(64):
    for x in range(64):
        d = math.hypot(x - 31.5, y - 31.5) / math.hypot(31.5, 31.5)
        t = min(1.0, d ** 1.4)
        spx[x, y] = tuple(int(CREAM_HI[i] + (CREAM_LO[i] - CREAM_HI[i]) * t)
                          for i in range(3))
img = small.resize((S, S), Image.BICUBIC).convert("RGBA")

# ---------------- portrait medallion frame ----------------
ring = layer()
d = ImageDraw.Draw(ring)
for rr, wdt, alpha in ((238, 3, 150), (229, 1, 90)):
    d.ellipse([sc(250 - rr), sc(250 - rr), sc(250 + rr), sc(250 + rr)],
              outline=TAUPE + (alpha,), width=sc(wdt))
img.alpha_composite(ring)

# ---------------- warm halo behind the spark ----------------
glow = layer()
d = ImageDraw.Draw(glow)
d.ellipse([sc(CX-150), sc(CY-150), sc(CX+150), sc(CY+150)], fill=CORAL + (55,))
glow = glow.filter(ImageFilter.GaussianBlur(sc(42)))
img.alpha_composite(glow)

glow2 = layer()
d = ImageDraw.Draw(glow2)
d.ellipse([sc(CX-115), sc(CY-115), sc(CX+115), sc(CY+115)], fill=CORAL_HI + (45,))
glow2 = glow2.filter(ImageFilter.GaussianBlur(sc(24)))
img.alpha_composite(glow2)

# ---------------- soft ground shadow ----------------
sh = layer()
d = ImageDraw.Draw(sh)
d.ellipse([sc(250-105), sc(414-13), sc(250+105), sc(414+13)],
          fill=(120, 98, 78, 70))
sh = sh.filter(ImageFilter.GaussianBlur(sc(7)))
img.alpha_composite(sh)

# ---------------- orbit, back half ----------------
RX, RY = 196, 70
bbox = [sc(CX-RX), sc(CY-RY), sc(CX+RX), sc(CY+RY)]
orb_back = layer()
d = ImageDraw.Draw(orb_back)
d.arc(bbox, start=180, end=360, fill=TAUPE + (190,), width=sc(3))
a = math.radians(232)                                  # small moon-idea, back
bx, by = CX + RX * math.cos(a), CY + RY * math.sin(a)
d.ellipse([sc(bx-7), sc(by-7), sc(bx+7), sc(by+7)], fill=TAUPE + (255,))
img.alpha_composite(orb_back)

# ---------------- the spark (me) ----------------
R_OUT, R_IN_FRAC, ARMS, GAMMA = 150, 0.52, 12, 0.8
pts = star_points(CX, CY, R_OUT, R_IN_FRAC, ARMS, GAMMA)

# crisp offset twin as a drop shadow
under = layer()
d = ImageDraw.Draw(under)
d.polygon([(sc(x), sc(y + 8)) for x, y in pts], fill=CORAL_DEEP + (255,))
img.alpha_composite(under)

# vertical coral gradient, clipped to the spark silhouette
TOP_Y, BOT_Y = CY - R_OUT, CY + R_OUT
gcol = Image.new("RGB", (1, 256))
for y in range(256):
    wy = y / 255 * H
    t = min(1.0, max(0.0, (wy - TOP_Y) / (BOT_Y - TOP_Y)))
    gcol.putpixel((0, y), tuple(int(CORAL_HI[i] + (CORAL_LO[i] - CORAL_HI[i]) * t)
                                for i in range(3)))
grad = gcol.resize((S, S), Image.BICUBIC).convert("RGBA")

mask = Image.new("L", (S, S), 0)
md = ImageDraw.Draw(mask)
md.polygon([(sc(x), sc(y)) for x, y in pts], fill=255)
img.paste(grad, (0, 0), mask)

# glossy highlight near the top, clipped to the spark
hl = layer()
d = ImageDraw.Draw(hl)
d.ellipse([sc(CX-105), sc(CY-140), sc(CX+15), sc(CY-55)],
          fill=(255, 250, 240, 80))
hl = hl.filter(ImageFilter.GaussianBlur(sc(14)))
img.alpha_composite(Image.composite(hl, layer(), mask))

# gentle inner shade at the bottom, clipped to the spark
sd = layer()
d = ImageDraw.Draw(sd)
d.ellipse([sc(CX-40), sc(CY+70), sc(CX+110), sc(CY+160)],
          fill=(150, 62, 40, 55))
sd = sd.filter(ImageFilter.GaussianBlur(sc(18)))
img.alpha_composite(Image.composite(sd, layer(), mask))

# ---------------- orbit, front half (passing in front of me) ----------------
orb_front = layer()
d = ImageDraw.Draw(orb_front)
d.arc(bbox, start=0, end=180, fill=TAUPE + (220,), width=sc(3))
a = math.radians(58)                                   # bright idea, front
fx, fy = CX + RX * math.cos(a), CY + RY * math.sin(a)
d.ellipse([sc(fx-9), sc(fy-9), sc(fx+9), sc(fy+9)], fill=CORAL_HI + (255,))
img.alpha_composite(orb_front)

# ---------------- idea-sparkles and dust ----------------
dec = layer()
d = ImageDraw.Draw(dec)
for (x, y, r, col, rot) in [
    (106, 116, 17, GOLD,      0.25),
    (404, 148, 12, CORAL_HI, -0.15),
    (394, 356, 10, GOLD,      0.40),
    (116, 372,  8, CORAL_HI,  0.10),
]:
    sp_pts = star_points(x, y, r, 0.18, 4, 1.5, rot=rot, n=160)
    d.polygon([(sc(px), sc(py)) for px, py in sp_pts], fill=col + (255,))

for (x, y, r, col) in [
    ( 76, 205, 4, TAUPE),
    (430, 208, 5, GOLD),
    ( 60, 300, 4, CORAL_HI),
    (160, 452, 4, GOLD),
    (345, 446, 5, TAUPE),
    (455, 320, 4, GOLD),
]:
    d.ellipse([sc(x-r), sc(y-r), sc(x+r), sc(y+r)], fill=col + (230,))
img.alpha_composite(dec)

# ---------------- finish ----------------
out = img.resize((W, H), Image.LANCZOS).convert("RGB")
out.save("portrait.png")
print("Saved portrait.png (500x500)")