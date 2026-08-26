# -*- coding: utf-8 -*-
"""Portada: todas las clases con sus especializaciones."""
from .. import datos, textos
from ..componentes.icono import ic
from ..html import bi, esc
from ..plantilla import documento

ORDEN_CLASES = [
    "Caballero de la Muerte", "Guerrero", "Paladín", "Cazador", "Pícaro",
    "Sacerdote", "Chamán", "Mago", "Brujo", "Druida",
]
ORDEN_ESPECS = {
    "Caballero de la Muerte": ["Sangre", "Escarcha", "Profano"],
    "Guerrero": ["Armas", "Furia", "Protección"],
    "Paladín": ["Sagrado", "Protección", "Reprensión"],
    "Cazador": ["Bestias", "Puntería", "Supervivencia"],
    "Pícaro": ["Asesinato", "Combate", "Sutileza"],
    "Sacerdote": ["Disciplina", "Sagrado", "Sombras"],
    "Chamán": ["Elemental", "Mejora", "Restauración"],
    "Mago": ["Arcano", "Fuego", "Escarcha"],
    "Brujo": ["Aflicción", "Demonología", "Destrucción"],
    "Druida": ["Equilibrio", "Feral — Tanque", "Feral — DPS", "Restauración"],
}
ROL_CORTO = {
    "DPS cuerpo a cuerpo — PvE": ("DPS cc", "Melee DPS"),
    "DPS a distancia — PvE": ("DPS distancia", "Ranged DPS"),
    "Tanque — PvE": ("Tanque", "Tank"),
    "Sanador — PvE": ("Sanador", "Healer"),
}

# Marca de rol, como en el buscador de mazmorras: escudo para el tanque, cruz
# para el sanador, espadas cruzadas para el cuerpo a cuerpo y flecha para la
# distancia. Se dibujan macizas porque a 14 px un trazo fino se pierde, y la X
# distingue al daño cuerpo a cuerpo de la cruz del sanador.
_BASE = ('<svg class="rol-ic" viewBox="0 0 24 24" aria-hidden="true"'
         ' stroke-linecap="round" stroke-linejoin="round">')

ROL_ICONO = {
    "Tanque — PvE": _BASE + (
        '<path d="M12 3 5 5.6v5.1c0 4 2.8 7.6 7 9 4.2-1.4 7-5 7-9V5.6L12 3z"'
        ' fill="#4a9eff" fill-opacity=".18" stroke="#4a9eff" stroke-width="1.9"/>'
        '</svg>'),
    "Sanador — PvE": _BASE + (
        '<path d="M9.8 4h4.4v5.8H20v4.4h-5.8V20H9.8v-5.8H4V9.8h5.8z"'
        ' fill="#40d97e"/></svg>'),
    "DPS cuerpo a cuerpo — PvE": _BASE + (
        '<path d="M5.5 5.5 18.5 18.5M18.5 5.5 5.5 18.5" fill="none"'
        ' stroke="#e5484d" stroke-width="2.1"/>'
        '<circle cx="5.5" cy="18.5" r="1.6" fill="#e5484d"/>'
        '<circle cx="18.5" cy="18.5" r="1.6" fill="#e5484d"/></svg>'),
    "DPS a distancia — PvE": _BASE + (
        '<path d="M4 20 19 5M13 5h6v6M4 20v-4M4 20h4" fill="none"'
        ' stroke="#e5484d" stroke-width="2.1"/></svg>'),
}


def marca_rol(rol):
    """Icono del rol, o cadena vacía si la build no lo declara."""
    return ROL_ICONO.get(rol, "")

