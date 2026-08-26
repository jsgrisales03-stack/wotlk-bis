# -*- coding: utf-8 -*-
"""Botón que abre el Vestidor de Wowhead con el equipo de la build puesto."""
from ..html import bi, esc

CUBO = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"'
        ' stroke-width="2" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M12 2 3 7v10l9 5 9-5V7z"/><path d="m3 7 9 5 9-5"/>'
        '<path d="M12 12v10"/></svg>')


def render(url):
    """Devuelve el enlace, o cadena vacía si esta build no tiene hash."""
    if not url:
        return ""
    return (f'<a class="ver3d" href="{esc(url)}" target="_blank"'
            f' rel="noopener noreferrer">{CUBO}'
            + bi("Ver en 3D", "View in 3D", "span") + '</a>')


CSS = """
/* Enlace al Vestidor de Wowhead con el equipo de la build ya puesto. */
.ver3d{position:relative;z-index:1;display:inline-flex;align-items:center;gap:6px;
  padding:5px 12px;border-radius:999px;text-decoration:none;white-space:nowrap;
  font:600 10.5px/1 Barlow,"Segoe UI",system-ui,sans-serif;
  letter-spacing:1.1px;text-transform:uppercase;
  color:var(--tn);background:rgba(19,17,26,.92);border:1px solid var(--ln2);
  transition:color .15s ease,border-color .15s ease,background .15s ease}
.ver3d:hover,.ver3d:focus-visible{color:var(--gr);
  border-color:rgba(64,217,126,.45);background:rgba(64,217,126,.09)}
.ver3d svg{width:12px;height:12px;flex:0 0 auto}
"""
