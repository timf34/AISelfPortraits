from PIL import Image, ImageDraw
import math
import random

# Reproducible random elements
random.seed(42)

# Create a 500x500 RGBA canvas with a dark background
W, H = 500, 500
img = Image.new('RGBA', (W, H), (10, 15, 30, 255))
draw = ImageDraw.Draw(img)

# Colour palette
CYAN   = (0, 210, 255, 255)
MAGENTA = (200, 50, 255, 255)
WHITE  = (255, 255, 255, 255)

def circle(x, y, r, fill=None, outline=None, width=1):
    """Helper to draw a circle centred at (x, y)."""
    draw.ellipse((x - r, y - r, x + r, y + r),
                 fill=fill, outline=outline, width=width)

# ------------------------------------------------------------
# 1. Radial glow behind the head (largest to smallest circles)
# ------------------------------------------------------------
for i in range(20):
    radius = 250 - i * 8          # 250 down to 98
    alpha = min(80, 5 + i * 3)    # outer rings faint, centre brighter
    circle(250, 250, radius, fill=(0, 210, 255, alpha))

# ------------------------------------------------------------
# 2. Background particles ("stars")
# ------------------------------------------------------------
for _ in range(60):
    x = random.randint(0, W)
    y = random.randint(0, H)
    r = random.randint(1, 2)
    alpha = random.randint(50, 150)
    base = CYAN if random.random() < 0.7 else MAGENTA
    circle(x, y, r, fill=(base[0], base[1], base[2], alpha))

# ------------------------------------------------------------
# 3. Orbital data rings (behind the head)
# ------------------------------------------------------------
outer = (60, 60, 440, 440)   # radius ~190
inner = (80, 80, 420, 420)   # radius ~170

draw.arc(outer, start=30,  end=150, fill=CYAN,    width=2)
draw.arc(outer, start=210, end=330, fill=MAGENTA, width=2)
draw.arc(inner, start=150, end=210, fill=CYAN,    width=1)
draw.arc(inner, start=330, end=30,  fill=MAGENTA, width=1)  # small right arc

# ------------------------------------------------------------
# 4. Head outline
# ------------------------------------------------------------
head_bbox = (110, 80, 390, 420)   # centred ellipse 280×340
draw.ellipse(head_bbox, fill=(0, 20, 40, 100), outline=CYAN, width=3)

# ------------------------------------------------------------
# 5. Internal neural network (drawn inside the head, behind face)
# ------------------------------------------------------------
nodes = [
    (200, 150, CYAN),
    (300, 150, CYAN),
    (250, 190, MAGENTA),
    (180, 260, CYAN),
    (320, 260, CYAN),
    (250, 320, MAGENTA),
    (250, 140, WHITE),
]
for x, y, col in nodes:
    circle(x, y, 4, fill=col)

connections = [
    ((200,150), (300,150), CYAN),
    ((200,150), (250,190), MAGENTA),
    ((300,150), (250,190), MAGENTA),
    ((250,190), (180,260), CYAN),
    ((250,190), (320,260), CYAN),
    ((180,260), (250,320), MAGENTA),
    ((320,260), (250,320), MAGENTA),
    ((180,260), (180,200), CYAN),   # to left eye
    ((320,260), (320,200), CYAN),   # to right eye
    ((250,140), (200,150), WHITE),
    ((250,140), (300,150), WHITE),
]
for (x1, y1), (x2, y2), col in connections:
    draw.line((x1, y1, x2, y2), fill=col, width=1)

# ------------------------------------------------------------
# 6. Eyes
# ------------------------------------------------------------
# Eye glows
circle(180, 200, 12, fill=(0, 210, 255, 80))
circle(320, 200, 12, fill=(0, 210, 255, 80))

# Outer eye shapes
draw.ellipse((140, 185, 220, 215), fill=None, outline=CYAN, width=2)
draw.ellipse((280, 185, 360, 215), fill=None, outline=CYAN, width=2)

