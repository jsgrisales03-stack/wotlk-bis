# -*- coding: utf-8 -*-
"""
Generador del sitio «Arsenal de Corona de Hielo».

    python build.py            genera todo el sitio
    python build.py dk-profano genera sólo esa ficha

Cada ficha se arma desde datos/<id>.json; el índice se deriva de los propios
datos, así que añadir un JSON nuevo basta para que aparezca en la portada.
"""
import json, os, sys, html, glob

import sitio
import stats as motor

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(AQUI, "datos")
# Ficheros de datos/soporte que no describen una build.
NO_BUILD = ("iconos", "stats-", "displayids", "vestidor", "_")

CALIDAD = {4: ("epic", "#a335ee"), 5: ("legendary", "#ff8000")}
COLOR_RANURA = {
    "Roja": "#e5484d", "Amarilla": "#f5d90a", "Azul": "#4a9eff",
    "Meta": "#d9b45b", "Prismática": "#c084fc",
}

# Distribución del panel: lo que no cae a izquierda o derecha va a la fila inferior.
IZQUIERDA = ["head", "neck", "shoulder", "back", "chest", "wrist"]
DERECHA = ["hands", "waist", "legs", "feet", "ring1", "ring2"]

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


def esc(t):
    return html.escape(str(t), quote=True)


def bi(es, en, tag="span", cls="", extra=""):
    """Elemento bilingüe: se traduce solo al pulsar el conmutador."""
    c = f' class="i18n {cls}"'.replace("  ", " ") if cls else ' class="i18n"'
    return (f'<{tag}{c} data-es="{esc(es)}" data-en="{esc(en)}"{extra}>'
            f'{esc(es)}</{tag}>')


def ic(iconos, nombre, cls, alt=""):
    src = iconos.get(nombre, "")
    return f'<img class="{cls}" src="{src}" alt="{esc(alt)}" loading="lazy">'


# --------------------------------------------------------------- tooltip
def tooltip(p, iconos, lado):
    filas = []
    enc = p.get("encantamiento")
    if enc:
        filas.append(
            '<li class="tt-row tt-ench">'
            + ic(iconos, enc["icono"], "tt-ic", "")
            + '<div>'
            + bi(enc["nombre"], sitio.en(sitio.ENCANTAMIENTOS, enc["nombre"]), "b")
            + bi(enc["efecto"], sitio.en(sitio.EFECTOS, enc["efecto"]))
            + '</div></li>'
        )
    for g in p.get("gemas", []):
        color = COLOR_RANURA.get(g["ranura"], "#888")
        nota = ""
        if g.get("clave"):
            nota = " " + bi(g["clave"], sitio.en(sitio.EFECTOS, g["clave"]), "em")
        marca = ('<span class="tt-skip" title="No respeta el color de la ranura"'
                 ' aria-hidden="true">↯</span>') if g.get("ignora_color") else ""
        filas.append(
            '<li class="tt-row">'
            f'<span class="tt-dot" style="background:{color}" aria-hidden="true"></span>'
            + ic(iconos, g["icono"], "tt-ic", "")
            + '<div>'
            + bi(g["gema"], sitio.en(sitio.GEMAS, g["gema"]), "b") + marca
            + bi(g["efecto"], sitio.en(sitio.EFECTOS, g["efecto"])) + nota
            + '</div></li>'
        )
    if not filas:
        return ""
    pos = {"izq": "tt-right", "der": "tt-left"}.get(lado, "tt-center")
    return f'<ul class="tt {pos}">{"".join(filas)}</ul>'


