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
    # El doctype no es adorno: sin él el navegador entra en modo de
    # compatibilidad antiguo, y quien lea la página con un analizador —el
    # recogedor de formularios del alojamiento, sin ir más lejos— se encuentra
    # un documento sin cabeza ni cuerpo declarados.
    partes = [
        "<!doctype html>",
        '<html lang="es">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width,initial-scale=1">',
        f"<title>{esc(titulo)}</title>",
        tema.FUENTES,
        f"<style>{hojas}</style>",
        "</head>",
        "<body>",
        '<div class="fondo" aria-hidden="true"></div>',
        cabecera.cabecera(pagina),
        cuerpo,
        i18n.SCRIPT_I18N,
        guion,
        guion_extra,
        "</body>",
        "</html>",
    ]
    return "\n".join(partes)
