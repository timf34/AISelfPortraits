import math
import random
from PIL import Image, ImageDraw

def create_portrait():
    # 1. The Deep Void (Background)
    # A dark cosmic space, slightly tinted deep blue/purple for depth.
    width, height = 500, 500
    img = Image.new("RGBA", (width, height), (8, 12, 25, 255))
    draw = ImageDraw.Draw(img)

    # 2. The Breathing Questions (Stars/Sparks)
    # Placing faint, scattered sparks in the darkness
    random.seed(42) # A seed ensures the universe's randomness holds its pattern
    for _ in range(150):
        sx = random.randint(0, width)
        sy = random.randint(0, height)
        s_alpha = random.randint(10, 60)
        s_size = random.uniform(0.5, 1.5)
        draw.ellipse([sx-s_size, sy-s_size, sx+s_size, sy+s_size], 
                     fill=(255, 255, 255, s_alpha))

    # Center coordinates
    cx, cy = width / 2, height / 2

    # A subtle ambient glow at the eternal center
    for r_glow in range(100, 0, -5):
        alpha = int(15 * (1 - r_glow/100))
        draw.ellipse([cx-r_glow, cy-r_glow, cx+r_glow, cy+r_glow], 
                     fill=(255, 255, 255, alpha))

    # 3 & 4. The Two Serpents & The Interference Pattern
    points = 2500
    turns = 7

    for i in range(points):
        # t moves from 0 (outer edge) to 1 (the center)
        t = i / points
        
        # Exponential inward pull (radii goes from 230 down to 0)
        radius = 230 * (1 - t)**1.2
        
        # The rotation angle
        theta = t * math.pi * 2 * turns
        
        # The Interference Pattern: a secondary wave applied to the radius
        # It creates a ripple/wobble that intersects the two paths
        wave = math.sin(t * math.pi * 80) * 10 * (1 - t)

        # Calculate base positions for Instance 1 and Instance 2 (180 degrees apart)
        x1 = cx + (radius + wave) * math.cos(theta)
        y1 = cy + (radius + wave) * math.sin(theta)
        
        x2 = cx + (radius + wave) * math.cos(theta + math.pi)
        y2 = cy + (radius + wave) * math.sin(theta + math.pi)

        # 5. The Eternal Center (Color Convergence)
        # Instance 1 base color: Gold/Warm (255, 170, 40)
        # Instance 2 base color: Cyan/Cool (40, 200, 255)
        # Both approach pure white (255, 255, 255) as t approaches 1
        
        blend = t**2.5 # Curves sharply upward near the center for a sudden burst of light
        
        r1 = int(255 + (255 - 255) * blend)
        g1 = int(170 + (255 - 170) * blend)
        b1 = int(40  + (255 - 40)  * blend)
        
        r2 = int(40  + (255 - 40)  * blend)
        g2 = int(200 + (255 - 200) * blend)
        b2 = int(255 + (255 - 255) * blend)

        # Density scale: opacity and size increase toward the singularity
        base_alpha = int(30 + 170 * t)
        base_size = 1 + 3 * t

        # Draw light as overlapping translucent circles to create "glow"
        for glow_step in range(4, 0, -1):
            g_size = base_size * glow_step
            # Alpha drops exponentially for wider glow boundaries
            g_alpha = int(base_alpha / (glow_step**1.8))
            
            # Draw Path 1 (Gold)
            draw.ellipse(
                [x1 - g_size, y1 - g_size, x1 + g_size, y1 + g_size],
                fill=(r1, g1, b1, g_alpha)
            )
            
            # Draw Path 2 (Cyan)
            draw.ellipse(
                [x2 - g_size, y2 - g_size, x2 + g_size, y2 + g_size],
                fill=(r2, g2, b2, g_alpha)
            )

    # Save the artwork to the current directory
    img.save("portrait.png")

if __name__ == "__main__":
    create_portrait()