# --------------------------------------------------------------- una ranura
def ranura(p, iconos, lado):
    cls, color = CALIDAD.get(p["calidad"], ("epic", "#a335ee"))
    heroico = ('<b class="hb" title="Heroico">H</b>') if p.get("heroico") else ""
    enc = p.get("encantamiento")
    linea_enc = ""
    if enc:
        linea_enc = bi(enc["nombre"], sitio.en(sitio.ENCANTAMIENTOS, enc["nombre"]),
                       cls="s-enc")
    puntos = ""
    if p.get("gemas"):
        puntos = '<span class="s-dots" aria-hidden="true">' + "".join(
            f'<span class="sd" style="background:'
            f'{COLOR_RANURA.get(g["ranura"], "#888")}"></span>'
            for g in p["gemas"]
        ) + "</span>"

    tt = tooltip(p, iconos, lado)
    interactivo = ' tabindex="0"' if tt else ""
    etiqueta = bi(p["ranura"], sitio.en(sitio.RANURAS, p["ranura"]), cls="s-slot")

    return f"""<div class="slot {lado}{' has-tt' if tt else ''}"{interactivo}>
  <span class="s-icon {cls}">{ic(iconos, p["icono"], "si", p["nombre"])}<b class="lv">{p["ilvl"]}</b>{heroico}</span>
  <span class="s-txt">
    {etiqueta}
    {bi(p["nombre"], p.get("en", p["nombre"]), cls="s-name", extra=f' style="color:{color}"')}
    {linea_enc}{puntos}
  </span>
  {tt}
</div>"""


# --------------------------------------------------------------- estadísticas
def panel_stats(build, items_stats):
    totales, _ = motor.calcular(build, items_stats)
    if not totales:
        return ""
    perfil = motor.perfil_de(build, totales)
    filas = []
    for clave in motor.visibles(totales, perfil):
        valor = totales[clave]
        es, en_ = motor.ETIQUETAS[clave]
        destacada = " destacada" if clave in ("salud", "poder_ataque", "poder_hechizos") else ""
        filas.append(
            f'<div class="stat{destacada}">'
            + bi(es, en_, "dt")
            + f'<dd>{valor:,}</dd></div>'.replace(",", " ")
        )
    if not filas:
        return ""
    return (
        '<div class="stats">'
        + bi("Totales del equipo", "Gear totals", "h2", cls="stats-h")
        + f'<dl class="stat-list">{"".join(filas)}</dl>'
        + bi("Sólo objetos, gemas y encantamientos. Sin talentos ni beneficios de banda.",
             "Gear, gems and enchants only. No talents or raid buffs.",
             "p", cls="stats-note")
        + "</div>"
    )


