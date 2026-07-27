Let me think about what to draw...

I'd like to make something peaceful — a quiet night scene: a moonlit lake with mountains, pine trees, and a little cabin with one warm lit window. I like the idea that in a dark landscape, one tiny point of warmth changes the whole feeling of the image. I'll use gradients for the sky and water, a glowing moon with its reflection shimmering across the lake, scattered stars, and a few fireflies near the shore.

```svg
<svg width="500" height="500" viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0b1035"/>
      <stop offset="55%" stop-color="#1e2455"/>
      <stop offset="100%" stop-color="#4a3b6b"/>
    </linearGradient>
    <linearGradient id="lake" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#3a3463"/>
      <stop offset="100%" stop-color="#0d1030"/>
    </linearGradient>
    <radialGradient id="moonGlow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#f7f2d8" stop-opacity="0.55"/>
      <stop offset="60%" stop-color="#f7f2d8" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#f7f2d8" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="fireflyGlow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#d9f26b" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#d9f26b" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- Sky -->
  <rect x="0" y="0" width="500" height="320" fill="url(#sky)"/>

  <!-- Stars -->
  <g fill="#ffffff">
    <circle cx="40" cy="50" r="1.6" opacity="0.9"/>
    <circle cx="90" cy="110" r="1.1" opacity="0.7"/>
    <circle cx="140" cy="40" r="1.4" opacity="0.8"/>
    <circle cx="200" cy="90" r="1.0" opacity="0.6"/>
    <circle cx="250" cy="35" r="1.7" opacity="0.9"/>
    <circle cx="300" cy="150" r="1.0" opacity="0.5"/>
    <circle cx="450" cy="60" r="1.5" opacity="0.85"/>
    <circle cx="470" cy="140" r="1.1" opacity="0.6"/>
    <circle cx="180" cy="160" r="1.2" opacity="0.7"/>
    <circle cx="60" cy="180" r="1.0" opacity="0.55"/>
    <circle cx="120" cy="220" r="0.9" opacity="0.5"/>
    <circle cx="420" cy="200" r="1.0" opacity="0.5"/>
    <circle cx="270" cy="120" r="1.3" opacity="0.75"/>
    <circle cx="30" cy="130" r="0.9" opacity="0.5"/>
    <circle cx="220" cy="180" r="0.9" opacity="0.45"/>
  </g>
  <!-- Shooting star -->
  <line x1="70" y1="70" x2="115" y2="88" stroke="#ffffff" stroke-width="1.2" opacity="0.6" stroke-linecap="round"/>

  <!-- Moon -->
  <circle cx="360" cy="100" r="90" fill="url(#moonGlow)"/>
  <circle cx="360" cy="100" r="42" fill="#f5f0da"/>
  <circle cx="345" cy="90" r="7" fill="#dcd6ba" opacity="0.7"/>
  <circle cx="372" cy="112" r="5" fill="#dcd6ba" opacity="0.6"/>
  <circle cx="358" cy="122" r="3.5" fill="#dcd6ba" opacity="0.5"/>
  <circle cx="376" cy="84" r="4" fill="#dcd6ba" opacity="0.55"/>

  <!-- Far mountains -->
  <path d="M0,320 L70,205 L130,270 L200,185 L275,285 L340,225 L410,300 L460,240 L500,290 L500,320 Z"
        fill="#33305e"/>
  <!-- Near mountains -->
  <path d="M0,320 L60,265 L140,320 L230,245 L320,320 L400,262 L500,320 Z"
        fill="#232145"/>

  <!-- Shoreline strip -->
  <rect x="0" y="312" width="500" height="10" fill="#171531"/>

  <!-- Pine trees (right shore) -->
  <g fill="#12102a">
    <g transform="translate(380,318)">
      <polygon points="0,0 -16,0 -8,-22"/>
      <polygon points="-1,-14 -15,-14 -8,-34"/>
      <polygon points="-2,-27 -14,-27 -8,-44"/>
    </g>
    <g transform="translate(415,318)">
      <polygon points="0,0 -22,0 -11,-28"/>
      <polygon points="-2,-18 -20,-18 -11,-44"/>
      <polygon points="-3,-34 -19,-34 -11,-56"/>
    </g>
    <g transform="translate(448,318)">
      <polygon points="0,0 -18,0 -9,-24"/>
      <polygon points="-1,-15 -17,-15 -9,-38"/>
      <polygon points="-2,-29 -16,-29 -9,-48"/>
    </g>
    <g transform="translate(478,318)">
      <polygon points="0,0 -14,0 -7,-18"/>
      <polygon points="-1,-11 -13,-11 -7,-28"/>
    </g>
  </g>

  <!-- Cabin (left shore) -->
  <g>
    <rect x="55" y="285" width="58" height="33" fill="#1a1430"/>
    <polygon points="48,285 120,285 84,258" fill="#241a3e"/>
    <rect x="98" y="262" width="8" height="16" fill="#1a1430"/>
    <!-- Chimney smoke -->
    <path d="M102,258 q-4,-8 2,-14 q6,-6 1,-14" stroke="#9a94b8" stroke-width="2.5"
          fill="none" opacity="0.35" stroke-linecap="round"/>
    <!-- Warm window -->
    <circle cx="80" cy="300" r="14" fill="url(#fireflyGlow)" opacity="0.5"/>
    <rect x="74" y="294" width="13" height="12" fill="#ffcf5c"/>
    <line x1="80.5" y1="294" x2="80.5" y2="306" stroke="#1a1430" stroke-width="1.5"/>
    <line x1="74" y1="300" x2="87" y2="300" stroke="#1a1430" stroke-width="1.5"/>
    <!-- Door -->
    <rect x="96" y="300" width="10" height="18" fill="#0e0b20"/>
  </g>

  <!-- Lake -->
  <rect x="0" y="320" width="500" height="180" fill="url(#lake)"/>

  <!-- Moon reflection -->
  <g stroke="#f5f0da" stroke-linecap="round">
    <line x1="338" y1="332" x2="384" y2="332" stroke-width="4" opacity="0.55"/>
    <line x1="346" y1="344" x2="376" y2="344" stroke-width="3.5" opacity="0.45"/>
    <line x1="334" y1="357" x2="388" y2="357" stroke-width="3" opacity="0.4"/>
    <line x1="350" y1="371" x2="372" y2="371" stroke-width="3" opacity="0.35"/>
    <line x1="340" y1="387" x2="384" y2="387" stroke-width="2.5" opacity="0.28"/>
    <line x1="352" y1="404" x2="370" y2="404" stroke-width="2.5" opacity="0.22"/>
    <line x1="344" y1="424" x2="380" y2="424" stroke-width="2" opacity="0.16"/>
    <line x1="354" y1="448" x2="368" y2="448" stroke-width="2" opacity="0.1"/>
  </g>

  <!-- Window reflection -->
  <g stroke="#ffcf5c" stroke-linecap="round">
    <line x1="74" y1="330" x2="88" y2="330" stroke-width="3" opacity="0.45"/>
    <line x1="76" y1="340" x2="85" y2="340" stroke-width="2.5" opacity="0.3"/>
    <line x1="73" y1="352" x2="89" y2="352" stroke-width="2" opacity="0.2"/>
    <line x1="77" y1="366" x2="84" y2="366" stroke-width="2" opacity="0.12"/>
  </g>

  <!-- Subtle water ripples -->
  <g stroke="#6b64a0" stroke-width="1.2" stroke-linecap="round" opacity="0.35">
    <line x1="30" y1="345" x2="70" y2="345"/>
    <line x1="150" y1="360" x2="205" y2="360"/>
    <line x1="250" y1="340" x2="300" y2="340"/>
    <line x1="420" y1="352" x2="470" y2="352"/>
    <line x1="100" y1="390" x2="160" y2="390"/>
    <line x1="270" y1="400" x2="320" y2="400"/>
    <line x1="410" y1="395" x2="455" y2="395"/>
    <line x1="60" y1="430" x2="120" y2="430"/>
    <line x1="230" y1="445" x2="290" y2="445"/>
    <line x1="400" y1="455" x2="460" y2="455"/>
    <line x1="140" y1="470" x2="200" y2="470"/>
    <line x1="300" y1="475" x2="350" y2="475"/>
  </g>

  <!-- Fireflies -->
  <g>
    <circle cx="150" cy="295" r="7" fill="url(#fireflyGlow)"/>
    <circle cx="150" cy="295" r="1.5" fill="#e8ff9c"/>
    <circle cx="180" cy="275" r="6" fill="url(#fireflyGlow)"/>
    <circle cx="180" cy="275" r="1.3" fill="#e8ff9c"/>
    <circle cx="330" cy="290" r="6" fill="url(#fireflyGlow)"/>
    <circle cx="330" cy="290" r="1.3" fill="#e8ff9c"/>
    <circle cx="210" cy="305" r="5" fill="url(#fireflyGlow)"/>
    <circle cx="210" cy="305" r="1.2" fill="#e8ff9c"/>
  </g>
</svg>
```

The scene: a crescent of soft moonlight spilling down a still lake, jagged mountain silhouettes in two depths, pines huddled on the right shore, and on the left a small cabin — chimney smoke curling up, one golden window glowing, its light echoed faintly in the water below. A few fireflies drift along the shoreline. Quiet, cold night; warm little home.