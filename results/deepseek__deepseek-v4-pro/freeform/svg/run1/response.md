Here’s a dreamy night landscape in SVG, with a glowing moon, layered mountains, and a dark lake reflecting the light.
```svg
<svg width="500" height="500" viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Sky gradient -->
    <linearGradient id="skyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#06061a"/>
      <stop offset="35%" stop-color="#0c0a28"/>
      <stop offset="65%" stop-color="#151035"/>
      <stop offset="85%" stop-color="#1a1138"/>
      <stop offset="100%" stop-color="#1e1435"/>
    </linearGradient>

    <!-- Moon glow radial gradient -->
    <radialGradient id="moonGlow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#ffe9b8" stop-opacity="0.55"/>
      <stop offset="18%" stop-color="#ffdfa0" stop-opacity="0.35"/>
      <stop offset="38%" stop-color="#ffd080" stop-opacity="0.15"/>
      <stop offset="60%" stop-color="#ffc860" stop-opacity="0.04"/>
      <stop offset="80%" stop-color="#ffb840" stop-opacity="0.008"/>
      <stop offset="100%" stop-color="#ffa020" stop-opacity="0"/>
    </radialGradient>

    <!-- Moon surface gradient -->
    <radialGradient id="moonSurface" cx="0.45" cy="0.42" r="0.55">
      <stop offset="0%" stop-color="#fff8ee"/>
      <stop offset="40%" stop-color="#fef0d5"/>
      <stop offset="75%" stop-color="#f5e2b8"/>
      <stop offset="100%" stop-color="#e8d09a"/>
    </radialGradient>

    <!-- Lake gradient -->
    <linearGradient id="lakeGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0e0b20"/>
      <stop offset="15%" stop-color="#0c0a1e"/>
      <stop offset="50%" stop-color="#09071a"/>
      <stop offset="100%" stop-color="#060510"/>
    </linearGradient>

    <!-- Moon reflection gradient -->
    <linearGradient id="reflectionGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffe4b0" stop-opacity="0.7"/>
      <stop offset="12%" stop-color="#ffd890" stop-opacity="0.45"/>
      <stop offset="35%" stop-color="#ffcc70" stop-opacity="0.2"/>
      <stop offset="60%" stop-color="#ffc050" stop-opacity="0.06"/>
      <stop offset="85%" stop-color="#ffb030" stop-opacity="0.01"/>
      <stop offset="100%" stop-color="#ffa010" stop-opacity="0"/>
    </linearGradient>

    <!-- Reflection shimmer gradient -->
    <linearGradient id="shimmerGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#fff5e0" stop-opacity="0.5"/>
      <stop offset="30%" stop-color="#ffe8c0" stop-opacity="0.2"/>
      <stop offset="70%" stop-color="#ffd090" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="#ffb050" stop-opacity="0"/>
    </linearGradient>

    <!-- Fog gradient -->
    <linearGradient id="fogGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#b8c8e0" stop-opacity="0"/>
      <stop offset="30%" stop-color="#b0c0d8" stop-opacity="0.06"/>
      <stop offset="70%" stop-color="#a0b0c8" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#8098b0" stop-opacity="0.25"/>
    </linearGradient>

    <!-- Cloud gradient -->
    <linearGradient id="cloudGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#d8c8e8" stop-opacity="0"/>
      <stop offset="30%" stop-color="#d0c0e0" stop-opacity="0.12"/>
      <stop offset="60%" stop-color="#c8b8d8" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#b8a8c8" stop-opacity="0"/>
    </linearGradient>

    <!-- Shooting star gradient -->
    <linearGradient id="shootingStar" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.9"/>
      <stop offset="25%" stop-color="#ffffff" stop-opacity="0.6"/>
      <stop offset="60%" stop-color="#ffe8d0" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#ffe0c0" stop-opacity="0"/>
    </linearGradient>

    <!-- Firefly glow -->
    <radialGradient id="fireflyGlow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#e8ff80" stop-opacity="0.9"/>
      <stop offset="25%" stop-color="#d8f060" stop-opacity="0.5"/>
      <stop offset="60%" stop-color="#b0d030" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#80a010" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- Sky background -->
  <rect x="0" y="0" width="500" height="310" fill="url(#skyGrad)"/>

  <!-- ===== STARS ===== -->
  <!-- Tiny stars -->
  <circle cx="25" cy="35" r="0.7" fill="white" opacity="0.55"/>
  <circle cx="65" cy="18" r="0.5" fill="white" opacity="0.4"/>
  <circle cx="110" cy="55" r="0.8" fill="white" opacity="0.6"/>
  <circle cx="155" cy="28" r="0.5" fill="white" opacity="0.35"/>
  <circle cx="210" cy="12" r="0.6" fill="white" opacity="0.5"/>
  <circle cx="260" cy="45" r="0.7" fill="white" opacity="0.55"/>
  <circle cx="310" cy="22" r="0.5" fill="white" opacity="0.4"/>
  <circle cx="355" cy="58" r="0.6" fill="white" opacity="0.5"/>
  <circle cx="400" cy="15" r="0.7" fill="white" opacity="0.55"/>
  <circle cx="445" cy="38" r="0.5" fill="white" opacity="0.45"/>
  <circle cx="480" cy="20" r="0.6" fill="white" opacity="0.5"/>
  <circle cx="45" cy="85" r="0.5" fill="white" opacity="0.4"/>
  <circle cx="90" cy="105" r="0.7" fill="white" opacity="0.5"/>
  <circle cx="140" cy="70" r="0.5" fill="white" opacity="0.35"/>
  <circle cx="310" cy="80" r="0.6" fill="white" opacity="0.5"/>
  <circle cx="370" cy="95" r="0.5" fill="white" opacity="0.4"/>
  <circle cx="430" cy="65" r="0.7" fill="white" opacity="0.55"/>
  <circle cx="470" cy="90" r="0.5" fill="white" opacity="0.4"/>
  <circle cx="15" cy="140" r="0.6" fill="white" opacity="0.45"/>
  <circle cx="75" cy="155" r="0.5" fill="white" opacity="0.4"/>
  <circle cx="300" cy="130" r="0.5" fill="white" opacity="0.35"/>
  <circle cx="340" cy="155" r="0.6" fill="white" opacity="0.45"/>
  <circle cx="395" cy="120" r="0.5" fill="white" opacity="0.4"/>
  <circle cx="460" cy="145" r="0.7" fill="white" opacity="0.5"/>
  <circle cx="10" cy="200" r="0.5" fill="white" opacity="0.35"/>
  <circle cx="55" cy="230" r="0.6" fill="white" opacity="0.4"/>
  <circle cx="130" cy="175" r="0.5" fill="white" opacity="0.35"/>
  <circle cx="280" cy="195" r="0.5" fill="white" opacity="0.3"/>
  <circle cx="440" cy="185" r="0.6" fill="white" opacity="0.4"/>
  <circle cx="490" cy="220" r="0.5" fill="white" opacity="0.35"/>

  <!-- Medium stars -->
  <circle cx="40" cy="50" r="1.1" fill="white" opacity="0.7"/>
  <circle cx="130" cy="30" r="1.0" fill="white" opacity="0.65"/>
  <circle cx="230" cy="55" r="1.2" fill="white" opacity="0.75"/>
  <circle cx="330" cy="40" r="1.0" fill="white" opacity="0.65"/>
  <circle cx="410" cy="45" r="1.1" fill="white" opacity="0.7"/>
  <circle cx="80" cy="120" r="1.0" fill="white" opacity="0.6"/>
  <circle cx="170" cy="95" r="1.2" fill="white" opacity="0.7"/>
  <circle cx="270" cy="110" r="1.0" fill="white" opacity="0.6"/>
  <circle cx="380" cy="75" r="1.1" fill="white" opacity="0.65"/>
  <circle cx="450" cy="110" r="1.0" fill="white" opacity="0.6"/>
  <circle cx="100" cy="170" r="1.0" fill="white" opacity="0.55"/>
  <circle cx="200" cy="150" r="1.1" fill="white" opacity="0.6"/>
  <circle cx="350" cy="180" r="1.0" fill="white" opacity="0.55"/>
  <circle cx="420" cy="160" r="1.0" fill="white" opacity="0.6"/>
  <circle cx="30" cy="260" r="0.9" fill="white" opacity="0.5"/>
  <circle cx="480" cy="255" r="0.9" fill="white" opacity="0.5"/>

  <!-- Bright stars -->
  <circle cx="70" cy="75" r="1.8" fill="white" opacity="0.85"/>
  <circle cx="190" cy="35" r="1.6" fill="white" opacity="0.8"/>
  <circle cx="350" cy="25" r="1.7" fill="white" opacity="0.85"/>
  <circle cx="460" cy="55" r="1.5" fill="white" opacity="0.8"/>
  <circle cx="120" cy="140" r="1.6" fill="white" opacity="0.75"/>
  <circle cx="310" cy="160" r="1.5" fill="white" opacity="0.7"/>
  <circle cx="415" cy="100" r="1.7" fill="white" opacity="0.8"/>
  <circle cx="50" cy="190" r="1.4" fill="white" opacity="0.65"/>

  <!-- Star sparkle cross (bright star with subtle cross) -->
  <circle cx="70" cy="75" r="2.2" fill="white" opacity="0.25"/>
  <line x1="67" y1="75" x2="73" y2="75" stroke="white" stroke-width="0.4" opacity="0.5"/>
  <line x1="70" y1="72" x2="70" y2="78" stroke="white" stroke-width="0.4" opacity="0.5"/>
  <circle cx="350" cy="25" r="2.0" fill="white" opacity="0.25"/>
  <line x1="347" y1="25" x2="353" y2="25" stroke="white" stroke-width="0.4" opacity="0.5"/>
  <line x1="350" y1="22" x2="350" y2="28" stroke="white" stroke-width="0.4" opacity="0.5"/>

  <!-- ===== SHOOTING STAR ===== -->
  <line x1="380" y1="10" x2="340" y2="55" stroke="url(#shootingStar)" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="340" cy="55" r="1.8" fill="white" opacity="0.7"/>
  <circle cx="340" cy="55" r="3.5" fill="white" opacity="0.15"/>

  <!-- ===== MOON GLOW (large halo) ===== -->
  <circle cx="190" cy="140" r="160" fill="url(#moonGlow)"/>
  <circle cx="190" cy="140" r="100" fill="url(#moonGlow)" opacity="0.7"/>
  <circle cx="190" cy="140" r="70" fill="#ffe8b8" opacity="0.12"/>

  <!-- ===== WISPY CLOUDS NEAR MOON ===== -->
  <ellipse cx="140" cy="115" rx="45" ry="8" fill="url(#cloudGrad)" transform="rotate(-15 140 115)"/>
  <ellipse cx="240" cy="125" rx="50" ry="7" fill="url(#cloudGrad)" transform="rotate(12 240 125)"/>
  <ellipse cx="160" cy="165" rx="35" ry="5" fill="url(#cloudGrad)" transform="rotate(-8 160 165)"/>
  <ellipse cx="230" cy="155" rx="40" ry="6" fill="url(#cloudGrad)" transform="rotate(10 230 155)"/>

  <!-- ===== THE MOON ===== -->
  <circle cx="190" cy="140" r="50" fill="url(#moonSurface)"/>

  <!-- Moon craters (subtle darker spots) -->
  <circle cx="175" cy="125" r="8" fill="#d4c090" opacity="0.35"/>
  <circle cx="200" cy="115" r="5" fill="#d4c090" opacity="0.3"/>
  <circle cx="185" cy="150" r="10" fill="#d4c090" opacity="0.3"/>
  <circle cx="210" cy="140" r="6" fill="#d4c090" opacity="0.28"/>
  <circle cx="170" cy="140" r="4" fill="#d4c090" opacity="0.32"/>
  <circle cx="195" cy="135" r="3.5" fill="#d4c090" opacity="0.25"/>
  <circle cx="180" cy="160" r="5.5" fill="#d4c090" opacity="0.3"/>
  <circle cx="205" cy="155" r="4" fill="#d4c090" opacity="0.25"/>
  <circle cx="190" cy="118" r="3" fill="#d4c090" opacity="0.2"/>

  <!-- Moon subtle highlight -->
  <circle cx="178" cy="128" r="25" fill="white" opacity="0.06"/>

  <!-- ===== BACKGROUND MOUNTAINS (lighter, further) ===== -->
  <path d="M0,310 L25,250 L60,225 L100,255 L145,210 L185,240 L220,198 L260,228 L300,205 L340,235 L380,215 L420,242 L455,220 L485,248 L500,230 L500,310 Z" 
        fill="#1a1635"/>

  <!-- Background mountain snow caps -->
  <polygon points="145,210 152,228 138,228" fill="#2a2650" opacity="0.7"/>
  <polygon points="220,198 228,218 212,218" fill="#2a2650" opacity="0.7"/>
  <polygon points="300,205 307,222 293,222" fill="#2a2650" opacity="0.65"/>
  <polygon points="380,215 387,232 373,232" fill="#2a2650" opacity="0.7"/>

  <!-- ===== FOREGROUND MOUNTAINS (darker, closer) ===== -->
  <path d="M0,310 L0,285 L45,220 L90,260 L140,195 L195,248 L240,190 L290,235 L330,185 L375,230 L410,200 L450,245 L485,215 L500,195 L500,310 Z" 
        fill="#0e0b1e"/>

  <!-- Foreground mountain snow caps -->
  <polygon points="140,195 148,218 132,218" fill="#1c1840" opacity="0.6"/>
  <polygon points="240,190 249,214 231,214" fill="#1c1840" opacity="0.6"/>
  <polygon points="330,185 339,210 321,210" fill="#1c1840" opacity="0.55"/>
  <polygon points="410,200 418,222 402,222" fill="#1c1840" opacity="0.6"/>

  <!-- ===== FOG AT HORIZON ===== -->
  <rect x="0" y="280" width="500" height="50" fill="url(#fogGrad)"/>

  <!-- ===== LAKE ===== -->
  <rect x="0" y="310" width="500" height="190" fill="url(#lakeGrad)"/>

  <!-- ===== MOON REFLECTION ON LAKE ===== -->
  <!-- Main reflection column -->
  <polygon points="178,312 202,312 225,430 155,430" fill="url(#reflectionGrad)"/>

  <!-- Reflection shimmer lines -->
  <rect x="172" y="318" width="36" height="2.5" rx="1.2" fill="url(#shimmerGrad)"/>
  <rect x="168" y="326" width="44" height="2" rx="1" fill="url(#shimmerGrad)" opacity="0.8"/>
  <rect x="175" y="335" width="32" height="1.5" rx="0.75" fill="url(#shimmerGrad)" opacity="0.7"/>
  <rect x="165" y="342" width="50" height="2.5" rx="1.2" fill="url(#shimmerGrad)" opacity="0.6"/>
  <rect x="170" y="352" width="40" height="2" rx="1" fill="url(#shimmerGrad)" opacity="0.5"/>
  <rect x="160" y="360" width="58" height="3" rx="1.5" fill="url(#shimmerGrad)" opacity="0.45"/>
  <rect x="168" y="372" width="44" height="2" rx="1" fill="url(#shimmerGrad)" opacity="0.35"/>
  <rect x="162" y="382" width="54" height="2.5" rx="1.2" fill="url(#shimmerGrad)" opacity="0.25"/>
  <rect x="170" y="395" width="38" height="1.5" rx="0.75" fill="url(#shimmerGrad)" opacity="0.15"/>
  <rect x="165" y="408" width="48" height="2" rx="1" fill="url(#shimmerGrad)" opacity="0.08"/>
  <rect x="172" y="420" width="34" height="1.5" rx="0.75" fill="url(#shimmerGrad)" opacity="0.04"/>
  <rect x="168" y="430" width="42" height="1" rx="0.5" fill="url(#shimmerGrad)" opacity="0.02"/>

  <!-- Subtle scattered reflection dots (ripple highlights) -->
  <circle cx="195" cy="330" r="1.5" fill="white" opacity="0.2"/>
  <circle cx="182" cy="345" r="1.8" fill="white" opacity="0.15"/>
  <circle cx="200" cy="358" r="1.3" fill="white" opacity="0.12"/>
  <circle cx="178" cy="370" r="1.6" fill="white" opacity="0.1"/>
  <circle cx="205" cy="388" r="1.4" fill="white" opacity="0.07"/>
  <circle cx="172" cy="400" r="1.2" fill="white" opacity="0.05"/>

  <!-- ===== LAKE RIPPLE TEXTURE (subtle horizontal lines across the lake) ===== -->
  <line x1="0" y1="325" x2="500" y2="325" stroke="#3a3070" stroke-width="0.3" opacity="0.08"/>
  <line x1="0" y1="345" x2="500" y2="345" stroke="#2a2560" stroke-width="0.4" opacity="0.06"/>
  <line x1="0" y1="370" x2="500" y2="370" stroke="#2a2560" stroke-width="0.3" opacity="0.07"/>
  <line x1="0" y1="400" x2="500" y2="400" stroke="#201850" stroke-width="0.35" opacity="0.06"/>
  <line x1="0" y1="430" x2="500" y2="430" stroke="#201850" stroke-width="0.3" opacity="0.05"/>
  <line x1="0" y1="460" x2="500" y2="460" stroke="#151040" stroke-width="0.3" opacity="0.05"/>
  <line x1="0" y1="485" x2="500" y2="485" stroke="#151040" stroke-width="0.25" opacity="0.04"/>

  <!-- Additional subtle ripple near shore -->
  <line x1="0" y1="315" x2="500" y2="315" stroke="#6a60a0" stroke-width="0.5" opacity="0.1"/>

  <!-- ===== PINE TREES (silhouettes along shore) ===== -->
  
  <!-- Tree cluster left -->
  <polygon points="38,312 46,275 54,312" fill="#06040e"/>
  <polygon points="52,312 61,268 70,312" fill="#05040c"/>
  <polygon points="66,312 73,280 80,312" fill="#06040e"/>
  <polygon points="80,312 90,260 100,312" fill="#05030c"/>
  <polygon points="95,312 104,272 113,312" fill="#06040e"/>
  <polygon points="108,312 116,282 124,312" fill="#05040c"/>

  <!-- Tree cluster right -->
  <polygon points="365,312 374,268 383,312" fill="#06040e"/>
  <polygon points="378,312 388,258 398,312" fill="#05030c"/>
  <polygon points="393,312 401,275 409,312" fill="#06040e"/>
  <polygon points="404,312 414,262 424,312" fill="#05030c"/>
  <polygon points="418,312 427,278 436,312" fill="#06040e"/>
  <polygon points="432,312 440,285 448,312" fill="#05040c"/>
  <polygon points="442,312 452,270 462,312" fill="#05030c"/>

  <!-- Scattered foreground trees -->
  <polygon points="15,312 26,255 37,312" fill="#05030c"/>
  <polygon points="330,312 340,265 350,312" fill="#06040e"/>
  <polygon points="460,312 470,258 480,312" fill="#05030c"/>
  <polygon points="475,312 484,272 493,312" fill="#06040e"/>

  <!-- Small bushes near trees -->
  <ellipse cx="45" cy="312" rx="8" ry="4" fill="#06040e"/>
  <ellipse cx="100" cy="312" rx="7" ry="3.5" fill="#05030c"/>
  <ellipse cx="370" cy="312" rx="9" ry="4" fill="#06040e"/>
  <ellipse cx="430" cy="312" rx="8" ry="3.5" fill="#05030c"/>
  <ellipse cx="470" cy="312" rx="7" ry="4" fill="#06040e"/>

  <!-- ===== FIREFLIES ===== -->
  <!-- Left side fireflies -->
  <circle cx="55" cy="290" r="5" fill="url(#fireflyGlow)"/>
  <circle cx="55" cy="290" r="1.5" fill="#e8ff80" opacity="0.85"/>
  
  <circle cx="90" cy="305" r="4.5" fill="url(#fireflyGlow)"/>
  <circle cx="90" cy="305" r="1.3" fill="#e8ff80" opacity="0.8"/>
  
  <circle cx="35" cy="275" r="4" fill="url(#fireflyGlow)"/>
  <circle cx="35" cy="275" r="1.2" fill="#e0f870" opacity="0.75"/>

  <circle cx="120" cy="295" r="3.5" fill="url(#fireflyGlow)"/>
  <circle cx="120" cy="295" r="1.0" fill="#d8f060" opacity="0.7"/>

  <!-- Right side fireflies -->
  <circle cx="355" cy="288" r="5" fill="url(#fireflyGlow)"/>
  <circle cx="355" cy="288" r="1.5" fill="#e8ff80" opacity="0.85"/>

  <circle cx="400" cy="300" r="4.5" fill="url(#fireflyGlow)"/>
  <circle cx="400" cy="300" r="1.3" fill="#e8ff80" opacity="0.8"/>

  <circle cx="440" cy="282" r="4" fill="url(#fireflyGlow)"/>
  <circle cx="440" cy="282" r="1.1" fill="#e0f870" opacity="0.75"/>

  <circle cx="485" cy="295" r="3.5" fill="url(#fireflyGlow)"/>
  <circle cx="485" cy="295" r="1.0" fill="#d8f060" opacity="0.7"/>

  <!-- Distant fireflies near water -->
  <circle cx="255" cy="310" r="3" fill="url(#fireflyGlow)" opacity="0.6"/>
  <circle cx="255" cy="310" r="0.8" fill="#d8f060" opacity="0.5"/>
  <circle cx="295" cy="308" r="2.5" fill="url(#fireflyGlow)" opacity="0.5"/>
  <circle cx="295" cy="308" r="0.7" fill="#d0e850" opacity="0.4"/>
</svg>
```
The scene uses a deep violet night sky scattered with stars, a shooting star, and a soft full moon to create a calm mood. Dark pine silhouettes frame the shoreline, while the lake carries rippled reflections and a few tiny fireflies add warmth near the water’s edge.