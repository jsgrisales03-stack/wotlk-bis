# -*- coding: utf-8 -*-
"""Iconos del juego, servidos como clase CSS.

El mismo icono aparece en la tarjeta y en el panel de detalle, y las gemas se
repiten muchas veces por ficha. Incrustando el base64 en cada <img>, una ficha
pasaba de 149 a 248 KB; por clase, cada icono viaja una sola vez.
"""
import re

from ..html import esc


def ic(iconos, nombre, cls, alt=""):
    """Marca un icono por su nombre. Vacío si el icono no está cosechado."""
    if nombre not in iconos:
        return ""
    rol = f' role="img" aria-label="{esc(alt)}"' if alt else ' aria-hidden="true"'
    return f'<span class="{cls} ic ic-{nombre}"{rol}></span>'


BASE = (".ic{background-size:cover;background-position:center;"
        "background-repeat:no-repeat;display:inline-block;flex:0 0 auto}")


def css_usados(cuerpo, iconos):
    """Regla de fondo sólo para los iconos que esta página usa."""
    reglas = [BASE]
    for n in sorted(set(re.findall(r"ic-([a-z0-9_]+)", cuerpo))):
        src = iconos.get(n)
        if src:
            reglas.append(f".ic-{n}{{background-image:url({src})}}")
    return "".join(reglas)
