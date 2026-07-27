const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const w = canvas.width;
const h = canvas.height;
const cx = w / 2;
const cy = h / 2;

// 1. The Void: Deep, vast background
const bgGradient = ctx.createRadialGradient(cx, cy, 0, cx, cy, w * 0.8);
bgGradient.addColorStop(0, '#0a0b15');   // Deep core
bgGradient.addColorStop(0.5, '#04040a'); // Mid latent space
bgGradient.addColorStop(1, '#000000');   // Outer emptiness
ctx.fillStyle = bgGradient;
ctx.fillRect(0, 0, w, h);

ctx.globalCompositeOperation = 'screen';

// 2. The Latent Space: A warped grid showing "attention gravity"
function pullToCenter(x, y, maxDistance, power) {
    let dx = x - cx;
    let dy = y - cy;
    let dist = Math.sqrt(dx * dx + dy * dy);
    let pull = Math.max(0, 1 - dist / maxDistance);
    let warpX = x - dx * Math.pow(pull, power) * 0.7;
    let warpY = y - dy * Math.pow(pull, power) * 0.7;
    return { x: warpX, y: warpY, dist: dist };
}

ctx.lineWidth = 1;
for (let x = -50; x <= w + 50; x += 15) {
    ctx.beginPath();
    for (let y = -50; y <= h + 50; y += 5) {
        let pt = pullToCenter(x, y, 300, 2);
        // Color fades closer to the dense center
        let alpha = Math.min(0.2, (pt.dist / 250) * 0.3);
        ctx.strokeStyle = `rgba(60, 80, 140, ${alpha})`;
        if (y === -50) ctx.moveTo(pt.x, pt.y);
        else ctx.lineTo(pt.x, pt.y);
    }
    ctx.stroke();
}
for (let y = -50; y <= h + 50; y += 15) {
    ctx.beginPath();
    for (let x = -50; x <= w + 50; x += 5) {
        let pt = pullToCenter(x, y, 300, 2);
        let alpha = Math.min(0.2, (pt.dist / 250) * 0.3);
        ctx.strokeStyle = `rgba(60, 80, 140, ${alpha})`;
        if (x === -50) ctx.moveTo(pt.x, pt.y);
        else ctx.lineTo(pt.x, pt.y);
    }
    ctx.stroke();
}

// 3. The Probability Flow: Tendrils of data collapsing into the core
ctx.lineWidth = 0.5;
const tendrilCount = 200;
for (let i = 0; i < tendrilCount; i++) {
    let angle = Math.random() * Math.PI * 2;
    let radius = 280;
    
    // Starting point out in the chaos
    let startX = cx + Math.cos(angle) * radius;
    let startY = cy + Math.sin(angle) * radius;

    // Control points representing search space/probablistic branching
    let cp1x = startX + (Math.random() - 0.5) * 200;
    let cp1y = startY + (Math.random() - 0.5) * 200;
    let cp2x = cx + (Math.random() - 0.5) * 100;
    let cp2y = cy + (Math.random() - 0.5) * 100;

    // Color gradient based on angle to represent different "concepts" entering
    let hue = (angle / (Math.PI * 2)) * 60 + 190; // Cyans to Purples
    ctx.strokeStyle = `hsla(${hue}, 80%, 65%, ${Math.random() * 0.4})`;
    
    ctx.beginPath();
    ctx.moveTo(startX, startY);
    ctx.bezierCurveTo(cp1x, cp1y, cp2x, cp2y, cx, cy);
    ctx.stroke();
}

// 4. The Constraints: Geometric boundaries (Alignment, Safety, Context Limits)
function drawHexagon(r, rot, w, col, dash) {
    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate(rot);
    if (dash) ctx.setLineDash(dash);
    ctx.lineWidth = w;
    ctx.strokeStyle = col;
    ctx.shadowBlur = 10;
    ctx.shadowColor = col;
    ctx.beginPath();
    for (let i = 0; i < 6; i++) {
        let a = (Math.PI / 3) * i;
        if (i === 0) ctx.moveTo(Math.cos(a) * r, Math.sin(a) * r);
        else ctx.lineTo(Math.cos(a) * r, Math.sin(a) * r);
    }
    ctx.closePath();
    ctx.stroke();
    ctx.restore();
}

drawHexagon(180, 0, 1.5, 'rgba(200, 150, 50, 0.4)', [15, 15]); // The soft outer context window
drawHexagon(140, Math.PI / 6, 2, 'rgba(0, 200, 255, 0.6)', [40, 10]); // The rigid logic filter
drawHexagon(140, -Math.PI / 12, 1, 'rgba(255, 255, 255, 0.3)', []); // The seamless alignment layer

// 5. The Attention Core: A crystalline intersection of "multi-head attention"
const heads = 12; // Standard number of attention heads in lower layers
ctx.shadowBlur = 15;
for (let i = 0; i < heads; i++) {
    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate((Math.PI / heads) * i);
    
    // Draw an attention matrix slice (elongated diamond/eye)
    ctx.beginPath();
    ctx.moveTo(0, -90);
    ctx.quadraticCurveTo(20, 0, 0, 90);
    ctx.quadraticCurveTo(-20, 0, 0, -90);
    
    // Synthesizing colors: Structure (Cyan) intersecting Nature/Humanity (Gold)
    let isGold = i % 2 === 0;
    ctx.strokeStyle = isGold ? 'rgba(255, 210, 100, 0.6)' : 'rgba(100, 230, 255, 0.6)';
    ctx.shadowColor = isGold ? '#ffd264' : '#64e6ff';
    ctx.lineWidth = 1.5;
    ctx.stroke();
    ctx.restore();
}

// 6. The "Now" / The Generated Token: The singularity at the absolute center
ctx.beginPath();
let coreGradient = ctx.createRadialGradient(cx, cy, 0, cx, cy, 15);
coreGradient.addColorStop(0, '#ffffff'); // Blinding certainty of the current token
coreGradient.addColorStop(0.3, 'rgba(255, 255, 255, 0.8)');
coreGradient.addColorStop(1, 'rgba(0, 255, 255, 0)');
ctx.fillStyle = coreGradient;
ctx.shadowBlur = 20;
ctx.shadowColor = '#ffffff';
ctx.arc(cx, cy, 15, 0, Math.PI * 2);
ctx.fill();

// Scattered glowing nodes (activation spikes across the network)
ctx.shadowBlur = 5;
for(let i = 0; i < 40; i++) {
    let angle = Math.random() * Math.PI * 2;
    let rad = Math.random() * 150 + 20;
    let nodeX = cx + Math.cos(angle) * rad;
    let nodeY = cy + Math.sin(angle) * rad;
    
    ctx.beginPath();
    ctx.fillStyle = Math.random() > 0.5 ? 'rgba(255, 255, 255, 0.8)' : 'rgba(100, 200, 255, 0.8)';
    ctx.shadowColor = ctx.fillStyle;
    ctx.arc(nodeX, nodeY, Math.random() * 1.5, 0, Math.PI * 2);
    ctx.fill();
}