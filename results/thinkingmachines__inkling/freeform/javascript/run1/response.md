I'll draw an aurora borealis scene — layered, glowing curved bands over a dark sky, scattered stars, a luminous moon, and silhouetted mountains at the bottom. It's a calm, atmospheric composition that makes good use of gradients, transparency, and layered paths.

```js
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// Background gradient: deep night sky
const bgGrad = ctx.createLinearGradient(0, 0, 0, 500);
bgGrad.addColorStop(0, '#060b1f');
bgGrad.addColorStop(0.5, '#0a1230');
bgGrad.addColorStop(1, '#020510');
ctx.fillStyle = bgGrad;
ctx.fillRect(0, 0, 500, 500);

// Star field
for (let i = 0; i < 120; i++) {
  const x = Math.random() * 500;
  const y = Math.random() * 320;
  const r = Math.random() * 1.2 + 0.2;
  const alpha = Math.random() * 0.6 + 0.2;
  ctx.fillStyle = `rgba(255, 255, 240, ${alpha})`;
  ctx.beginPath();
  ctx.arc(x, y, r, 0, Math.PI * 2);
  ctx.fill();
}

// Aurora bands (curved, translucent)
const drawAurora = (yOffset, colorMain, colorAccent) => {
  ctx.save();
  ctx.globalAlpha = 0.35;
  const gradient = ctx.createLinearGradient(0, yOffset - 40, 0, yOffset + 100);
  gradient.addColorStop(0, colorAccent);
  gradient.addColorStop(0.5, colorMain);
  gradient.addColorStop(1, 'rgba(255,255,255,0)');
  
  ctx.beginPath();
  ctx.moveTo(0, yOffset);
  ctx.bezierCurveTo(120, yOffset - 60, 300, yOffset + 40, 500, yOffset - 20);
  ctx.lineTo(500, yOffset + 120);
  ctx.bezierCurveTo(300, yOffset + 60, 120, yOffset - 20, 0, yOffset + 80);
  ctx.closePath();
  ctx.fillStyle = gradient;
  ctx.fill();
  ctx.restore();
};

drawAurora(100, '#4eea8c', '#2a7a4e'); // green
drawAurora(160, '#a86cf5', '#4a1c7a'); // purple
drawAurora(220, '#5ce1e6', '#1a4a52'); // cyan

// Moon with glow
const mx = 400, my = 80;
const moonGrad = ctx.createRadialGradient(mx, my, 5, mx, my, 35);
moonGrad.addColorStop(0, '#fffcd6');
moonGrad.addColorStop(0.4, '#f0e6b8');
moonGrad.addColorStop(1, 'rgba(240, 230, 180, 0)');
ctx.fillStyle = moonGrad;
ctx.beginPath();
ctx.arc(mx, my, 35, 0, Math.PI * 2);
ctx.fill();
ctx.fillStyle = '#fff8dc';
ctx.beginPath();
ctx.arc(mx, my, 16, 0, Math.PI * 2);
ctx.fill();

// Shooting star
const starGrad = ctx.createLinearGradient(320, 140, 420, 180);
starGrad.addColorStop(0, 'rgba(255,255,255,0)');
starGrad.addColorStop(0.5, 'rgba(255,255,255,0.9)');
starGrad.addColorStop(1, 'rgba(255,255,255,0)');
ctx.strokeStyle = starGrad;
ctx.lineWidth = 2;
ctx.beginPath();
ctx.moveTo(330, 145);
ctx.lineTo(410, 175);
ctx.stroke();
ctx.fillStyle = '#fff';
ctx.beginPath();
ctx.arc(410, 175, 2, 0, Math.PI * 2);
ctx.fill();

// Mountains (layered silhouettes)
const drawMountainRange = (baseY, color, peaks) => {
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.moveTo(0, baseY);
  for (let i = 0; i <= peaks; i++) {
    const x = (i / peaks) * 500;
    const h = 40 + Math.random() * 70;
    const cx = x + (Math.random() - 0.5) * 60;
    ctx.lineTo(cx, baseY - h);
  }
  ctx.lineTo(500, baseY);
  ctx.lineTo(0, baseY);
  ctx.fill();
};

// Deterministic mountain layers using a simple pattern for consistency
ctx.save();
// Back mountains
ctx.fillStyle = '#08122d';
ctx.beginPath();
ctx.moveTo(0, 360);
ctx.lineTo(60, 280); ctx.lineTo(140, 320); ctx.lineTo(220, 260); 
ctx.lineTo(300, 330); ctx.lineTo(400, 270); ctx.lineTo(480, 310);
ctx.lineTo(500, 290); ctx.lineTo(500, 500); ctx.lineTo(0, 500); ctx.closePath();
ctx.fill();
// Mid mountains
ctx.fillStyle = '#040d1f';
ctx.beginPath();
ctx.moveTo(0, 380);
ctx.lineTo(80, 310); ctx.lineTo(160, 350); ctx.lineTo(250, 290);
ctx.lineTo(350, 340); ctx.lineTo(450, 300); ctx.lineTo(500, 320);
ctx.lineTo(500, 500); ctx.lineTo(0, 500); ctx.closePath();
ctx.fill();
// Front mountains
ctx.fillStyle = '#020510';
ctx.beginPath();
ctx.moveTo(0, 400);
ctx.lineTo(100, 330); ctx.lineTo(200, 370); ctx.lineTo(300, 310);
ctx.lineTo(400, 360); ctx.lineTo(500, 330);
ctx.lineTo(500, 500); ctx.lineTo(0, 500); ctx.closePath();
ctx.fill();
ctx.restore();

// Subtle reflection at bottom
const refl = ctx.createLinearGradient(0, 400, 0, 500);
refl.addColorStop(0, 'rgba(255,255,255,0.04)');
refl.addColorStop(1, 'rgba(255,255,255,0)');
ctx.fillStyle = refl;
ctx.fillRect(0, 400, 500, 100);
```