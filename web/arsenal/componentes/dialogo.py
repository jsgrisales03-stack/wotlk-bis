# -*- coding: utf-8 -*-
"""Diálogo de detalle de un objeto.

Cada pieza deja en la página un panel oculto; al pulsarla el script lo copia
dentro del diálogo. Así el contenido se genera una sola vez y sigue siendo
traducible por el conmutador de idioma.
"""
from .. import textos
from ..html import bi, esc
from .icono import ic
from .objeto import CALIDAD, COLOR_RANURA, bloque_stats, texto_origen

MARCO = """<div class="modal" id="modal" hidden>
  <div class="modal-fondo" data-cerrar></div>
  <div class="modal-caja" role="dialog" aria-modal="true" aria-labelledby="modal-tit">
    <button type="button" class="modal-x" data-cerrar aria-label="Cerrar"
      data-i18n-title data-title-es="Cerrar" data-title-en="Close">&times;</button>
    <div class="modal-cuerpo" id="modal-tit"></div>
  </div>
</div>"""


def panel(p, iconos, items_stats, origenes, ident):
    """Panel que se abre al pulsar una pieza. Va oculto en la página y el
    script lo copia dentro del diálogo."""
    cls, color = CALIDAD.get(p["calidad"], ("epic", "#a335ee"))
    partes = [
        '<div class="det-cab">',
        f'<span class="s-icon {cls}">' + ic(iconos, p["icono"], "si", p["nombre"])
        + f'<b class="lv">{p["ilvl"]}</b>'
        + ('<b class="hb">H</b>' if p.get("heroico") else "") + '</span>',
        '<div class="det-tit">',
        bi(p["nombre"], p.get("en", p["nombre"]), "h3", extra=f' style="color:{color}"'),
        bi(p["ranura"], textos.en(textos.RANURAS, p["ranura"]), "p", cls="det-ranura"),
        '</div></div>',
        '<div class="det-stats">' + bloque_stats(p, items_stats) + '</div>',
    ]

    gemas = p.get("gemas", [])
    if gemas:
        filas = []
        for g in gemas:
            color_g = COLOR_RANURA.get(g["ranura"], "#888")
            marca = ('<span class="tt-skip" title="No respeta el color de la ranura"'
                     ' aria-hidden="true">↯</span>') if g.get("ignora_color") else ""
            filas.append(
                '<li class="det-fila">'
                f'<span class="tt-dot" style="background:{color_g}" aria-hidden="true"></span>'
                + ic(iconos, g["icono"], "det-ic", "")
                + '<div>' + bi(g["gema"], textos.en(textos.GEMAS, g["gema"]), "b") + marca
                + bi(g["efecto"], textos.en(textos.EFECTOS, g["efecto"])) + '</div></li>')
        partes.append('<section class="det-sec">'
                      + bi("Gemas", "Gems", "h4")
                      + f'<ul class="det-lista">{"".join(filas)}</ul></section>')

    enc = p.get("encantamiento")
    if enc:
        extra = ""
        if enc.get("origen"):
            extra = bi(enc["origen"], textos.en(textos.ORIGENES, enc["origen"]),
                       "span", cls="det-fuente")
        partes.append(
            '<section class="det-sec">' + bi("Encantamiento", "Enchant", "h4")
            + '<ul class="det-lista"><li class="det-fila">'
            + ic(iconos, enc["icono"], "det-ic", "")
            + '<div>' + bi(enc["nombre"], textos.en(textos.ENCANTAMIENTOS, enc["nombre"]), "b")
            + bi(enc["efecto"], textos.en(textos.EFECTOS, enc["efecto"])) + extra
            + '</div></li></ul></section>')

    org = texto_origen(origenes.get(str(p["id"])))
    if org:
        partes.append('<section class="det-sec det-origen">'
                      + bi("Cómo conseguirlo", "How to get it", "h4")
                      + f'<p class="i18n" data-es="{esc(org[0])}" data-en="{esc(org[1])}">{org[0]}</p>'
                      + '</section>')

    return f'<div class="det-fuente-html" id="{ident}" hidden>{"".join(partes)}</div>'


