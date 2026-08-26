# -*- coding: utf-8 -*-
"""
Generador del sitio «Arsenal de Corona de Hielo».

    python build.py            genera todo el sitio
    python build.py dk-profano genera sólo esa ficha

Cada ficha se arma desde datos/<id>.json; el índice se deriva de los propios
datos, así que añadir un JSON nuevo basta para que aparezca en la portada.
"""
import json
import re, os, sys, html, glob

import sitio
import stats as motor

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(AQUI, "datos")
# Ficheros de datos/soporte que no describen una build.
NO_BUILD = ("iconos", "stats-", "displayids", "vestidor", "origenes", "_")

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
    """Icono como clase CSS, no como <img> con el base64 incrustado.

    El mismo icono aparece en la tarjeta y en el panel de detalle, y las gemas
    se repiten muchas veces por ficha. Incrustándolo cada vez, una ficha pasaba
    de 149 a 248 KB; por clase, cada icono viaja una sola vez.
    """
    if nombre not in iconos:
        return ""
    rol = f' role="img" aria-label="{esc(alt)}"' if alt else ' aria-hidden="true"'
    return f'<span class="{cls} ic ic-{nombre}"{rol}></span>'


# --------------------------------------------------------------- tooltip
# En el tooltip del juego las características primarias van como "+N Aguante"
# y las secundarias como una línea "Equipar: ...". Se respeta ese orden.
PRIMARIAS_TT = ("fuerza", "agilidad", "intelecto", "espiritu", "aguante")
SECUNDARIAS_TT = ("poder_ataque", "poder_hechizos", "critico", "golpe", "celeridad",
                  "pericia", "penetracion_armadura", "defensa", "esquiva", "parada",
                  "mp5", "temple")
EQUIPAR = {
    "poder_ataque": ("Aumenta el poder de ataque en {n}.", "Increases attack power by {n}."),
    "poder_hechizos": ("Aumenta el poder con hechizos en {n}.", "Increases spell power by {n}."),
    "critico": ("Mejora el índice de golpe crítico en {n}.", "Improves critical strike rating by {n}."),
    "golpe": ("Mejora el índice de golpe en {n}.", "Improves hit rating by {n}."),
    "celeridad": ("Mejora el índice de celeridad en {n}.", "Improves haste rating by {n}."),
    "pericia": ("Aumenta la pericia en {n}.", "Increases expertise rating by {n}."),
    "penetracion_armadura": ("Aumenta la penetración de armadura en {n}.", "Increases armor penetration rating by {n}."),
    "defensa": ("Aumenta el índice de defensa en {n}.", "Increases defense rating by {n}."),
    "esquiva": ("Aumenta el índice de esquiva en {n}.", "Increases dodge rating by {n}."),
    "parada": ("Aumenta el índice de parada en {n}.", "Increases parry rating by {n}."),
    "mp5": ("Restaura {n} p. de maná cada 5 s.", "Restores {n} mana per 5 sec."),
    "temple": ("Aumenta el temple en {n}.", "Increases resilience rating by {n}."),
}


def bloque_stats(p, items_stats):
    """Filas del tooltip: nivel, armadura, primarias, ranuras y efectos."""
    st = items_stats.get(p["id"], {})
    filas = []
    if p.get("heroico"):
        filas.append(bi("Heroico", "Heroic", "p", cls="tt-heroico"))
    filas.append(bi(f'Nivel de objeto {p.get("ilvl", "")}',
                    f'Item Level {p.get("ilvl", "")}', "p", cls="tt-ilvl"))
    filas.append('<p class="tt-ranura">'
                 + bi(p["ranura"], sitio.en(sitio.RANURAS, p["ranura"]), "span") + "</p>")
    if st.get("armadura"):
        filas.append(bi(f'{st["armadura"]} de armadura', f'{st["armadura"]} Armor', "p"))
    for k in PRIMARIAS_TT:
        if st.get(k):
            es, en_ = motor.ETIQUETAS[k]
            filas.append(bi(f'+{st[k]} {es.lower()}', f'+{st[k]} {en_}', "p", cls="tt-prim"))
    for g in p.get("gemas", []):
        color = COLOR_RANURA.get(g["ranura"], "#888")
        filas.append('<p class="tt-soc">'
                     f'<span class="tt-sd" style="background:{color}" aria-hidden="true"></span>'
                     + bi(f'Ranura {g["ranura"].lower()}',
                          f'{sitio.en(sitio.RANURAS, g["ranura"])} Socket', "span") + "</p>")
    if p.get("bono_ranura"):
        filas.append(bi(f'Bono de ranura: {p["bono_ranura"]}',
                        f'Socket Bonus: {sitio.en(sitio.EFECTOS, p["bono_ranura"])}',
                        "p", cls="tt-bono"))
    for k in SECUNDARIAS_TT:
        if st.get(k) and k in EQUIPAR:
            es, en_ = EQUIPAR[k]
            filas.append(bi("Equipar: " + es.format(n=st[k]),
                            "Equip: " + en_.format(n=st[k]), "p", cls="tt-eq"))
    return "".join(filas)


