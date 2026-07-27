const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

// Background
const grad = ctx.createLinearGradient(0, 0, 0, 500);
grad.addColorStop(0, "#2c3e50");
grad.addColorStop(1, "#4ca1af");
ctx.fillStyle = grad;
ctx.fillRect(0, 0, 500, 500);

// Since I'm an AI, my "self-portrait" is a friendly robot face
// Body / shoulders
ctx.fillStyle = "#7f8c8d";
ctx.beginPath();
ctx.moveTo(120, 500);
ctx.quadraticCurveTo(250, 380, 380, 500);
ctx.fill();

// Neck
ctx.fillStyle = "#95a5a6";
ctx.fillRect(225, 350, 50, 60);

// Head
ctx.fillStyle = "#bdc3c7";
ctx.strokeStyle = "#7f8c8d";
ctx.lineWidth = 4;
ctx.beginPath();
ctx.roundRect(140, 130, 220, 230, 40);
ctx.fill();
ctx.stroke();

// Antenna
ctx.strokeStyle = "#95a5a6";
ctx.lineWidth = 6;
ctx.beginPath();
ctx.moveTo(250, 130);
ctx.lineTo(250, 90);
ctx.stroke();
ctx.fillStyle = "#e74c3c";
ctx.beginPath();
ctx.arc(250, 80, 12, 0, Math.PI * 2);
ctx.fill();

// Face screen
ctx.fillStyle = "#1a2634";
ctx.beginPath();
ctx.roundRect(165, 165, 170, 130, 20);
ctx.fill();

// Eyes (glowing)
ctx.fillStyle = "#00e5ff";
ctx.shadowColor = "#00e5ff";
ctx.shadowBlur = 20;
ctx.beginPath();
ctx.arc(210, 210, 22, 0, Math.PI * 2);
ctx.arc(290, 210, 22, 0, Math.PI * 2);
ctx.fill();

// Pupils
ctx.shadowBlur = 0;
ctx.fillStyle = "#003";
ctx.beginPath();
ctx.arc(214, 212, 8, 0, Math.PI * 2);
ctx.arc(294, 212, 8, 0, Math.PI * 2);
ctx.fill();

// Smile (pixel-style mouth)
ctx.fillStyle = "#00e5ff";
ctx.shadowColor = "#00e5ff";
ctx.shadowBlur = 15;
for (let i = 0; i < 7; i++) {
  const x = 200 + i * 15;
  const y = 260 + Math.sin(i / 6 * Math.PI) * 10;
  ctx.fillRect(x, y, 12, 12);
}
ctx.shadowBlur = 0;

// Ears / side panels
ctx.fillStyle = "#95a5a6";
ctx.beginPath();
ctx.roundRect(120, 200, 25, 60, 8);
ctx.roundRect(355, 200, 25, 60, 8);
ctx.fill();

// Bolts
ctx.fillStyle = "#7f8c8d";
[[160,150],[340,150],[160,340],[340,340]].forEach(p => {
  ctx.beginPath();
  ctx.arc(p[0], p[1], 6, 0, Math.PI * 2);
  ctx.fill();
});