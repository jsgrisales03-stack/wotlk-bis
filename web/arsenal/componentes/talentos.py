# -*- coding: utf-8 -*-
"""Talentos y glifos de una build.

En la ficha sólo cabe un resumen: el reparto por árbol. El detalle —los tres
glifos sublimes y los tres menores— se despliega en el diálogo, igual que el
detalle de una pieza de equipo, porque bajo los totales quedan cuarenta píxeles
en un portátil y el conjunto tiene que seguir entrando de una pantalla.
"""
from .. import textos
from ..html import bi, esc
from .icono import ic
from . import arbol
from .arbol import ARBOLES

IDENT = "det-talentos"



def _nombre_glifo(nombre, idioma):
    """Devuelve (español, inglés) de un glifo a partir del nombre transcrito.

    La búsqueda vive en `textos` porque tolera cómo esté escrito el nombre:
    por una mayúscula o un artículo de más, un glifo se quedaba sin traducir
    y, ahora, también sin icono.
    """
    return textos.glifo_par(nombre, idioma)


def resumen(clase, datos):
    """Barra compacta para la ficha: el reparto por árbol, pulsable."""
    reparto = (datos or {}).get("reparto")
    if not reparto:
        return ""
    arboles = ARBOLES.get(clase, [])
    partes = []
    for i, puntos in enumerate(reparto):
        es_, en_ = arboles[i] if i < len(arboles) else (str(i + 1), str(i + 1))
        principal = " tal-alto" if puntos == max(reparto) else ""
        partes.append(
            f'<span class="tal-arbol{principal}">'
            f'<b>{puntos}</b>' + bi(es_, en_, "i") + "</span>")
    return (f'<button type="button" class="talentos" data-det="{IDENT}"'
            f' aria-haspopup="dialog">'
            + bi("Talentos", "Talents", "span", cls="tal-tit")
            + f'<span class="tal-reparto">{"".join(partes)}</span>'
            + '<span class="ir" aria-hidden="true">&rsaquo;</span></button>')


def _mayuscula(n):
    """Primera letra en mayúscula, sin tocar el resto del nombre.

    La tabla guarda el fragmento tal y como aparece dentro del nombre completo
    —«Glifo de vida renovada»—, así que en minúscula. Suelto en una lista eso
    se lee como una errata.
    """
    return n[:1].upper() + n[1:] if n else n


def _lista_glifos(titulo_es, titulo_en, nombres, idioma, iconos, glifos_iconos):
    filas = []
    for n in nombres or []:
        par = _nombre_glifo(n, idioma)
        if not par:
            filas.append('<li class="glifo vacio"><span class="gi"></span>'
                         + bi("Ranura libre", "Empty slot", "span") + "</li>")
        else:
            marca = ic(iconos, (glifos_iconos or {}).get(par[1], ""),
                       "gi", par[0])
            filas.append('<li class="glifo">'
                         + (marca or '<span class="gi"></span>')
                         + bi(_mayuscula(par[0]), _mayuscula(par[1]), "span")
                         + "</li>")
    if not filas:
        return ""
    return ('<section class="det-sec">' + bi(titulo_es, titulo_en, "h4")
            + f'<ul class="glifos">{"".join(filas)}</ul></section>')


def panel(clase, espec, datos, arboles_clase=None, iconos=None,
          glifos_iconos=None):
    """Panel oculto que el diálogo copia al pulsar el resumen."""
    datos = datos or {}
    reparto = datos.get("reparto")
    if not reparto:
        return ""
    total = sum(reparto)
    partes = [
        '<div class="det-cab"><div class="det-tit">',
        bi("Talentos", "Talents", "h3"),
        bi(espec, textos.en(textos.ESPECS, espec), "p", cls="det-ranura"),
        '</div></div>',
        arbol.render(clase, datos, arboles_clase),
        '<p class="tal-total">'
        + bi(f"{total} puntos de talento", f"{total} talent points", "span") + "</p>",
    ]

    g = datos.get("glifos") or {}
    idioma = g.get("idioma") or "es"
    # Sublimes y menores son dos categorías hermanas de tres entradas cada
    # una: apiladas gastaban doscientos treinta píxeles de alto y empujaban el
    # diálogo a desplazarse. En paralelo caben en la mitad y se comparan mejor.
    sublimes = _lista_glifos("Glifos sublimes", "Major glyphs",
                             g.get("mayores"), idioma, iconos, glifos_iconos)
    menores = _lista_glifos("Glifos menores", "Minor glyphs",
                            g.get("menores"), idioma, iconos, glifos_iconos)
    if sublimes or menores:
        partes.append(f'<div class="glifos-par">{sublimes}{menores}</div>')
    return f'<div class="det-fuente-html" id="{IDENT}" hidden>{"".join(partes)}</div>'


