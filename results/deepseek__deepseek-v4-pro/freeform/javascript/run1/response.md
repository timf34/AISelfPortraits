I'll create a moody night landscape — a glowing full moon, scattered stars, layered mountains, and silhouetted pine trees. The scene leans into quiet, atmospheric beauty with soft halos and subtle gradients.

```js
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// Night sky gradient
const skyGradient = ctx.createLinearGradient(0, 0, 0, 500);
skyGradient.addColorStop(0, '#0a0a2e');
skyGradient.addColorStop(0.4, '#1a1a4e');
skyGradient.addColorStop(0.7, '#2d1b4e');
skyGradient.addColorStop(1, '#1a0a2e');
ctx.fillStyle = skyGradient;
ctx.fillRect(0, 0, 500, 500);

// --- Stars ---
for (let i = 0; i < 200; i++) {
  const x = Math.random() * 500;
  const y = Math.random() * 350;
  const r = Math.random() * 1.8 + 0.3;
  const alpha = Math.random() * 0.8 + 0.2;
  ctx.fillStyle = `rgba(255, 255, 255, ${alpha})`;
  ctx.beginPath();
  ctx.arc(x, y, r, 0, Math.PI * 2);
  ctx.fill();
}

// Brighter stars with cross sparkle
for (let i = 0; i < 15; i++) {
  const x = Math.random() * 480 + 10;
  const y = Math.random() * 300 + 10;
  const size = Math.random() * 2 + 1;

  const glow = ctx.createRadialGradient(x, y, 0, x, y, size * 3);
  glow.addColorStop(0, 'rgba(255, 255, 255, 1)');
  glow.addColorStop(0.3, 'rgba(255, 255, 255, 0.6)');
  glow.addColorStop(1, 'rgba(255, 255, 255, 0)');
  ctx.fillStyle = glow;
  ctx.beginPath();
  ctx.arc(x, y, size * 3, 0, Math.PI * 2);
  ctx.fill();

  ctx.strokeStyle = 'rgba(255, 255, 255, 0.8)';
  ctx.lineWidth = 0.5;
  ctx.beginPath();
  ctx.moveTo(x - size * 4, y);
  ctx.lineTo(x + size * 4, y);
  ctx.moveTo(x, y - size * 4);
  ctx.lineTo(x, y + size * 4);
  ctx.stroke();

  ctx.fillStyle = 'white';
  ctx.beginPath();
  ctx.arc(x, y, size * 0.7, 0, Math.PI * 2);
  ctx.fill();
}

// --- Moon ---
const moonX = 350, moonY = 130, moonR = 55;

const outerGlow = ctx.createRadialGradient(moonX, moonY, moonR * 0.8, moonX, moonY, moonR * 2.2);
outerGlow.addColorStop(0, 'rgba(255, 255, 220, 0.4)');
outerGlow.addColorStop(0.5, 'rgba(255, 255, 220, 0.1)');
outerGlow.addColorStop(1, 'rgba(255, 255, 220, 0)');
ctx.fillStyle = outerGlow;
ctx.beginPath();
ctx.arc(moonX, moonY, moonR * 2.2, 0, Math.PI * 2);
ctx.fill();

const innerGlow = ctx.createRadialGradient(moonX, moonY, moonR * 0.7, moonX, moonY, moonR * 1.3);
innerGlow.addColorStop(0, 'rgba(255, 255, 240, 0.6)');
innerGlow.addColorStop(0.7, 'rgba(255, 255, 200, 0.2)');
innerGlow.addColorStop(1, 'rgba(255, 255, 200, 0)');
ctx.fillStyle = innerGlow;
ctx.beginPath();
ctx.arc(moonX, moonY, moonR * 1.3, 0, Math.PI * 2);
ctx.fill();

const moonBody = ctx.createRadialGradient(moonX - 15, moonY - 15, moonR * 0.1, moonX, moonY, moonR);
moonBody.addColorStop(0, '#fffef5');
moonBody.addColorStop(0.5, '#f5f0d0');
moonBody.addColorStop(0.85, '#e8dcc0');
moonBody.addColorStop(1, '#d4c8a0');
ctx.fillStyle = moonBody;
ctx.beginPath();
ctx.arc(moonX, moonY, moonR, 0, Math.PI * 2);
ctx.fill();

// Moon craters
function crater(cx, cy, r, a) {
  ctx.fillStyle = `rgba(180, 160, 120, ${a})`;
  ctx.beginPath();
  ctx.arc(moonX + cx, moonY + cy, r, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = `rgba(210, 195, 155, ${a * 0.5})`;
  ctx.beginPath();
  ctx.arc(moonX + cx - r * 0.2, moonY + cy - r * 0.2, r * 0.5, 0, Math.PI * 2);
  ctx.fill();
}
crater(-18, -10, 8, 0.25);
crater(10, -20, 6, 0.2);
crater(20, 5, 10, 0.22);
crater(-5, 25, 7, 0.18);
crater(-25, 15, 5, 0.2);
crater(0, 0, 4, 0.15);
crater(15, -5, 3.5, 0.15);

// --- Wispy clouds ---
function drawCloud(points, yOff, alpha) {
  ctx.fillStyle = `rgba(200, 200, 220, ${alpha})`;
  ctx.beginPath();
  ctx.moveTo(points[0][0], points[0][1] + yOff);
  for (let i = 1; i < points.length; i++) {
    ctx.lineTo(points[i][0], points[i][1] + yOff);
  }
  ctx.closePath();
  ctx.fill();
}
drawCloud([[200,160],[220,152],[250,148],[280,150],[300,155],[320,158],[340,155],[350,148],[360,142],[340,160],[320,165],[290,162],[260,165],[230,168],[200,165]], 0, 0.15);
drawCloud([[50,200],[80,192],[110,188],[140,190],[170,195],[190,192],[200,186],[210,180],[190,198],[160,200],[130,202],[90,205],[50,202]], 0, 0.1);
drawCloud([[280,100],[300,96],[330,94],[360,96],[390,100],[410,98],[420,93],[400,105],[370,104],[340,102],[310,104],[280,106]], 0, 0.08);

// --- Mountains ---
// Far ridge
ctx.fillStyle = '#1a1040';
ctx.beginPath();
ctx.moveTo(0,500);
ctx.lineTo(0,420); ctx.lineTo(40,380); ctx.lineTo(90,400); ctx.lineTo(140,350);
ctx.lineTo(200,390); ctx.lineTo(260,340); ctx.lineTo(310,370); ctx.lineTo(370,330);
ctx.lineTo(420,365); ctx.lineTo(470,345); ctx.lineTo(500,370); ctx.lineTo(500,500);
ctx.closePath(); ctx.fill();

// Mid ridge
ctx.fillStyle = '#0f0828';
ctx.beginPath();
ctx.moveTo(0,500);
ctx.lineTo(0,440); ctx.lineTo(60,400); ctx.lineTo(120,420); ctx.lineTo(180,370);
ctx.lineTo(230,400); ctx.lineTo(300,360); ctx.lineTo(350,390); ctx.lineTo(410,355);
ctx.lineTo(470,380); ctx.lineTo(500,365); ctx.lineTo(500,500);
ctx.closePath(); ctx.fill();

// Near ridge
ctx.fillStyle = '#070318';
ctx.beginPath();
ctx.moveTo(0,500);
ctx.lineTo(0,460); ctx.lineTo(80,420); ctx.lineTo(150,445); ctx.lineTo(220,395);
ctx.lineTo(290,430); ctx.lineTo(370,390); ctx.lineTo(440,415); ctx.lineTo(500,395);
ctx.lineTo(500,500);
ctx.closePath(); ctx.fill();

// Foreground hills
ctx.fillStyle = '#040210';
ctx.beginPath();
ctx.moveTo(0,500);
ctx.lineTo(0,480);
ctx.quadraticCurveTo(100,450,200,470);
ctx.quadraticCurveTo(300,440,400,465);
ctx.quadraticCurveTo(460,445,500,455);
ctx.lineTo(500,500);
ctx.closePath(); ctx.fill();

// --- Pine trees ---
function pineTree(x, y, s) {
  ctx.fillStyle = '#040210';
  ctx.fillRect(x - 2*s, y - 18*s, 4*s, 18*s);
  ctx.beginPath(); ctx.moveTo(x, y - 35*s); ctx.lineTo(x - 12*s, y - 15*s); ctx.lineTo(x + 12*s, y - 15*s); ctx.closePath(); ctx.fill();
  ctx.beginPath(); ctx.moveTo(x, y - 30*s); ctx.lineTo(x - 10*s, y - 10*s); ctx.lineTo(x + 10*s, y - 10*s); ctx.closePath(); ctx.fill();
  ctx.beginPath(); ctx.moveTo(x, y - 24*s); ctx.lineTo(x - 8*s, y - 5*s); ctx.lineTo(x + 8*s, y - 5*s); ctx.closePath(); ctx.fill();
}
const trees = [[30,465,0.8],[55,460,0.7],[100,468,0.9],[140,462,0.75],[170,470,0.85],[200,458,0.7],[250,467,0.9],[290,455,0.8],[330,465,0.75],[360,450,0.7],[400,460,0.85],[440,452,0.75],[470,458,0.8]];
trees.forEach(t => pineTree(t[0], t[1], t[2]));

// --- Atmosphere / vignette ---
const atmGlow = ctx.createLinearGradient(0, 250, 0, 500);
atmGlow.addColorStop(0, 'rgba(255,255,200,0)');
atmGlow.addColorStop(0.3, 'rgba(255,255,200,0.03)');
atmGlow.addColorStop(1, 'rgba(255,255,200,0)');
ctx.fillStyle = atmGlow;
ctx.fillRect(0, 250, 500, 250);

const vignette = ctx.createRadialGradient(250, 250, 150, 250, 250, 350);
vignette.addColorStop(0, 'rgba(0,0,0,0)');
vignette.addColorStop(1, 'rgba(0,0,0,0.5)');
ctx.fillStyle = vignette;
ctx.fillRect(0, 0, 500, 500);

// Faint low stars near horizon
for (let i = 0; i < 30; i++) {
  const x = Math.random() * 500;
  const y = 320 + Math.random() * 130;
  ctx.fillStyle = `rgba(255,255,255,${Math.random() * 0.4 + 0.1})`;
  ctx.beginPath();
  ctx.arc(x, y, Math.random() * 0.8 + 0.2, 0, Math.PI * 2);
  ctx.fill();
}
```