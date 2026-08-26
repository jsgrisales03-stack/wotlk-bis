# -*- coding: utf-8 -*-
"""Tarjeta de una pieza del equipo, con su tip de estadísticas.

La tarjeta es un botón: al pasar el cursor enseña las estadísticas del objeto
y al pulsarla abre el panel de detalle. En táctil no hay hover, así que allí
sólo queda el segundo gesto.
"""
from .. import textos
from ..html import bi, esc
from .icono import ic
from .objeto import CALIDAD, COLOR_RANURA, bloque_stats, texto_origen

def tooltip(p, iconos, lado, items_stats, origenes):
    cls, color = CALIDAD.get(p["calidad"], ("epic", "#a335ee"))
    pos = {"izq": "tt-right", "der": "tt-left"}.get(lado, "tt-center")
    org = texto_origen(origenes.get(str(p["id"])))
    linea = ""
    if org:
        linea = ('<p class="tt-org i18n" '
                 f'data-es="{esc(org[0])}" data-en="{esc(org[1])}">{org[0]}</p>')
    return (f'<div class="tt {pos}">'
            + bi(p["nombre"], p.get("en", p["nombre"]), "p",
                 cls="tt-nombre", extra=f' style="color:{color}"')
            + bloque_stats(p, items_stats)
            + linea
            + '</div>')


def render(p, iconos, lado, items_stats, origenes, ident):
    cls, color = CALIDAD.get(p["calidad"], ("epic", "#a335ee"))
    heroico = ('<b class="hb" title="Heroico">H</b>') if p.get("heroico") else ""
    enc = p.get("encantamiento")
    linea_enc = ""
    if enc:
        linea_enc = bi(enc["nombre"], textos.en(textos.ENCANTAMIENTOS, enc["nombre"]),
                       cls="s-enc")
    puntos = ""
    if p.get("gemas"):
        puntos = '<span class="s-dots" aria-hidden="true">' + "".join(
            f'<span class="sd" style="background:'
            f'{COLOR_RANURA.get(g["ranura"], "#888")}"></span>'
            for g in p["gemas"]
        ) + "</span>"

    tt = tooltip(p, iconos, lado, items_stats, origenes)
    etiqueta = bi(p["ranura"], textos.en(textos.RANURAS, p["ranura"]), cls="s-slot")

    return f"""<button type="button" class="slot {lado} has-tt" data-det="{ident}"
    aria-haspopup="dialog">
  <span class="s-icon {cls}">{ic(iconos, p["icono"], "si", p["nombre"])}<b class="lv">{p["ilvl"]}</b>{heroico}</span>
  <span class="s-txt">
    {etiqueta}
    {bi(p["nombre"], p.get("en", p["nombre"]), cls="s-name", extra=f' style="color:{color}"')}
    {linea_enc}{puntos}
  </span>
  {tt}
</button>"""