SCRIPT_DETALLE = """<script>
(function(){
  var modal = document.getElementById('modal');
  if (!modal) return;
  var cuerpo = modal.querySelector('.modal-cuerpo');
  var ultimo = null;

  function abrir(id){
    var origen = document.getElementById(id);
    if (!origen) return;
    cuerpo.innerHTML = origen.innerHTML;
    modal.hidden = false;
    document.body.style.overflow = 'hidden';
    if (window.__idioma) window.__idioma();
    var x = modal.querySelector('.modal-x');
    if (x) x.focus();
  }

  function cerrar(){
    modal.hidden = true;
    cuerpo.innerHTML = '';
    document.body.style.overflow = '';
    if (ultimo) { ultimo.focus(); ultimo = null; }
  }

  // Cualquier elemento con data-det abre su panel, no sólo las piezas
  // de equipo: los talentos usan el mismo mecanismo.
  document.querySelectorAll('[data-det]').forEach(function(b){
    b.addEventListener('click', function(){ ultimo = b; abrir(b.dataset.det); });
  });
  modal.querySelectorAll('[data-cerrar]').forEach(function(e){
    e.addEventListener('click', cerrar);
  });
  document.addEventListener('keydown', function(e){
    if (e.key === 'Escape' && !modal.hidden) cerrar();
  });
})();
</script>"""


CSS = """
/* Diálogo de detalle. */
.paneles{display:none}
.modal{position:fixed;inset:0;z-index:400;display:flex;
  align-items:center;justify-content:center;padding:20px}
.modal[hidden]{display:none}
.modal-fondo{position:absolute;inset:0;background:rgba(6,5,10,.78);
  backdrop-filter:blur(3px)}
.modal-caja{position:relative;z-index:1;width:100%;max-width:430px;
  max-height:86vh;overflow-y:auto;
  background:#14121d;border:1px solid var(--ln2);border-radius:13px;
  padding:20px 22px 22px;box-shadow:0 24px 70px rgba(0,0,0,.75)}
.modal-x{position:absolute;top:10px;right:12px;border:0;background:transparent;
  color:var(--tn);font-size:24px;line-height:1;cursor:pointer;padding:4px 8px;
  border-radius:6px}
.modal-x:hover,.modal-x:focus-visible{color:var(--tx);background:var(--p2)}

.det-cab{display:flex;gap:13px;align-items:flex-start;padding-right:26px}
.det-cab .si{width:46px;height:46px}
.det-tit h3{font:600 15.5px/1.25 Barlow,sans-serif;text-wrap:balance}
.det-ranura{font-size:10px;letter-spacing:1.2px;text-transform:uppercase;
  color:var(--db);margin-top:3px}
.det-stats{margin-top:14px;padding-top:12px;border-top:1px solid var(--ln)}
.det-stats p{font-size:12px;line-height:1.5;color:#c8c2d6}
.det-sec{margin-top:16px;padding-top:13px;border-top:1px solid var(--ln)}
.det-sec h4{font:600 10px Barlow,sans-serif;letter-spacing:1.6px;
  text-transform:uppercase;color:var(--go);margin-bottom:8px}
.det-lista{list-style:none;display:flex;flex-direction:column;gap:9px}
.det-fila{display:flex;gap:9px;align-items:flex-start}
.det-ic{width:26px;height:26px;border-radius:5px;flex:0 0 auto;border:1px solid var(--ln2)}
.det-fila b{display:block;font-size:12.5px;font-weight:600;color:#d5cee3;line-height:1.3}
.det-fila span{display:block;font-size:11.5px;color:var(--tn);line-height:1.4}
.det-fuente{color:var(--db);font-size:10.5px;margin-top:2px}
.det-origen p{font-size:12.5px;line-height:1.55;color:var(--tx)}
.det-origen b{color:var(--go);font-weight:600}
@media(max-width:980px){
  .modal-caja{max-width:100%;padding:18px 16px 20px}
}

/* Con tres árboles al lado los 430px de la tarjeta se quedan cortos. La regla
   va al final a propósito: el @media de arriba fuerza max-width:100% y con
   la misma especificidad ganaría la última declarada. */
.modal-caja:has(.tal-mapa){max-width:min(760px,calc(100vw - 24px))}

/* Cuando el contenido no cabe, la barra del sistema es un tajo gris sobre un
   panel oscuro. Se adelgaza y se tiñe para que acompañe en vez de estorbar. */
.modal-caja{scrollbar-width:thin;scrollbar-color:var(--ln2) transparent}
.modal-caja::-webkit-scrollbar{width:8px}
.modal-caja::-webkit-scrollbar-track{background:transparent}
.modal-caja::-webkit-scrollbar-thumb{background:var(--ln2);border-radius:4px;
  border:2px solid transparent;background-clip:content-box}
.modal-caja::-webkit-scrollbar-thumb:hover{background:var(--db);
  border:2px solid transparent;background-clip:content-box}
"""