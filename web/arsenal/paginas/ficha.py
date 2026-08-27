# -*- coding: utf-8 -*-
"""Ficha de una especialización: el paperdoll con su equipo.

Esta página sólo pone el armazón —cabecera, las dos columnas y la fila de
abajo— y compone los componentes; el marcado y los estilos de cada pieza viven
en su propio módulo.
"""
import os

from .. import datos, textos
from ..componentes import arbol, dialogo, personaje, pieza, talentos, totales
from ..html import bi
from ..plantilla import documento

# Reparto de ranuras entre las dos columnas; lo que no cae en ninguna va a la
# fila inferior, en el orden que fije la propia build.
IZQUIERDA = ["head", "neck", "shoulder", "back", "chest", "wrist"]
DERECHA = ["hands", "waist", "legs", "feet", "ring1", "ring2"]

CSS_LAYOUT = """
body{background:var(--bg);color:var(--tx);
  font:13px/1.45 Barlow,"Segoe UI",system-ui,sans-serif;
  font-variant-numeric:tabular-nums;min-height:100vh;
  display:flex;flex-direction:column}
.page{max-width:1560px;width:100%;margin:0 auto;padding:0 16px;
  flex:1;display:flex;flex-direction:column;min-height:0}

.ficha-head{text-align:center;padding:16px 0 4px;flex:0 0 auto}
.ficha-head h1{font:700 clamp(21px,3.2vw,31px)/1.1 Cinzel,Georgia,serif;
  color:#f0eaf8;letter-spacing:.4px}
.spec-lab{font-size:13px;letter-spacing:4px;text-transform:uppercase;
  color:var(--go);margin-top:5px;font-weight:500}
.rol-lab{font-size:11.5px;color:var(--tn);margin-top:4px}

.pd{flex:1;display:grid;
  grid-template-columns:1fr minmax(200px,264px) 1fr;
  grid-template-rows:1fr auto;gap:0;min-height:0;padding:6px 0 0}
.col{display:flex;flex-direction:column;gap:4px;justify-content:center;min-height:0}
.col-l{align-items:flex-end}
.col-r{align-items:flex-start}

.bot-row{grid-column:1/4;display:flex;justify-content:center;
  gap:6px;flex-wrap:wrap;padding:8px 0 0;flex:0 0 auto}

/* En pantallas grandes crece el propio paperdoll: como las tarjetas se pegan
   al centro, ensanchar la página sólo empujaría hueco hacia los lados. */
@media(min-width:1440px){
  .pd{grid-template-columns:1fr minmax(250px,336px) 1fr}
}
@media(min-width:1800px){
  .pd{grid-template-columns:1fr minmax(280px,382px) 1fr}
}
@media(max-width:980px){
  /* En vertical el contenido tiene que poder crecer. La cadena de flex:1 con
     min-height:0 dejaba la ficha a la altura de la ventana y las tarjetas se
     solapaban unas con otras. */
  .page{display:block;min-height:auto;padding-bottom:14px}
  .pd{display:flex;flex-direction:column;flex:none;min-height:auto;
    gap:8px;padding-top:10px}
  .col{align-items:stretch;justify-content:flex-start;min-height:auto;gap:5px}
  .col-l{order:2}
  .col-r{order:3}
  .bot-row{order:4;padding-top:4px}
}
@media(max-width:430px){
  .ficha-head{padding:10px 0 2px}
  .spec-lab{letter-spacing:2.5px;font-size:12px}
  .bot-row{gap:5px}
}
/* Portátiles de pantalla baja: se recorta el aire para que la ficha siga
   entrando de una sola vez, que es el objetivo del diseño. */
@media(min-width:981px) and (max-height:860px){
  .ficha-head{padding:10px 0 2px}
  .pd{padding-top:2px}
  .bot-row{padding-top:6px}
}
@media(prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
"""

CSS = (CSS_LAYOUT + pieza.CSS + personaje.CSS + talentos.CSS + arbol.CSS
       + totales.CSS + dialogo.CSS)


def construir(build_id, iconos, items_stats, origenes=None, talentos_datos=None,
              arboles=None, glifos_iconos=None):
    d = datos.build(build_id)
    origenes = origenes or {}
    tal = (talentos_datos or {}).get(build_id)
    arboles = arboles or {}
    piezas = d["piezas"]

    en_izq = [s for s in IZQUIERDA if s in piezas]
    en_der = [s for s in DERECHA if s in piezas]
    abajo = [s for s in d["orden"] if s not in en_izq and s not in en_der]

    paneles = []

    def columna(claves, lado):
        """Monta una columna y va apartando el panel de detalle de cada pieza."""
        salida = []
        for clave in claves:
            ident = "det-" + clave
            salida.append(pieza.render(piezas[clave], iconos, lado,
                                       items_stats, origenes, ident))
            paneles.append(dialogo.panel(piezas[clave], iconos,
                                         items_stats, origenes, ident))
        return "".join(salida)

    col_l = columna(en_izq, "izq")
    col_r = columna(en_der, "der")
    bot = columna(abajo, "btm")

    clase, espec = d["clase"], d["especializacion"]
    raza = d.get("raza", "Orco")
    faccion = d.get("faccion", "Horda")
    rol = d.get("rol", "")

    figura, con_personaje = personaje.render(
        build_id, raza, d.get("genero", "macho"),
        d.get("clase_icono", "spell_deathknight_classicon"),
        iconos, os.path.join(datos.ASSETS, "personajes"))

    cuerpo = f"""<div class="page">
<div class="ficha-head">
  {bi(clase, textos.en(textos.CLASES, clase), "h1")}
  {bi(espec, textos.en(textos.ESPECS, espec), "p", cls="spec-lab")}
  {bi(rol, textos.en(textos.ROLES, rol), "p", cls="rol-lab") if rol else ""}
</div>

<div class="pd">
  <div class="col col-l">{col_l}</div>
  <div class="ctr{' con-personaje' if con_personaje else ''}">
    <div class="ctr-bg" aria-hidden="true"></div>
    {figura}
    <p class="ctr-t">
      {bi(raza, textos.en(textos.RAZAS, raza), "span", cls="race")}
      {bi(faccion, textos.en(textos.FACCIONES, faccion), "span", cls="fac")}
    </p>
    {totales.render(d, items_stats)}
    {talentos.resumen(clase, tal)}
  </div>
  <div class="col col-r">{col_r}</div>
  <div class="bot-row">{bot}</div>
</div>
</div>
{dialogo.MARCO}
<div class="paneles" hidden>{"".join(paneles)}{talentos.panel(clase, espec, tal, arboles.get(arbol.CLASE_SLUG.get(clase)), iconos, glifos_iconos)}</div>"""

    titulo = f"{clase} · {espec} — {textos.MARCA_ES}"
    return documento(titulo, CSS, cuerpo, "builds", iconos)