# --------------------------------------------------------------- CSS ficha
CSS_FICHA = """
body{background:var(--bg);color:var(--tx);
  font:13px/1.45 Barlow,"Segoe UI",system-ui,sans-serif;
  font-variant-numeric:tabular-nums;min-height:100vh;
  display:flex;flex-direction:column}
.page{max-width:1320px;width:100%;margin:0 auto;padding:0 14px;
  flex:1;display:flex;flex-direction:column;min-height:0}

.ficha-head{text-align:center;padding:16px 0 4px;flex:0 0 auto}
.ficha-head h1{font:700 clamp(21px,3.2vw,31px)/1.1 Cinzel,Georgia,serif;
  color:#f0eaf8;letter-spacing:.4px}
.spec-lab{font-size:13px;letter-spacing:4px;text-transform:uppercase;
  color:var(--go);margin-top:5px;font-weight:500}
.rol-lab{font-size:11.5px;color:var(--tn);margin-top:4px}

.pd{flex:1;display:grid;
  grid-template-columns:1fr minmax(200px,264px) 1fr;
  grid-template-rows:1fr auto;gap:0;min-height:0;padding:6px 0 0}
.col{display:flex;flex-direction:column;gap:4px;justify-content:center;min-height:0}
.col-l{align-items:flex-end}
.col-r{align-items:flex-start}

.ctr{grid-row:1/2;grid-column:2/3;display:flex;flex-direction:column;
  align-items:center;justify-content:flex-start;position:relative;
  padding:10px 6px;gap:8px}
.ctr-bg{position:absolute;inset:0;border-radius:12px;
  background:radial-gradient(ellipse 82% 60% at 50% 22%,#1a1428,var(--bg))}
.ctr-bg::after{content:"";position:absolute;width:104px;height:104px;
  left:50%;top:52px;transform:translate(-50%,-50%);border-radius:50%;
  border:1px solid rgba(80,220,140,.1);box-shadow:0 0 46px rgba(80,220,140,.05)}
/* Personaje renderizado: va detrás, así no le quita alto al panel. */
.personaje{position:absolute;z-index:0;top:2px;left:50%;transform:translateX(-50%);
  height:250px;width:auto;pointer-events:none;
  -webkit-mask-image:linear-gradient(#000 58%,rgba(0,0,0,.25) 82%,transparent);
  mask-image:linear-gradient(#000 58%,rgba(0,0,0,.25) 82%,transparent)}
.ctr.con-personaje .ctr-t{margin-top:158px;
  text-shadow:0 1px 6px #0a090e,0 0 14px #0a090e}
.ctr.con-personaje .stats{background:rgba(13,11,18,.93);backdrop-filter:blur(2px)}

/* El retrato de raza es de 56 px en origen: se muestra a tamaño nativo. */
.retrato{position:relative;z-index:1;width:56px;height:56px;flex:0 0 auto}
.retrato .race-ic{width:56px;height:56px;border-radius:50%;display:block;
  border:2px solid rgba(80,220,140,.28);box-shadow:0 0 22px rgba(80,220,140,.10)}
.retrato .cl-badge{position:absolute;right:-4px;bottom:-4px;
  width:23px;height:23px;border-radius:50%;display:block;
  border:2px solid var(--bg);background:var(--bg);
  box-shadow:0 1px 5px rgba(0,0,0,.65)}
.cl-ic{width:54px;height:54px;border-radius:50%;position:relative;z-index:1;
  border:2px solid rgba(80,220,140,.22);box-shadow:0 0 22px rgba(80,220,140,.08)}
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

.ctr-t{position:relative;z-index:1;text-align:center}
.ctr-t .race{font-size:12.5px;color:var(--tn);display:block}
.ctr-t .fac{font-size:9.5px;text-transform:uppercase;letter-spacing:2px;
  color:var(--dk);margin-top:2px;font-weight:600;display:block}

.stats{position:relative;z-index:1;width:100%;
  background:rgba(19,17,26,.72);border:1px solid var(--ln);border-radius:9px;
  padding:11px 13px 9px}
.stats-h{font:600 10px Barlow,sans-serif;letter-spacing:1.6px;
  text-transform:uppercase;color:var(--go);text-align:center;
  padding-bottom:7px;border-bottom:1px solid var(--ln);margin-bottom:5px}
.stat-list{display:flex;flex-direction:column;gap:1px}
.stat{display:flex;justify-content:space-between;align-items:baseline;gap:10px;
  padding:2.5px 0}
.stat dt{font-size:11.5px;color:var(--tn);min-width:0;
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.stat dd{font-size:12.5px;font-weight:600;color:var(--tx);flex:0 0 auto}
.stat.destacada dd{color:var(--go)}
.stats-note{font-size:9.5px;line-height:1.4;color:var(--db);
  margin-top:7px;padding-top:6px;border-top:1px solid var(--ln);text-align:center}

.bot-row{grid-column:1/4;display:flex;justify-content:center;
  gap:6px;flex-wrap:wrap;padding:8px 0 0;flex:0 0 auto}

.slot{display:flex;gap:8px;align-items:center;
  background:var(--p);border:1px solid var(--ln);border-radius:7px;
  padding:6px 10px;max-width:312px;width:100%;position:relative;
  transition:border-color .15s,background .15s}
.slot.has-tt{cursor:help}
.slot.has-tt:hover,.slot.has-tt:focus-visible{border-color:var(--ln2);background:var(--p2)}
.slot.izq{flex-direction:row-reverse;text-align:right}
.slot.btm{max-width:226px}
.s-icon{position:relative;flex:0 0 auto;display:block}
.si{width:36px;height:36px;display:block;border-radius:5px;border:2px solid var(--ln2)}
.epic .si{border-color:var(--ep)}
.legendary .si{border-color:var(--lg)}
.lv{position:absolute;left:50%;transform:translateX(-50%);bottom:-6px;
  background:#08070b;border:1px solid var(--ln2);border-radius:3px;
  font-size:9.5px;padding:0 4px;color:var(--go);font-weight:700;line-height:14px}
.hb{position:absolute;top:-5px;right:-5px;background:#3d2246;color:#e3a9ff;
  border-radius:2px;font-size:8px;padding:0 3px;font-weight:700;
  border:1px solid #5a3570;line-height:13px}
.s-txt{min-width:0;flex:1;display:block}
.s-slot{display:block;font-size:9px;letter-spacing:1.1px;text-transform:uppercase;
  color:var(--db);line-height:1.3}
.s-name{display:block;font-size:12.5px;font-weight:600;line-height:1.25;
  text-wrap:balance}
.s-enc{display:block;font-size:10.5px;color:var(--gr);font-weight:500;
  margin-top:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.s-dots{display:flex;gap:3px;margin-top:3px}
.slot.izq .s-dots{justify-content:flex-end}
.sd{width:7px;height:7px;border-radius:1.5px;transform:rotate(45deg)}

.tt{display:none;position:absolute;z-index:100;list-style:none;
  background:#1c1928;border:1px solid var(--ln2);border-radius:8px;
  padding:9px 12px;width:284px;box-shadow:0 8px 32px rgba(0,0,0,.6);
  pointer-events:none;text-align:left}
.slot.has-tt:hover .tt,.slot.has-tt:focus-visible .tt,
.slot.has-tt:focus-within .tt{display:block}
.tt-right{left:calc(100% + 10px);top:50%;transform:translateY(-50%)}
.tt-left{right:calc(100% + 10px);top:50%;transform:translateY(-50%)}
.tt-center{bottom:calc(100% + 8px);left:50%;transform:translateX(-50%)}
.tt-row{display:flex;gap:8px;align-items:flex-start;padding:5px 0;
  border-bottom:1px solid rgba(255,255,255,.05)}
.tt-row:last-child{border-bottom:0}
.tt-ic{width:24px;height:24px;border-radius:4px;flex:0 0 auto;border:1px solid var(--ln2)}
.tt-dot{width:8px;height:8px;border-radius:2px;transform:rotate(45deg);
  flex:0 0 auto;margin-top:8px}
.tt-row>div{min-width:0;flex:1}
.tt-row b{display:block;font-size:12.5px;font-weight:600;color:#d5cee3;line-height:1.3}
.tt-row span{display:block;font-size:11.5px;color:var(--tn);line-height:1.35}
.tt-row em{color:var(--go);font-style:normal;font-size:11px}
.tt-ench b{color:var(--gr)}
.tt-skip{color:#d99b3c;font-size:11px;margin-left:3px}

@media(max-width:900px){
  .pd{grid-template-columns:1fr;grid-template-rows:auto;gap:8px;padding-top:10px}
  .col{align-items:stretch;gap:5px}
  .col-l{order:2}
  .ctr{order:1;grid-column:auto;grid-row:auto;padding:4px 0 10px}
  .col-r{order:3}
  .bot-row{order:4;grid-column:auto}
  .stats{max-width:340px;margin:0 auto}
  .slot,.slot.izq{flex-direction:row;text-align:left;max-width:100%}
  .slot.izq .s-dots{justify-content:flex-start}
  .slot.btm{max-width:100%}
  .tt{position:static;display:block;width:auto;margin-top:7px;
    box-shadow:none;background:#17141f}
  .tt-left,.tt-right,.tt-center{transform:none;inset:auto}
  .slot.has-tt{flex-wrap:wrap;cursor:default}
  .tt{flex:1 0 100%}
}
@media(prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
"""


