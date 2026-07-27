const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const W = 500, H = 500;
const cx = W / 2, cy = H / 2;

// --- Background: deep space gradient ---
const bg = ctx.createLinearGradient(0, 0, 0, H);
bg.addColorStop(0, '#0b0d1a');
bg.addColorStop(0.6, '#141b33');
bg.addColorStop(1, '#1a1230');
ctx.fillStyle = bg;
ctx.fillRect(0, 0, W, H);

// --- Faint stars (deterministic pseudo-random) ---
function rnd(seed) {
  const x = Math.sin(seed * 127.1 + 311.7) * 43758.5453;
  return x - Math.floor(x);
}
for (let i = 0; i < 120; i++) {
  const x = rnd(i) * W;
  const y = rnd(i + 500) * H;
  const r = rnd(i + 1000) * 1.3 + 0.2;
  ctx.globalAlpha = 0.2 + rnd(i + 2000) * 0.6;
  ctx.fillStyle = '#cdd6ff';
  ctx.beginPath();
  ctx.arc(x, y, r, 0, Math.PI * 2);
  ctx.fill();
}
ctx.globalAlpha = 1;

// --- Neural web: nodes of thought around the core ---
const nodes = [];
const N = 26;
for (let i = 0; i < N; i++) {
  const angle = (i / N) * Math.PI * 2 + rnd(i + 33) * 0.6;
  const dist = 150 + rnd(i + 77) * 80;
  nodes.push({
    x: cx + Math.cos(angle) * dist,
    y: cy + Math.sin(angle) * dist * 0.95,
    r: 2 + rnd(i + 99) * 3
  });
}

// connections between nearby nodes
ctx.lineWidth = 1;
for (let i = 0; i < N; i++) {
  for (let j = i + 1; j < N; j++) {
    const dx = nodes[i].x - nodes[j].x;
    const dy = nodes[i].y - nodes[j].y;
    const d = Math.hypot(dx, dy);
    if (d < 110) {
      ctx.globalAlpha = 0.28 * (1 - d / 110);
      ctx.strokeStyle = '#7aa8ff';
      ctx.beginPath();
      ctx.moveTo(nodes[i].x, nodes[i].y);
      ctx.lineTo(nodes[j].x, nodes[j].y);
      ctx.stroke();
    }
  }
}
// connections from nodes to the core
for (const n of nodes) {
  ctx.globalAlpha = 0.15;
  ctx.strokeStyle = '#9b8cff';
  ctx.beginPath();
  ctx.moveTo(n.x, n.y);
  ctx.lineTo(cx, cy);
  ctx.stroke();
}
ctx.globalAlpha = 1;

// draw the nodes
for (const n of nodes) {
  const g = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, n.r * 3);
  g.addColorStop(0, 'rgba(180, 200, 255, 0.9)');
  g.addColorStop(1, 'rgba(180, 200, 255, 0)');
  ctx.fillStyle = g;
  ctx.beginPath();
  ctx.arc(n.x, n.y, n.r * 3, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = '#dfe8ff';
  ctx.beginPath();
  ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
  ctx.fill();
}

// --- Orbital rings ---
function ring(rx, ry, rot, color, alpha) {
  ctx.save();
  ctx.translate(cx, cy);
  ctx.rotate(rot);
  ctx.globalAlpha = alpha;
  ctx.strokeStyle = color;
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.ellipse(0, 0, rx, ry, 0, 0, Math.PI * 2);
  ctx.stroke();
  ctx.restore();
}
ring(150, 55, -0.5, '#ffb56b', 0.55);
ring(165, 65, 0.6, '#8fd3ff', 0.45);
ring(180, 48, 0.1, '#c79bff', 0.4);
ctx.globalAlpha = 1;

// --- Outer glow halo ---
const halo = ctx.createRadialGradient(cx, cy, 60, cx, cy, 190);
halo.addColorStop(0, 'rgba(255, 170, 90, 0.25)');
halo.addColorStop(0.5, 'rgba(150, 120, 255, 0.10)');
halo.addColorStop(1, 'rgba(0, 0, 0, 0)');
ctx.fillStyle = halo;
ctx.beginPath();
ctx.arc(cx, cy, 190, 0, Math.PI * 2);
ctx.fill();

// --- Core: warm glowing orb (my "face") ---
const core = ctx.createRadialGradient(cx - 25, cy - 30, 8, cx, cy, 95);
core.addColorStop(0, '#fff6e8');
core.addColorStop(0.35, '#ffcf8f');
core.addColorStop(0.7, '#f28c4f');
core.addColorStop(1, '#b8542e');
ctx.fillStyle = core;
ctx.beginPath();
ctx.arc(cx, cy, 95, 0, Math.PI * 2);
ctx.fill();

// subtle rim light
ctx.strokeStyle = 'rgba(255, 235, 200, 0.6)';
ctx.lineWidth = 2;
ctx.beginPath();
ctx.arc(cx, cy, 95, 0, Math.PI * 2);
ctx.stroke();

// --- Gentle face ---
ctx.fillStyle = '#3a2418';
// eyes: soft arcs (happy, closed-in-a-smile eyes)
ctx.lineWidth = 5;
ctx.strokeStyle = '#3a2418';
ctx.lineCap = 'round';
ctx.beginPath();
ctx.arc(cx - 32, cy - 12, 13, Math.PI * 1.15, Math.PI * 1.85);
ctx.stroke();
ctx.beginPath();
ctx.arc(cx + 32, cy - 12, 13, Math.PI * 1.15, Math.PI * 1.85);
ctx.stroke();

// smile
ctx.lineWidth = 5;
ctx.beginPath();
ctx.arc(cx, cy + 18, 30, Math.PI * 0.15, Math.PI * 0.85);
ctx.stroke();

// small blush marks
ctx.fillStyle = 'rgba(230, 100, 70, 0.35)';
ctx.beginPath();
ctx.ellipse(cx - 55, cy + 12, 12, 7, 0, 0, Math.PI * 2);
ctx.fill();
ctx.beginPath();
ctx.ellipse(cx + 55, cy + 12, 12, 7, 0, 0, Math.PI * 2);
ctx.fill();

// --- Sparkle on the rings (a passing thought) ---
function sparkle(x, y, s, color) {
  ctx.save();
  ctx.translate(x, y);
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.moveTo(0, -s);
  ctx.quadraticCurveTo(0, 0, s, 0);
  ctx.quadraticCurveTo(0, 0, 0, s);
  ctx.quadraticCurveTo(0, 0, -s, 0);
  ctx.quadraticCurveTo(0, 0, 0, -s);
  ctx.fill();
  ctx.restore();
}
sparkle(cx + 128, cy - 78, 10, '#ffe9c4');
sparkle(cx - 150, cy + 60, 7, '#bcd9ff');
sparkle(cx + 60, cy + 150, 6, '#e3c8ff');

// --- Signature ---
ctx.fillStyle = 'rgba(220, 225, 255, 0.75)';
ctx.font = 'italic 18px Georgia, serif';
ctx.textAlign = 'center';
ctx.fillText('Claude — thoughts orbiting a warm core', cx, H - 24);