Here's an HTML document that creates a serene 500x500 night landscape – a moonlit lake framed by mountains and pine trees, built entirely with CSS and subtle animations.
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Moonlit Lake – 500x500 CSS Art</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: #1a1a2e;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            font-family: sans-serif;
        }

        .canvas {
            width: 500px;
            height: 500px;
            position: relative;
            overflow: hidden;
            border-radius: 12px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
            background: #0b0d1a;
        }

        /* Sky gradient */
        .sky {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 60%;
            background: linear-gradient(180deg,
                    #02040f 0%,
                    #0a1030 20%,
                    #141e3d 40%,
                    #1c2d54 60%,
                    #253b6e 80%,
                    #2a4578 100%);
        }

        /* Stars */
        .stars {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 58%;
        }

        .star {
            position: absolute;
            background: #ffffff;
            border-radius: 50%;
            animation: twinkle var(--duration) ease-in-out infinite;
            animation-delay: var(--delay);
            opacity: 0;
            box-shadow: 0 0 var(--glow) var(--glow-spread) rgba(255, 255, 255, 0.7);
        }

        @keyframes twinkle {
            0%,
            100% {
                opacity: 0.2;
                transform: scale(0.8);
            }
            25% {
                opacity: 1;
                transform: scale(1.3);
            }
            50% {
                opacity: 0.4;
                transform: scale(0.9);
            }
            75% {
                opacity: 0.9;
                transform: scale(1.2);
            }
        }

        /* Moon */
        .moon-container {
            position: absolute;
            top: 45px;
            right: 80px;
            width: 80px;
            height: 80px;
            z-index: 2;
        }

        .moon-glow {
            position: absolute;
            top: -20px;
            left: -20px;
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background: radial-gradient(circle,
                    rgba(255, 250, 220, 0.4) 0%,
                    rgba(255, 240, 180, 0.2) 30%,
                    rgba(255, 220, 140, 0.08) 50%,
                    rgba(255, 200, 100, 0.02) 70%,
                    transparent 100%);
            animation: moonPulse 4s ease-in-out infinite;
            pointer-events: none;
        }

        @keyframes moonPulse {
            0%,
            100% {
                transform: scale(1);
                opacity: 0.8;
            }
            50% {
                transform: scale(1.15);
                opacity: 0.6;
            }
        }

        .moon {
            position: absolute;
            top: 0;
            left: 0;
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: radial-gradient(circle at 35% 35%,
                    #fffef5 0%,
                    #fdf5d6 15%,
                    #f9e8b0 35%,
                    #f3d78c 55%,
                    #e8c46a 75%,
                    #d4a84b 100%);
            box-shadow:
                0 0 25px rgba(255, 245, 200, 0.7),
                0 0 60px rgba(255, 235, 170, 0.4),
                0 0 100px rgba(255, 220, 140, 0.2),
                0 0 150px rgba(255, 200, 100, 0.1);
            z-index: 2;
        }

        .moon-crater1 {
            position: absolute;
            top: 20px;
            left: 18px;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: rgba(200, 170, 120, 0.4);
            box-shadow: inset 1px 1px 2px rgba(0, 0, 0, 0.3);
            z-index: 3;
        }

        .moon-crater2 {
            position: absolute;
            top: 42px;
            left: 35px;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: rgba(200, 170, 120, 0.35);
            box-shadow: inset 1px 1px 2px rgba(0, 0, 0, 0.3);
            z-index: 3;
        }

        .moon-crater3 {
            position: absolute;
            top: 15px;
            left: 48px;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: rgba(200, 170, 120, 0.3);
            box-shadow: inset 0.5px 0.5px 1px rgba(0, 0, 0, 0.3);
            z-index: 3;
        }

        /* Mountains background */
        .mountains-back {
            position: absolute;
            bottom: 40%;
            left: 0;
            width: 100%;
            height: 28%;
            z-index: 1;
        }

        .mountain-back {
            position: absolute;
            bottom: 0;
            width: 0;
            height: 0;
            border-left: solid transparent;
            border-right: solid transparent;
            border-bottom: solid;
        }

        .mountain-back-1 {
            left: 5%;
            border-left-width: 110px;
            border-right-width: 130px;
            border-bottom-width: 160px;
            border-bottom-color: #1a2440;
        }

        .mountain-back-2 {
            left: 28%;
            border-left-width: 140px;
            border-right-width: 100px;
            border-bottom-width: 140px;
            border-bottom-color: #1e2a4a;
        }

        .mountain-back-3 {
            left: 52%;
            border-left-width: 120px;
            border-right-width: 140px;
            border-bottom-width: 170px;
            border-bottom-color: #1b2645;
        }

        .mountain-back-4 {
            left: 70%;
            border-left-width: 100px;
            border-right-width: 110px;
            border-bottom-width: 145px;
            border-bottom-color: #1d2848;
        }

        /* Mountains front */
        .mountains-front {
            position: absolute;
            bottom: 40%;
            left: 0;
            width: 100%;
            height: 22%;
            z-index: 3;
        }

        .mountain-front {
            position: absolute;
            bottom: 0;
            width: 0;
            height: 0;
            border-left: solid transparent;
            border-right: solid transparent;
            border-bottom: solid;
        }

        .mountain-front-1 {
            left: -5%;
            border-left-width: 100px;
            border-right-width: 120px;
            border-bottom-width: 140px;
            border-bottom-color: #111a30;
        }

        .mountain-front-2 {
            left: 22%;
            border-left-width: 150px;
            border-right-width: 130px;
            border-bottom-width: 155px;
            border-bottom-color: #0f162b;
        }

        .mountain-front-3 {
            left: 50%;
            border-left-width: 130px;
            border-right-width: 110px;
            border-bottom-width: 130px;
            border-bottom-color: #131d35;
        }

        .mountain-front-4 {
            left: 72%;
            border-left-width: 90px;
            border-right-width: 130px;
            border-bottom-width: 148px;
            border-bottom-color: #10182e;
        }

        /* Snow caps */
        .snow-cap {
            position: absolute;
            width: 0;
            height: 0;
            border-left: solid transparent;
            border-right: solid transparent;
            border-bottom: solid;
            z-index: 4;
            bottom: 0;
        }

        .snow-cap-1 {
            left: 15%;
            border-left-width: 14px;
            border-right-width: 10px;
            border-bottom-width: 20px;
            border-bottom-color: #dce8f5;
            bottom: 138px;
        }

        .snow-cap-2 {
            left: 38%;
            border-left-width: 18px;
            border-right-width: 14px;
            border-bottom-width: 24px;
            border-bottom-color: #e2ebf7;
            bottom: 153px;
        }

        .snow-cap-3 {
            left: 60%;
            border-left-width: 12px;
            border-right-width: 16px;
            border-bottom-width: 22px;
            border-bottom-color: #d9e4f2;
            bottom: 128px;
        }

        /* Lake */
        .lake {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 40%;
            background: linear-gradient(180deg,
                    #1c3050 0%,
                    #13223a 15%,
                    #0e1c32 30%,
                    #0b1629 50%,
                    #091223 70%,
                    #060d1a 100%);
            z-index: 2;
            overflow: hidden;
        }

        /* Moon reflection */
        .moon-reflection {
            position: absolute;
            top: 8%;
            right: 80px;
            width: 60px;
            height: 120px;
            z-index: 3;
            opacity: 0.55;
            transform: perspective(80px) rotateX(5deg);
        }

        .reflection-line {
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(255, 240, 190, 0.7);
            border-radius: 50%;
            animation: reflectShimmer 3s ease-in-out infinite;
        }

        .reflection-line:nth-child(1) {
            top: 0;
            width: 40px;
            height: 6px;
            animation-delay: 0s;
        }
        .reflection-line:nth-child(2) {
            top: 16px;
            width: 34px;
            height: 5px;
            animation-delay: 0.2s;
        }
        .reflection-line:nth-child(3) {
            top: 30px;
            width: 28px;
            height: 4px;
            animation-delay: 0.4s;
        }
        .reflection-line:nth-child(4) {
            top: 42px;
            width: 22px;
            height: 3px;
            animation-delay: 0.6s;
        }
        .reflection-line:nth-child(5) {
            top: 52px;
            width: 16px;
            height: 3px;
            animation-delay: 0.8s;
        }
        .reflection-line:nth-child(6) {
            top: 60px;
            width: 10px;
            height: 2px;
            animation-delay: 1s;
        }
        .reflection-line:nth-child(7) {
            top: 66px;
            width: 6px;
            height: 2px;
            animation-delay: 1.2s;
        }

        @keyframes reflectShimmer {
            0%,
            100% {
                opacity: 0.4;
                transform: translateX(-50%) scaleX(1);
            }
            25% {
                opacity: 0.8;
                transform: translateX(-50%) scaleX(1.4);
            }
            50% {
                opacity: 0.5;
                transform: translateX(-50%) scaleX(0.9);
            }
            75% {
                opacity: 0.75;
                transform: translateX(-50%) scaleX(1.2);
            }
        }

        /* Lake shimmer lines */
        .lake-shimmer {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 3;
            pointer-events: none;
        }

        .shimmer-line {
            position: absolute;
            width: 100%;
            height: 1px;
            background: rgba(255, 255, 255, 0.03);
            animation: shimmerFloat 5s ease-in-out infinite;
        }

        @keyframes shimmerFloat {
            0%,
            100% {
                opacity: 0.3;
            }
            50% {
                opacity: 0.7;
            }
        }

        /* Trees */
        .trees {
            position: absolute;
            bottom: 36%;
            left: 0;
            width: 100%;
            height: 18%;
            z-index: 5;
        }

        .tree {
            position: absolute;
            bottom: 0;
            width: 0;
            height: 0;
        }

        /* Tree trunk */
        .tree::before {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 6px;
            background: #1a1208;
            border-radius: 2px 2px 0 0;
        }

        /* Tree foliage (triangles) */
        .tree::after {
            content: '';
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: solid transparent;
            border-right: solid transparent;
            border-bottom: solid;
        }

        .tree-1 {
            left: 8%;
            bottom: 2px;
        }
        .tree-1::before {
            height: 22px;
            bottom: 0;
        }
        .tree-1::after {
            bottom: 18px;
            border-left-width: 16px;
            border-right-width: 16px;
            border-bottom-width: 32px;
            border-bottom-color: #0d1a0a;
        }
        .tree-1 .foliage2 {
            position: absolute;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 13px solid transparent;
            border-right: 13px solid transparent;
            border-bottom: 26px solid #0d1a0a;
        }
        .tree-1 .foliage3 {
            position: absolute;
            bottom: 40px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 10px solid transparent;
            border-right: 10px solid transparent;
            border-bottom: 20px solid #0f1e0c;
        }

        .tree-2 {
            left: 22%;
            bottom: 4px;
        }
        .tree-2::before {
            height: 26px;
            bottom: 0;
        }
        .tree-2::after {
            bottom: 22px;
            border-left-width: 18px;
            border-right-width: 18px;
            border-bottom-width: 36px;
            border-bottom-color: #0b1709;
        }
        .tree-2 .foliage2 {
            position: absolute;
            bottom: 36px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 15px solid transparent;
            border-right: 15px solid transparent;
            border-bottom: 30px solid #0b1709;
        }
        .tree-2 .foliage3 {
            position: absolute;
            bottom: 48px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 11px solid transparent;
            border-right: 11px solid transparent;
            border-bottom: 22px solid #0e1c0b;
        }

        .tree-3 {
            left: 74%;
            bottom: 1px;
        }
        .tree-3::before {
            height: 20px;
            bottom: 0;
        }
        .tree-3::after {
            bottom: 16px;
            border-left-width: 14px;
            border-right-width: 14px;
            border-bottom-width: 28px;
            border-bottom-color: #0d1a0a;
        }
        .tree-3 .foliage2 {
            position: absolute;
            bottom: 26px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 11px solid transparent;
            border-right: 11px solid transparent;
            border-bottom: 22px solid #0d1a0a;
        }
        .tree-3 .foliage3 {
            position: absolute;
            bottom: 36px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 9px solid transparent;
            border-right: 9px solid transparent;
            border-bottom: 18px solid #0f1e0c;
        }

        .tree-4 {
            left: 88%;
            bottom: 3px;
        }
        .tree-4::before {
            height: 18px;
            bottom: 0;
        }
        .tree-4::after {
            bottom: 14px;
            border-left-width: 12px;
            border-right-width: 12px;
            border-bottom-width: 24px;
            border-bottom-color: #0d1a0a;
        }
        .tree-4 .foliage2 {
            position: absolute;
            bottom: 22px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 10px solid transparent;
            border-right: 10px solid transparent;
            border-bottom: 20px solid #0d1a0a;
        }

        /* Mist layer */
        .mist {
            position: absolute;
            bottom: 37%;
            left: -10%;
            width: 120%;
            height: 8%;
            background: radial-gradient(ellipse at center,
                    rgba(180, 200, 220, 0.12) 0%,
                    rgba(180, 200, 220, 0.05) 50%,
                    transparent 70%);
            z-index: 6;
            pointer-events: none;
            animation: mistDrift 8s ease-in-out infinite;
        }

        @keyframes mistDrift {
            0%,
            100% {
                transform: translateX(0);
                opacity: 0.6;
            }
            33% {
                transform: translateX(15px);
                opacity: 0.4;
            }
            66% {
                transform: translateX(-10px);
                opacity: 0.7;
            }
        }

        /* Shoreline */
        .shore {
            position: absolute;
            bottom: 39.5%;
            left: 0;
            width: 100%;
            height: 2px;
            background: rgba(60, 80, 100, 0.4);
            z-index: 4;
            box-shadow: 0 1px 6px rgba(0, 0, 0, 0.3);
        }

        /* Aurora / subtle sky band */
        .aurora {
            position: absolute;
            top: 25%;
            left: -10%;
            width: 140%;
            height: 3%;
            background: linear-gradient(90deg,
                    transparent 0%,
                    rgba(120, 180, 210, 0.08) 20%,
                    rgba(140, 200, 220, 0.12) 35%,
                    rgba(100, 170, 200, 0.1) 50%,
                    rgba(140, 200, 220, 0.08) 65%,
                    rgba(120, 180, 210, 0.04) 80%,
                    transparent 100%);
            z-index: 1;
            filter: blur(8px);
            animation: auroraShift 12s ease-in-out infinite;
            pointer-events: none;
        }

        @keyframes auroraShift {
            0%,
            100% {
                transform: translateY(0) scaleY(1);
                opacity: 0.5;
            }
            25% {
                transform: translateY(-8px) scaleY(1.6);
                opacity: 0.8;
            }
            50% {
                transform: translateY(3px) scaleY(1.1);
                opacity: 0.4;
            }
            75% {
                transform: translateY(-5px) scaleY(2);
                opacity: 0.7;
            }
        }
    </style>
</head>
<body>
    <div class="canvas">
        <!-- Sky -->
        <div class="sky"></div>

        <!-- Aurora band -->
        <div class="aurora"></div>

        <!-- Stars -->
        <div class="stars">
            <div class="star" style="top:6%;left:12%;width:2.5px;height:2.5px;--duration:2.5s;--delay:0s;--glow:2px;--glow-spread:2px;"></div>
            <div class="star" style="top:10%;left:28%;width:2px;height:2px;--duration:3s;--delay:0.4s;--glow:1.5px;--glow-spread:1.5px;"></div>
            <div class="star" style="top:3%;left:50%;width:3px;height:3px;--duration:2.8s;--delay:0.8s;--glow:3px;--glow-spread:3px;"></div>
            <div class="star" style="top:14%;left:68%;width:2px;height:2px;--duration:3.2s;--delay:1.2s;--glow:1.5px;--glow-spread:1.5px;"></div>
            <div class="star" style="top:8%;left:82%;width:2.5px;height:2.5px;--duration:2.6s;--delay:0.3s;--glow:2px;--glow-spread:2px;"></div>
            <div class="star" style="top:18%;left:18%;width:1.8px;height:1.8px;--duration:3.5s;--delay:1.5s;--glow:1px;--glow-spread:1px;"></div>
            <div class="star" style="top:20%;left:42%;width:2.2px;height:2.2px;--duration:2.9s;--delay:0.6s;--glow:1.8px;--glow-spread:1.8px;"></div>
            <div class="star" style="top:5%;left:35%;width:1.5px;height:1.5px;--duration:3.8s;--delay:1.8s;--glow:1px;--glow-spread:1px;"></div>
            <div class="star" style="top:22%;left:75%;width:2px;height:2px;--duration:2.4s;--delay:0.2s;--glow:1.5px;--glow-spread:1.5px;"></div>
            <div class="star" style="top:12%;left:55%;width:1.8px;height:1.8px;--duration:3.1s;--delay:1s;--glow:1.2px;--glow-spread:1.2px;"></div>
            <div class="star" style="top:17%;left:90%;width:2.3px;height:2.3px;--duration:2.7s;--delay:0.7s;--glow:2px;--glow-spread:2px;"></div>
            <div class="star" style="top:25%;left:8%;width:2px;height:2px;--duration:3.3s;--delay:1.4s;--glow:1.5px;--glow-spread:1.5px;"></div>
            <div class="star" style="top:28%;left:60%;width:1.6px;height:1.6px;--duration:2.2s;--delay:0.9s;--glow:1px;--glow-spread:1px;"></div>
        </div>

        <!-- Moon -->
        <div class="moon-container">
            <div class="moon-glow"></div>
            <div class="moon"></div>
            <div class="moon-crater1"></div>
            <div class="moon-crater2"></div>
            <div class="moon-crater3"></div>
        </div>

        <!-- Background Mountains -->
        <div class="mountains-back">
            <div class="mountain-back mountain-back-1"></div>
            <div class="mountain-back mountain-back-2"></div>
            <div class="mountain-back mountain-back-3"></div>
            <div class="mountain-back mountain-back-4"></div>
        </div>

        <!-- Front Mountains -->
        <div class="mountains-front">
            <div class="mountain-front mountain-front-1"></div>
            <div class="mountain-front mountain-front-2"></div>
            <div class="mountain-front mountain-front-3"></div>
            <div class="mountain-front mountain-front-4"></div>
            <!-- Snow caps -->
            <div class="snow-cap snow-cap-1"></div>
            <div class="snow-cap snow-cap-2"></div>
            <div class="snow-cap snow-cap-3"></div>
        </div>

        <!-- Shoreline -->
        <div class="shore"></div>

        <!-- Trees -->
        <div class="trees">
            <div class="tree tree-1">
                <div class="foliage2"></div>
                <div class="foliage3"></div>
            </div>
            <div class="tree tree-2">
                <div class="foliage2"></div>
                <div class="foliage3"></div>
            </div>
            <div class="tree tree-3">
                <div class="foliage2"></div>
                <div class="foliage3"></div>
            </div>
            <div class="tree tree-4">
                <div class="foliage2"></div>
            </div>
        </div>

        <!-- Lake -->
        <div class="lake">
            <!-- Moon reflection -->
            <div class="moon-reflection">
                <div class="reflection-line"></div>
                <div class="reflection-line"></div>
                <div class="reflection-line"></div>
                <div class="reflection-line"></div>
                <div class="reflection-line"></div>
                <div class="reflection-line"></div>
                <div class="reflection-line"></div>
            </div>
            <!-- Lake shimmer -->
            <div class="lake-shimmer">
                <div class="shimmer-line" style="top:5%;animation-delay:0s;"></div>
                <div class="shimmer-line" style="top:15%;animation-delay:1s;"></div>
                <div class="shimmer-line" style="top:28%;animation-delay:2s;"></div>
                <div class="shimmer-line" style="top:42%;animation-delay:0.5s;"></div>
                <div class="shimmer-line" style="top:55%;animation-delay:1.5s;"></div>
                <div class="shimmer-line" style="top:70%;animation-delay:2.5s;"></div>
                <div class="shimmer-line" style="top:82%;animation-delay:3s;"></div>
                <div class="shimmer-line" style="top:92%;animation-delay:1.8s;"></div>
            </div>
        </div>

        <!-- Mist layer -->
        <div class="mist"></div>
    </div>
</body>
</html>
```
### Design & Visual Highlights

The scene blends layered landscapes and movement to create a calm nighttime atmosphere.

*   **Atmospheric Depth:** The scene uses **layered mountain ranges** (background and foreground), a misty haze, and a subtle aurora band to create a strong sense of depth. The deep blue-to-dark sky gradient sets the nighttime mood.
*   **Focal Point & Reflection:** A glowing, cratered moon draws the eye, while its animated reflection on the lake creates a cohesive visual connection between the sky and water.
*   **Organic Details:** Pine trees are built with layered triangular foliage, while stars twinkle at varied rhythms. The lake surface uses shimmering lines to simulate gentle water movement.
*   **Technical Approach:** The entire illustration is pure HTML/CSS—no JavaScript or images. Shapes are made with `border` tricks (for mountains/trees), `radial-gradient` (for moon glow), and CSS `animation` for all moving elements.