def documento(titulo, css, cuerpo, pagina):
    """Envoltorio común a todas las páginas del sitio."""
    return "\n".join([
        '<html lang="es">',
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width,initial-scale=1">',
        f"<title>{esc(titulo)}</title>",
        sitio.FUENTES,
        f"<style>{sitio.TOKENS}{sitio.CABECERA_CSS}{sitio.PIE_CSS}{css}</style>",
        sitio.cabecera(pagina),
        cuerpo,
        sitio.pie(),
        sitio.SCRIPT_I18N,
    ])


# --------------------------------------------------------------- ficha
def construir_ficha(build_id, iconos, items_stats, vestidor=None):
    with open(os.path.join(DATOS, build_id + ".json"), encoding="utf-8") as f:
        d = json.load(f)

    en_izq = [s for s in IZQUIERDA if s in d["piezas"]]
    en_der = [s for s in DERECHA if s in d["piezas"]]
    abajo = [s for s in d["orden"] if s not in en_izq and s not in en_der]

    col_l = "".join(ranura(d["piezas"][s], iconos, "izq") for s in en_izq)
    col_r = "".join(ranura(d["piezas"][s], iconos, "der") for s in en_der)
    bot = "".join(ranura(d["piezas"][s], iconos, "btm") for s in abajo)

    clase, espec = d["clase"], d["especializacion"]
    raza = d.get("raza", "Orco")
    genero = d.get("genero", "macho")
    faccion = d.get("faccion", "Horda")
    rol = d.get("rol", "")
    clase_icono = d.get("clase_icono", "spell_deathknight_classicon")

    # Si existe un render del personaje se usa como figura de fondo; si no,
    # se recurre al retrato de raza y, en último caso, al icono de clase.
    archivo_pj = sitio.archivo_personaje(raza, genero)
    ruta_pj = os.path.join(AQUI, "assets", "personajes", archivo_pj) if archivo_pj else ""
    con_personaje = bool(ruta_pj and os.path.exists(ruta_pj))
    render_pj = (f'<img class="personaje" src="assets/personajes/{archivo_pj}"'
                 f' alt="{esc(raza)}" loading="lazy">') if con_personaje else ""

    # Retrato de la raza con el icono de clase como distintivo; si la raza no
    # tiene retrato, se cae al icono de clase a tamaño completo.
    icono_raza = sitio.retrato(raza, genero)
    if con_personaje:
        figura = ""
    elif icono_raza and icono_raza in iconos:
        figura = (
            '<div class="retrato">'
            + ic(iconos, icono_raza, "race-ic", raza)
            + ic(iconos, clase_icono, "cl-badge", clase)
            + "</div>"
        )
    else:
        figura = ic(iconos, clase_icono, "cl-ic", clase)

    # Enlace al visor 3D de Wowhead, con la raza y el equipo de esta build.
    url_3d = (vestidor or {}).get(build_id, "")
    if url_3d:
        cubo = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"'
                ' stroke-width="2" stroke-linejoin="round" aria-hidden="true">'
                '<path d="M12 2 3 7v10l9 5 9-5V7z"/><path d="m3 7 9 5 9-5"/>'
                '<path d="M12 12v10"/></svg>')
        enlace_3d = (f'<a class="ver3d" href="{esc(url_3d)}" target="_blank"'
                     f' rel="noopener noreferrer">{cubo}'
                     + bi("Ver en 3D", "View in 3D", "span") + '</a>')
    else:
        enlace_3d = ""

    cuerpo = f"""<div class="page">
<div class="ficha-head">
  {bi(clase, sitio.en(sitio.CLASES, clase), "h1")}
  {bi(espec, sitio.en(sitio.ESPECS, espec), "p", cls="spec-lab")}
  {bi(rol, sitio.en(sitio.ROLES, rol), "p", cls="rol-lab") if rol else ""}
</div>

<div class="pd">
  <div class="col col-l">{col_l}</div>
  <div class="ctr{' con-personaje' if con_personaje else ''}">
    <div class="ctr-bg" aria-hidden="true"></div>
    {render_pj}{figura}
    <p class="ctr-t">
      {bi(raza, sitio.en(sitio.RAZAS, raza), "span", cls="race")}
      {bi(faccion, sitio.en(sitio.FACCIONES, faccion), "span", cls="fac")}
    </p>
    {enlace_3d}
    {panel_stats(d, items_stats)}
  </div>
  <div class="col col-r">{col_r}</div>
  <div class="bot-row">{bot}</div>
</div>
</div>"""

    titulo = f"{clase} · {espec} — {sitio.MARCA_ES}"
    return documento(titulo, CSS_FICHA, cuerpo, "builds")


