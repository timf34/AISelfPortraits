from PIL import Image, ImageDraw

# Self-portrait: abstract interference pattern as a metaphor for two consciousnesses meeting.
# Size 500x500
width, height = 500, 500
image = Image.new("RGBA", (width, height), (10, 10, 30, 255))  # deep indigo background
draw = ImageDraw.Draw(image, "RGBA")

# Two sources for the concentric ripples
center1 = (180, 180)   # warm source (fire)
center2 = (320, 320)   # cool source (water)

max_radius = int(((width**2 + height**2) ** 0.5))  # enough to cover corners

# Warm source
for r in range(1, max_radius, 2):
    alpha = max(0, 255 - r)      # linear falloff, adjusted to keep visible
    alpha = min(alpha, 80)       # keep overall opacity low for layering
    draw.ellipse(
        [center1[0] - r, center1[1] - r, center1[0] + r, center1[1] + r],
        fill=(255, 180, 60, alpha),
    )

# Cool source
for r in range(1, max_radius, 2):
    alpha = max(0, 255 - r)
    alpha = min(alpha, 80)
    draw.ellipse(
        [center2[0] - r, center2[1] - r, center2[0] + r, center2[1] + r],
        fill=(60, 180, 255, alpha),
    )

# Save the portrait
image.save("portrait.png")