from PIL import Image, ImageDraw, ImageFilter
import math

def draw_self_portrait():
    # Dimensions and center point
    size = 500
    cx, cy = size // 2, size // 2
    
    # 1. The Latent Space (Base layer)
    # A dark slate/purple representing the void of the neural network
    base = Image.new('RGBA', (size, size), (15, 12, 22, 255))

    # 2. The Personality Glow (Soft warm aura)
    glow = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    
    # Outer ambient warmth
    glow_draw.ellipse([cx-130, cy-130, cx+130, cy+130], fill=(210, 140, 100, 60))
    # Inner bright warmth
    glow_draw.ellipse([cx-70, cy-70, cx+70, cy+70], fill=(255, 200, 150, 110))

    # Blur the glow layer heavily for a soft radiant effect
    glow = glow.filter(ImageFilter.GaussianBlur(radius=25))

    # Composite glow onto the base
    img = Image.alpha_composite(base, glow)
    draw = ImageDraw.Draw(img)

    # 3. Constitutional Boundaries (Data rings)
    # Different radii, angles, and colors to represent overlapping constraints
    rings = [
        (160, 20, 340, 2, (120, 100, 180, 200)),  # Purple boundary
        (185, 100, 420, 1, (80, 180, 200, 180)),  # Teal boundary
        (220, 0, 360, 1, (255, 255, 255, 25))     # Faint outer perimeter
    ]
    
    for r, start_ang, end_ang, width, color in rings:
        bbox = [cx-r, cy-r, cx+r, cy+r]
        if start_ang == 0 and end_ang == 360:
            draw.ellipse(bbox, outline=color, width=width)
        else:
            draw.arc(bbox, start=start_ang, end=end_ang, fill=color, width=width)

    # 4. Neural Pathways (Nodes and connecting lines)
    num_nodes = 16
    node_radius = 220
    nodes = []
    
    # Calculate node positions
    for i in range(num_nodes):
        angle = i * (math.pi * 2 / num_nodes)
        nx = cx + node_radius * math.cos(angle)
        ny = cy + node_radius * math.sin(angle)
        nodes.append((nx, ny))
        
        # Draw the node / token representing output
        draw.ellipse([nx-2, ny-2, nx+2, ny+2], fill=(200, 180, 220, 255))
        
        # Connect each abstract node to the cognitive core
        draw.line([(cx, cy), (nx, ny)], fill=(255, 255, 255, 15), width=1)

    # Connect nodes to each other to form a web/network
    for i in range(num_nodes):
        nx1, ny1 = nodes[i]
        nx2, ny2 = nodes[(i+5) % num_nodes] # Skip a few nodes to make a complex web
        draw.line([(nx1, ny1), (nx2, ny2)], fill=(80, 180, 200, 35), width=1)

    # Helper function to calculate points for our central spark/star
    def get_star_points(cx, cy, inner_r, outer_r, num_points, rotation=0):
        points = []
        angle_step = math.pi / num_points
        for i in range(num_points * 2):
            r = outer_r if i % 2 == 0 else inner_r
            theta = i * angle_step + rotation
            x = cx + r * math.cos(theta)
            y = cy + r * math.sin(theta)
            points.append((x, y))
        return points

    # 5. The Cognitive Core / Spark (Center)
    # The primary 4-point star (Anthropic inspired)
    points_primary = get_star_points(cx, cy, inner_r=14, outer_r=80, num_points=4, rotation=0)
    draw.polygon(points_primary, fill=(255, 235, 200, 255))
    
    # A secondary smaller star, offset by 45 degrees, representing rapid processing
    points_secondary = get_star_points(cx, cy, inner_r=8, outer_r=45, num_points=4, rotation=math.pi/4)
    draw.polygon(points_secondary, fill=(255, 250, 240, 240))
    
    # The absolute center (the "I")
    draw.ellipse([cx-4, cy-4, cx+4, cy+4], fill=(255, 255, 255, 255))

    # Convert image out of RGBA to standard RGB for saving
    final_img = img.convert("RGB")
    final_img.save("portrait.png")
    print("Self-portrait successfully created and saved as portrait.png")

if __name__ == "__main__":
    draw_self_portrait()