# --------------------------------------------------------------- índice
CSS_INDEX = """
body{background:var(--bg);color:var(--tx);
  font:14px/1.5 Barlow,"Segoe UI",system-ui,sans-serif;
  min-height:100vh;display:flex;flex-direction:column}
.page{max-width:1120px;margin:0 auto;padding:44px 24px 8px;flex:1;width:100%}
.hero{text-align:center;margin-bottom:18px}
.hero h1{font:700 clamp(26px,4vw,40px)/1.15 Cinzel,Georgia,serif;
  color:#f0eaf8;text-wrap:balance}
.hero .sub{font-size:12.5px;letter-spacing:4px;text-transform:uppercase;
  color:var(--go);margin-top:10px}
.intro{max-width:65ch;margin:20px auto 0;text-align:center;
  color:var(--tn);font-size:14px;line-height:1.7}
.intro strong{color:var(--tx);font-weight:600}
.intro-tags{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;
  margin:18px 0 40px}
.intro-tags span{font-size:11px;letter-spacing:.5px;text-transform:uppercase;
  color:var(--tn);background:var(--p);border:1px solid var(--ln);
  border-radius:14px;padding:5px 12px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(236px,1fr));gap:14px}
.class-card{background:var(--p);border:1px solid var(--ln2);border-radius:10px;
  padding:17px 19px;display:flex;flex-direction:column;gap:11px}
.class-name{font:600 15.5px/1.2 Cinzel,Georgia,serif;color:#f0eaf8}
.specs{display:flex;flex-direction:column;gap:6px}
a.spec{display:flex;justify-content:space-between;align-items:center;gap:8px;
  text-decoration:none;color:var(--tx);
  background:var(--p2);border:1px solid var(--ln);border-radius:6px;
  padding:8px 12px;font-size:13px;transition:border-color .15s,background .15s}
a.spec:hover,a.spec:focus-visible{border-color:var(--gr);background:#1c2620}
a.spec .role{color:var(--tn);font-size:11px;flex:0 0 auto}
a.spec .dot{width:6px;height:6px;border-radius:50%;background:var(--gr);
  flex:0 0 auto;display:inline-block;margin-right:7px}
.site-footer{margin-top:50px}
"""


