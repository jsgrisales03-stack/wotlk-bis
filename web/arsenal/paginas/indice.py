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
.intro-tags{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;
  margin:18px 0 40px}
.intro-tags span{font-size:11px;letter-spacing:.5px;text-transform:uppercase;
  color:var(--tn);background:var(--p);border:1px solid var(--ln);
  border-radius:14px;padding:5px 12px}
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
  padding:8px 12px;font-size:13px;transition:border-color .15s,background .15s}
a.spec:hover,a.spec:focus-visible{border-color:var(--gr);background:#1c2620}
a.spec .role{color:var(--tn);font-size:11px;flex:0 0 auto}
a.spec .dot{width:6px;height:6px;border-radius:50%;background:var(--gr);
  flex:0 0 auto;display:inline-block;margin-right:7px}
@media(max-width:760px){
  .page{padding:30px 16px 8px}
  .intro{font-size:13.5px;line-height:1.65}
  .intro-tags{margin:16px 0 26px;gap:6px}
  .class-card{padding:15px 16px;gap:9px}
}
@media(max-width:430px){
  .page{padding:22px 12px 8px}
  .hero .sub{letter-spacing:2.5px;font-size:11.5px}
  .intro-tags span{font-size:10px;padding:4px 9px}
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
                + "</span>"
                + bi(rol_es, rol_en, cls="role")
                + "</a>"
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
<div class="intro-tags">{"".join(bi(a, b) for a, b in etiquetas)}</div>
<div class="grid">{"".join(tarjetas)}</div>
</div>"""

    return documento(textos.MARCA_ES, CSS, cuerpo, "builds", iconos)