CSS = """
.slot{display:flex;gap:8px;align-items:center;
  background:var(--p);border:1px solid var(--ln);border-radius:7px;
  padding:6px 10px;max-width:312px;width:100%;position:relative;
  transition:border-color .15s,background .15s}
.slot.has-tt{cursor:help}
.slot.has-tt:hover,.slot.has-tt:focus-visible{border-color:var(--ln2);background:var(--p2)}
.slot.izq{flex-direction:row-reverse;text-align:right}
.slot.btm{max-width:226px}
.s-icon{position:relative;flex:0 0 auto;display:block}
.si{width:36px;height:36px;display:block;border-radius:5px;border:2px solid var(--ln2)}
.epic .si{border-color:var(--ep)}
.legendary .si{border-color:var(--lg)}
.lv{position:absolute;left:50%;transform:translateX(-50%);bottom:-6px;
  background:#08070b;border:1px solid var(--ln2);border-radius:3px;
  font-size:9.5px;padding:0 4px;color:var(--go);font-weight:700;line-height:14px}
.hb{position:absolute;top:-5px;right:-5px;background:#3d2246;color:#e3a9ff;
  border-radius:2px;font-size:8px;padding:0 3px;font-weight:700;
  border:1px solid #5a3570;line-height:13px}
.s-txt{min-width:0;flex:1;display:block}
.s-slot{display:block;font-size:9px;letter-spacing:1.1px;text-transform:uppercase;
  color:var(--db);line-height:1.3}
.s-name{display:block;font-size:12.5px;font-weight:600;line-height:1.25;
  text-wrap:balance}
.s-enc{display:block;font-size:10.5px;color:var(--gr);font-weight:500;
  margin-top:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.s-dots{display:flex;gap:3px;margin-top:3px}
.slot.izq .s-dots{justify-content:flex-end}
.sd{width:7px;height:7px;border-radius:1.5px;transform:rotate(45deg)}

/* La tarjeta es un botón: al pasar el cursor muestra las estadísticas y al
   pulsarla abre el panel completo. */
.slot{font:inherit;color:inherit;text-align:left;cursor:pointer;-webkit-appearance:none;appearance:none}

.tt{display:none;position:absolute;z-index:100;
  background:#12101a;border:1px solid var(--ln2);border-radius:8px;
  padding:10px 13px;width:268px;box-shadow:0 10px 34px rgba(0,0,0,.7);
  pointer-events:none;text-align:left}
.slot.has-tt:hover .tt,.slot.has-tt:focus-visible .tt{display:block}
.tt-right{left:calc(100% + 10px);top:50%;transform:translateY(-50%)}
.tt-left{right:calc(100% + 10px);top:50%;transform:translateY(-50%)}
.tt-center{bottom:calc(100% + 8px);left:50%;transform:translateX(-50%)}
.tt p{font-size:11.5px;line-height:1.45;color:#c8c2d6}
.tt-nombre{font-size:13px;font-weight:600;line-height:1.3;margin-bottom:2px}
.tt-heroico{color:var(--gr)}
.tt-ilvl{color:var(--go)}
.tt-ranura{color:var(--tn);margin-bottom:3px}
.tt-prim{color:#e4dff0}
.tt-soc{display:flex;align-items:center;gap:6px;color:var(--tn);margin-top:2px}
.tt-sd{width:8px;height:8px;border-radius:2px;transform:rotate(45deg);flex:0 0 auto}
.tt-bono{color:var(--tn)}
.tt-eq{color:var(--gr);margin-top:2px}
.tt-skip{color:#d99b3c;font-size:11px;margin-left:3px}
.tt-org{margin-top:7px;padding-top:6px;border-top:1px solid var(--ln);
  color:var(--tn);font-size:11px;line-height:1.4}
.tt-org b{color:var(--go);font-weight:600}
@media(min-width:1440px){
  .slot{max-width:388px}
  .slot.btm{max-width:276px}
  .s-name{font-size:13px}
}
@media(min-width:1800px){
  .slot{max-width:432px}
  .slot.btm{max-width:308px}
  .s-name{font-size:13.5px}
  .s-enc{font-size:11px}
  .si{width:40px;height:40px}
}
@media(max-width:980px){
  .slot,.slot.izq{flex-direction:row;text-align:left;max-width:100%}
  .slot.izq .s-dots{justify-content:flex-start}
  .slot.btm{max-width:100%}
  /* En táctil no hay hover: la pieza se pulsa y se abre el diálogo. */
  .slot.has-tt{padding-right:24px}
  .slot.has-tt::after{content:"";position:absolute;right:10px;top:50%;
    width:6px;height:6px;margin-top:-4px;
    border-right:1.5px solid var(--db);border-bottom:1.5px solid var(--db);
    transform:rotate(45deg);transition:transform .15s ease,border-color .15s ease}
  .slot.has-tt:focus-within::after{transform:rotate(-135deg);margin-top:-1px;
    border-color:var(--gr)}
  .tt{display:none!important}
}
@media(max-width:430px){
  .slot{padding:5px 9px;gap:7px}
  .si{width:32px;height:32px}
  .s-name{font-size:12px}
  .s-enc{font-size:10px}
}
"""
