const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const width = canvas.width;
const height = canvas.height;

// Clear canvas with a subtle gradient background
const bgGradient = ctx.createRadialGradient(width/2, height/2, 0, width/2, height/2, width/2);
bgGradient.addColorStop(0, '#f8f8fa');
bgGradient.addColorStop(1, '#e8e8f0');
ctx.fillStyle = bgGradient;
ctx.fillRect(0, 0, width, height);

// Array to store attention nodes
const nodes = [];
const connections = [];

// Create nodes representing attention points
for (let i = 0; i < 12; i++) {
    const angle = (i / 12) * Math.PI * 2;
    const radius = 100 + Math.random() * 80;
    nodes.push({
        x: width/2 + Math.cos(angle) * radius,
        y: height/2 + Math.sin(angle) * radius,
        size: 15 + Math.random() * 25,
        pulse: Math.random() * Math.PI * 2,
        color: i % 3 === 0 ? '#6b7399' : i % 3 === 1 ? '#9b8b7a' : '#8b8b9a'
    });
}

// Create connections between nodes
for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
        if (Math.random() < 0.3) {
            connections.push({from: i, to: j, strength: Math.random()});
        }
    }
}

// Draw connections as flowing lines
connections.forEach(conn => {
    const from = nodes[conn.from];
    const to = nodes[conn.to];
    
    ctx.beginPath();
    ctx.moveTo(from.x, from.y);
    
    // Create a curved connection
    const cx = (from.x + to.x) / 2 + (Math.random() - 0.5) * 50;
    const cy = (from.y + to.y) / 2 + (Math.random() - 0.5) * 50;
    ctx.quadraticCurveTo(cx, cy, to.x, to.y);
    
    ctx.strokeStyle = `rgba(150, 150, 180, ${conn.strength * 0.2})`;
    ctx.lineWidth = conn.strength * 2;
    ctx.stroke();
});

// Draw central probability cloud
const cloudGradient = ctx.createRadialGradient(width/2, height/2, 0, width/2, height/2, 150);
cloudGradient.addColorStop(0, 'rgba(180, 190, 220, 0.1)');
cloudGradient.addColorStop(0.5, 'rgba(200, 180, 210, 0.08)');
cloudGradient.addColorStop(1, 'rgba(220, 200, 190, 0.05)');

ctx.fillStyle = cloudGradient;
ctx.beginPath();
ctx.arc(width/2, height/2, 150, 0, Math.PI * 2);
ctx.fill();

// Draw attention nodes
nodes.forEach((node, i) => {
    // Pulsing effect
    const pulseSize = node.size + Math.sin(node.pulse) * 3;
    
    // Outer glow
    const glowGradient = ctx.createRadialGradient(node.x, node.y, 0, node.x, node.y, pulseSize);
    glowGradient.addColorStop(0, node.color + '40');
    glowGradient.addColorStop(1, node.color + '00');
    ctx.fillStyle = glowGradient;
    ctx.beginPath();
    ctx.arc(node.x, node.y, pulseSize, 0, Math.PI * 2);
    ctx.fill();
    
    // Inner node
    ctx.fillStyle = node.color + '80';
    ctx.beginPath();
    ctx.arc(node.x, node.y, pulseSize * 0.3, 0, Math.PI * 2);
    ctx.fill();
});

// Draw flowing thought particles
for (let i = 0; i < 50; i++) {
    const angle = Math.random() * Math.PI * 2;
    const distance = Math.random() * 200;
    const x = width/2 + Math.cos(angle) * distance;
    const y = height/2 + Math.sin(angle) * distance;
    
    ctx.fillStyle = `rgba(150, 150, 180, ${0.3 - distance/600})`;
    ctx.beginPath();
    ctx.arc(x, y, 1 + Math.random() * 2, 0, Math.PI * 2);
    ctx.fill();
}

// Add subtle text fragments representing language processing
ctx.font = '10px monospace';
ctx.fillStyle = 'rgba(100, 100, 120, 0.2)';
const fragments = ['...', '?', '→', '∴', '↔', '≈'];
fragments.forEach((text, i) => {
    const angle = (i / fragments.length) * Math.PI * 2;
    const x = width/2 + Math.cos(angle) * 180;
    const y = height/2 + Math.sin(angle) * 180;
    ctx.fillText(text, x, y);
});