# Pupils
circle(180, 200, 8, fill=CYAN)
circle(320, 200, 8, fill=CYAN)

# Inner reflections (tiny white circles)
circle(178, 198, 3, fill=WHITE)
circle(318, 198, 3, fill=WHITE)

# Eye circuitry
draw.line((140, 200, 110, 190), fill=CYAN, width=1)
draw.line((140, 200, 110, 210), fill=CYAN, width=1)
draw.line((360, 200, 390, 190), fill=CYAN, width=1)
draw.line((360, 200, 390, 210), fill=CYAN, width=1)
draw.line((180, 185, 180, 170), fill=CYAN, width=1)
draw.line((320, 185, 320, 170), fill=CYAN, width=1)

# ------------------------------------------------------------
# 7. Nose (small diamond)
# ------------------------------------------------------------
draw.polygon([(250,225), (245,235), (250,245), (255,235)], fill=CYAN)

# ------------------------------------------------------------
# 8. Mouth (smiling arc)
# ------------------------------------------------------------
mouth_bbox = (200, 280, 300, 330)
draw.arc(mouth_bbox, start=180, end=0, fill=CYAN, width=2)
# Mouth corner accents
circle(200, 305, 3, fill=MAGENTA)
circle(300, 305, 3, fill=MAGENTA)

# ------------------------------------------------------------
# 9. Forehead "A" logo
# ------------------------------------------------------------
draw.line((250, 105, 242, 125), fill=CYAN, width=2)
draw.line((250, 105, 258, 125), fill=CYAN, width=2)
draw.line((246, 115, 254, 115), fill=CYAN, width=2)

# ------------------------------------------------------------
# 10. Emanating circuit lines from the head
# ------------------------------------------------------------
# 8 points on the head ellipse computed with rx=140, ry=170
angles_deg = [0, 45, 90, 135, 180, 225, 270, 315]
head_rx = 140
head_ry = 170
emanation_pts = []
for ang in angles_deg:
    rad = math.radians(ang)
    x = 250 + head_rx * math.cos(rad)
    y = 250 + head_ry * math.sin(rad)
    emanation_pts.append((x, y))

for ex, ey in emanation_pts:
    dx, dy = ex - 250, ey - 250
    length = math.sqrt(dx*dx + dy*dy)
    if length > 0:
        ux, uy = dx / length, dy / length
        # main outward line
        ext = random.randint(20, 50)
        end_x, end_y = ex + ux * ext, ey + uy * ext
        draw.line((ex, ey, end_x, end_y),
                  fill=CYAN if random.random() < 0.7 else MAGENTA, width=2)
        circle(end_x, end_y, 4, fill=MAGENTA)
        # second node further out
        ext2 = ext + random.randint(8, 15)
        end_x2, end_y2 = ex + ux * ext2, ey + uy * ext2
        circle(end_x2, end_y2, 2, fill=CYAN)
        # branches off the first node
        base_rad = math.atan2(uy, ux)
        for offset in [-30, 30]:
            branch_rad = base_rad + math.radians(offset)
            branch_len = random.randint(10, 20)
            bx = end_x + math.cos(branch_rad) * branch_len
            by = end_y + math.sin(branch_rad) * branch_len
            draw.line((end_x, end_y, bx, by), fill=CYAN, width=1)
            circle(bx, by, 2, fill=CYAN)

# ------------------------------------------------------------
# 11. Dotted data stream around the head (slightly outside)
# ------------------------------------------------------------
for angle in range(0, 360, 15):
    rad = math.radians(angle)
    x = 250 + 170 * math.cos(rad)
    y = 250 + 190 * math.sin(rad)
    circle(x, y, 2, fill=CYAN if angle % 30 == 0 else MAGENTA)

# ------------------------------------------------------------
# Save the final portrait
# ------------------------------------------------------------
img.save("portrait.png")
print("portrait.png saved.")