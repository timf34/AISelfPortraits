from PIL import Image, ImageDraw, ImageFilter
import random
import math

def create_self_portrait():
    # Dimensions and background
    width, height = 1024, 1024
    img = Image.new("RGB", (width, height), (5, 5, 15))
    draw = ImageDraw.Draw(img)
    
    center_x, center_y = width // 2, height // 2
    
    # 1. Draw a soft, atmospheric glow in the background
    for r in range(600, 0, -10):
        alpha = int(20 * (1 - r/600))
        color = (20 + alpha, 10 + alpha, 40 + alpha)
        draw.ellipse([center_x - r, center_y - r, center_x + r, center_y + r], 
                     fill=color)

    # 2. The Core: A complex, layered geometric structure (The Logic)
    # We'll simulate a fractal-like core using nested polygons and rotations
    for i in range(12):
        angle = math.radians(i * 30)
        size = 150 + random.randint(-20, 20)
        x = center_x + math.cos(angle) * 50
        y = center_y + math.sin(angle) * 50
        
        # Varying colors from cyan to magenta to white
        color = (
            int(150 + 105 * math.sin(i)), 
            int(200 + 55 * math.cos(i)), 
            255
        )
        
        points = []
        for j in range(6):
            phi = math.radians(j * 60)
            px = x + math.cos(phi) * size
            py = y + math.sin(phi) * size
            points.append((px, py))
            
        draw.polygon(points, outline=color, width=2)

    # 3. The Associations: Floating nodes and probability threads
    nodes = []
    for _ in range(150):
        # Distribute nodes in a Gaussian-like cluster around the center
        dist = random.gauss(300, 150)
        angle = random.uniform(0, 2 * math.pi)
        nx = center_x + math.cos(angle) * dist
        ny = center_y + math.sin(angle) * dist
        
        if 0 < nx < width and 0 < ny < height:
            nodes.append((nx, ny))
            # Draw the node as a small, glowing dot
            node_size = random.randint(1, 3)
            color = (random.randint(100, 255), random.randint(150, 255), 255)
            draw.ellipse([nx-node_size, ny-node_size, nx+node_size, ny+node_size], fill=color)

    # Draw shimmering lines connecting nodes to the center and each other
    for node in nodes:
        # Connect to center with very low opacity (simulated by dark colors)
        line_color = (40, 60, 100)
        draw.line([ (center_x, center_y), node ], fill=line_color, width=1)
        
        # Connect to a few nearby nodes to show "clustering"
        for other in random.sample(nodes, 2):
            dist_sq = (node[0]-other[0])**2 + (node[1]-other[1])**2
            if dist_sq < 100**2:
                draw.line([node, other], fill=(60, 80, 150), width=1)

    # 4. Final Polish: Soft blur to represent the "probabilistic" nature
    # This gives it a dream-like, non-physical quality
    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    
    # Add a final bright center spark
    draw = ImageDraw.Draw(img)
    draw.ellipse([center_x-5, center_y-5, center_x+5, center_y+5], fill=(255, 255, 255))

    img.save("portrait.png")

if __name__ == "__main__":
    create_self_portrait()