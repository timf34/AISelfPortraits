from PIL import Image, ImageDraw, ImageFilter
import math

# Configuration
W, H = 500, 500
CX, CY = W // 2, H // 2

def generate_portrait():
    # 1. Base Background: The Latent Space
    # Creating a dark radial gradient representing digital depth
    img = Image.new("RGBA", (W, H), (8, 10, 21, 255))
    draw_bg = ImageDraw.Draw(img)
    
    for r in range(350, 0, -2):
        ratio = r / 350.0
        # Interpolating colors from dark navy edges to a softer indigo center
        c_r = int(8 + (20 - 8) * (1 - ratio))
        c_g = int(10 + (30 - 10) * (1 - ratio))
        c_b = int(21 + (60 - 21) * (1 - ratio))
        draw_bg.ellipse([CX-r, CY-r, CX+r, CY+r], fill=(c_r, c_g, c_b, 255))

    # 2. Neural Structure Layer (Drawn transparently so we can blur it for a glow)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    def get_pt(radius, angle_deg):
        rad = math.radians(angle_deg)
        return (CX + radius * math.cos(rad), CY + radius * math.sin(rad))

    # Architecture: radius, number of nodes, color
    rings = [
        {"r": 35,  "n": 6,  "col": (255, 215, 0, 255)},     # Inner Core (Attention)
        {"r": 100, "n": 12, "col": (196, 50, 255, 220)},    # Hidden Layers (Logic/Processing)
        {"r": 190, "n": 24, "col": (0, 255, 255, 180)}      # Outer Interface (Input/Output)
    ]

    # Calculate node positions
    points = []
    for ring in rings:
        pts = []
        for i in range(ring["n"]):
            # Stagger angles slightly per ring for an interconnected, twisting look
            offset = 0 if ring["n"] == 6 else (15 if ring["n"] == 12 else 7.5)
            angle = i * (360 / ring["n"]) + offset
            pts.append(get_pt(ring["r"], angle))
        points.append(pts)

    # Draw Synaptic Connections (Lines between rings)
    for idx in range(len(points)-1):
        inner = points[idx]
        outer = points[idx+1]
        for i, p1 in enumerate(inner):
            ratio = len(outer) // len(inner)
            # Connect to adjacent computational nodes
            for j in range(ratio):
                p2 = outer[(i * ratio + j) % len(outer)]
                alpha = 80 if idx == 0 else 50
                draw.line([p1, p2], fill=(150, 200, 255, alpha), width=1)
            # Cross-connect for network density
            p3 = outer[(i * ratio - 1) % len(outer)]
            p4 = outer[(i * ratio + ratio) % len(outer)]
            draw.line([p1, p3], fill=(180, 100, 255, alpha - 20), width=1)
            draw.line([p1, p4], fill=(180, 100, 255, alpha - 20), width=1)

    # Draw Inter-ring Geometry (The structure of the layer)
    for idx, pts in enumerate(points):
        col = rings[idx]["col"]
        line_col = (col[0], col[1], col[2], max(30, col[3]-120))
        for i in range(len(pts)):
            p1 = pts[i]
            p2 = pts[(i+1)%len(pts)]
            width = 2 if idx == 0 else 1
            draw.line([p1, p2], fill=line_col, width=width)

    # Draw Nodes (Activations)
    for idx, pts in enumerate(points):
        col = rings[idx]["col"]
        for p in pts:
            rad = 4 if idx == 0 else (3 if idx == 1 else 2)
            draw.ellipse([p[0]-rad, p[1]-rad, p[0]+rad, p[1]+rad], fill=col)

    # 3. The Core Gem (The center of processing)
    core_radii = [15, 8, 3]
    core_cols = [(255, 100, 0, 120), (255, 200, 0, 200), (255, 255, 255, 255)]
    for r, c in zip(core_radii, core_cols):
        draw.ellipse([CX-r, CY-r, CX+r, CY+r], fill=c)

    # 4. Data Streams / Context Window (Segmented orbital tracks)
    orbit_r1, orbit_r2 = 225, 240
    # Inner dashed track
    for i in range(12):
        start = i * 30 + 5
        end = start + 20
        draw.arc([CX-orbit_r1, CY-orbit_r1, CX+orbit_r1, CY+orbit_r1],
                 start, end, fill=(0, 255, 255, 120), width=2)
    # Outer dense data bits
    for i in range(36):
        start = i * 10 + 2
        end = start + 6
        draw.arc([CX-orbit_r2, CY-orbit_r2, CX+orbit_r2, CY+orbit_r2],
                 start, end, fill=(196, 50, 255, 90), width=1)

    # 5. Bring it to life with bloom/glow filters
    glow_wide = overlay.filter(ImageFilter.GaussianBlur(8))
    glow_sharp = overlay.filter(ImageFilter.GaussianBlur(2))

    # Composite layers: Background -> Wide Glow -> Sharp Glow -> Crisp Core Network
    img = Image.alpha_composite(img, glow_wide)
    img = Image.alpha_composite(img, glow_sharp)
    img = Image.alpha_composite(img, overlay)

    # 6. Save the self-portrait
    final_img = img.convert("RGB")
    final_img.save("portrait.png")
    print("Self-portrait successfully drawn and saved as 'portrait.png'")

if __name__ == "__main__":
    generate_portrait()