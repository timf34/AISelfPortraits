Sorry about that — the code got cut off last time. Here's the complete, self-contained lighthouse scene:

```svg
<svg width="500" height="500" viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">
  <title>Lighthouse at dusk</title>
  <desc>A red-and-white lighthouse on a rocky shore sweeps its beam across a starry dusk sky. A crescent moon and a small sailboat shimmer on the calm sea.</desc>

  <defs>
    <linearGradient id="skyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#070b20"/>
      <stop offset="0.55" stop-color="#141b3e"/>
      <stop offset="1" stop-color="#2f3e6a"/>
    </linearGradient>
    <linearGradient id="seaGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#2c3c66"/>
      <stop offset="0.4" stop-color="#1a2547"/>
      <stop offset="1" stop-color="#060a1a"/>
    </linearGradient>
    <radialGradient id="moonGlow">
      <stop offset="0" stop-color="#f7ecc9" stop-opacity="0.30"/>
      <stop offset="0.5" stop-color="#f7ecc9" stop-opacity="0.10"/>
      <stop offset="1" stop-color="#f7ecc9" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="horizonGlow">
      <stop offset="0" stop-color="#ffb268" stop-opacity="0.38"/>
      <stop offset="0.55" stop-color="#ff9e5c" stop-opacity="0.13"/>
      <stop offset="1" stop-color="#ff9e5c" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="beamGradL" gradientUnits="userSpaceOnUse" x1="340" y1="176" x2="26" y2="176">
      <stop offset="0" stop-color="#ffe4a0" stop-opacity="0.5"/>
      <stop offset="0.6" stop-color="#ffe4a0" stop-opacity="0.15"/>
      <stop offset="1" stop-color="#ffe4a0" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="beamGradR" gradientUnits="userSpaceOnUse" x1="340" y1="176" x2="500" y2="270">
      <stop offset="0" stop-color="#ffe4a0" stop-opacity="0.3"/>
      <stop offset="0.55" stop-color="#ffe4a0" stop-opacity="0.08"/>
      <stop offset="1" stop-color="#ffe4a0" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="glowStrong">
      <stop offset="0" stop-color="#ffe296" stop-opacity="0.95"/>
      <stop offset="0.35" stop-color="#ffd682" stop-opacity="0.4"/>
      <stop offset="1" stop-color="#ffd682" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glassGrad">
      <stop offset="0" stop-color="#fff6cf"/>
      <stop offset="0.5" stop-color="#ffd77c"/>
      <stop offset="1" stop-color="#f2a93e"/>
    </radialGradient>
    <linearGradient id="towerShade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.14"/>
      <stop offset="0.45" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="1" stop-color="#090d1e" stop-opacity="0.32"/>
    </linearGradient>
    <linearGradient id="shootGrad" gradientUnits="userSpaceOnUse" x1="366" y1="58" x2="420" y2="92">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.85"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="waterBeam" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffdf9a" stop-opacity="0.3"/>
      <stop offset="1" stop-color="#ffdf9a" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="vignette" cx="0.5" cy="0.45" r="0.75">
      <stop offset="0" stop-color="#02040e" stop-opacity="0"/>
      <stop offset="0.7" stop-color="#02040e" stop-opacity="0"/>
      <stop offset="1" stop-color="#02040e" stop-opacity="0.5"/>
    </radialGradient>
    <clipPath id="towerClip">
      <path d="M 310 342 L 370 342 L 359 202 L 321 202 Z"/>
    </clipPath>
    <mask id="crescentMask" maskUnits="userSpaceOnUse" x="60" y="30" width="120" height="120">
      <circle cx="120" cy="88" r="26" fill="#ffffff"/>
      <circle cx="110" cy="82" r="23" fill="#000000"/>
    </mask>
  </defs>

  <!-- Sky -->
  <rect x="0" y="0" width="500" height="342" fill="url(#skyGrad)"/>

  <!-- Stars -->
  <g fill="#ffffff">
    <circle cx="36" cy="52" r="1.4" opacity="0.9"/>
    <circle cx="88" cy="36" r="1" opacity="0.6"/>
    <circle cx="160" cy="44" r="1.2" opacity="0.8"/>
    <circle cx="208" cy="84" r="1" opacity="0.5"/>
    <circle cx="252" cy="34" r="1.5" opacity="0.9"/>
    <circle cx="300" cy="66" r="1" opacity="0.55"/>
    <circle cx="356" cy="32" r="1.2" opacity="0.75"/>
    <circle cx="418" cy="52" r="1" opacity="0.6"/>
    <circle cx="462" cy="96" r="1.3" opacity="0.8"/>
    <circle cx="404" cy="140" r="1" opacity="0.5"/>
    <circle cx="470" cy="170" r="1.1" opacity="0.6"/>
    <circle cx="48" cy="150" r="1" opacity="0.55"/>
    <circle cx="96" cy="200" r="1.2" opacity="0.7"/>
    <circle cx="150" cy="170" r="1" opacity="0.5"/>
    <circle cx="236" cy="150" r="1.1" opacity="0.6"/>
    <circle cx="288" cy="118" r="1" opacity="0.45"/>
    <circle cx="200" cy="232" r="1" opacity="0.5"/>
    <circle cx="60" cy="240" r="1.1" opacity="0.55"/>
    <circle cx="128" cy="258" r="1" opacity="0.45"/>
    <circle cx="262" cy="206" r="1.2" opacity="0.6"/>
    <circle cx="318" cy="262" r="1" opacity="0.4"/>
    <circle cx="40" cy="300" r="1" opacity="0.4"/>
    <circle cx="160" cy="300" r="1.1" opacity="0.45"/>
    <circle cx="232" cy="286" r="1" opacity="0.4"/>
    <circle cx="430" cy="220" r="1.2" opacity="0.55"/>
    <circle cx="392" cy="268" r="1" opacity="0.4"/>
    <circle cx="452" cy="300" r="1" opacity="0.35"/>
    <circle cx="96" cy="118" r="1.3" opacity="0.7"/>
    <circle cx="172" cy="120" r="1" opacity="0.35"/>
    <circle cx="330" cy="96" r="1.1" opacity="0.5"/>
  </g>

  <!-- Sparkle stars -->
  <g stroke="#ffffff" stroke-linecap="round" fill="none">
    <path d="M 180 66 L 180 78 M 174 72 L 186 72" stroke-width="1.2" opacity="0.8"/>
    <path d="M 442 62 L 442 72 M 437 67 L 447 67" stroke-width="1" opacity="0.6"/>
    <path d="M 70 108 L 70 118 M 65 113 L 75 113" stroke-width="1" opacity="0.6"/>
  </g>

  <!-- Shooting star -->
  <line x1="366" y1="58" x2="420" y2="92" stroke="url(#shootGrad)" stroke-width="2" stroke-linecap="round"/>
  <circle cx="366" cy="58" r="2" fill="#ffffff" opacity="0.9"/>

  <!-- Crescent moon -->
  <circle cx="120" cy="88" r="48" fill="url(#moonGlow)"/>
  <circle cx="120" cy="88" r="26" fill="#f7ecc9" mask="url(#crescentMask)"/>

  <!-- Faint clouds -->
  <ellipse cx="210" cy="312" rx="100" ry="7" fill="#1c2547" opacity="0.55"/>
  <ellipse cx="430" cy="292" rx="70" ry="6" fill="#1c2547" opacity="0.45"/>

  <!-- Horizon glow -->
  <ellipse cx="130" cy="342" rx="210" ry="60" fill="url(#horizonGlow)"/>

  <!-- Sea -->
  <rect x="0" y="342" width="500" height="158" fill="url(#seaGrad)"/>
  <line x1="0" y1="342" x2="500" y2="342" stroke="#46598c" stroke-width="1" opacity="0.5"/>

  <!-- Moon reflection -->
  <g stroke="#f7ecc9" stroke-linecap="round">
    <line x1="106" y1="352" x2="134" y2="352" stroke-width="2" opacity="0.35"/>
    <line x1="110" y1="362" x2="130" y2="362" stroke-width="2" opacity="0.28"/>
    <line x1="104" y1="374" x2="136" y2="374" stroke-width="2" opacity="0.22"/>
    <line x1="112" y1="388" x2="128" y2="388" stroke-width="2" opacity="0.16"/>
    <line x1="108" y1="404" x2="132" y2="404" stroke-width="2" opacity="0.1"/>
  </g>

  <!-- Beam reflection on water -->
  <polygon points="322,346 358,346 374,440 306,440" fill="url(#waterBeam)"/>

  <!-- Water sheen -->
  <g stroke="#4a5b8c" stroke-linecap="round" fill="none">
    <line x1="30" y1="368" x2="90" y2="368" stroke-width="1.5" opacity="0.25"/>
    <line x1="180" y1="380" x2="250" y2="380" stroke-width="1.5" opacity="0.2"/>
    <line x1="400" y1="360" x2="470" y2="360" stroke-width="1.5" opacity="0.25"/>
    <line x1="60" y1="420" x2="140" y2="420" stroke-width="1.5" opacity="0.15"/>
    <line x1="330" y1="460" x2="430" y2="460" stroke-width="1.5" opacity="0.12"/>
  </g>

  <!-- Sailboat -->
  <g>
    <polygon points="119,300 119,330 141,330" fill="#e8e2d2" opacity="0.9"/>
    <polygon points="115,306 115,330 97,330" fill="#cfc8b6" opacity="0.85"/>
    <line x1="117" y1="298" x2="117" y2="334" stroke="#0a0e1c" stroke-width="1.5"/>
    <path d="M 96 334 L 138 334 L 130 344 L 104 344 Z" fill="#0a0e1c"/>
    <line x1="104" y1="350" x2="130" y2="350" stroke="#e8e2d2" stroke-width="1.5" opacity="0.15" stroke-linecap="round"/>
  </g>

  <!-- Light beams -->
  <polygon points="340,168 340,184 26,238 26,118" fill="url(#beamGradL)"/>
  <polygon points="340,170 340,182 500,296 500,236" fill="url(#beamGradR)"/>

  <!-- Rocks -->
  <path d="M 282 362 Q 296 338 318 344 Q 330 330 350 338 Q 372 330 388 344 Q 408 340 420 356 L 424 384 L 278 384 Z" fill="#0a0e1c"/>
  <path d="M 288 366 Q 320 358 360 362" stroke="#3a4a72" stroke-width="1.5" fill="none" opacity="0.5" stroke-linecap="round"/>
  <path d="M 380 368 Q 400 364 416 368" stroke="#3a4a72" stroke-width="1.5" fill="none" opacity="0.4" stroke-linecap="round"/>

  <!-- Lighthouse tower -->
  <g clip-path="url(#towerClip)">
    <rect x="305" y="200" width="70" height="145" fill="#f2ede3"/>
    <rect x="305" y="204" width="70" height="24" fill="#b13a2e"/>
    <rect x="305" y="258" width="70" height="30" fill="#b13a2e"/>
    <rect x="305" y="318" width="70" height="26" fill="#b13a2e"/>
  </g>
  <path d="M 310 342 L 370 342 L 359 202 L 321 202 Z" fill="url(#towerShade)"/>

  <!-- Door and windows -->
  <path d="M 334 342 L 334 324 Q 340 317 346 324 L 346 342 Z" fill="#10162e"/>
  <rect x="336" y="236" width="8" height="11" rx="3" fill="#ffd77c"/>
  <rect x="336" y="294" width="8" height="11" rx="3" fill="#10162e"/>

  <!-- Gallery and railing -->
  <g stroke="#10162e" stroke-width="1.5">
    <line x1="314" y1="178" x2="314" y2="192"/>
    <line x1="324" y1="178" x2="324" y2="192"/>
    <line x1="334" y1="178" x2="334" y2="192"/>
    <line x1="346" y1="178" x2="346" y2="192"/>
    <line x1="356" y1="178" x2="356" y2="192"/>
    <line x1="366" y1="178" x2="366" y2="192"/>
  </g>
  <rect x="310" y="175" width="60" height="3" rx="1.5" fill="#10162e"/>
  <rect x="310" y="192" width="60" height="9" rx="2" fill="#10162e"/>

  <!-- Lantern room -->
  <rect x="324" y="160" width="32" height="30" fill="url(#glassGrad)"/>
  <g stroke="#10162e" stroke-width="2">
    <line x1="332" y1="160" x2="332" y2="190"/>
    <line x1="340" y1="160" x2="340" y2="190"/>
    <line x1="348" y1="160" x2="348" y2="190"/>
  </g>
  <rect x="322" y="158" width="36" height="3" fill="#10162e"/>
  <rect x="322" y="189" width="36" height="3" fill="#10162e"/>

  <!-- Dome and finial -->
  <path d="M 322 158 Q 340 136 358 158 Z" fill="#a93529"/>
  <line x1="340" y1="140" x2="340" y2="130" stroke="#10162e" stroke-width="2"/>
  <circle cx="340" cy="128" r="2.5" fill="#10162e"/>

  <!-- Light glow -->
  <circle cx="340" cy="175" r="60" fill="url(#glowStrong)" opacity="0.55"/>
  <circle cx="340" cy="175" r="26" fill="url(#glowStrong)"/>
  <circle cx="340" cy="175" r="7" fill="#fff3c4"/>

  <!-- Vignette -->
  <rect x="0" y="0" width="500" height="500" fill="url(#vignette)"/>
</svg>
```

The scene: a dusk gradient sky scattered with stars (plus a shooting star), a crescent moon made with a mask, warm horizon glow, and a calm sea carrying reflections of both the moon and the sweeping beam. The lighthouse itself uses a clip path for its tapered red-and-white stripes, a glowing lantern room with mullions, and a little sailboat rests near the horizon for scale.