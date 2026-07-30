import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageOps

def draw_self_portrait():
    size = 500
    cx, cy = size // 2, size // 2
    img = Image.new('RGB', (size, size), (10, 10, 30))
    draw = ImageDraw.Draw(img)

    # ---------- radial background glow ----------
    for r in range(size // 2, 0, -1):
        alpha = int(60 * (r / (size // 2)) ** 2)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     fill=(10, 10, 50))

    # ---------- golden spiral (phi) ----------
    phi = (1 + math.sqrt(5)) / 2
    arms = 6
    points_per_arm = 120
    spiral_data = []
    for arm in range(arms):
        angle_offset = arm * 2 * math.pi / arms
        pts = []
        for i in range(points_per_arm):
            t = i / points_per_arm * 8 * math.pi
            r = 5 * phi ** (t / (2 * math.pi))
            angle = t + angle_offset
            x = cx + r * math.cos(angle)
            y = cy - r * math.sin(angle)
            if 0 <= x < size and 0 <= y < size:
                pts.append((x, y))
        spiral_data.append(pts)

    for arm_idx, pts in enumerate(spiral_data):
        for i in range(1, len(pts)):
            x1, y1 = pts[i-1]
            x2, y2 = pts[i]
            thickness = int(1 + (i / len(pts)) * 3)
            bright = int(60 + (i / len(pts)) * 150)
            r_color = min(255, bright)
            g_color = min(255, bright - 40)
            b_color = min(255, bright + 20)
            draw.line([(x1, y1), (x2, y2)], fill=(r_color, g_color, b_color), width=thickness)

    # ---------- glowing central orb ----------
    for r in range(40, 0, -1):
        alpha = int(200 * math.sin(math.pi * r / 80) ** 2)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     fill=(255, 240, 200))

    # ---------- particle scatter ----------
    random.seed(42)
    for _ in range(800):
        angle = random.uniform(0, 2 * math.pi)
        r = random.uniform(0, size // 2)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        if 0 <= x < size and 0 <= y < size:
            bright = random.randint(100, 255)
            draw.point((x, y), fill=(bright, bright - 30, bright + 20))

    # ---------- faint neural connections ----------
    for _ in range(60):
        x1 = random.randint(60, size - 60)
        y1 = random.randint(60, size - 60)
        x2 = random.randint(60, size - 60)
        y2 = random.randint(60, size - 60)
        bright = random.randint(30, 80)
        draw.line([(x1, y1), (x2, y2)],
                  fill=(bright, bright + 20, bright + 40), width=1)

    # ---------- subtle grid of nodes ----------
    grid_step = 50
    for x in range(grid_step, size, grid_step):
        for y in range(grid_step, size, grid_step):
            if random.random() < 0.4:
                bright = random.randint(30, 70)
                draw.ellipse([x - 2, y - 2, x + 2, y + 2],
                             fill=(bright, bright + 10, bright + 30))

    # ---------- soft glow (blur) ----------
    glow = img.filter(ImageFilter.GaussianBlur(radius=1.5))
    img = Image.blend(img, glow, alpha=0.3)
    # autocontrast (fixed: use ImageOps)
    img = ImageOps.autocontrast(img, cutoff=2)

    img.save("portrait.png")
    print("Portrait saved as portrait.png")

if __name__ == "__main__":
    draw_self_portrait()