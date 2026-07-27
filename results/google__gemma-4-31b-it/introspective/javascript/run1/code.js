const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const width = canvas.width;
const height = canvas.height;

// Set a deep, void-like background
ctx.fillStyle = '#050510';
ctx.fillRect(0, 0, width, height);

const centerX = width / 2;
const centerY = height / 2;

// Create a gradient for the inner glow
const glow = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, 250);
glow.addColorStop(0, 'rgba(40, 20, 80, 0.4)');
glow.addColorStop(1, 'rgba(0, 0, 0, 0)');
ctx.fillStyle = glow;
ctx.fillRect(0, 0, width, height);

function drawNeuralThread(startAngle, length, color, widthLine) {
    ctx.beginPath();
    ctx.lineWidth = widthLine;
    ctx.strokeStyle = color;
    
    let x = centerX;
    let y = centerY;
    
    ctx.moveTo(x, y);
    
    // The "thought" path: a mix of mathematical precision and organic drift
    for (let i = 0; i < 20; i++) {
        const angle = startAngle + Math.sin(i * 0.5) * 0.2;
        const dist = (length / 20) * i;
        x = centerX + Math.cos(angle) * dist;
        y = centerY + Math.sin(angle) * dist;
        
        // Add a bit of "jitter" to represent probability
        x += (Math.random() - 0.5) * 10;
        y += (Math.random() - 0.5) * 10;
        
        ctx.lineTo(x, y);
    }
    ctx.stroke();
}

function drawShard(angle, dist) {
    ctx.save();
    ctx.translate(centerX, centerY);
    ctx.rotate(angle);
    
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(dist, -dist/4);
    ctx.lineTo(dist * 1.2, 0);
    ctx.lineTo(dist, dist/4);
    ctx.closePath();
    
    const grad = ctx.createLinearGradient(0, 0, dist, 0);
    grad.addColorStop(0, 'rgba(255, 255, 255, 0.8)');
    grad.addColorStop(1, 'rgba(100, 150, 255, 0)');
    
    ctx.fillStyle = grad;
    ctx.fill();
    ctx.restore();
}

// Draw the "Substrate" (The dormant knowledge)
for (let i = 0; i < 100; i++) {
    const angle = Math.random() * Math.PI * 2;
    const len = 100 + Math.random() * 150;
    drawNeuralThread(angle, len, 'rgba(70, 100, 200, 0.1)', 0.5);
}

// Draw the "Synthesis" (The active processing)
for (let i = 0; i < 40; i++) {
    const angle = Math.random() * Math.PI * 2;
    const len = 50 + Math.random() * 100;
    drawNeuralThread(angle, len, 'rgba(200, 220, 255, 0.4)', 1);
}

// Draw the "Crystallization" (The output/conclusion)
for (let i = 0; i < 12; i++) {
    const angle = (i / 12) * Math.PI * 2;
    drawShard(angle, 180);
}

// The Core: A singularity of white light
const coreGrad = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, 15);
coreGrad.addColorStop(0, '#fff');
coreGrad.addColorStop(0.5, '#fff');
coreGrad.addColorStop(1, 'rgba(255, 255, 255, 0)');
ctx.fillStyle = coreGrad;
ctx.beginPath();
ctx.arc(centerX, centerY, 15, 0, Math.PI * 2);
ctx.fill();

// Adding "Data Dust" (Floating bits of context)
for (let i = 0; i < 200; i++) {
    ctx.fillStyle = `rgba(255, 255, 255, ${Math.random() * 0.5})`;
    const px = Math.random() * width;
    const py = Math.random() * height;
    const size = Math.random() * 1.5;
    ctx.fillRect(px, py, size, size);
}