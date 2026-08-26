# -*- coding: utf-8 -*-
"""Paleta, fondo y tipografías: la base visual común a todas las páginas."""

TOKENS = """
:root{
  --bg:#0a090e; --p:#13111a; --p2:#1a1722; --ln:#2a2536; --ln2:#362f45;
  --tx:#ddd8e8; --tn:#918aa5; --db:#7e7494; --go:#d9b45b; --gr:#40d97e;
  --ep:#a335ee; --lg:#ff8000; --dk:#c41e3a;
  --focus:#7fd8ff;
}
*{box-sizing:border-box;margin:0;padding:0}
:focus-visible{outline:2px solid var(--focus);outline-offset:2px;border-radius:4px}
img{max-width:100%}
"""

# Textura de fondo del sitio. Va en una capa fija propia para que no se mueva
# con el scroll ni afecte al flujo; todo son gradientes y un SVG en línea, así
# que no añade ninguna petición externa.
FONDO_CSS = """
/* Fondo del sitio: capa fija propia para que no se mueva con el scroll ni
   afecte al flujo. Todo son gradientes y un SVG en línea, sin peticiones
   externas. La paleta busca el frío de Corona de Hielo.

   Cada elemento lleva su propia opacidad: agrupar la trama y el grano bajo
   una sola dejaba el grano diez veces más marcado de la cuenta. */
.fondo{position:fixed;inset:0;z-index:0;pointer-events:none;
  background-color:var(--bg);
  background-image:
    repeating-linear-gradient(115deg,
      transparent 0 74px,
      rgba(150,200,255,.022) 74px 75px,
      transparent 75px 150px),
    repeating-linear-gradient(-115deg,
      transparent 0 108px,
      rgba(150,200,255,.014) 108px 109px,
      transparent 109px 216px)}

/* Halos de color. */
.fondo::before{content:"";position:absolute;inset:0;
  background:
    radial-gradient(ellipse 1200px 620px at 50% -12%,rgba(86,150,224,.16),transparent 66%),
    radial-gradient(ellipse 700px 420px at 50% -4%,rgba(150,214,255,.08),transparent 58%),
    radial-gradient(ellipse 900px 560px at 96% 104%,rgba(126,64,178,.10),transparent 62%),
    radial-gradient(ellipse 760px 520px at 2% 64%,rgba(64,217,126,.05),transparent 60%),
    radial-gradient(ellipse 135% 95% at 50% 42%,transparent 46%,rgba(0,0,0,.6))}

/* Grano fino: rompe el plano liso sin llamar la atención. */
.fondo::after{content:"";position:absolute;inset:0;opacity:.05;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.82' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='220' height='220' filter='url(%23g)'/%3E%3C/svg%3E");
  background-size:220px 220px}

/* El contenido debe quedar por encima de la capa de fondo. */
.page{position:relative;z-index:1}
"""

FUENTES = (
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    'family=Cinzel:wght@600;700&family=Barlow:wght@400;500;600&display=swap">'
)
