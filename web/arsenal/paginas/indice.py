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

# Marca de rol con el aspecto del buscador de mazmorras: medallón de aro
# dorado con el escudo del tanque, la cruz del sanador y la espada del daño.
# Se dibujan en SVG porque esas texturas del juego no están publicadas en
# ninguna ruta accesible, y así además quedan nítidas a cualquier tamaño y no
# añaden ninguna petición. El daño a distancia comparte medallón con el
# cuerpo a cuerpo, igual que en el juego.
_ARO = ('<circle cx="16" cy="16" r="15.2" fill="#6b5219"/>'
        '<circle cx="16" cy="16" r="13.6" fill="#c9a94e"/>'
        '<circle cx="16" cy="16" r="11.7" fill="#2a2208"/>')

_TANQUE = (_ARO + '<circle cx="16" cy="16" r="10.7" fill="#1b3157"/>'
           '<path d="M16 8.2 9.9 10.5v4.6c0 3.7 2.4 7 6.1 8.2 3.7-1.2 6.1-4.5'
           ' 6.1-8.2v-4.6L16 8.2z" fill="#dae3f2"/>'
           '<path d="M16 8.2 9.9 10.5v4.6c0 3.7 2.4 7 6.1 8.2z" fill="#9fb4d8"/>')

_SANADOR = (_ARO + '<circle cx="16" cy="16" r="10.7" fill="#123322"/>'
            '<path d="M13.4 8.3h5.2v5.1h5.1v5.2h-5.1v5.1h-5.2v-5.1H8.3v-5.2h5.1z"'
            ' fill="#dff0b8" stroke="#7a8f4a" stroke-width=".8"/>')

_DANO = (_ARO + '<circle cx="16" cy="16" r="10.7" fill="#4a1216"/>'
         '<path d="M24.2 7.8 22.2 15.1 15.1 22.2 11.6 18.7 18.7 11.6z" fill="#e8eef8"/>'
         '<path d="M18.9 11.4 22.4 14.9 20.6 16.7 17.1 13.2z" fill="#b9c4d6"/>'
         '<path d="M13.6 16.6 17.2 20.2 12.9 24.5 9.3 20.9z" fill="#c9a94e"/>'
         '<path d="M10.4 21.8 12.8 24.2 10.2 26.8 7.8 24.4z" fill="#8a6a22"/>')

ROL_ICONO = {
    "Tanque — PvE": _TANQUE,
    "Sanador — PvE": _SANADOR,
    "DPS cuerpo a cuerpo — PvE": _DANO,
    "DPS a distancia — PvE": _DANO,
}


def marca_rol(rol):
    """Medallón del rol, o cadena vacía si la build no lo declara."""
    trazo = ROL_ICONO.get(rol)
    if not trazo:
        return ""
    return (f'<svg class="rol-ic" viewBox="0 0 32 32" aria-hidden="true">'
            f'{trazo}</svg>')

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
.rol-ic{width:16px;height:16px;flex:0 0 auto;opacity:.9}
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
