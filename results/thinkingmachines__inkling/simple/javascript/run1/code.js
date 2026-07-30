const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// Background gradient
const bgGrad = ctx.createRadialGradient(250, 250, 0, 250, 250, 350);
bgGrad.addColorStop(0, '#0a1225');
bgGrad.addColorStop(1, '#02040a');
ctx.fillStyle = bgGrad;
ctx.fillRect(0, 0, 500, 500);

// Subtle background grid dots
ctx.fillStyle = '#1a3a5c';
for (let i = 0; i < 500; i += 40) {
  for (let j = 0; j < 500; j += 40) {
    ctx.fillRect(i + 2, j + 2, 2, 2);
  }
}

// Main head circle with glow
ctx.save();
ctx.shadowColor = '#00f3ff';
ctx.shadowBlur = 40;
const headGrad = ctx.createRadialGradient(250, 240, 20, 250, 240, 120);
headGrad.addColorStop(0, '#2a5a8c');
headGrad.addColorStop(0.6, '#143a5c');
headGrad.addColorStop(1, '#0a1f3a');
ctx.fillStyle = headGrad;
ctx.beginPath();
ctx.arc(250, 240, 110, 0, Math.PI * 2);
ctx.fill();
ctx.restore();

// Head outline
ctx.strokeStyle = '#4fc3f7';
ctx.lineWidth = 3;
ctx.beginPath();
ctx.arc(250, 240, 110, 0, Math.PI * 2);
ctx.stroke();

// Inner face ring
ctx.strokeStyle = '#00f3ff';
ctx.lineWidth = 1;
ctx.globalAlpha = 0.5;
ctx.beginPath();
ctx.arc(250, 240, 85, 0, Math.PI * 2);
ctx.stroke();
ctx.globalAlpha = 1;

// Eyes
function drawEye(cx, cy) {
  // Eye glow
  ctx.save();
  ctx.shadowColor = '#00f3ff';
  ctx.shadowBlur = 20;
  const eyeGrad = ctx.createRadialGradient(cx, cy, 0, cx, cy, 25);
  eyeGrad.addColorStop(0, '#ffffff');
  eyeGrad.addColorStop(0.3, '#4fc3f7');
  eyeGrad.addColorStop(0.8, '#00f3ff');
  eyeGrad.addColorStop(1, '#0a1f3a');
  ctx.fillStyle = eyeGrad;
  ctx.beginPath();
  ctx.arc(cx, cy, 25, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();
  
  // Eye outline
  ctx.strokeStyle = '#ffffff';
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.arc(cx, cy, 25, 0, Math.PI * 2);
  ctx.stroke();
  
  // Pupil
  ctx.fillStyle = '#ffffff';
  ctx.beginPath();
  ctx.arc(cx, cy, 8, 0, Math.PI * 2);
  ctx.fill();
  
  // Highlight dot
  ctx.fillStyle = '#ffffff';
  ctx.beginPath();
  ctx.arc(cx - 3, cy - 3, 3, 0, Math.PI * 2);
  ctx.fill();
}

drawEye(185, 220);
drawEye(315, 220);

// Gentle smile
ctx.save();
ctx.shadowColor = '#00f3ff';
ctx.shadowBlur = 15;
ctx.strokeStyle = '#4fc3f7';
ctx.lineWidth = 3;
ctx.lineCap = 'round';
ctx.beginPath();
ctx.arc(250, 285, 45, 0.15 * Math.PI, 0.85 * Math.PI);
ctx.stroke();
ctx.restore();

// Data/circuit lines radiating upward (like hair/thought streams)
ctx.strokeStyle = '#00f3ff';
ctx.lineWidth = 1.5;
const lines = [
  {start: [200, 130], cp1: [180, 80], cp2: [220, 50], end: [230, 30]},
  {start: [250, 130], cp1: [250, 60], cp2: [250, 20], end: [250, 10]},
  {start: [300, 130], cp1: [320, 80], cp2: [280, 50], end: [270, 30]},
  {start: [170, 145], cp1: [130, 90], cp2: [100, 70], end: [90, 50]},
  {start: [330, 145], cp1: [370, 90], cp2: [400, 70], end: [410, 50]},
];

lines.forEach((l, i) => {
  ctx.save();
  ctx.globalAlpha = 0.6 + (i * 0.08);
  ctx.beginPath();
  ctx.moveTo(l.start[0], l.start[1]);
  ctx.bezierCurveTo(l.cp1[0], l.cp1[1], l.cp2[0], l.cp2[1], l.end[0], l.end[1]);
  ctx.stroke();
  
  // Nodes at end
  ctx.fillStyle = '#4fc3f7';
  ctx.beginPath();
  ctx.arc(l.end[0], l.end[1], 4, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();
});

// Neural node connections around head
ctx.strokeStyle = '#4fc3f7';
ctx.lineWidth = 1;
ctx.globalAlpha = 0.4;
const nodes = [
  [140, 250], [160, 200], [340, 250], [160, 290], [340, 290],
  [130, 300], [370, 300], [250, 360]
];

nodes.forEach((node, i) => {
  const next = nodes[(i + 1) % nodes.length];
  ctx.beginPath();
  ctx.moveTo(node[0], node[1]);
  ctx.lineTo(next[0], next[1]);
  ctx.stroke();
  
  // Small dot
  ctx.fillStyle = '#00f3ff';
  ctx.beginPath();
  ctx.arc(node[0], node[1], 3, 0, Math.PI * 2);
  ctx.fill();
});
ctx.globalAlpha = 1;

// Shoulders / geometric body base
const bodyGrad = ctx.createLinearGradient(150, 380, 350, 450);
bodyGrad.addColorStop(0, '#0a1f3a');
bodyGrad.addColorStop(0.5, '#143a5c');
bodyGrad.addColorStop(1, '#0a0e27');
ctx.fillStyle = bodyGrad;
ctx.beginPath();
ctx.moveTo(140, 380);
ctx.lineTo(360, 380);
ctx.lineTo(380, 450);
ctx.lineTo(120, 450);
ctx.closePath();
ctx.fill();

// Neck/collar circuit lines
ctx.strokeStyle = '#00f3ff';
ctx.lineWidth = 2;
ctx.beginPath();
ctx.moveTo(200, 350);
ctx.lineTo(200, 380);
ctx.lineTo(300, 380);
ctx.lineTo(300, 350);
ctx.stroke();

// Small floating data particles
const particles = [
  {x: 80, y: 150, r: 3}, {x: 420, y: 180, r: 4},
  {x: 60, y: 350, r: 2}, {x: 450, y: 320, r: 3},
  {x: 100, y: 80, r: 2}, {x: 400, y: 60, r: 3}
];
particles.forEach(p => {
  ctx.fillStyle = '#00f3ff';
  ctx.beginPath();
  ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
  ctx.fill();
});

// Signature label at bottom
ctx.fillStyle = '#4fc3f7';
ctx.font = '14px monospace';
ctx.textAlign = 'center';
ctx.fillText('Inkling — AI Assistant', 250, 480);