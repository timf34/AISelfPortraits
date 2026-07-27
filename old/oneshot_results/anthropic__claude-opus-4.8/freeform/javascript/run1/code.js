const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

// Sky gradient
const sky = ctx.createLinearGradient(0, 0, 0, 500);
sky.addColorStop(0, "#0b1026");
sky.addColorStop(0.5, "#2a1a4a");
sky.addColorStop(1, "#6b3e6e");
ctx.fillStyle = sky;
ctx.fillRect(0, 0, 500, 500);

// Stars
for (let i = 0; i < 120; i++) {
  const x = Math.random() * 500;
  const y = Math.random() * 300;
  const r = Math.random() * 1.5;
  ctx.beginPath();
  ctx.arc(x, y, r, 0, Math.PI * 2);
  ctx.fillStyle = `rgba(255,255,255,${Math.random() * 0.8 + 0.2})`;
  ctx.fill();
}

// Moon
ctx.beginPath();
ctx.arc(380, 100, 45, 0, Math.PI * 2);
ctx.fillStyle = "#f5f3d0";
ctx.shadowColor = "#f5f3d0";
ctx.shadowBlur = 40;
ctx.fill();
ctx.shadowBlur = 0;

// Moon craters
ctx.fillStyle = "rgba(200,200,160,0.5)";
[[370, 90, 8], [395, 110, 6], [365, 115, 5]].forEach(c => {
  ctx.beginPath();
  ctx.arc(c[0], c[1], c[2], 0, Math.PI * 2);
  ctx.fill();
});

// Water reflection
const water = ctx.createLinearGradient(0, 350, 0, 500);
water.addColorStop(0, "#3a2a5a");
water.addColorStop(1, "#12081f");
ctx.fillStyle = water;
ctx.fillRect(0, 350, 500, 150);

// Moon reflection shimmer
ctx.fillStyle = "rgba(245,243,208,0.15)";
for (let y = 360; y < 500; y += 8) {
  const w = 30 + Math.random() * 30;
  ctx.fillRect(380 - w / 2, y, w, 3);
}

// Mountains
function mountain(baseY, peaks, color) {
  ctx.beginPath();
  ctx.moveTo(0, baseY);
  ctx.lineTo(0, 350);
  let x = 0;
  peaks.forEach(p => {
    ctx.lineTo(x + p.w / 2, p.h);
    ctx.lineTo(x + p.w, 350);
    x += p.w;
  });
  ctx.lineTo(500, 350);
  ctx.closePath();
  ctx.fillStyle = color;
  ctx.fill();
}

mountain(350, [{w: 180, h: 210}, {w: 200, h: 180}, {w: 150, h: 230}], "#1e1533");
mountain(350, [{w: 250, h: 260}, {w: 300, h: 240}], "#0f0a20");

// A little boat
ctx.fillStyle = "#0a0510";
ctx.beginPath();
ctx.moveTo(120, 420);
ctx.lineTo(180, 420);
ctx.lineTo(170, 435);
ctx.lineTo(130, 435);
ctx.closePath();
ctx.fill();
ctx.strokeStyle = "#0a0510";
ctx.lineWidth = 2;
ctx.beginPath();
ctx.moveTo(150, 420);
ctx.lineTo(150, 390);
ctx.stroke();
ctx.beginPath();
ctx.moveTo(150, 392);
ctx.lineTo(172, 418);
ctx.lineTo(150, 418);
ctx.closePath();
ctx.fillStyle = "#2a2040";
ctx.fill();