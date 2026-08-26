# -*- coding: utf-8 -*-
"""Panel con los totales del conjunto, en el centro de la ficha."""
from .. import motor
from ..html import bi


def render(build, items_stats):
    totales, _ = motor.calcular(build, items_stats)
    if not totales:
        return ""
    perfil = motor.perfil_de(build, totales)
    filas = []
    for clave in motor.visibles(totales, perfil):
        valor = totales[clave]
        es, en_ = motor.ETIQUETAS[clave]
        destacada = " destacada" if clave in ("salud", "poder_ataque", "poder_hechizos") else ""
        filas.append(
            f'<div class="stat{destacada}">'
            + bi(es, en_, "dt")
            + f'<dd>{valor:,}</dd></div>'.replace(",", " ")
        )
    if not filas:
        return ""
    return (
        '<div class="stats">'
        + bi("Totales del equipo", "Gear totals", "h2", cls="stats-h")
        + f'<dl class="stat-list">{"".join(filas)}</dl>'
        + bi("Sólo objetos, gemas y encantamientos. Sin talentos ni beneficios de banda.",
             "Gear, gems and enchants only. No talents or raid buffs.",
             "p", cls="stats-note")
        + "</div>"
    )


CSS = """
.stats{position:relative;z-index:1;width:100%;
  background:rgba(19,17,26,.72);border:1px solid var(--ln);border-radius:9px;
  padding:11px 13px 9px}
.stats-h{font:600 10px Barlow,sans-serif;letter-spacing:1.6px;
  text-transform:uppercase;color:var(--go);text-align:center;
  padding-bottom:7px;border-bottom:1px solid var(--ln);margin-bottom:5px}
.stat-list{display:flex;flex-direction:column;gap:1px}
.stat{display:flex;justify-content:space-between;align-items:baseline;gap:10px;
  padding:2.5px 0}
.stat dt{font-size:11.5px;color:var(--tn);min-width:0;
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.stat dd{font-size:12.5px;font-weight:600;color:var(--tx);flex:0 0 auto}
.stat.destacada dd{color:var(--go)}
.stats-note{font-size:9.5px;line-height:1.4;color:var(--db);
  margin-top:7px;padding-top:6px;border-top:1px solid var(--ln);text-align:center}
@media(min-width:1440px){
  .stat dt{font-size:12px}
  .stat dd{font-size:13px}
}
@media(max-width:980px){
  .stats{max-width:340px;margin:0 auto}
}
@media(max-width:430px){
  .stats{padding:10px 11px 8px}
}
"""
