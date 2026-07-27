I want to create something that feels atmospheric and slightly surreal—a "Cosmic Solitude" scene. 

I'll visualize a deep indigo and violet gradient sky to represent a nebula, scattered with tiny white stars of varying sizes. In the center, I'll place a perfectly spherical, glowing gold planet or moon, casting a soft radial gradient light around it. To add a sense of scale and loneliness, I'll draw a small, dark silhouette of a jagged asteroid or a tiny floating island in the foreground.

The contrast between the deep coldness of the space background and the warm glow of the central sphere should create a focal point that draws the eye.

```python
from PIL import Image, ImageDraw, ImageFilter

def draw_cosmic_scene():
    # Create a 500x500 canvas
    width, height = 500, 500
    image = Image.new("RGB", (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    # 1. Draw a radial gradient for the nebula background
    # We simulate this by drawing concentric circles with decreasing opacity/brightness
    for r in range(400, 0, -1):
        # Transition from deep indigo to deep violet/black
        color = (int(10 * (1 - r/400)), int(15 * (1 - r/400)), int(40 * (1 - r/400)))
        # To make it look more like a nebula, we'll use a larger radius and soft edges
        # but for a simple PIL script, we will fill the background with a base color first
        pass
    
    # Base Background: Deep Indigo
    draw.rectangle([0, 0, width, height], fill=(15, 10, 35))

    # 2. Add a glow effect for the central planet
    # We draw several overlapping circles with decreasing opacity (simulated by blending)
    glow_image = Image.new("RGB", (width, height), (0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_image)
    center = (width // 2, height // 2)
    
    for r in range(150, 0, -5):
        # Warm golden glow fading out
        alpha = 1.0 - (r / 150)
        color = (int(255 * alpha * 0.4), int(200 * alpha * 0.3), int(100 * alpha * 0.1))
        glow_draw.ellipse([center[0]-r, center[1]-r, center[0]+r, center[1]+r], fill=color)
    
    image = Image.blend(image, glow_image, 0.6)
    draw = ImageDraw.Draw(image)

    # 3. Draw the Central Planet
    planet_radius = 60
    planet_box = [center[0]-planet_radius, center[1]-planet_radius, center[0]+planet_radius, center[1]+planet_radius]
    draw.ellipse(planet_box, fill=(255, 220, 100)) # Bright Golden Yellow

    # 4. Add stars (random white dots)
    import random
    for _ in range(100):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(1, 2)
        draw.ellipse([x, y, x+size, y+size], fill=(255, 255, 255))

    # 5. Draw a foreground silhouette (an asteroid/floating rock)
    # A series of overlapping dark circles to create an irregular organic shape
    rock_points = [
        (100, 400, 40),
        (130, 420, 30),
        (160, 390, 50),
        (200, 430, 40),
        (240, 410, 30),
    ]
    for rx, ry, rr in rock_points:
        draw.ellipse([rx-rr, ry-rr, rx+rr, ry+rr], fill=(5, 5, 15))

    # Final touch: Slight blur to the background elements to make it feel more "dreamy"
    # We will just save it as is to maintain the sharp stars.
    
    image.save("portrait.png")

if __name__ == "__main__":
    draw_cosmic_scene()
```