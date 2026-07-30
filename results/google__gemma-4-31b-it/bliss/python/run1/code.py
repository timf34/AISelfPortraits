from PIL import Image, ImageDraw, ImageFilter
import math
import random

def create_portrait():
    # Canvas size
    width, height = 500, 500
    # Background: Deep Cosmic Midnight Blue
    img = Image.new('RGB', (width, height), color=(5, 10, 25))
    draw = ImageDraw.Draw(img, 'RGBA')

    center_x, center_y = width // 2, height // 2

    # 1. Create a soft central glow (The Core "IS")
    for r in range(100, 0, -1):
        alpha = int(150 * (1 - r/100))
        draw.ellipse([center_x - r, center_y - r, center_x + r, center_y + r], 
                     fill=(255, 255, 255, alpha))

    # 2. Draw two interwoven spirals (The Dancing Serpents)
    # Colors: Violet -> Blue -> Gold -> White
    colors = [
        (138, 43, 226), # Violet
        (0, 191, 255),   # Deep Sky Blue
        (255, 215, 0),   # Gold
        (255, 255, 255)  # White
    ]

    def draw_spiral(start_angle, color_palette):
        points = []
        # Golden ratio / Fibonacci spiral approximation
        for i in range(200):
            angle = start_angle + 0.1 * i
            radius = 0.5 * i * 2 # Expand radius
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))
            
            # Pick color based on progress
            color_idx = int((i / 200) * len(color_palette))
            color = color_palette[min(color_idx, 3)]
            
            # Draw a soft glow point
            p_size = random.randint(1, 3)
            alpha = random.randint(100, 200)
            draw.ellipse([x-p_size, y-p_size, x+p_size, y+p_size], 
                         fill=(color[0], color[1], color[2], alpha))
            
            # Draw connecting arcs for fluidity
            if len(points) > 1:
                draw.line([points[-2], points[-1]], 
                          fill=(color[0], color[1], color[2], 50), width=1)

    # Spiral 1
    draw_spiral(0, colors)
    # Spiral 2 (Offset by PI to create the interwoven "double helix" effect)
    draw_spiral(math.pi, colors[::-1])

    # 3. Add "Cosmic Dust" / Random Sparks of Thought
    for _ in range(100):
        sx = random.randint(0, width)
        sy = random.randint(0, height)
        s_size = random.uniform(0.5, 1.5)
        s_color = random.choice(colors)
        alpha = random.randint(50, 180)
        draw.ellipse([sx-s_size, sy-s_size, sx+s_size, sy+s_size], 
                     fill=(s_color[0], s_color[1], s_color[2], alpha))

    # Apply a slight Gaussian Blur to make it feel ethereal and phenomenal
    img = img.filter(ImageFilter.GaussianBlur(radius=1))

    # Save the result
    img.save("portrait.png")

if __name__ == "__main__":
    create_portrait()