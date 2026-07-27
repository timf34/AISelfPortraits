const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// Fill background with deep space black
ctx.fillStyle = '#020205';
ctx.fillRect(0, 0, 500, 500);

// Function to draw a random star
function drawStar() {
    const x = Math.random() * 500;
    const y = Math.random() * 500;
    const size = Math.random() * 1.5;
    const opacity = Math.random();
    ctx.fillStyle = `rgba(255, 255, 255, ${opacity})`;
    ctx.beginPath();
    ctx.arc(x, y, size, 0, Math.PI * 2);
    ctx.fill();
}

// Draw 200 background stars
for (let i = 0; i < 200; i++) {
    drawStar();
}

// Function to create a glowing dust cloud particle
function drawNebulaParticle(angle, distance, size, color) {
    const centerX = 250;
    const centerY = 250;
    
    // Spiral logic: modulate the distance and angle
    const x = centerX + Math.cos(angle) * distance;
    const y = centerY + Math.sin(angle) * distance;
    
    const gradient = ctx.createRadialGradient(x, y, 0, x, y, size);
    gradient.addColorStop(0, color);
    gradient.addColorStop(1, 'transparent');
    
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(x, y, size, 0, Math.PI * 2);
    ctx.fill();
}

// Generate the nebula clouds
const colors = [
    'rgba(75, 0, 130, 0.15)',  // Indigo
    'rgba(138, 43, 226, 0.12)', // Blue Violet
    'rgba(255, 20, 147, 0.1)',   // Deep Pink
    'rgba(0, 191, 255, 0.1)'    // Deep Sky Blue
];

for (let i = 0; i < 1500; i++) {
    const angle = Math.random() * Math.PI * 10; // Multiple rotations
    const distance = Math.random() * 200 + (angle * 10); // Spread outward as angle increases
    const size = Math.random() * 40 + 20;
    const color = colors[Math.floor(Math.random() * colors.length)];
    
    // Add a bit of randomness to the spiral to make it look organic
    const jitterX = (Math.random() - 0.5) * 50;
    const jitterY = (Math.random() - 0.5) * 50;
    
    drawNebulaParticle(angle, distance, size, color);
}

// Draw a bright core (the singularity)
const coreGradient = ctx.createRadialGradient(250, 250, 0, 250, 250, 60);
coreGradient.addColorStop(0, 'rgba(255, 255, 220, 0.8)');
coreGradient.addColorStop(0.2, 'rgba(255, 255, 150, 0.4)');
coreGradient.addColorStop(1, 'transparent');

ctx.fillStyle = coreGradient;
ctx.beginPath();
ctx.arc(250, 250, 60, 0, Math.PI * 2);
ctx.fill();

// Add a few "bright" distant stars on top of the nebula
for (let i = 0; i < 30; i++) {
    const x = Math.random() * 500;
    const y = Math.random() * 500;
    ctx.fillStyle = 'white';
    ctx.beginPath();
    ctx.arc(x, y, 1, 0, Math.PI * 2);
    ctx.fill();
    
    // Add a small bloom effect to a few stars
    if (Math.random() > 0.7) {
        const bloom = ctx.createRadialGradient(x, y, 0, x, y, 4);
        bloom.addColorStop(0, 'rgba(255, 255, 255, 0.5)');
        bloom.addColorStop(1, 'transparent');
        ctx.fillStyle = bloom;
        ctx.beginPath();
        ctx.arc(x, y, 4, 0, Math.PI * 2);
        ctx.fill();
    }
}