CSS = """
body{background:var(--bg);color:var(--tx);
  font:14px/1.5 Barlow,"Segoe UI",system-ui,sans-serif;
  min-height:100vh;display:flex;flex-direction:column}
.page{max-width:1620px;margin:0 auto;padding:44px 26px 8px;flex:1;width:100%}
.hero{text-align:center;margin-bottom:18px}
.hero h1{font:700 clamp(26px,4vw,40px)/1.15 Cinzel,Georgia,serif;
  color:#f0eaf8;text-wrap:balance}
.hero .sub{font-size:12.5px;letter-spacing:4px;text-transform:uppercase;
  color:var(--go);margin-top:10px}
.intro{max-width:62ch;margin:20px auto 0;text-align:center;
  color:var(--tn);font-size:14px;line-height:1.7}
.intro strong{color:var(--tx);font-weight:600}
/* Antes eran píldoras con borde y fondo, y la gente las pulsaba creyendo que
   filtraban algo. Ahora son una línea de datos: sin caja, sin relieve. */
.intro-meta{display:flex;flex-wrap:wrap;justify-content:center;
  margin:18px 0 40px;font:11px/1.9 Barlow,sans-serif;letter-spacing:1.4px;
  text-transform:uppercase;color:var(--db)}
.intro-meta span{padding:0 15px;position:relative}
.intro-meta span+span::before{content:"";position:absolute;left:0;top:50%;
  width:1px;height:11px;margin-top:-6px;background:var(--ln2)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(262px,1fr));gap:16px}
.class-card{background:var(--p);border:1px solid var(--ln2);border-radius:11px;
  padding:18px 20px;display:flex;flex-direction:column;gap:13px;
  transition:border-color .15s ease}
.class-card:hover{border-color:var(--ln2)}
.class-head{display:flex;align-items:center;gap:10px}
.class-ic{width:30px;height:30px;border-radius:7px;flex:0 0 auto;
  border:1px solid var(--ln2);box-shadow:0 1px 6px rgba(0,0,0,.5)}
.class-name{font:600 15.5px/1.2 Cinzel,Georgia,serif;color:#f0eaf8;flex:1;min-width:0}
.class-n{font:600 10.5px/1 Barlow,sans-serif;color:var(--db);
  border:1px solid var(--ln);border-radius:10px;padding:4px 7px;flex:0 0 auto}
.specs{display:flex;flex-direction:column;gap:6px}
a.spec{display:flex;justify-content:space-between;align-items:center;gap:8px;
  text-decoration:none;color:var(--tx);
  background:var(--p2);border:1px solid var(--ln);border-radius:6px;
  padding:8px 10px 8px 12px;font-size:13px;
  transition:border-color .15s,background .15s}
a.spec:hover,a.spec:focus-visible{border-color:var(--gr);background:#1c2620}
a.spec .fin{display:flex;align-items:center;gap:7px;flex:0 0 auto}
.rol-ic{width:14px;height:14px;flex:0 0 auto;opacity:.85}
a.spec:hover .rol-ic,a.spec:focus-visible .rol-ic{opacity:1}
/* El galón es la única señal de que la fila navega; en táctil no hay hover. */
a.spec .ir{color:var(--db);font-size:16px;line-height:1;
  transition:transform .15s ease,color .15s ease}
a.spec:hover .ir,a.spec:focus-visible .ir{color:var(--gr);transform:translateX(3px)}
a.spec .role{color:var(--tn);font-size:11px;flex:0 0 auto}
a.spec .dot{width:6px;height:6px;border-radius:50%;background:var(--gr);
  flex:0 0 auto;display:inline-block;margin-right:7px}
@media(max-width:760px){
  .page{padding:30px 16px 8px}
  .intro{font-size:13.5px;line-height:1.65}
  .intro-meta{margin:16px 0 26px}
  .class-card{padding:15px 16px;gap:9px}
}
@media(max-width:430px){
  .page{padding:22px 12px 8px}
  .hero .sub{letter-spacing:2.5px;font-size:11.5px}
  .intro-meta{font-size:10px;letter-spacing:1.1px}
  .intro-meta span{padding:0 10px}
  .class-card{padding:13px 14px}
  a.spec{padding:9px 11px;font-size:12.5px}
}
"""


def construir(iconos):
    builds = [{"id": d["id"], "clase": d["clase"],
               "espec": d["especializacion"], "rol": d.get("rol", ""),
               "icono": d.get("clase_icono", "")}
              for d in datos.builds()]

    por_clase = {}
    for b in builds:
        por_clase.setdefault(b["clase"], []).append(b)

    tarjetas = []
    for clase in ORDEN_CLASES:
        if clase not in por_clase:
            continue
        orden = ORDEN_ESPECS.get(clase, [])
        specs = sorted(
            por_clase[clase],
            key=lambda b: orden.index(b["espec"]) if b["espec"] in orden else 99,
        )
        filas = []
        for b in specs:
            rol_es, rol_en = ROL_CORTO.get(b["rol"], ("", ""))
            filas.append(
                f'<a class="spec" href="{b["id"]}.html">'
                '<span><span class="dot" aria-hidden="true"></span>'
                + bi(b["espec"], textos.en(textos.ESPECS, b["espec"]))
                + '</span><span class="fin">'
                + marca_rol(b["rol"])
                + bi(rol_es, rol_en, cls="role")
                + '<span class="ir" aria-hidden="true">&rsaquo;</span>'
                + "</span></a>"
            )
        icono = next((b["icono"] for b in specs if b["icono"]), "")
        cabecera = (
            '<div class="class-head">'
            + (ic(iconos, icono, "class-ic", clase) if icono in iconos else "")
            + bi(clase, textos.en(textos.CLASES, clase), "h2", cls="class-name")
            + f'<span class="class-n">{len(specs)}</span>'
            + "</div>"
        )
        tarjetas.append(
            '<div class="class-card">' + cabecera
            + f'<div class="specs">{"".join(filas)}</div></div>'
        )

    intro_es = ("Referencia de <strong>equipo BiS de PvE</strong> para cada clase y "
                "especialización de Wrath of the Lich King, centrada en Ciudadela de la "
                "Corona de Hielo 25 heroico. Cada ficha reúne las piezas, gemas y "
                "encantamientos recomendados, con los totales del conjunto y el detalle "
                "de cada engarce al pasar el cursor.")
    intro_en = ("A reference for <strong>PvE BiS gear</strong> across every Wrath of the "
                "Lich King class and specialization, built around Icecrown Citadel "
                "25-man Heroic. Each page gathers the recommended pieces, gems and "
                "enchants, with full set totals and per-socket detail on hover.")

    etiquetas = [
        ("ICC 25 heroico", "ICC 25 Heroic"),
        ("Gemas y encantamientos", "Gems & enchants"),
        ("Totales del conjunto", "Set totals"),
        (f"{len(builds)} especializaciones", f"{len(builds)} specializations"),
    ]

    cuerpo = f"""<div class="page">
<div class="hero">
  {bi(textos.MARCA_ES, textos.MARCA_EN, "h1")}
  {bi("Guías de equipo WotLK · PvE", "WotLK gear guides · PvE", "p", cls="sub")}
</div>
<p class="intro i18n" data-es="{esc(intro_es)}" data-en="{esc(intro_en)}">{intro_es}</p>
<p class="intro-meta">{"".join(bi(a, b) for a, b in etiquetas)}</p>
<div class="grid">{"".join(tarjetas)}</div>
</div>"""

    return documento(textos.MARCA_ES, CSS, cuerpo, "builds", iconos)