def tooltip(p, iconos, lado, items_stats):
    cls, color = CALIDAD.get(p["calidad"], ("epic", "#a335ee"))
    pos = {"izq": "tt-right", "der": "tt-left"}.get(lado, "tt-center")
    return (f'<div class="tt {pos}">'
            + bi(p["nombre"], p.get("en", p["nombre"]), "p",
                 cls="tt-nombre", extra=f' style="color:{color}"')
            + bloque_stats(p, items_stats)
            + '</div>')


# --------------------------------------------------------------- detalle
def texto_origen(o):
    """Frase de procedencia en ambos idiomas. Los nombres propios de jefes y
    zonas vienen de Wowhead en español; no se traducen."""
    if not o or o.get("tipo") in (None, "desconocido", "error"):
        return None
    quien = esc(o.get("quien", "").strip())
    donde = esc(o.get("donde", "").strip())
    t = o.get("tipo")
    if t == "botin":
        prob = o.get("prob", "")
        cola = f" · {prob}%" if prob else ""
        return (f"Botín de <b>{quien}</b>{' · ' + donde if donde else ''}{cola}",
                f"Dropped by <b>{quien}</b>{' · ' + donde if donde else ''}{cola}")
    if t == "vendedor":
        rol = o.get("rol", "")
        cola = f" · {esc(rol)}" if rol else ""
        return (f"Lo vende <b>{quien}</b>{' · ' + donde if donde else ''}{cola}",
                f"Sold by <b>{quien}</b>{' · ' + donde if donde else ''}{cola}")
    if t == "mision":
        return (f"Recompensa de la misión <b>{quien}</b>{' · ' + donde if donde else ''}",
                f"Quest reward: <b>{quien}</b>{' · ' + donde if donde else ''}")
    if quien:
        return (f"<b>{quien}</b>{' · ' + donde if donde else ''}",
                f"<b>{quien}</b>{' · ' + donde if donde else ''}")
    return None


def detalle(p, iconos, items_stats, origenes, ident):
    """Panel que se abre al pulsar una pieza. Va oculto en la página y el
    script lo copia dentro del diálogo."""
    cls, color = CALIDAD.get(p["calidad"], ("epic", "#a335ee"))
    partes = [
        '<div class="det-cab">',
        f'<span class="s-icon {cls}">' + ic(iconos, p["icono"], "si", p["nombre"])
        + f'<b class="lv">{p["ilvl"]}</b>'
        + ('<b class="hb">H</b>' if p.get("heroico") else "") + '</span>',
        '<div class="det-tit">',
        bi(p["nombre"], p.get("en", p["nombre"]), "h3", extra=f' style="color:{color}"'),
        bi(p["ranura"], sitio.en(sitio.RANURAS, p["ranura"]), "p", cls="det-ranura"),
        '</div></div>',
        '<div class="det-stats">' + bloque_stats(p, items_stats) + '</div>',
    ]

    gemas = p.get("gemas", [])
    if gemas:
        filas = []
        for g in gemas:
            color_g = COLOR_RANURA.get(g["ranura"], "#888")
            marca = ('<span class="tt-skip" title="No respeta el color de la ranura"'
                     ' aria-hidden="true">↯</span>') if g.get("ignora_color") else ""
            filas.append(
                '<li class="det-fila">'
                f'<span class="tt-dot" style="background:{color_g}" aria-hidden="true"></span>'
                + ic(iconos, g["icono"], "det-ic", "")
                + '<div>' + bi(g["gema"], sitio.en(sitio.GEMAS, g["gema"]), "b") + marca
                + bi(g["efecto"], sitio.en(sitio.EFECTOS, g["efecto"])) + '</div></li>')
        partes.append('<section class="det-sec">'
                      + bi("Gemas", "Gems", "h4")
                      + f'<ul class="det-lista">{"".join(filas)}</ul></section>')

    enc = p.get("encantamiento")
    if enc:
        extra = ""
        if enc.get("origen"):
            extra = bi(enc["origen"], sitio.en(sitio.ORIGENES, enc["origen"]),
                       "span", cls="det-fuente")
        partes.append(
            '<section class="det-sec">' + bi("Encantamiento", "Enchant", "h4")
            + '<ul class="det-lista"><li class="det-fila">'
            + ic(iconos, enc["icono"], "det-ic", "")
            + '<div>' + bi(enc["nombre"], sitio.en(sitio.ENCANTAMIENTOS, enc["nombre"]), "b")
            + bi(enc["efecto"], sitio.en(sitio.EFECTOS, enc["efecto"])) + extra
            + '</div></li></ul></section>')

    org = texto_origen(origenes.get(str(p["id"])))
    if org:
        partes.append('<section class="det-sec det-origen">'
                      + bi("Cómo conseguirlo", "How to get it", "h4")
                      + f'<p class="i18n" data-es="{esc(org[0])}" data-en="{esc(org[1])}">{org[0]}</p>'
                      + '</section>')

    return f'<div class="det-fuente-html" id="{ident}" hidden>{"".join(partes)}</div>'


