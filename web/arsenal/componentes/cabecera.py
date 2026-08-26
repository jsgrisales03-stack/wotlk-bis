# -*- coding: utf-8 -*-
"""Barra superior: marca, navegación y conmutador de idioma."""

from .. import textos

CABECERA_CSS = """
.site-header{position:sticky;top:0;z-index:150;
  display:flex;align-items:center;justify-content:space-between;gap:12px;
  padding:12px 20px;background:rgba(10,9,14,.92);backdrop-filter:blur(6px);
  border-bottom:1px solid var(--ln)}
.brand{display:flex;align-items:center;gap:9px;text-decoration:none;color:inherit;min-width:0}
.brand-mark{width:24px;height:24px;border-radius:6px;flex:0 0 auto;
  background:linear-gradient(135deg,var(--go),#7a5a1e);
  display:flex;align-items:center;justify-content:center;
  font:700 12px Cinzel,Georgia,serif;color:#1a1408}
.brand-name{font:600 14.5px Cinzel,Georgia,serif;color:#f0eaf8;letter-spacing:.3px;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.nav{display:flex;align-items:center;gap:4px;flex:0 0 auto}
.nav a{text-decoration:none;color:var(--tn);font-size:12.5px;font-weight:600;
  padding:6px 11px;border-radius:16px;transition:color .15s,background .15s;white-space:nowrap}
.nav a:hover{color:var(--tx);background:var(--p2)}
.nav a[aria-current="page"]{color:#f0eaf8;background:var(--p2)}
.lang-switch{display:flex;gap:2px;background:var(--p);border:1px solid var(--ln);
  border-radius:20px;padding:3px;margin-left:4px}
.lang-switch button{border:0;background:transparent;color:var(--tn);
  font:600 11px/1 Barlow,sans-serif;padding:5px 10px;border-radius:16px;
  cursor:pointer;letter-spacing:.5px}
.lang-switch button[aria-pressed="true"]{background:var(--ln2);color:#f0eaf8}
@media(max-width:520px){
  .brand-name{display:none}
  .nav a{padding:6px 8px;font-size:12px}
}
"""



def cabecera(pagina="builds"):
    """pagina: 'builds' | 'comentarios' — marca el enlace activo."""
    def actual(p):
        return ' aria-current="page"' if p == pagina else ""
    return f"""<header class="site-header">
  <a class="brand" href="index.html">
    <span class="brand-mark" aria-hidden="true">A</span>
    <span class="brand-name i18n" data-es="{textos.MARCA_ES}" data-en="{textos.MARCA_EN}">{textos.MARCA_ES}</span>
  </a>
  <nav class="nav" aria-label="Principal">
    <a href="index.html"{actual('builds')} class="i18n" data-es="Builds" data-en="Builds">Builds</a>
    <a href="comentarios.html"{actual('comentarios')} class="i18n" data-es="Comentarios" data-en="Comments">Comentarios</a>
    <span class="lang-switch">
      <button type="button" data-lang="es" aria-pressed="true">ES</button>
      <button type="button" data-lang="en" aria-pressed="false">EN</button>
    </span>
  </nav>
</header>"""
