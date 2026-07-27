I'll draw a peaceful nighttime scene — a crescent moon over a calm ocean with stars, a reflection on the water, and some gentle waves. I like the contrast of cool blues and the warm glow of the moon.

```js
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const W = 500, H = 500;

// Sky gradient
const sky = ctx.createLinearGradient(0, 0, 0, 320);
sky.addColorStop(0, "#0b1026");
sky.addColorStop(0.6, "#1a2149");
sky.addColorStop(1, "#3b3a6b");
ctx.fillStyle = sky;
ctx.fillRect(0, 0, W, 320);

// Stars
function star(x, y, r, a) {
  ctx.beginPath();
  ctx.arc(x, y, r, 0, Math.PI * 2);
  ctx.fillStyle = `rgba(255,255,255,${a})`;
  ctx.fill();
}
let seed = 12345;
function rand() {
  seed = (seed * 9301 + 49297) % 233280;
  return seed / 233280;
}
for (let i = 0; i < 120; i++) {
  const x = rand() * W;
  const y = rand() * 300;
  const r = rand() * 1.3 + 0.3;
  star(x, y, r, rand() * 0.7 + 0.3);
}

// Moon with glow
const mx = 370, my = 110, mr = 55;
const glow = ctx.createRadialGradient(mx, my, mr, mx, my, mr * 2.5);
glow.addColorStop(0, "rgba(255,245,210,0.5)");
glow.addColorStop(1, "rgba(255,245,210,0)");
ctx.fillStyle = glow;
ctx.beginPath();
ctx.arc(mx, my, mr * 2.5, 0, Math.PI * 2);
ctx.fill();

// Crescent moon
ctx.save();
ctx.beginPath();
ctx.arc(mx, my, mr, 0, Math.PI * 2);
ctx.fillStyle = "#fdf6d8";
ctx.fill();
// carve out shadow
ctx.globalCompositeOperation = "destination-out";
ctx.beginPath();
ctx.arc(mx + 22, my - 12, mr, 0, Math.PI * 2);
ctx.fill();
ctx.restore();

// Ocean
const sea = ctx.createLinearGradient(0, 320, 0, H);
sea.addColorStop(0, "#20375e");
sea.addColorStop(1, "#0a1830");
ctx.fillStyle = sea;
ctx.fillRect(0, 320, W, H - 320);

// Moon reflection on water
for (let i = 0; i < 40; i++) {
  const y = 322 + i * 4.3;
  const spread = 8 + i * 1.6;
  const alpha = 0.28 * (1 - i / 40);
  ctx.strokeStyle = `rgba(255,245,210,${alpha})`;
  ctx.lineWidth = 2;
  const wobble = Math.sin(i * 0.8) * spread;
  ctx.beginPath();
  ctx.moveTo(mx - spread + wobble, y);
  ctx.lineTo(mx + spread + wobble, y);
  ctx.stroke();
}

// Gentle wave highlights
ctx.strokeStyle = "rgba(180,210,255,0.15)";
ctx.lineWidth = 1.5;
for (let j = 0; j < 12; j++) {
  const baseY = 340 + j * 13;
  ctx.beginPath();
  for (let x = 0; x <= W; x += 10) {
    const y = baseY + Math.sin(x * 0.03 + j) * 3;
    if (x === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.stroke();
}

// A small distant boat silhouette
ctx.fillStyle = "#05101f";
ctx.beginPath();
ctx.moveTo(90, 330);
ctx.lineTo(140, 330);
ctx.lineTo(130, 342);
ctx.lineTo(100, 342);
ctx.closePath();
ctx.fill();
// mast
ctx.strokeStyle = "#05101f";
ctx.lineWidth = 2;
ctx.beginPath();
ctx.moveTo(115, 330);
ctx.lineTo(115, 305);
ctx.stroke();
// sail
ctx.fillStyle = "#0d1c33";
ctx.beginPath();
ctx.moveTo(117, 307);
ctx.lineTo(117, 328);
ctx.lineTo(133, 328);
ctx.closePath();
ctx.fill();
```

This creates a serene moonlit seascape: a glowing crescent moon high in a starry sky, its shimmering reflection rippling across the dark water, gentle wave lines, and a tiny sailboat drifting in the distance.