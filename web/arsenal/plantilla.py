# -*- coding: utf-8 -*-
"""Envoltorio común a todas las páginas."""
from . import i18n, tema
from .componentes import arbol, cabecera, dialogo, icono
from .html import esc


def documento(titulo, css, cuerpo, pagina, iconos=None, guion_extra=""):
    """Arma la página: cabeza, fondo, cabecera, cuerpo y scripts.

    El CSS de los iconos se calcula sobre el cuerpo ya montado, así cada página
    lleva sólo los que usa. El script del diálogo se añade únicamente donde hay
    diálogo que manejar, y `guion_extra` deja que una página cuelgue el suyo
    sin que la plantilla tenga que conocerla.
    """
    iconos = iconos or {}
    hojas = (tema.TOKENS + cabecera.CABECERA_CSS + css + tema.FONDO_CSS
             + icono.css_usados(cuerpo, iconos))
    guion = dialogo.SCRIPT_DETALLE if 'id="modal"' in cuerpo else ""
    # El guion del arbol solo hace falta en las fichas que lo dibujan.
    if 'tal-mapa' in cuerpo:
        guion += arbol.SCRIPT
    partes = [
        '<html lang="es">',
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width,initial-scale=1">',
        f"<title>{esc(titulo)}</title>",
        tema.FUENTES,
        f"<style>{hojas}</style>",
        '<div class="fondo" aria-hidden="true"></div>',
        cabecera.cabecera(pagina),
        cuerpo,
        i18n.SCRIPT_I18N,
        guion,
        guion_extra,
    ]
    return "\n".join(partes)
