# -*- coding: utf-8 -*-
"""Utilidades de marcado compartidas por todos los componentes."""
import html as _html


def esc(t):
    """Escapa texto para incrustarlo en atributos o contenido."""
    return _html.escape(str(t), quote=True)


def bi(es, en, tag="span", cls="", extra=""):
    """Elemento bilingüe: el conmutador de idioma intercambia data-es/data-en."""
    c = f' class="i18n {cls}"'.replace("  ", " ") if cls else ' class="i18n"'
    return (f'<{tag}{c} data-es="{esc(es)}" data-en="{esc(en)}"{extra}>'
            f'{esc(es)}</{tag}>')
