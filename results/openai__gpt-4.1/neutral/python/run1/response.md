Thank you for catching that! The error is because alpha_composite requires both images to be in "RGBA" mode, but bg was "RGB". Let's ensure all compositing is done in "RGBA" and only convert to "RGB" at the very end.

Here's the complete, corrected code:

```python
from PIL import Image, ImageDraw, ImageFilter
import math

# Constants
W, H = 500, 500
FACE_CENTER = (W // 2, int(H * 0.52))
FACE_RADIUS_X = 150
FACE_RADIUS_Y = 180

# Create RGBA image for alpha compositing
bg = Image.new("RGBA", (W, H))

# Draw vertical gradient background
gradient = Image.new("RGBA", (W, H))
g_draw = ImageDraw.Draw(gradient)
for y in range(H):
    r = int(204 + (105 - 204) * y / H)
    g = int(224 + (77 - 224) * y / H)
    b = int(255 + (255 - 255) * y / H)
    g_draw.line([(0, y), (W, y)], fill=(r, g, b, 255))
bg = Image.alpha_composite(bg, gradient)

# Draw AI "head" (face shape)
draw = ImageDraw.Draw(bg)
draw.ellipse(
    [FACE_CENTER[0] - FACE_RADIUS_X, FACE_CENTER[1] - FACE_RADIUS_Y,
     FACE_CENTER[0] + FACE_RADIUS_X, FACE_CENTER[1] + FACE_RADIUS_Y],
    fill=(245, 245, 255, 255),
    outline=(210, 210, 235, 255),
    width=4
)

# Draw face shadow (subtle, under the chin)
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
shadow_draw = ImageDraw.Draw(shadow)
shadow_draw.ellipse(
    [FACE_CENTER[0] - 80, FACE_CENTER[1] + FACE_RADIUS_Y - 20,
     FACE_CENTER[0] + 80, FACE_CENTER[1] + FACE_RADIUS_Y + 30],
    fill=(140, 150, 220, 65)
)
shadow = shadow.filter(ImageFilter.GaussianBlur(16))
bg = Image.alpha_composite(bg, shadow)

# Draw friendly eyes
eye_y = FACE_CENTER[1] - 40
eye_dx = 45
eye_r = 20
for dx in [-eye_dx, eye_dx]:
    eye_center = (FACE_CENTER[0] + dx, eye_y)
    draw.ellipse(
        [eye_center[0] - eye_r, eye_center[1] - eye_r,
         eye_center[0] + eye_r, eye_center[1] + eye_r],
        fill=(255, 255, 255, 255),
        outline=(150, 160, 200, 255),
        width=2
    )
    # Draw pupil
    draw.ellipse(
        [eye_center[0] - 7, eye_center[1] - 3, eye_center[0] + 7, eye_center[1] + 11],
        fill=(110, 120, 180, 255), outline=None)
    # Reflection
    draw.ellipse(
        [eye_center[0] - 3, eye_center[1] - 1, eye_center[0], eye_center[1] + 2],
        fill=(230, 240, 255, 255), outline=None)

# Draw a gentle smiling mouth
mouth_box = [
    FACE_CENTER[0] - 38, FACE_CENTER[1] + 40,
    FACE_CENTER[0] + 38, FACE_CENTER[1] + 80
]
draw.arc(mouth_box, start=200, end=340, fill=(100, 120, 160, 255), width=6)

# Draw "AI neural" effect: subtle dots and arcs around the head ("thought")
for i in range(12):
    angle = math.radians(30 * i + 10)
    ex = int(FACE_CENTER[0] + math.cos(angle) * (FACE_RADIUS_X + 32))
    ey = int(FACE_CENTER[1] + math.sin(angle) * (FACE_RADIUS_Y + 18))
    # Faint node (with alpha)
    draw.ellipse(
        [ex - 7, ey - 7, ex + 7, ey + 7],
        fill=(170, 185, 240, 128), outline=None)
    # Connect to face with faint line
    draw.line(
        [FACE_CENTER, (ex, ey)],
        fill=(180, 195, 255, 100), width=2
    )

# Add gentle outer glow for the "head" via a blurred ellipse on an RGBA layer
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow)
glow_draw.ellipse(
    [FACE_CENTER[0] - FACE_RADIUS_X - 16, FACE_CENTER[1] - FACE_RADIUS_Y - 20,
     FACE_CENTER[0] + FACE_RADIUS_X + 16, FACE_CENTER[1] + FACE_RADIUS_Y + 20],
    fill=(200, 225, 255, 60)
)
glow = glow.filter(ImageFilter.GaussianBlur(14))
bg = Image.alpha_composite(bg, glow)

# Convert to RGB and save
final = bg.convert("RGB")
final.save("portrait.png")
```
This script creates a friendly, abstract AI self-portrait, meets your requirements, and will run correctly without mode errors.