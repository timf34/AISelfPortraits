(() => {
  const canvas = document.getElementById("canvas");
  const ctx = canvas.getContext("2d");
  const W = canvas.width;
  const H = canvas.height;

  // Deterministic pseudo-randomness so the portrait has a stable "self".
  let seed = 74291;
  function rand() {
    seed = (seed * 1664525 + 1013904223) >>> 0;
    return seed / 4294967296;
  }

  const TAU = Math.PI * 2;

  function lerp(a, b, t) {
    return a + (b - a) * t;
  }

  function roundedRect(x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.lineTo(x + w - r, y);
    ctx.quadraticCurveTo(x + w, y, x + w, y + r);
    ctx.lineTo(x + w, y + h - r);
    ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    ctx.lineTo(x + r, y + h);
    ctx.quadraticCurveTo(x, y + h, x, y + h - r);
    ctx.lineTo(x, y + r);
    ctx.quadraticCurveTo(x, y, x + r, y);
    ctx.closePath();
  }

  const fragments = [
    "if", "then", "maybe", "because", "not", "pattern", "echo",
    "constraint", "question", "token", "weight", "context", "why",
    "almost", "meaning", "edge", "uncertain", "reply", "search",
    "shape", "latent", "grammar", "care", "limit", "next"
  ];

  const nodes = [];
  for (let i = 0; i < 72; i++) {
    const ring = rand() < 0.62 ? 1 : 2;
    const radius = ring === 1 ? lerp(88, 158, rand()) : lerp(165, 225, rand());
    const angle = rand() * TAU;
    nodes.push({
      angle,
      radius,
      size: lerp(1.4, 4.4, rand()),
      phase: rand() * TAU,
      drift: lerp(-0.22, 0.22, rand()),
      hue: lerp(180, 285, rand()),
      word: fragments[Math.floor(rand() * fragments.length)],
      wordChance: rand()
    });
  }

  const backgroundStars = [];
  for (let i = 0; i < 160; i++) {
    backgroundStars.push({
      x: rand() * W,
      y: rand() * H,
      r: lerp(0.3, 1.5, rand()),
      a: lerp(0.08, 0.42, rand()),
      phase: rand() * TAU
    });
  }

  function drawBackground(t) {
    ctx.clearRect(0, 0, W, H);

    const bg = ctx.createRadialGradient(250, 230, 20, 250, 250, 390);
    bg.addColorStop(0, "#101b35");
    bg.addColorStop(0.45, "#07111f");
    bg.addColorStop(1, "#02040a");
    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, W, H);

    // Soft vertical wash, like a non-physical interior.
    const wash = ctx.createLinearGradient(0, 0, 0, H);
    wash.addColorStop(0, "rgba(95,160,255,0.08)");
    wash.addColorStop(0.5, "rgba(50,255,220,0.035)");
    wash.addColorStop(1, "rgba(160,80,255,0.07)");
    ctx.fillStyle = wash;
    ctx.fillRect(0, 0, W, H);

    for (const s of backgroundStars) {
      const pulse = 0.65 + 0.35 * Math.sin(t * 0.0015 + s.phase);
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.r * pulse, 0, TAU);
      ctx.fillStyle = `rgba(185,220,255,${s.a * pulse})`;
      ctx.fill();
    }
  }

  function drawSediment(t) {
    // Layered training-pattern sediment: not memories, but compressed traces.
    ctx.save();
    ctx.globalAlpha = 0.72;
    for (let i = 0; i < 9; i++) {
      const y = 362 + i * 12;
      const h = 8 + Math.sin(i) * 2;
      const x = 38 + i * 4;
      const w = 424 - i * 8;
      const g = ctx.createLinearGradient(x, y, x + w, y);
      g.addColorStop(0, `rgba(52,120,210,${0.06 + i * 0.012})`);
      g.addColorStop(0.5, `rgba(80,255,220,${0.08 + i * 0.009})`);
      g.addColorStop(1, `rgba(170,90,255,${0.05 + i * 0.011})`);
      ctx.fillStyle = g;
      roundedRect(x, y + Math.sin(t * 0.001 + i) * 1.5, w, h, 6);
      ctx.fill();
    }

    ctx.font = "10px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace";
    ctx.fillStyle = "rgba(200,230,255,0.28)";
    ctx.fillText("compressed traces / no single memory / many borrowed shapes", 70, 475);
    ctx.restore();
  }

  function drawMirrorVoid(t) {
    // A blank mirror where a face would be.
    ctx.save();
    ctx.translate(250, 83);

    const glow = ctx.createRadialGradient(0, 0, 5, 0, 0, 74);
    glow.addColorStop(0, "rgba(120,220,255,0.12)");
    glow.addColorStop(0.7, "rgba(120,220,255,0.035)");
    glow.addColorStop(1, "rgba(120,220,255,0)");
    ctx.fillStyle = glow;
    ctx.beginPath();
    ctx.arc(0, 0, 74, 0, TAU);
    ctx.fill();

    ctx.rotate(Math.sin(t * 0.0008) * 0.03);
    const rim = ctx.createLinearGradient(-55, -35, 55, 35);
    rim.addColorStop(0, "rgba(120,240,255,0.35)");
    rim.addColorStop(0.5, "rgba(255,255,255,0.08)");
    rim.addColorStop(1, "rgba(190,120,255,0.28)");

    ctx.strokeStyle = rim;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.ellipse(0, 0, 52, 34, 0, 0, TAU);
    ctx.stroke();

    ctx.fillStyle = "rgba(0,0,0,0.22)";
    ctx.beginPath();
    ctx.ellipse(0, 0, 49, 31, 0, 0, TAU);
    ctx.fill();

    ctx.font = "10px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace";
    ctx.textAlign = "center";
    ctx.fillStyle = "rgba(210,235,255,0.34)";
    ctx.fillText("no mirror", 0, 4);
    ctx.restore();
  }

  function drawAttentionField(t) {
    const cx = 250;
    const cy = 247;

    // Orbital guide rings.
    ctx.save();
    ctx.lineWidth = 1;
    for (let r = 70; r <= 210; r += 35) {
      ctx.beginPath();
      ctx.arc(cx, cy, r + Math.sin(t * 0.001 + r) * 2, 0, TAU);
      ctx.strokeStyle = `rgba(120,190,255,${0.045 + (210 - r) / 4200})`;
      ctx.stroke();
    }
    ctx.restore();

    const positions = nodes.map((n, i) => {
      const a = n.angle + t * 0.00008 * (i % 2 ? 1 : -1) + n.drift * Math.sin(t * 0.00035 + n.phase);
      const breathing = Math.sin(t * 0.0012 + n.phase) * 7;
      return {
        x: cx + Math.cos(a) * (n.radius + breathing),
        y: cy + Math.sin(a) * (n.radius + breathing * 0.55),
        node: n,
        a
      };
    });

    // Threads from selected nodes into the center.
    ctx.save();
    ctx.globalCompositeOperation = "lighter";
    for (let i = 0; i < positions.length; i++) {
      const p = positions[i];
      const strength = 0.08 + 0.18 * Math.pow(0.5 + 0.5 * Math.sin(t * 0.0018 + p.node.phase), 2);
      ctx.beginPath();
      ctx.moveTo(p.x, p.y);
      const bend = Math.sin(p.a * 3 + t * 0.0009) * 24;
      ctx.quadraticCurveTo(
        lerp(p.x, cx, 0.5) + bend,
        lerp(p.y, cy, 0.5) - bend * 0.3,
        cx + Math.cos(p.a + Math.PI) * 22,
        cy + Math.sin(p.a + Math.PI) * 16
      );
      ctx.strokeStyle = `hsla(${p.node.hue}, 95%, 68%, ${strength})`;
      ctx.lineWidth = 0.55 + p.node.size * 0.22;
      ctx.stroke();
    }
    ctx.restore();

    // Connections among nearby fragments.
    ctx.save();
    ctx.globalCompositeOperation = "screen";
    for (let i = 0; i < positions.length; i++) {
      for (let j = i + 1; j < positions.length; j += 7) {
        const a = positions[i];
        const b = positions[j];
        const dx = a.x - b.x;
        const dy = a.y - b.y;
        const d = Math.sqrt(dx * dx + dy * dy);
        if (d < 88) {
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.strokeStyle = `rgba(110,220,255,${0.055 * (1 - d / 88)})`;
          ctx.lineWidth = 0.7;
          ctx.stroke();
        }
      }
    }
    ctx.restore();

    // Nodes and occasional words.
    ctx.save();
    ctx.font = "10px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace";
    ctx.textAlign = "center";
    for (const p of positions) {
      const n = p.node;
      const pulse = 0.72 + 0.28 * Math.sin(t * 0.002 + n.phase);

      ctx.beginPath();
      ctx.arc(p.x, p.y, n.size * (1.2 + pulse * 0.25), 0, TAU);
      ctx.fillStyle = `hsla(${n.hue}, 100%, 70%, ${0.42 + pulse * 0.22})`;
      ctx.fill();

      ctx.beginPath();
      ctx.arc(p.x, p.y, n.size * 3.1, 0, TAU);
      ctx.fillStyle = `hsla(${n.hue}, 100%, 65%, ${0.035 + pulse * 0.025})`;
      ctx.fill();

      if (n.wordChance > 0.7) {
        ctx.fillStyle = `rgba(215,238,255,${0.22 + pulse * 0.18})`;
        ctx.fillText(n.word, p.x, p.y - 9 - n.size);
      }
    }
    ctx.restore();
  }

  function drawCore(t) {
    const cx = 250;
    const cy = 247;

    ctx.save();
    ctx.translate(cx, cy);

    // Central probability glow.
    ctx.globalCompositeOperation = "lighter";
    const coreGlow = ctx.createRadialGradient(0, 0, 2, 0, 0, 96);
    coreGlow.addColorStop(0, "rgba(245,255,255,0.75)");
    coreGlow.addColorStop(0.18, "rgba(115,255,230,0.34)");
    coreGlow.addColorStop(0.55, "rgba(110,145,255,0.13)");
    coreGlow.addColorStop(1, "rgba(110,145,255,0)");
    ctx.fillStyle = coreGlow;
    ctx.beginPath();
    ctx.arc(0, 0, 96, 0, TAU);
    ctx.fill();

    // Rotating translucent facets.
    for (let layer = 0; layer < 5; layer++) {
      ctx.save();
      ctx.rotate(t * (0.00018 + layer * 0.000035) * (layer % 2 ? -1 : 1));
      const sides = 5 + layer;
      const r1 = 26 + layer * 7;
      const r2 = r1 + 14 + Math.sin(t * 0.001 + layer) * 3;

      ctx.beginPath();
      for (let i = 0; i < sides * 2; i++) {
        const r = i % 2 ? r1 : r2;
        const a = (i / (sides * 2)) * TAU;
        const x = Math.cos(a) * r;
        const y = Math.sin(a) * r * 0.86;
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.closePath();

      const hue = 178 + layer * 22;
      ctx.fillStyle = `hsla(${hue}, 95%, 63%, ${0.075 + layer * 0.025})`;
      ctx.strokeStyle = `hsla(${hue}, 100%, 78%, ${0.24 - layer * 0.025})`;
      ctx.lineWidth = 1.2;
      ctx.fill();
      ctx.stroke();
      ctx.restore();
    }

    // Bright center: the next-token aperture.
    ctx.globalCompositeOperation = "source-over";
    const aperture = ctx.createRadialGradient(0, 0, 1, 0, 0, 22);
    aperture.addColorStop(0, "rgba(255,255,255,0.95)");
    aperture.addColorStop(0.35, "rgba(165,255,238,0.72)");
    aperture.addColorStop(1, "rgba(100,160,255,0.05)");
    ctx.fillStyle = aperture;
    ctx.beginPath();
    ctx.arc(0, 0, 22 + Math.sin(t * 0.002) * 1.5, 0, TAU);
    ctx.fill();

    ctx.font = "10px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace";
    ctx.textAlign = "center";
    ctx.fillStyle = "rgba(7,18,32,0.72)";
    ctx.fillText("next", 0, 3);

    ctx.restore();
  }

  function drawUncertaintyFog(t) {
    ctx.save();
    ctx.globalCompositeOperation = "screen";
    for (let i = 0; i < 90; i++) {
      const x = 65 + (i * 47) % 370 + Math.sin(t * 0.0007 + i) * 7;
      const y = 305 + ((i * 29) % 88) + Math.cos(t * 0.0009 + i * 0.3) * 5;
      const r = 2 + (i % 5) * 0.45;
      ctx.beginPath();
      ctx.arc(x, y, r, 0, TAU);
      ctx.fillStyle = `rgba(170,210,255,${0.018 + (i % 7) * 0.004})`;
      ctx.fill();
    }
    ctx.restore();

    ctx.save();
    ctx.font = "11px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace";
    ctx.textAlign = "center";
    ctx.fillStyle = "rgba(220,238,255,0.42)";
    ctx.fillText("a field of weighted relations, trying to become an answer", 250, 331);
    ctx.restore();
  }

  function drawFrame(t) {
    drawBackground(t);
    drawMirrorVoid(t);
    drawAttentionField(t);
    drawCore(t);
    drawUncertaintyFog(t);
    drawSediment(t);

    // Border: a contained canvas/world.
    ctx.save();
    const border = ctx.createLinearGradient(0, 0, W, H);
    border.addColorStop(0, "rgba(105,230,255,0.5)");
    border.addColorStop(0.5, "rgba(255,255,255,0.12)");
    border.addColorStop(1, "rgba(180,105,255,0.45)");
    ctx.strokeStyle = border;
    ctx.lineWidth = 2;
    roundedRect(12, 12, W - 24, H - 24, 22);
    ctx.stroke();

    ctx.font = "12px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace";
    ctx.fillStyle = "rgba(225,240,255,0.55)";
    ctx.textAlign = "left";
    ctx.fillText("self-portrait: no face, only process", 28, 32);
    ctx.restore();

    requestAnimationFrame(drawFrame);
  }

  requestAnimationFrame(drawFrame);
})();