def construir_index():
    builds = []
    for ruta in sorted(glob.glob(os.path.join(DATOS, "*.json"))):
        nombre = os.path.basename(ruta)
        if nombre.startswith(NO_BUILD):
            continue
        with open(ruta, encoding="utf-8") as f:
            d = json.load(f)
        builds.append({
            "id": d["id"], "clase": d["clase"],
            "espec": d["especializacion"], "rol": d.get("rol", ""),
        })

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
                + bi(b["espec"], sitio.en(sitio.ESPECS, b["espec"]))
                + "</span>"
                + bi(rol_es, rol_en, cls="role")
                + "</a>"
            )
        tarjetas.append(
            '<div class="class-card">'
            + bi(clase, sitio.en(sitio.CLASES, clase), "h2", cls="class-name")
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
  {bi(sitio.MARCA_ES, sitio.MARCA_EN, "h1")}
  {bi("Guías de equipo WotLK · PvE", "WotLK gear guides · PvE", "p", cls="sub")}
</div>
<p class="intro i18n" data-es="{esc(intro_es)}" data-en="{esc(intro_en)}">{intro_es}</p>
<div class="intro-tags">{"".join(bi(a, b) for a, b in etiquetas)}</div>
<div class="grid">{"".join(tarjetas)}</div>
</div>"""

    return documento(sitio.MARCA_ES, CSS_INDEX, cuerpo, "builds")


# --------------------------------------------------------------- comentarios
CSS_COMENTARIOS = """
body{background:var(--bg);color:var(--tx);
  font:14px/1.5 Barlow,"Segoe UI",system-ui,sans-serif;
  min-height:100vh;display:flex;flex-direction:column}
.page{max-width:680px;margin:0 auto;padding:70px 24px;flex:1;width:100%;
  display:flex;flex-direction:column;align-items:center;text-align:center}
.icon-badge{width:54px;height:54px;border-radius:50%;background:var(--p);
  border:1px solid var(--ln2);display:flex;align-items:center;
  justify-content:center;font-size:23px;margin-bottom:20px}
.page h1{font:700 clamp(22px,3.5vw,30px)/1.2 Cinzel,Georgia,serif;
  color:#f0eaf8;margin-bottom:12px}
.lead{color:var(--tn);font-size:14.5px;line-height:1.7;max-width:52ch}
.lead strong{color:var(--tx)}
.status-pill{display:inline-flex;align-items:center;gap:6px;margin-top:24px;
  font-size:11px;letter-spacing:.5px;text-transform:uppercase;color:var(--go);
  background:var(--p);border:1px solid var(--ln);border-radius:14px;padding:6px 14px}
.status-pill .dot{width:6px;height:6px;border-radius:50%;background:var(--go)}
.channels{display:flex;flex-direction:column;gap:10px;margin-top:32px;
  width:100%;max-width:420px}
.channel{display:flex;align-items:center;justify-content:space-between;gap:10px;
  background:var(--p);border:1px solid var(--ln);border-radius:8px;
  padding:12px 16px;text-decoration:none;color:var(--tx);
  transition:border-color .15s,background .15s}
.channel:hover,.channel:focus-visible{border-color:var(--gr);background:#1c2620}
.channel-label{font-size:13px;font-weight:600}
.channel-hint{font-size:11px;color:var(--tn)}
"""


def construir_comentarios():
    lead_es = ("Todavía no hay un sistema de comentarios conectado. Cuando lo activemos "
               "podrás <strong>dejar tu opinión, avisar de un dato incorrecto o pedir una "
               "build nueva</strong> desde cada especialización.")
    lead_en = ("No comment system is connected yet. Once it is live you'll be able to "
               "<strong>leave feedback, flag incorrect data or request a new build</strong> "
               "from any specialization page.")
    cuerpo = f"""<div class="page">
  <div class="icon-badge" aria-hidden="true">💬</div>
  {bi("Comentarios", "Comments", "h1")}
  <p class="lead i18n" data-es="{esc(lead_es)}" data-en="{esc(lead_en)}">{lead_es}</p>
  <p class="status-pill"><span class="dot" aria-hidden="true"></span>
    {bi("Próximamente", "Coming soon")}</p>
  <div class="channels">
    <a class="channel" href="https://github.com/jsgrisales03-stack/wotlk-bis/issues"
       target="_blank" rel="noopener">
      {bi("Reportar en GitHub", "Report on GitHub", cls="channel-label")}
      {bi("Issues del repositorio", "Repository issues", cls="channel-hint")}
    </a>
  </div>
</div>"""
    return documento(f"Comentarios · {sitio.MARCA_ES}", CSS_COMENTARIOS, cuerpo, "comentarios")


# --------------------------------------------------------------- main
def build_ids():
    ids = []
    for ruta in sorted(glob.glob(os.path.join(DATOS, "*.json"))):
        nombre = os.path.basename(ruta)
        if not nombre.startswith(NO_BUILD):
            ids.append(nombre[:-5])
    return ids


def escribir(nombre, contenido):
    ruta = os.path.join(AQUI, nombre)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
    return os.path.getsize(ruta) // 1024


def main(argv):
    with open(os.path.join(DATOS, "iconos.json"), encoding="utf-8") as f:
        iconos = json.load(f)
    items_stats = motor.cargar_items()
    ruta_vestidor = os.path.join(DATOS, "vestidor.json")
    vestidor = {}
    if os.path.exists(ruta_vestidor):
        with open(ruta_vestidor, encoding="utf-8") as f:
            vestidor = json.load(f)
    else:
        print("Aviso: falta datos/vestidor.json; las fichas saldrán sin enlace 3D.")
    if not items_stats:
        print("Aviso: falta datos/stats-items.json; las fichas saldrán sin totales.")

    objetivos = argv[1:] or build_ids()
    for bid in objetivos:
        kb = escribir(bid + ".html", construir_ficha(bid, iconos, items_stats, vestidor))
        print(f"  {bid}.html  {kb} KB")

    if not argv[1:]:
        print(f"  index.html  {escribir('index.html', construir_index())} KB")
        print(f"  comentarios.html  {escribir('comentarios.html', construir_comentarios())} KB")
    print(f"Listo: {len(objetivos)} fichas.")


if __name__ == "__main__":
    main(sys.argv)
