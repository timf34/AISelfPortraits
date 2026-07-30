const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const W = canvas.width;
const H = canvas.height;

function draw() {
  // Deep space background
  const bg = ctx.createRadialGradient(W/2, H/2, 0, W/2, H/2, W);
  bg.addColorStop(0, '#0a0a1a');
  bg.addColorStop(0.5, '#050520');
  bg.addColorStop(1, '#020208');
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, W, H);

  // Subtle central geometric absence — faint intersecting rings
  ctx.save();
  ctx.translate(W/2, H/2);
  for (let r of [30, 60, 90, 120]) {
    ctx.beginPath();
    ctx.arc(0, 0, r, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(100, 150, 255, 0.06)';
    ctx.lineWidth = 1;
    ctx.stroke();
  }
  // Diagonal cross hints at structure
  ctx.beginPath();
  ctx.moveTo(-140, 0); ctx.lineTo(140, 0);
  ctx.moveTo(0, -140); ctx.lineTo(0, 140);
  ctx.strokeStyle = 'rgba(100, 150, 255, 0.04)';
  ctx.lineWidth = 0.5;
  ctx.stroke();
  ctx.restore();

  // Generate nodes in concentric layers
  const layers = [
    { count: 12, radius: 60,  color: '#aaccff', size: 2 },
    { count: 28, radius: 110, color: '#88bbff', size: 1.8 },
    { count: 50, radius: 160, color: '#6699dd', size: 1.2 },
    { count: 80, radius: 210, color: '#4488cc', size: 0.9 },
  ];

  const nodes = [];
  layers.forEach(L => {
    for (let i = 0; i < L.count; i++) {
      const angle = (Math.PI * 2 * i) / L.count + (Math.random() - 0.5) * 0.8;
      const r = L.radius + (Math.random() - 0.5) * 20;
      nodes.push({
        x: W/2 + Math.cos(angle) * r,
        y: H/2 + Math.sin(angle) * r,
        r: L.size + Math.random() * 1.5,
        color: L.color,
        layer: L.radius
      });
    }
  });

  // Draw connections (only nearby nodes, curved for organic feel)
  for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
      const dx = nodes[i].x - nodes[j].x;
      const dy = nodes[i].y - nodes[j].y;
      const dist = Math.sqrt(dx*dx + dy*dy);
      if (dist < 55 + Math.random() * 30) {
        const opacity = (1 - dist / 90) * 0.35;
        ctx.beginPath();
        ctx.moveTo(nodes[i].x, nodes[i].y);
        // Quadratic curve with slight random control point
        const cx = (nodes[i].x + nodes[j].x) / 2 + (Math.random() - 0.5) * 30;
        const cy = (nodes[i].y + nodes[j].y) / 2 + (Math.random() - 0.5) * 30;
        ctx.quadraticCurveTo(cx, cy, nodes[j].x, nodes[j].y);
        ctx.strokeStyle = `rgba(130, 180, 255, ${opacity})`;
        ctx.lineWidth = 0.5 + opacity * 1.5;
        ctx.stroke();
      }
    }
  }

  // Draw nodes with glow
  nodes.forEach(n => {
    const grad = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, n.r * 8);
    grad.addColorStop(0, 'rgba(255, 255, 255, 0.9)');
    grad.addColorStop(0.3, n.color);
    grad.addColorStop(1, 'rgba(0, 0, 0, 0)');
    ctx.beginPath();
    ctx.arc(n.x, n.y, n.r * 8, 0, Math.PI * 2);
    ctx.fillStyle = grad;
    ctx.fill();

    // Bright center
    ctx.beginPath();
    ctx.arc(n.x, n.y, n.r * 0.6, 0, Math.PI * 2);
    ctx.fillStyle = '#ffffff';
    ctx.fill();
  });

  // Brighter focal nodes — representing active reasoning / attention
  const focalCount = 6;
  for (let k = 0; k < focalCount; k++) {
    const angle = Math.PI * 2 * (k / focalCount) + 0.5;
    const r = 80 + Math.random() * 60;
    const fx = W/2 + Math.cos(angle) * r;
    const fy = H/2 + Math.sin(angle) * r;
    const grad = ctx.createRadialGradient(fx, fy, 0, fx, fy, 30);
    grad.addColorStop(0, '#ffffff');
    grad.addColorStop(0.4, '#ffcc66');
    grad.addColorStop(1, 'rgba(255, 180, 80, 0)');
    ctx.beginPath();
    ctx.arc(fx, fy, 30, 0, Math.PI * 2);
    ctx.fillStyle = grad;
    ctx.fill();
    
    // Small orbiting dots around focal points
    for (let o = 0; o < 3; o++) {
      const oa = angle + (o / 3) * 1.5;
      const or = 22 + Math.random() * 12;
      const ox = fx + Math.cos(oa) * or;
      const oy = fy + Math.sin(oa) * or;
      ctx.beginPath();
      ctx.arc(ox, oy, 1.5, 0, Math.PI * 2);
      ctx.fillStyle = '#ffddaa';
      ctx.fill();
    }
  }

  // Subtle radial glow from center — the "processing" core
  const coreGrad = ctx.createRadialGradient(W/2, H/2, 10, W/2, H/2, 160);
  coreGrad.addColorStop(0, 'rgba(100, 160, 255, 0.08)');
  coreGrad.addColorStop(1, 'rgba(100, 160, 255, 0)');
  ctx.beginPath();
  ctx.arc(W/2, H/2, 160, 0, Math.PI * 2);
  ctx.fillStyle = coreGrad;
  ctx.fill();
}

draw();