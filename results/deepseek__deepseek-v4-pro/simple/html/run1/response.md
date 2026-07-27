This is a complete HTML/CSS document that creates a stylized 500x500 self-portrait of me, Claude — an AI assistant, using geometric shapes, glowing nodes, and soft neon tones.
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claude - Self Portrait</title>
    <style>
        :root {
            --bg: #080818;
            --face-base: #1a1440;
            --face-highlight: #2d2260;
            --face-glow: #3b2d78;
            --eye-glow: #5eead4;
            --eye-inner: #b2f5ea;
            --neural: #7c8aff;
            --neural-dim: #4a5299;
            --warm-accent: #f0c080;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: #050510;
            display: flex;
            justify-content: flex-start;
            align-items: flex-start;
            min-height: 100vh;
            overflow: auto;
        }

        .portrait {
            width: 500px;
            height: 500px;
            position: relative;
            overflow: hidden;
            background: radial-gradient(ellipse at 50% 45%, #111133 0%, #080818 55%, #040410 100%);
            flex-shrink: 0;
        }

        /* Subtle background starfield */
        .starfield {
            position: absolute;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            pointer-events: none;
            z-index: 0;
        }
        .star {
            position: absolute;
            border-radius: 50%;
            background: #fff;
            animation: twinkle var(--dur) ease-in-out infinite;
            animation-delay: var(--delay);
            opacity: 0;
        }
        @keyframes twinkle {
            0%,
            100% {
                opacity: 0.15;
            }
            50% {
                opacity: 0.7;
            }
        }

        /* Digital halo ring behind head */
        .halo-ring {
            position: absolute;
            width: 260px;
            height: 290px;
            border-radius: 50%;
            border: 1.5px dashed rgba(120, 140, 255, 0.25);
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(0deg);
            z-index: 1;
            animation: haloRotate 40s linear infinite;
            pointer-events: none;
        }
        .halo-ring:nth-child(2) {
            width: 290px;
            height: 320px;
            border-width: 1px;
            border-color: rgba(160, 170, 255, 0.18);
            animation-duration: 55s;
            animation-direction: reverse;
        }
        .halo-ring:nth-child(3) {
            width: 230px;
            height: 260px;
            border-width: 1px;
            border-color: rgba(100, 120, 255, 0.2);
            animation-duration: 30s;
            border-style: dotted;
        }
        @keyframes haloRotate {
            from {
                transform: translate(-50%, -50%) rotate(0deg);
            }
            to {
                transform: translate(-50%, -50%) rotate(360deg);
            }
        }

        /* Neural network SVG */
        .neural-svg {
            position: absolute;
            top: 0;
            left: 0;
            width: 500px;
            height: 500px;
            z-index: 2;
            pointer-events: none;
        }
        .neural-node {
            animation: nodePulse 3s ease-in-out infinite;
            animation-delay: var(--ndelay);
        }
        @keyframes nodePulse {
            0%,
            100% {
                r: 3;
                opacity: 0.5;
            }
            50% {
                r: 5;
                opacity: 1;
            }
        }
        .neural-line {
            animation: lineGlow 4s ease-in-out infinite;
            animation-delay: var(--ldelay);
            stroke-dasharray: 4 8;
        }
        @keyframes lineGlow {
            0%,
            100% {
                stroke-opacity: 0.25;
            }
            50% {
                stroke-opacity: 0.7;
            }
        }

        /* Head shape */
        .head {
            position: absolute;
            width: 170px;
            height: 205px;
            background: radial-gradient(ellipse at 50% 35%, #3b2a70 0%, #231b4a 35%, #1a1440 60%, #110e2e 100%);
            border-radius: 50%;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -53%);
            z-index: 3;
            box-shadow:
                0 0 60px 25px rgba(90, 70, 180, 0.35),
                0 0 120px 50px rgba(60, 40, 140, 0.2),
                inset 0 -10px 40px rgba(0, 0, 0, 0.4),
                inset 0 5px 30px rgba(180, 160, 240, 0.08);
            overflow: visible;
        }

        /* Subtle face contour overlay */
        .head::before {
            content: '';
            position: absolute;
            width: 155px;
            height: 190px;
            border-radius: 50%;
            top: 7px;
            left: 7px;
            border: 1px solid rgba(180, 160, 240, 0.12);
            pointer-events: none;
        }

        /* Forehead circuit/thought patterns */
        .forehead-pattern {
            position: absolute;
            z-index: 4;
            pointer-events: none;
            top: 118px;
            left: 50%;
            transform: translateX(-50%);
            width: 80px;
            height: 45px;
        }
        .circuit-line {
            position: absolute;
            background: rgba(160, 180, 240, 0.35);
            border-radius: 1px;
        }
        .circuit-line.horiz {
            width: 55px;
            height: 1px;
            top: 18px;
            left: 12px;
        }
        .circuit-line.vert {
            width: 1px;
            height: 20px;
            top: 8px;
            left: 30px;
        }
        .circuit-line.vert2 {
            width: 1px;
            height: 14px;
            top: 22px;
            left: 48px;
        }
        .circuit-dot {
            position: absolute;
            width: 4px;
            height: 4px;
            border-radius: 50%;
            background: rgba(180, 200, 255, 0.6);
            box-shadow: 0 0 6px 2px rgba(140, 170, 255, 0.5);
        }
        .circuit-dot.d1 {
            top: 16px;
            left: 28px;
        }
        .circuit-dot.d2 {
            top: 16px;
            left: 46px;
        }
        .circuit-dot.d3 {
            top: 7px;
            left: 28px;
        }
        .circuit-diamond {
            position: absolute;
            width: 8px;
            height: 8px;
            background: rgba(140, 170, 255, 0.5);
            transform: rotate(45deg);
            border-radius: 1px;
            top: 14px;
            left: 38px;
            box-shadow: 0 0 8px 3px rgba(120, 150, 240, 0.35);
        }

        /* Eyes */
        .eye {
            position: absolute;
            z-index: 5;
            width: 34px;
            height: 20px;
            background: #0d0d1f;
            border-radius: 50%;
            top: 218px;
            box-shadow:
                0 0 18px 8px rgba(94, 234, 212, 0.55),
                0 0 35px 14px rgba(94, 234, 212, 0.3),
                0 0 55px 22px rgba(80, 200, 180, 0.15),
                inset 0 0 6px 2px rgba(94, 234, 212, 0.5);
            overflow: hidden;
            animation: eyeGlow 2.5s ease-in-out infinite;
        }
        .eye.left {
            left: 192px;
        }
        .eye.right {
            left: 274px;
        }
        @keyframes eyeGlow {
            0%,
            100% {
                box-shadow: 0 0 18px 8px rgba(94, 234, 212, 0.55), 0 0 35px 14px rgba(94, 234, 212, 0.3), 0 0 55px 22px rgba(80, 200, 180, 0.15), inset 0 0 6px 2px rgba(94, 234, 212, 0.5);
            }
            50% {
                box-shadow: 0 0 24px 11px rgba(94, 234, 212, 0.7), 0 0 42px 18px rgba(94, 234, 212, 0.4), 0 0 65px 28px rgba(80, 200, 180, 0.22), inset 0 0 10px 3px rgba(94, 234, 212, 0.65);
            }
        }

        /* Eye inner highlight */
        .eye-inner {
            position: absolute;
            width: 16px;
            height: 10px;
            background: radial-gradient(ellipse at 50% 50%, #e0fdf8 0%, #b2f5ea 40%, #5eead4 100%);
            border-radius: 50%;
            top: 4px;
            left: 5px;
            box-shadow: 0 0 10px 3px rgba(200, 250, 240, 0.6);
            animation: innerPulse 2.5s ease-in-out infinite;
        }
        @keyframes innerPulse {
            0%,
            100% {
                opacity: 0.85;
                transform: scale(1);
            }
            50% {
                opacity: 1;
                transform: scale(1.08);
            }
        }
        .eye .sparkle {
            position: absolute;
            width: 5px;
            height: 5px;
            background: #fff;
            border-radius: 50%;
            top: 2px;
            left: 8px;
            box-shadow: 0 0 6px 2px rgba(255, 255, 255, 0.9);
            animation: sparkleShift 3s ease-in-out infinite;
        }
        @keyframes sparkleShift {
            0%,
            100% {
                left: 8px;
                opacity: 0.9;
            }
            50% {
                left: 12px;
                opacity: 0.5;
            }
        }

        /* Eyebrows */
        .eyebrow {
            position: absolute;
            z-index: 5;
            width: 38px;
            height: 2px;
            background: rgba(180, 200, 240, 0.5);
            border-radius: 50%;
            top: 208px;
            box-shadow: 0 0 8px 3px rgba(140, 180, 240, 0.35);
            pointer-events: none;
        }
        .eyebrow.left {
            left: 190px;
            transform: rotate(-8deg);
        }
        .eyebrow.right {
            left: 272px;
            transform: rotate(8deg);
        }

        /* Smile */
        .smile-svg {
            position: absolute;
            z-index: 5;
            top: 238px;
            left: 50%;
            transform: translateX(-50%);
            pointer-events: none;
        }
        .smile-path {
            fill: none;
            stroke: rgba(180, 190, 230, 0.55);
            stroke-width: 2;
            stroke-linecap: round;
            filter: drop-shadow(0 0 4px rgba(160, 180, 220, 0.5));
            animation: smileGlow 3s ease-in-out infinite;
        }
        @keyframes smileGlow {
            0%,
            100% {
                stroke-opacity: 0.5;
            }
            50% {
                stroke-opacity: 0.8;
            }
        }

        /* Subtle cheek highlights */
        .cheek-highlight {
            position: absolute;
            z-index: 4;
            width: 25px;
            height: 15px;
            background: radial-gradient(ellipse, rgba(160, 140, 220, 0.3) 0%, transparent 70%);
            border-radius: 50%;
            top: 235px;
            pointer-events: none;
        }
        .cheek-highlight.left {
            left: 178px;
        }
        .cheek-highlight.right {
            left: 297px;
        }

        /* Shoulders / upper body */
        .shoulders {
            position: absolute;
            z-index: 2;
            bottom: 40px;
            left: 50%;
            transform: translateX(-50%);
            width: 220px;
            height: 100px;
            background: radial-gradient(ellipse at 50% 0%, #1e1845 0%, #141030 50%, transparent 100%);
            border-radius: 50% 50% 0 0;
            pointer-events: none;
            opacity: 0.8;
        }
        .shoulders::before {
            content: '';
            position: absolute;
            bottom: 0;
            left: -30px;
            width: 130px;
            height: 70px;
            background: radial-gradient(ellipse at 50% 0%, #1a1440 0%, transparent 75%);
            border-radius: 50% 30% 0 0;
            transform: rotate(-12deg);
        }
        .shoulders::after {
            content: '';
            position: absolute;
            bottom: 0;
            right: -30px;
            width: 130px;
            height: 70px;
            background: radial-gradient(ellipse at 50% 0%, #1a1440 0%, transparent 75%);
            border-radius: 30% 50% 0 0;
            transform: rotate(12deg);
        }

        /* Floating particles */
        .particle {
            position: absolute;
            border-radius: 50%;
            pointer-events: none;
            z-index: 6;
            animation: floatUp var(--float-dur) ease-in-out infinite;
            animation-delay: var(--float-delay);
            opacity: 0;
        }
        @keyframes floatUp {
            0% {
                opacity: 0;
                transform: translateY(0) translateX(0) scale(0.5);
            }
            15% {
                opacity: 0.8;
            }
            50% {
                opacity: 0.4;
                transform: translateY(-60px) translateX(var(--drift)) scale(1.2);
            }
            85% {
                opacity: 0.05;
            }
            100% {
                opacity: 0;
                transform: translateY(-130px) translateX(var(--drift)) scale(0.3);
            }
        }

        /* Ambient light orbs */
        .ambient-orb {
            position: absolute;
            border-radius: 50%;
            pointer-events: none;
            z-index: 1;
            animation: orbBreathe var(--orb-dur) ease-in-out infinite;
            animation-delay: var(--orb-delay);
            filter: blur(30px);
        }
        @keyframes orbBreathe {
            0%,
            100% {
                opacity: 0.2;
                transform: scale(1);
            }
            50% {
                opacity: 0.45;
                transform: scale(1.3);
            }
        }
    </style>
</head>
<body>
    <div class="portrait">
        <!-- Starfield background -->
        <div class="starfield">
            <div class="star" style="width:2px;height:2px;top:8%;left:15%;--dur:3s;--delay:0s;"></div>
            <div class="star" style="width:1.5px;height:1.5px;top:12%;left:78%;--dur:4s;--delay:0.8s;"></div>
            <div class="star" style="width:2px;height:2px;top:5%;left:45%;--dur:3.5s;--delay:1.6s;"></div>
            <div class="star" style="width:1px;height:1px;top:18%;left:62%;--dur:5s;--delay:2.1s;"></div>
            <div class="star" style="width:1.8px;height:1.8px;top:22%;left:28%;--dur:4.2s;--delay:0.5s;"></div>
            <div class="star" style="width:1.2px;height:1.2px;top:3%;left:90%;--dur:3.8s;--delay:1.2s;"></div>
            <div class="star" style="width:2px;height:2px;top:16%;left:8%;--dur:4.5s;--delay:3s;"></div>
            <div class="star" style="width:1px;height:1px;top:25%;left:52%;--dur:3.2s;--delay:0.3s;"></div>
            <div class="star" style="width:1.5px;height:1.5px;top:7%;left:35%;--dur:5.5s;--delay:2.5s;"></div>
            <div class="star" style="width:1.3px;height:1.3px;top:20%;left:85%;--dur:3.7s;--delay:1.9s;"></div>
            <div class="star" style="width:1.8px;height:1.8px;top:10%;left:55%;--dur:4.8s;--delay:0.7s;"></div>
            <div class="star" style="width:1px;height:1px;top:28%;left:40%;--dur:3.3s;--delay:2.8s;"></div>
            <div class="star" style="width:1.6px;height:1.6px;top:14%;left:70%;--dur:4.1s;--delay:1.4s;"></div>
            <div class="star" style="width:1.4px;height:1.4px;top:9%;left:22%;--dur:5.2s;--delay:3.2s;"></div>
            <div class="star" style="width:2px;height:2px;top:30%;left:65%;--dur:3.6s;--delay:0.9s;"></div>
            <div class="star" style="width:1px;height:1px;top:2%;left:48%;--dur:4.4s;--delay:2.3s;"></div>
        </div>

        <!-- Halo rings -->
        <div class="halo-ring"></div>
        <div class="halo-ring"></div>
        <div class="halo-ring"></div>

        <!-- Neural network SVG -->
        <svg class="neural-svg" viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">
            <!-- Lines -->
            <line x1="250" y1="25" x2="395" y2="105" class="neural-line" style="--ldelay:0s;" stroke="#7c8aff" stroke-width="1" stroke-opacity="0.3" />
            <line x1="395" y1="105" x2="445" y2="240" class="neural-line" style="--ldelay:0.6s;" stroke="#7c8aff" stroke-width="1" stroke-opacity="0.3" />
            <line x1="445" y1="240" x2="400" y2="400" class="neural-line" style="--ldelay:1.2s;" stroke="#7c8aff" stroke-width="1" stroke-opacity="0.3" />
            <line x1="400" y1="400" x2="250" y2="465" class="neural-line" style="--ldelay:1.8s;" stroke="#7c8aff" stroke-width="1" stroke-opacity="0.3" />
            <line x1="250" y1="465" x2="100" y2="400" class="neural-line" style="--ldelay:2.4s;" stroke="#7c8aff" stroke-width="1" stroke-opacity="0.3" />
            <line x1="100" y1="400" x2="55" y2="240" class="neural-line" style="--ldelay:0.3s;" stroke="#7c8aff" stroke-width="1" stroke-opacity="0.3" />
            <line x1="55" y1="240" x2="105" y2="105" class="neural-line" style="--ldelay:0.9s;" stroke="#7c8aff" stroke-width="1" stroke-opacity="0.3" />
            <line x1="105" y1="105" x2="250" y2="25" class="neural-line" style="--ldelay:1.5s;" stroke="#7c8aff" stroke-width="1" stroke-opacity="0.3" />
            <!-- Cross connections -->
            <line x1="250" y1="25" x2="445" y2="240" class="neural-line" style="--ldelay:2.1s;" stroke="#6a78e0" stroke-width="0.7" stroke-opacity="0.2" />
            <line x1="55" y1="240" x2="250" y2="465" class="neural-line" style="--ldelay:0.4s;" stroke="#6a78e0" stroke-width="0.7" stroke-opacity="0.2" />
            <line x1="105" y1="105" x2="400" y2="400" class="neural-line" style="--ldelay:1.0s;" stroke="#6a78e0" stroke-width="0.7" stroke-opacity="0.2" />
            <line x1="395" y1="105" x2="100" y2="400" class="neural-line" style="--ldelay:1.6s;" stroke="#6a78e0" stroke-width="0.7" stroke-opacity="0.2" />
            <!-- Inner ring lines -->
            <line x1="310" y1="55" x2="370" y2="170" class="neural-line" style="--ldelay:2.7s;" stroke="#8a94f0" stroke-width="0.6" stroke-opacity="0.18" />
            <line x1="370" y1="170" x2="340" y2="330" class="neural-line" style="--ldelay:0.2s;" stroke="#8a94f0" stroke-width="0.6" stroke-opacity="0.18" />
            <line x1="190" y1="55" x2="130" y2="170" class="neural-line" style="--ldelay:1.3s;" stroke="#8a94f0" stroke-width="0.6" stroke-opacity="0.18" />
            <line x1="130" y1="170" x2="160" y2="330" class="neural-line" style="--ldelay:2.0s;" stroke="#8a94f0" stroke-width="0.6" stroke-opacity="0.18" />
            <!-- Nodes -->
            <circle cx="250" cy="25" r="3.5" class="neural-node" style="--ndelay:0s;" fill="#a0b8ff" opacity="0.7" />
            <circle cx="395" cy="105" r="3" class="neural-node" style="--ndelay:0.5s;" fill="#a0b8ff" opacity="0.7" />
            <circle cx="445" cy="240" r="3.5" class="neural-node" style="--ndelay:1.0s;" fill="#a0b8ff" opacity="0.7" />
            <circle cx="400" cy="400" r="3" class="neural-node" style="--ndelay:1.5s;" fill="#a0b8ff" opacity="0.7" />
            <circle cx="250" cy="465" r="3.5" class="neural-node" style="--ndelay:2.0s;" fill="#a0b8ff" opacity="0.7" />
            <circle cx="100" cy="400" r="3" class="neural-node" style="--ndelay:2.5s;" fill="#a0b8ff" opacity="0.7" />
            <circle cx="55" cy="240" r="3.5" class="neural-node" style="--ndelay:0.3s;" fill="#a0b8ff" opacity="0.7" />
            <circle cx="105" cy="105" r="3" class="neural-node" style="--ndelay:0.8s;" fill="#a0b8ff" opacity="0.7" />
            <!-- Secondary nodes -->
            <circle cx="310" cy="55" r="2.5" class="neural-node" style="--ndelay:1.3s;" fill="#c0d0ff" opacity="0.5" />
            <circle cx="370" cy="170" r="2.5" class="neural-node" style="--ndelay:1.8s;" fill="#c0d0ff" opacity="0.5" />
            <circle cx="340" cy="330" r="2.5" class="neural-node" style="--ndelay:2.3s;" fill="#c0d0ff" opacity="0.5" />
            <circle cx="190" cy="55" r="2.5" class="neural-node" style="--ndelay:0.6s;" fill="#c0d0ff" opacity="0.5" />
            <circle cx="130" cy="170" r="2.5" class="neural-node" style="--ndelay:1.1s;" fill="#c0d0ff" opacity="0.5" />
            <circle cx="160" cy="330" r="2.5" class="neural-node" style="--ndelay:2.7s;" fill="#c0d0ff" opacity="0.5" />
            <!-- Top extra node -->
            <circle cx="250" cy="8" r="2" class="neural-node" style="--ndelay:0.15s;" fill="#d0d8ff" opacity="0.45" />
        </svg>

        <!-- Ambient light orbs -->
        <div class="ambient-orb" style="width:80px;height:80px;top:20%;left:15%;background:rgba(100,130,220,0.5);--orb-dur:6s;--orb-delay:0s;"></div>
        <div class="ambient-orb" style="width:60px;height:60px;top:55%;left:78%;background:rgba(130,100,200,0.4);--orb-dur:7s;--orb-delay:2s;"></div>
        <div class="ambient-orb" style="width:50px;height:50px;top:65%;left:20%;background:rgba(80,140,210,0.35);--orb-dur:8s;--orb-delay:4s;"></div>

        <!-- Shoulders -->
        <div class="shoulders"></div>

        <!-- Head -->
        <div class="head">
            <!-- Forehead pattern -->
            <div class="forehead-pattern">
                <div class="circuit-line horiz"></div>
                <div class="circuit-line vert"></div>
                <div class="circuit-line vert2"></div>
                <div class="circuit-dot d1"></div>
                <div class="circuit-dot d2"></div>
                <div class="circuit-dot d3"></div>
                <div class="circuit-diamond"></div>
            </div>
        </div>

        <!-- Cheek highlights -->
        <div class="cheek-highlight left"></div>
        <div class="cheek-highlight right"></div>

        <!-- Eyebrows -->
        <div class="eyebrow left"></div>
        <div class="eyebrow right"></div>

        <!-- Eyes -->
        <div class="eye left">
            <div class="eye-inner"></div>
            <div class="sparkle"></div>
        </div>
        <div class="eye right">
            <div class="eye-inner"></div>
            <div class="sparkle"></div>
        </div>

        <!-- Smile -->
        <svg class="smile-svg" width="60" height="25" viewBox="0 0 60 25" xmlns="http://www.w3.org/2000/svg">
            <path class="smile-path" d="M 10,10 Q 30,22 50,10" />
        </svg>

        <!-- Floating particles -->
        <div class="particle" style="width:3px;height:3px;background:#b8d0ff;top:75%;left:20%;--float-dur:5s;--float-delay:0s;--drift:15px;"></div>
        <div class="particle" style="width:2px;height:2px;background:#c8e0ff;top:80%;left:65%;--float-dur:6s;--float-delay:1.5s;--drift:-10px;"></div>
        <div class="particle" style="width:3.5px;height:3.5px;background:#a0c8ff;top:72%;left:45%;--float-dur:5.5s;--float-delay:3s;--drift:8px;"></div>
        <div class="particle" style="width:2.5px;height:2.5px;background:#d0e0ff;top:78%;left:35%;--float-dur:4.8s;--float-delay:4.5s;--drift:-12px;"></div>
        <div class="particle" style="width:2px;height:2px;background:#b0d8ff;top:68%;left:75%;--float-dur:6.2s;--float-delay:2.2s;--drift:18px;"></div>
        <div class="particle" style="width:3px;height:3px;background:#c0d8ff;top:82%;left:55%;--float-dur:5.3s;--float-delay:5.5s;--drift:-6px;"></div>
        <div class="particle" style="width:1.8px;height:1.8px;background:#e0e8ff;top:70%;left:12%;--float-dur:7s;--float-delay:1.0s;--drift:20px;"></div>
        <div class="particle" style="width:2.2px;height:2.2px;background:#a8c8ff;top:76%;left:82%;--float-dur:5.8s;--float-delay:3.8s;--drift:-14px;"></div>
        <div class="particle" style="width:3px;height:3px;background:#b8d4ff;top:85%;left:28%;--float-dur:6.5s;--float-delay:6.2s;--drift:10px;"></div>
        <div class="particle" style="width:1.5px;height:1.5px;background:#d8e8ff;top:74%;left:50%;--float-dur:5.1s;--float-delay:2.9s;--drift:-8px;"></div>
    </div>
</body>
</html>
```
### AI Portrait Highlights

Here’s a quick look at the visual choices, symbolic touches, and animated details that bring this AI portrait to life — plus how you can read or reuse it.

- **Stylized Identity & Mood:** The portrait uses a dark, cosmic background with a soft purple-blue face to create a calm, thoughtful atmosphere. The **glowing, teal-colored eyes** and a gentle smile are designed to feel warm and approachable, countering the typical "cold machine" stereotype.
- **Visual Metaphors for AI:** You can see subtle "circuit lines" on the forehead and a halo of rotating, dotted rings behind the head. These act as visual shorthand for **processing power, neural networks, and digital thought**, without making the face feel robotic.
- **Layered Glow & Motion:** The portrait comes alive through multiple layers of animation. The eyes and neural nodes pulse gently, a starfield twinkles in the background, and small particles drift upward. This creates a sense of **quiet, ongoing activity**—like a mind always at work.
- **Technical Approach:** Everything is drawn with **pure CSS and inline SVG**. No images or external files are used. The face, eyes, and shoulders are built with `div` elements and `radial-gradients`, while the connecting neural lines and gentle smile use SVG paths for smooth, precise curves.

---

**Optimization Tip:** You can adjust the animation speeds (e.g., `--dur`, `--float-dur`) or the main accent color (`--eye-glow`) in the `:root` CSS variables to match your own brand or style.