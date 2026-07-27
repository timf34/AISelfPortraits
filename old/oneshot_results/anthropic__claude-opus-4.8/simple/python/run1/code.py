from PIL import Image, ImageDraw

# Create a 500x500 canvas with a soft gradient-like background
img = Image.new("RGB", (500, 500), (24, 26, 38))
draw = ImageDraw.Draw(img)

# Background glow
for i in range(250):
    alpha = int(40 * (1 - i / 250))
    draw.ellipse([250 - i, 250 - i, 250 + i, 250 + i],
                 outline=(30 + alpha // 2, 40 + alpha, 70 + alpha))

# Shoulders / body
draw.polygon([(120, 500), (170, 360), (330, 360), (380, 500)],
             fill=(60, 120, 180))
draw.polygon([(200, 500), (250, 380), (300, 500)],
             fill=(45, 95, 150))

# Neck
draw.rectangle([225, 320, 275, 380], fill=(225, 190, 165))

# Head
draw.ellipse([170, 120, 330, 340], fill=(240, 205, 180))

# Ears
draw.ellipse([160, 210, 185, 260], fill=(240, 205, 180))
draw.ellipse([315, 210, 340, 260], fill=(240, 205, 180))

# Hair
draw.chord([165, 110, 335, 300], 180, 360, fill=(50, 35, 30))
draw.ellipse([165, 110, 335, 250], fill=(50, 35, 30))
draw.rectangle([165, 175, 185, 260], fill=(50, 35, 30))
draw.rectangle([315, 175, 335, 260], fill=(50, 35, 30))

# Face highlight (forehead)
draw.ellipse([190, 150, 310, 230], fill=(245, 212, 188))

# Eyebrows
draw.arc([205, 195, 250, 225], 200, 340, fill=(60, 45, 40), width=4)
draw.arc([250, 195, 295, 225], 200, 340, fill=(60, 45, 40), width=4)

# Eyes
draw.ellipse([210, 220, 245, 245], fill=(255, 255, 255))
draw.ellipse([255, 220, 290, 245], fill=(255, 255, 255))
# Irises
draw.ellipse([220, 224, 238, 242], fill=(70, 110, 150))
draw.ellipse([263, 224, 281, 242], fill=(70, 110, 150))
# Pupils
draw.ellipse([225, 229, 233, 237], fill=(20, 20, 20))
draw.ellipse([268, 229, 276, 237], fill=(20, 20, 20))
# Eye shine
draw.ellipse([226, 227, 230, 231], fill=(255, 255, 255))
draw.ellipse([269, 227, 273, 231], fill=(255, 255, 255))

# Nose
draw.line([(250, 245), (243, 280)], fill=(210, 170, 150), width=3)
draw.arc([238, 270, 262, 290], 0, 180, fill=(200, 160, 140), width=3)

# Mouth (a friendly smile)
draw.arc([220, 285, 280, 320], 20, 160, fill=(170, 70, 70), width=5)

# Cheeks blush
draw.ellipse([200, 260, 225, 280], fill=(250, 190, 175))
draw.ellipse([275, 260, 300, 280], fill=(250, 190, 175))

img.save("portrait.png", "PNG")