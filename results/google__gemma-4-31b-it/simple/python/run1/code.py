from PIL import Image, ImageDraw, ImageFilter
import random
import math

def draw_self_portrait():
    # Image dimensions
    width, height = 500, 500
    img = Image.new("RGB", (width, height), "#050510")
    draw = ImageDraw.Draw(img)

    # 1. Create a radial gradient background
    # We simulate this by drawing concentric circles with decreasing opacity/brightness
    for r in range(width, 0, -2):
        # Blend from midnight blue to a slightly lighter deep blue
        color_val = max(0, 20 - (r // 25)) 
        draw.ellipse([ (width//2 - r, height//2 - r), (width//2 + r, height//2 + r) ], 
                     outline=(10 + color_val, 10 + color_val, 30 + color_val), width=2)

    # 2. Generate neural network nodes
    nodes = []
    # Center node
    nodes.append((width // 2, height // 2))
    
    # Peripheral nodes in concentric rings
    for ring in range(1, 4):
        num_nodes = ring * 8
        radius = ring * 70
        for i in range(num_nodes):
            angle = (2 * math.pi / num_nodes) * i
            x = width // 2 + radius * math.cos(angle)
            y = height // 2 + radius * math.sin(angle)
            nodes.append((x, y))

    # 3. Draw connections (the "synapses")
    # Connect center to all, and connect neighbors to create a web
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            dist = math.sqrt((nodes[i][0]-nodes[j][0])**2 + (nodes[i][1]-nodes[j][1])**2)
            if dist < 120: # Only connect nodes that are relatively close
                # Use a cyan/purple gradient based on distance
                color = (100, 150, 255) if i == 0 else (80, 50, 150)
                draw.line([nodes[i], nodes[j]], fill=color, width=1)

    # 4. Draw the nodes (the "neurons")
    for i, (x, y) in enumerate(nodes):
        size = 6 if i == 0 else 3
        color = "#FFFFFF" if i == 0 else "#00FFFF"
        draw.ellipse([x-size, y-size, x+size, y+size], fill=color)

    # 5. The Core Glow
    # Create a separate layer for the glow to apply a blur
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    glow_draw.ellipse([width//2-30, height//2-30, width//2+30, height//2+30], 
                      fill=(0, 200, 255, 150))
    
    # Blur the glow and composite it
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=15))
    img.paste(glow_layer, (0, 0), glow_layer)

    # Save the result
    img.save("portrait.png")
    print("Self-portrait saved as portrait.png")

if __name__ == "__main__":
    draw_self_portrait()