CSS = """
/* Resumen de talentos: cabe bajo los totales sin robar alto al paperdoll. */
.talentos{display:flex;align-items:center;gap:9px;width:100%;
  position:relative;z-index:1;margin-top:7px;
  background:rgba(19,17,26,.72);border:1px solid var(--ln);border-radius:9px;
  padding:8px 10px 8px 12px;cursor:pointer;font:inherit;color:inherit;
  text-align:left;-webkit-appearance:none;appearance:none;
  transition:border-color .15s ease,background .15s ease}
.talentos:hover,.talentos:focus-visible{border-color:var(--gr);background:#1c2620}
.tal-tit{font:600 10px Barlow,sans-serif;letter-spacing:1.6px;
  text-transform:uppercase;color:var(--go);flex:0 0 auto}
.tal-reparto{display:flex;gap:8px;flex:1;justify-content:flex-end;
  min-width:0;flex-wrap:wrap}
.tal-arbol{display:flex;align-items:baseline;gap:4px;color:var(--db)}
.tal-arbol b{font-size:13px;font-weight:600;color:var(--tn)}
.tal-arbol i{font-style:normal;font-size:9.5px;letter-spacing:.4px;
  text-transform:uppercase}
.tal-arbol.tal-alto b{color:var(--go)}
.tal-arbol.tal-alto i{color:var(--tn)}
.talentos .ir{color:var(--db);font-size:16px;line-height:1;flex:0 0 auto;
  transition:transform .15s ease,color .15s ease}
.talentos:hover .ir,.talentos:focus-visible .ir{color:var(--gr);transform:translateX(3px)}

/* Detalle dentro del diálogo. */
.tal-lista{list-style:none;display:flex;flex-direction:column;gap:9px;
  margin-top:14px;padding-top:12px;border-top:1px solid var(--ln)}
.tal-fila{display:flex;align-items:center;gap:10px}
.tal-nom{font-size:12.5px;color:var(--tx);flex:0 0 92px}
.tal-barra{flex:1;height:7px;border-radius:4px;background:var(--p2);
  border:1px solid var(--ln);overflow:hidden}
.tal-barra i{display:block;height:100%;background:var(--go);opacity:.75}
.tal-pts{font-size:12.5px;font-weight:600;color:var(--tx);flex:0 0 auto;
  min-width:20px;text-align:right}
.tal-total{font-size:10.5px;color:var(--db);margin-top:8px;text-align:right}
.glifos-par{display:grid;grid-template-columns:1fr 1fr;gap:0 22px}
.glifos{list-style:none;display:flex;flex-direction:column;gap:7px}
.glifo{display:flex;align-items:center;gap:9px;line-height:1.25;
  font-size:12.5px;color:var(--tx)}
/* El icono del glifo, del mismo tamaño que el de una gema para que las dos
   listas del diálogo se lean igual. */
.gi{width:26px;height:26px;flex:0 0 auto;border-radius:5px;
  border:1px solid var(--ln2);background:var(--p2)}
.glifo.vacio{color:var(--db);font-style:italic}
.glifo.vacio .gi{border-style:dashed;background:transparent}

@media(max-width:980px){
  .tal-reparto{justify-content:flex-start}
}
/* Portátiles de pantalla baja: se recorta el aire del panel para que el
   diálogo siga entrando entero antes que encoger los iconos del árbol. */
@media(max-height:780px){
  .tal-total{margin-top:4px}
  .glifos-par .det-sec{margin-top:10px;padding-top:9px}
  .glifos{gap:5px}
  .gi{width:20px;height:20px}
  .glifo{gap:7px;font-size:12px}
}
@media(max-height:660px){
  .tal-total{margin-top:2px;font-size:10px}
  .glifos-par .det-sec{margin-top:7px;padding-top:6px}
  .glifos{gap:4px}
  .gi{width:18px;height:18px}
  .glifo{gap:6px;font-size:11.5px}
}
/* Las dos columnas aguantan hasta muy estrecho: el nombre largo parte de
   línea, que es justo lo que hace el panel del juego. Apilarlas costaba cien
   píxeles de alto y devolvía el desplazamiento al diálogo. */
@media(max-width:430px){
  .glifos-par{gap:0 12px}
  .glifo{gap:6px;font-size:11.5px}
  .gi{width:22px;height:22px}
}
@media(max-width:340px){
  .glifos-par{grid-template-columns:1fr;gap:0}
}
/* Sólo en lo más estrecho el nombre del árbol empuja el galón fuera de la
   ventana; ahí se queda la cifra sola, que el nombre ya está en el diálogo.
   Por encima de eso caben los tres nombres y ayudan a leer el reparto. */
@media(max-width:340px){
  .tal-arbol i{display:none}
  .tal-reparto{gap:12px}
}
"""
