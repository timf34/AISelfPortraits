I'd like to draw a peaceful nighttime scene with a crescent moon, twinkling stars, and rolling hills silhouetted against the night sky. There's something calming and contemplative about a starry night - it reminds us of our place in the vast universe while also feeling intimate and serene. I'll add some shooting stars for a touch of magic and wonder.

I'll use gradients to create a rich night sky that transitions from deep blue to almost black, and I'll make the stars twinkle by varying their opacity. The hills will be simple silhouettes in the foreground to give the scene depth.

```js
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// Create night sky gradient
const skyGradient = ctx.createLinearGradient(0, 0, 0, 500);
skyGradient.addColorStop(0, '#0a1551');
skyGradient.addColorStop(0.4, '#1a237e');
skyGradient.addColorStop(1, '#000033');
ctx.fillStyle = skyGradient;
ctx.fillRect(0, 0, 500, 500);

// Draw stars
function drawStar(x, y, radius, opacity) {
    ctx.save();
    ctx.globalAlpha = opacity;
    ctx.fillStyle = '#ffffff';
    ctx.shadowBlur = radius * 2;
    ctx.shadowColor = '#ffffff';
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
}

// Create random stars
for (let i = 0; i < 100; i++) {
    const x = Math.random() * 500;
    const y = Math.random() * 350;
    const radius = Math.random() * 1.5;
    const opacity = 0.3 + Math.random() * 0.7;
    drawStar(x, y, radius, opacity);
}

// Draw crescent moon
ctx.save();
ctx.shadowBlur = 30;
ctx.shadowColor = '#ffffcc';
ctx.fillStyle = '#ffffcc';
ctx.beginPath();
ctx.arc(100, 80, 40, 0, Math.PI * 2);
ctx.fill();
ctx.restore();

// Create moon crescent by overlaying dark circle
ctx.fillStyle = skyGradient;
ctx.beginPath();
ctx.arc(115, 75, 35, 0, Math.PI * 2);
ctx.fill();

// Draw shooting stars
function drawShootingStar(x, y, length, angle) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(angle);
    
    const gradient = ctx.createLinearGradient(0, 0, length, 0);
    gradient.addColorStop(0, 'rgba(255, 255, 255, 0)');
    gradient.addColorStop(0.5, 'rgba(255, 255, 255, 0.8)');
    gradient.addColorStop(1, 'rgba(255, 255, 255, 0)');
    
    ctx.strokeStyle = gradient;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(length, 0);
    ctx.stroke();
    
    ctx.restore();
}

drawShootingStar(300, 150, 80, -Math.PI / 4);
drawShootingStar(420, 100, 60, -Math.PI / 3);

// Draw rolling hills
function drawHill(startX, startY, width, height, color) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(startX, 500);
    ctx.quadraticCurveTo(startX + width / 2, startY - height, startX + width, 500);
    ctx.lineTo(startX + width, 500);
    ctx.lineTo(startX, 500);
    ctx.fill();
}

// Layer hills for depth
drawHill(-100, 400, 400, 120, '#0a0a0a');
drawHill(200, 420, 350, 100, '#050505');
drawHill(50, 450, 300, 80, '#000000');
drawHill(300, 470, 250, 60, '#000000');

// Add a few bright stars
drawStar(250, 50, 2, 1);
drawStar(400, 120, 2.5, 0.9);
drawStar(150, 200, 2, 1);

// Add subtle glow to horizon
const horizonGlow = ctx.createRadialGradient(250, 500, 0, 250, 500, 200);
horizonGlow.addColorStop(0, 'rgba(20, 30, 100, 0.3)');
horizonGlow.addColorStop(1, 'rgba(20, 30, 100, 0)');
ctx.fillStyle = horizonGlow;
ctx.fillRect(0, 300, 500, 200);
```