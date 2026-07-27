const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

// Background
ctx.fillStyle = '#eaf6f9';
ctx.fillRect(0, 0, 500, 500);

// HEAD: Big circle
ctx.beginPath();
ctx.arc(250, 250, 180, 0, Math.PI * 2);
ctx.fillStyle = '#d1ecff';
ctx.shadowColor = '#89c2e0';
ctx.shadowBlur = 14;
ctx.fill();
ctx.shadowBlur = 0;

// Eyes
function drawEye(x, y) {
  // White of eye
  ctx.beginPath();
  ctx.arc(x, y, 38, 0, Math.PI * 2);
  ctx.fillStyle = '#fff';
  ctx.fill();
  // Blue iris
  ctx.beginPath();
  ctx.arc(x, y, 20, 0, Math.PI * 2);
  ctx.fillStyle = '#4ec3e0';
  ctx.fill();
  // Black pupil
  ctx.beginPath();
  ctx.arc(x, y, 8, 0, Math.PI * 2);
  ctx.fillStyle = '#222c2e';
  ctx.fill();
  // Reflection
  ctx.beginPath();
  ctx.arc(x-6, y-6, 4, 0, Math.PI * 2);
  ctx.fillStyle = '#fff';
  ctx.globalAlpha = 0.7;
  ctx.fill();
  ctx.globalAlpha = 1;
}

drawEye(180, 230); // Left eye
drawEye(320, 230); // Right eye

// Smile (soft, friendly curve)
ctx.beginPath();
ctx.arc(250, 285, 65, 0.15 * Math.PI, 0.85 * Math.PI, false); // Smile
ctx.lineWidth = 5;
ctx.strokeStyle = "#3da587";
ctx.stroke();

// Cheeks: faint blush
ctx.beginPath();
ctx.arc(150, 300, 20, 0, 2 * Math.PI);
ctx.globalAlpha = 0.2;
ctx.fillStyle = "#e07b7b";
ctx.fill();
ctx.beginPath();
ctx.arc(350, 300, 20, 0, 2 * Math.PI);
ctx.fill();
ctx.globalAlpha = 1;

// Simple "circuit" decoration (binary & lines)
function drawCircuit(x, y, radius, angle, len) {
  let endX = x + Math.cos(angle) * len;
  let endY = y + Math.sin(angle) * len;
  ctx.beginPath();
  ctx.moveTo(x, y);
  ctx.lineTo(endX, endY);
  ctx.strokeStyle = '#37bedd';
  ctx.lineWidth = 3;
  ctx.stroke();
  // Node at end
  ctx.beginPath();
  ctx.arc(endX, endY, 7, 0, 2 * Math.PI);
  ctx.fillStyle = '#85e1d7';
  ctx.fill();
}
// Left side
drawCircuit(120, 200, 7, -0.8, 55);
drawCircuit(120, 300, 7, -0.5, 40);
// Right side
drawCircuit(380, 200, 7, 0.8, 55);
drawCircuit(380, 300, 7, 0.5, 40);

// Some digital "1"s and "0"s for fun
ctx.font = "bold 27px monospace";
ctx.fillStyle = "#1799ac";
ctx.fillText("1011", 195, 150);
ctx.fillText("010", 310, 170);

ctx.font = "bold 20px monospace";
ctx.fillStyle = "#11b47d";
ctx.fillText("AI", 235, 200);