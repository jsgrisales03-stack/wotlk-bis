# -*- coding: utf-8 -*-
"""Talentos y glifos de una build.

En la ficha sólo cabe un resumen: el reparto por árbol. El detalle —los tres
glifos sublimes y los tres menores— se despliega en el diálogo, igual que el
detalle de una pieza de equipo, porque bajo los totales quedan cuarenta píxeles
en un portátil y el conjunto tiene que seguir entrando de una pantalla.
"""
from .. import textos
from ..html import bi, esc

IDENT = "det-talentos"

# Nombre de los tres árboles por clase, en el orden en que los numera el juego.
ARBOLES = {
    "Caballero de la Muerte": [("Sangre", "Blood"), ("Escarcha", "Frost"),
                               ("Profano", "Unholy")],
    "Guerrero": [("Armas", "Arms"), ("Furia", "Fury"), ("Protección", "Protection")],
    "Paladín": [("Sagrado", "Holy"), ("Protección", "Protection"),
                ("Reprensión", "Retribution")],
    "Cazador": [("Bestias", "Beast Mastery"), ("Puntería", "Marksmanship"),
                ("Supervivencia", "Survival")],
    "Pícaro": [("Asesinato", "Assassination"), ("Combate", "Combat"),
               ("Sutileza", "Subtlety")],
    "Sacerdote": [("Disciplina", "Discipline"), ("Sagrado", "Holy"),
                  ("Sombras", "Shadow")],
    "Chamán": [("Elemental", "Elemental"), ("Mejora", "Enhancement"),
               ("Restauración", "Restoration")],
    "Mago": [("Arcano", "Arcane"), ("Fuego", "Fire"), ("Escarcha", "Frost")],
    "Brujo": [("Aflicción", "Affliction"), ("Demonología", "Demonology"),
              ("Destrucción", "Destruction")],
    "Druida": [("Equilibrio", "Balance"), ("Feral", "Feral Combat"),
               ("Restauración", "Restoration")],
}


def _nombre_glifo(nombre, idioma):
    """Devuelve (español, inglés) de un glifo a partir del nombre transcrito."""
    if not nombre:
        return None
    otro = textos.GLIFOS_EN.get(nombre) if idioma == "es" else textos.GLIFOS_ES.get(nombre)
    if idioma == "es":
        return (nombre, otro or nombre)
    return (otro or nombre, nombre)


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


def _lista_glifos(titulo_es, titulo_en, nombres, idioma):
    filas = []
    for n in nombres or []:
        par = _nombre_glifo(n, idioma)
        if not par:
            filas.append('<li class="glifo vacio">'
                         + bi("Ranura libre", "Empty slot", "span") + "</li>")
        else:
            filas.append('<li class="glifo">'
                         + bi(par[0], par[1], "span") + "</li>")
    if not filas:
        return ""
    return ('<section class="det-sec">' + bi(titulo_es, titulo_en, "h4")
            + f'<ul class="glifos">{"".join(filas)}</ul></section>')


def panel(clase, espec, datos):
    """Panel oculto que el diálogo copia al pulsar el resumen."""
    datos = datos or {}
    reparto = datos.get("reparto")
    if not reparto:
        return ""
    arboles = ARBOLES.get(clase, [])
    filas = []
    total = sum(reparto)
    for i, puntos in enumerate(reparto):
        es_, en_ = arboles[i] if i < len(arboles) else (str(i + 1), str(i + 1))
        ancho = round(100 * puntos / total, 1) if total else 0
        filas.append(
            '<li class="tal-fila">'
            + bi(es_, en_, "span", cls="tal-nom")
            + f'<span class="tal-barra"><i style="width:{ancho}%"></i></span>'
            + f'<b class="tal-pts">{puntos}</b></li>')

    partes = [
        '<div class="det-cab"><div class="det-tit">',
        bi("Talentos", "Talents", "h3"),
        bi(espec, textos.en(textos.ESPECS, espec), "p", cls="det-ranura"),
        '</div></div>',
        f'<ul class="tal-lista">{"".join(filas)}</ul>',
        '<p class="tal-total">'
        + bi(f"{total} puntos de talento", f"{total} talent points", "span") + "</p>",
    ]

    g = datos.get("glifos") or {}
    idioma = g.get("idioma") or "es"
    partes.append(_lista_glifos("Glifos sublimes", "Major glyphs",
                                g.get("mayores"), idioma))
    partes.append(_lista_glifos("Glifos menores", "Minor glyphs",
                                g.get("menores"), idioma))
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
.glifos{list-style:none;display:flex;flex-direction:column;gap:6px}
.glifo{font-size:12.5px;color:var(--tx);padding-left:13px;position:relative}
.glifo::before{content:"";position:absolute;left:0;top:7px;width:5px;height:5px;
  border-radius:1px;transform:rotate(45deg);background:var(--go)}
.glifo.vacio{color:var(--db);font-style:italic}
.glifo.vacio::before{background:var(--ln2)}

@media(max-width:980px){
  .tal-reparto{justify-content:flex-start}
}
/* En pantallas muy estrechas el nombre del árbol empujaba el galón fuera de
   la ventana. Se queda sólo la cifra: el nombre ya está en el diálogo. */
@media(max-width:380px){
  .tal-arbol i{display:none}
  .tal-reparto{gap:12px}
}
"""
