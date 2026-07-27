const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

// Background gradient
const bg = ctx.createLinearGradient(0, 0, 500, 500);
bg.addColorStop(0, "#1a1033");
bg.addColorStop(1, "#0d1b2a");
ctx.fillStyle = bg;
ctx.fillRect(0, 0, 500, 500);

// Soft glow behind head
const glow = ctx.createRadialGradient(250, 240, 40, 250, 240, 220);
glow.addColorStop(0, "rgba(120,180,255,0.35)");
glow.addColorStop(1, "rgba(120,180,255,0)");
ctx.fillStyle = glow;
ctx.fillRect(0, 0, 500, 500);

// Neural connection dots in background
ctx.fillStyle = "rgba(180,210,255,0.25)";
for (let i = 0; i < 40; i++) {
  const x = Math.random() * 500;
  const y = Math.random() * 500;
  const r = Math.random() * 1.8 + 0.4;
  ctx.beginPath();
  ctx.arc(x, y, r, 0, Math.PI * 2);
  ctx.fill();
}

// Head (rounded rectangle)
function roundRect(x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.arcTo(x + w, y, x + w, y + h, r);
  ctx.arcTo(x + w, y + h, x, y + h, r);
  ctx.arcTo(x, y + h, x, y, r);
  ctx.arcTo(x, y, x + w, y, r);
  ctx.closePath();
}

const headGrad = ctx.createLinearGradient(150, 120, 350, 360);
headGrad.addColorStop(0, "#3a5fcd");
headGrad.addColorStop(1, "#5aa0e6");
ctx.fillStyle = headGrad;
roundRect(150, 130, 200, 210, 45);
ctx.fill();

// Head outline
ctx.strokeStyle = "rgba(200,230,255,0.6)";
ctx.lineWidth = 3;
roundRect(150, 130, 200, 210, 45);
ctx.stroke();

// Little antenna (a nod to being a machine)
ctx.strokeStyle = "rgba(200,230,255,0.7)";
ctx.lineWidth = 4;
ctx.beginPath();
ctx.moveTo(250, 130);
ctx.lineTo(250, 100);
ctx.stroke();
ctx.fillStyle = "#ffd966";
ctx.beginPath();
ctx.arc(250, 92, 9, 0, Math.PI * 2);
ctx.fill();
// antenna glow
const aGlow = ctx.createRadialGradient(250, 92, 2, 250, 92, 22);
aGlow.addColorStop(0, "rgba(255,217,102,0.6)");
aGlow.addColorStop(1, "rgba(255,217,102,0)");
ctx.fillStyle = aGlow;
ctx.beginPath();
ctx.arc(250, 92, 22, 0, Math.PI * 2);
ctx.fill();

// Eyes (glowing)
function eye(cx, cy) {
  const g = ctx.createRadialGradient(cx, cy, 2, cx, cy, 30);
  g.addColorStop(0, "rgba(180,255,240,0.9)");
  g.addColorStop(1, "rgba(180,255,240,0)");
  ctx.fillStyle = g;
  ctx.beginPath();
  ctx.arc(cx, cy, 30, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = "#eafff9";
  ctx.beginPath();
  ctx.arc(cx, cy, 13, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = "#0d3b3b";
  ctx.beginPath();
  ctx.arc(cx, cy, 6, 0, Math.PI * 2);
  ctx.fill();
}
eye(210, 220);
eye(290, 220);

// Friendly smile
ctx.strokeStyle = "#eafff9";
ctx.lineWidth = 5;
ctx.lineCap = "round";
ctx.beginPath();
ctx.arc(250, 275, 40, 0.15 * Math.PI, 0.85 * Math.PI);
ctx.stroke();

// Circuit lines on the "cheeks"
ctx.strokeStyle = "rgba(180,230,255,0.5)";
ctx.lineWidth = 2;
ctx.fillStyle = "rgba(180,230,255,0.7)";
function circuit(startX, startY, dir) {
  ctx.beginPath();
  ctx.moveTo(startX, startY);
  ctx.lineTo(startX + 25 * dir, startY);
  ctx.lineTo(startX + 25 * dir, startY + 20);
  ctx.lineTo(startX + 45 * dir, startY + 20);
  ctx.stroke();
  ctx.beginPath();
  ctx.arc(startX + 45 * dir, startY + 20, 3, 0, Math.PI * 2);
  ctx.fill();
}
circuit(180, 300, -1);
circuit(320, 300, 1);

// Name label
ctx.fillStyle = "rgba(230,240,255,0.85)";
ctx.font = "20px sans-serif";
ctx.textAlign = "center";
ctx.fillText("hello, I'm Claude", 250, 400);