# --------------------------------------------------------------- una ranura
def ranura(p, iconos, lado, items_stats, origenes, ident):
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

    tt = tooltip(p, iconos, lado, items_stats)
    etiqueta = bi(p["ranura"], sitio.en(sitio.RANURAS, p["ranura"]), cls="s-slot")

    return f"""<button type="button" class="slot {lado} has-tt" data-det="{ident}"
    aria-haspopup="dialog">
  <span class="s-icon {cls}">{ic(iconos, p["icono"], "si", p["nombre"])}<b class="lv">{p["ilvl"]}</b>{heroico}</span>
  <span class="s-txt">
    {etiqueta}
    {bi(p["nombre"], p.get("en", p["nombre"]), cls="s-name", extra=f' style="color:{color}"')}
    {linea_enc}{puntos}
  </span>
  {tt}
</button>"""


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
.page{max-width:1560px;width:100%;margin:0 auto;padding:0 16px;
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
/* Termina en transparente, no en el color de fondo: si no, recorta la
   textura del sitio y el panel se lee como una caja vacía. */
.ctr-bg{position:absolute;inset:0;border-radius:12px;
  background:radial-gradient(ellipse 78% 52% at 50% 20%,
    rgba(32,24,52,.85),rgba(20,15,34,.35) 58%,transparent 78%)}
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

/* La tarjeta es un botón: al pasar el cursor muestra las estadísticas y al
   pulsarla abre el panel completo. */
.slot{font:inherit;color:inherit;text-align:left;cursor:pointer;-webkit-appearance:none;appearance:none}

.tt{display:none;position:absolute;z-index:100;
  background:#12101a;border:1px solid var(--ln2);border-radius:8px;
  padding:10px 13px;width:268px;box-shadow:0 10px 34px rgba(0,0,0,.7);
  pointer-events:none;text-align:left}
.slot.has-tt:hover .tt,.slot.has-tt:focus-visible .tt{display:block}
.tt-right{left:calc(100% + 10px);top:50%;transform:translateY(-50%)}
.tt-left{right:calc(100% + 10px);top:50%;transform:translateY(-50%)}
.tt-center{bottom:calc(100% + 8px);left:50%;transform:translateX(-50%)}
.tt p{font-size:11.5px;line-height:1.45;color:#c8c2d6}
.tt-nombre{font-size:13px;font-weight:600;line-height:1.3;margin-bottom:2px}
.tt-heroico{color:var(--gr)}
.tt-ilvl{color:var(--go)}
.tt-ranura{color:var(--tn);margin-bottom:3px}
.tt-prim{color:#e4dff0}
.tt-soc{display:flex;align-items:center;gap:6px;color:var(--tn);margin-top:2px}
.tt-sd{width:8px;height:8px;border-radius:2px;transform:rotate(45deg);flex:0 0 auto}
.tt-bono{color:var(--tn)}
.tt-eq{color:var(--gr);margin-top:2px}
.tt-skip{color:#d99b3c;font-size:11px;margin-left:3px}

/* Diálogo de detalle. */
.paneles{display:none}
.modal{position:fixed;inset:0;z-index:400;display:flex;
  align-items:center;justify-content:center;padding:20px}
.modal[hidden]{display:none}
.modal-fondo{position:absolute;inset:0;background:rgba(6,5,10,.78);
  backdrop-filter:blur(3px)}
.modal-caja{position:relative;z-index:1;width:100%;max-width:430px;
  max-height:86vh;overflow-y:auto;
  background:#14121d;border:1px solid var(--ln2);border-radius:13px;
  padding:20px 22px 22px;box-shadow:0 24px 70px rgba(0,0,0,.75)}
.modal-x{position:absolute;top:10px;right:12px;border:0;background:transparent;
  color:var(--tn);font-size:24px;line-height:1;cursor:pointer;padding:4px 8px;
  border-radius:6px}
.modal-x:hover,.modal-x:focus-visible{color:var(--tx);background:var(--p2)}

.det-cab{display:flex;gap:13px;align-items:flex-start;padding-right:26px}
.det-cab .si{width:46px;height:46px}
.det-tit h3{font:600 15.5px/1.25 Barlow,sans-serif;text-wrap:balance}
.det-ranura{font-size:10px;letter-spacing:1.2px;text-transform:uppercase;
  color:var(--db);margin-top:3px}
.det-stats{margin-top:14px;padding-top:12px;border-top:1px solid var(--ln)}
.det-stats p{font-size:12px;line-height:1.5;color:#c8c2d6}
.det-sec{margin-top:16px;padding-top:13px;border-top:1px solid var(--ln)}
.det-sec h4{font:600 10px Barlow,sans-serif;letter-spacing:1.6px;
  text-transform:uppercase;color:var(--go);margin-bottom:8px}
.det-lista{list-style:none;display:flex;flex-direction:column;gap:9px}
.det-fila{display:flex;gap:9px;align-items:flex-start}
.det-ic{width:26px;height:26px;border-radius:5px;flex:0 0 auto;border:1px solid var(--ln2)}
.det-fila b{display:block;font-size:12.5px;font-weight:600;color:#d5cee3;line-height:1.3}
.det-fila span{display:block;font-size:11.5px;color:var(--tn);line-height:1.4}
.det-fuente{color:var(--db);font-size:10.5px;margin-top:2px}
.det-origen p{font-size:12.5px;line-height:1.55;color:var(--tx)}
.det-origen b{color:var(--go);font-weight:600}

@media(max-width:980px){
  /* En vertical el contenido tiene que poder crecer. La cadena de flex:1 con
     min-height:0 dejaba la ficha a la altura de la ventana y las tarjetas se
     solapaban unas con otras. */
  .page{display:block;min-height:auto;padding-bottom:14px}
  .pd{display:flex;flex-direction:column;flex:none;min-height:auto;
    gap:8px;padding-top:10px}
  .col{align-items:stretch;justify-content:flex-start;min-height:auto;gap:5px}
  .col-l{order:2}
  .ctr{order:1;padding:4px 0 10px}
  .col-r{order:3}
  .bot-row{order:4;padding-top:4px}
  .stats{max-width:340px;margin:0 auto}
  .slot,.slot.izq{flex-direction:row;text-align:left;max-width:100%}
  .slot.izq .s-dots{justify-content:flex-start}
  .slot.btm{max-width:100%}
  /* En táctil no hay hover: la pieza se pulsa y se abre el diálogo. */
  .slot.has-tt{padding-right:24px}
  .slot.has-tt::after{content:"";position:absolute;right:10px;top:50%;
    width:6px;height:6px;margin-top:-4px;
    border-right:1.5px solid var(--db);border-bottom:1.5px solid var(--db);
    transform:rotate(45deg);transition:transform .15s ease,border-color .15s ease}
  .slot.has-tt:focus-within::after{transform:rotate(-135deg);margin-top:-1px;
    border-color:var(--gr)}
  .tt{display:none!important}
  .modal-caja{max-width:100%;padding:18px 16px 20px}
}
/* En pantallas grandes crece el propio paperdoll: como las tarjetas se pegan
   al centro, ensanchar la página sólo empujaría hueco hacia los lados. */
@media(min-width:1440px){
  .pd{grid-template-columns:1fr minmax(250px,336px) 1fr}
  .slot{max-width:388px}
  .slot.btm{max-width:276px}
  .personaje{height:300px}
  .ctr.con-personaje .ctr-t{margin-top:206px}
  .s-name{font-size:13px}
  .stat dt{font-size:12px}
  .stat dd{font-size:13px}
}
@media(min-width:1800px){
  .pd{grid-template-columns:1fr minmax(280px,382px) 1fr}
  .slot{max-width:432px}
  .slot.btm{max-width:308px}
  .personaje{height:344px}
  .ctr.con-personaje .ctr-t{margin-top:238px}
  .s-name{font-size:13.5px}
  .s-enc{font-size:11px}
  .si{width:40px;height:40px}
}
@media(max-width:430px){
  .ficha-head{padding:10px 0 2px}
  .spec-lab{letter-spacing:2.5px;font-size:12px}
  .slot{padding:5px 9px;gap:7px}
  .si{width:32px;height:32px}
  .s-name{font-size:12px}
  .s-enc{font-size:10px}
  .stats{padding:10px 11px 8px}
  .bot-row{gap:5px}
}
/* Portátiles de pantalla baja: se recorta el aire para que la ficha siga
   entrando de una sola vez, que es el objetivo del diseño. */
@media(min-width:981px) and (max-height:860px){
  .ficha-head{padding:10px 0 2px}
  .personaje{height:228px}
  .ctr.con-personaje .ctr-t{margin-top:142px}
  .pd{padding-top:2px}
  .bot-row{padding-top:6px}
}
@media(prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
"""


def css_iconos(cuerpo, iconos):
    """Regla de fondo para cada icono que aparece en esta página."""
    usados = sorted(set(re.findall(r"ic-([a-z0-9_]+)", cuerpo)))
    reglas = [".ic{background-size:cover;background-position:center;"
              "background-repeat:no-repeat;display:inline-block;flex:0 0 auto}"]
    for n in usados:
        src = iconos.get(n)
        if src:
            reglas.append(f".ic-{n}{{background-image:url({src})}}")
    return "".join(reglas)


def documento(titulo, css, cuerpo, pagina, iconos=None):
    """Envoltorio común a todas las páginas del sitio."""
    return "\n".join([
        '<html lang="es">',
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width,initial-scale=1">',
        f"<title>{esc(titulo)}</title>",
        sitio.FUENTES,
        f"<style>{sitio.TOKENS}{sitio.CABECERA_CSS}{css}{sitio.FONDO_CSS}"
        f"{css_iconos(cuerpo, iconos or {})}</style>",
        '<div class="fondo" aria-hidden="true"></div>',
        sitio.cabecera(pagina),
        cuerpo,
        sitio.SCRIPT_I18N,
        sitio.SCRIPT_DETALLE if 'id="modal"' in cuerpo else "",
    ])


# --------------------------------------------------------------- ficha
def construir_ficha(build_id, iconos, items_stats, vestidor=None, origenes=None):
    with open(os.path.join(DATOS, build_id + ".json"), encoding="utf-8") as f:
        d = json.load(f)

    en_izq = [s for s in IZQUIERDA if s in d["piezas"]]
    en_der = [s for s in DERECHA if s in d["piezas"]]
    abajo = [s for s in d["orden"] if s not in en_izq and s not in en_der]

    origenes = origenes or {}
    paneles = []

    def col(claves, lado):
        salida = []
        for k in claves:
            ident = "det-" + k
            salida.append(ranura(d["piezas"][k], iconos, lado, items_stats, origenes, ident))
            paneles.append(detalle(d["piezas"][k], iconos, items_stats, origenes, ident))
        return "".join(salida)

    col_l = col(en_izq, "izq")
    col_r = col(en_der, "der")
    bot = col(abajo, "btm")

    clase, espec = d["clase"], d["especializacion"]
    raza = d.get("raza", "Orco")
    genero = d.get("genero", "macho")
    faccion = d.get("faccion", "Horda")
    rol = d.get("rol", "")
    clase_icono = d.get("clase_icono", "spell_deathknight_classicon")

    # Si existe un render del personaje se usa como figura de fondo; si no,
    # se recurre al retrato de raza y, en último caso, al icono de clase.
    # Se prefiere el render propio de esta build (con su equipo puesto); si no
    # existe, se cae al render genérico de la raza.
    carpeta_pj = os.path.join(AQUI, "assets", "personajes")
    archivo_pj = ""
    if os.path.exists(os.path.join(carpeta_pj, build_id + ".png")):
        archivo_pj = build_id + ".png"
    else:
        generico = sitio.archivo_personaje(raza, genero)
        if generico and os.path.exists(os.path.join(carpeta_pj, generico)):
            archivo_pj = generico
    con_personaje = bool(archivo_pj)
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
</div>
<div class="modal" id="modal" hidden>
  <div class="modal-fondo" data-cerrar></div>
  <div class="modal-caja" role="dialog" aria-modal="true" aria-labelledby="modal-tit">
    <button type="button" class="modal-x" data-cerrar aria-label="Cerrar"
      data-i18n-title data-title-es="Cerrar" data-title-en="Close">&times;</button>
    <div class="modal-cuerpo" id="modal-tit"></div>
  </div>
</div>
<div class="paneles" hidden>{"".join(paneles)}</div>"""

    titulo = f"{clase} · {espec} — {sitio.MARCA_ES}"
    return documento(titulo, CSS_FICHA, cuerpo, "builds", iconos)


# --------------------------------------------------------------- índice
CSS_INDEX = """
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


def construir_index(iconos):
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
            "icono": d.get("clase_icono", ""),
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
        icono = next((b["icono"] for b in specs if b["icono"]), "")
        cabecera = (
            '<div class="class-head">'
            + (ic(iconos, icono, "class-ic", clase) if icono in iconos else "")
            + bi(clase, sitio.en(sitio.CLASES, clase), "h2", cls="class-name")
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
  {bi(sitio.MARCA_ES, sitio.MARCA_EN, "h1")}
  {bi("Guías de equipo WotLK · PvE", "WotLK gear guides · PvE", "p", cls="sub")}
</div>
<p class="intro i18n" data-es="{esc(intro_es)}" data-en="{esc(intro_en)}">{intro_es}</p>
<div class="intro-tags">{"".join(bi(a, b) for a, b in etiquetas)}</div>
<div class="grid">{"".join(tarjetas)}</div>
</div>"""

    return documento(sitio.MARCA_ES, CSS_INDEX, cuerpo, "builds", iconos)


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
.previsto{list-style:none;margin:30px auto 0;max-width:430px;width:100%;
  display:flex;flex-direction:column;gap:9px;text-align:left}
.previsto li{display:flex;align-items:flex-start;gap:10px;
  background:var(--p);border:1px solid var(--ln);border-radius:8px;
  padding:12px 15px;font-size:13px;color:var(--tx);line-height:1.45}
.pv-ic{color:var(--go);font-size:9px;line-height:1.9;flex:0 0 auto}
@media(max-width:600px){
  .page{padding:44px 18px}
  .channels{max-width:100%}
  .lead{font-size:13.5px}
}
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
  <ul class="previsto">
    <li><span class="pv-ic" aria-hidden="true">◆</span>
      {bi("Señalar un dato incorrecto en cualquier ficha",
          "Flag incorrect data on any page")}</li>
    <li><span class="pv-ic" aria-hidden="true">◆</span>
      {bi("Proponer una alternativa de gema o encantamiento",
          "Suggest an alternative gem or enchant")}</li>
    <li><span class="pv-ic" aria-hidden="true">◆</span>
      {bi("Pedir una especialización o una variante de banda",
          "Request a specialization or raid variant")}</li>
  </ul>
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
    ruta_origenes = os.path.join(DATOS, "origenes.json")
    origenes = {}
    if os.path.exists(ruta_origenes):
        with open(ruta_origenes, encoding="utf-8") as f:
            origenes = json.load(f)
    else:
        print("Aviso: falta datos/origenes.json; no se mostrará la procedencia.")
    if not items_stats:
        print("Aviso: falta datos/stats-items.json; las fichas saldrán sin totales.")

    objetivos = argv[1:] or build_ids()
    for bid in objetivos:
        kb = escribir(bid + ".html", construir_ficha(bid, iconos, items_stats, vestidor, origenes))
        print(f"  {bid}.html  {kb} KB")

    if not argv[1:]:
        print(f"  index.html  {escribir('index.html', construir_index(iconos))} KB")
        print(f"  comentarios.html  {escribir('comentarios.html', construir_comentarios())} KB")
    print(f"Listo: {len(objetivos)} fichas.")


if __name__ == "__main__":
    main(sys.argv)
