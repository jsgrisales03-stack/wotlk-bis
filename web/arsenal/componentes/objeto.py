# -*- coding: utf-8 -*-
"""Presentación de un objeto: lo que comparten el tip y el panel de detalle."""
from .. import motor, textos
from ..html import bi, esc

COLOR_RANURA = {
    "Roja": "#e5484d", "Amarilla": "#f5d90a", "Azul": "#4a9eff",
    "Meta": "#d9b45b", "Prismática": "#c084fc",
}
CALIDAD = {4: ("epic", "#a335ee"), 5: ("legendary", "#ff8000")}

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


def bloque_stats(p, items_stats):
    """Filas del tooltip: nivel, armadura, primarias, ranuras y efectos."""
    st = items_stats.get(p["id"], {})
    filas = []
    if p.get("heroico"):
        filas.append(bi("Heroico", "Heroic", "p", cls="tt-heroico"))
    filas.append(bi(f'Nivel de objeto {p.get("ilvl", "")}',
                    f'Item Level {p.get("ilvl", "")}', "p", cls="tt-ilvl"))
    filas.append('<p class="tt-ranura">'
                 + bi(p["ranura"], textos.en(textos.RANURAS, p["ranura"]), "span") + "</p>")
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
                          f'{textos.en(textos.RANURAS, g["ranura"])} Socket', "span") + "</p>")
    if p.get("bono_ranura"):
        filas.append(bi(f'Bono de ranura: {p["bono_ranura"]}',
                        f'Socket Bonus: {textos.en(textos.EFECTOS, p["bono_ranura"])}',
                        "p", cls="tt-bono"))
    for k in SECUNDARIAS_TT:
        if st.get(k) and k in EQUIPAR:
            es, en_ = EQUIPAR[k]
            filas.append(bi("Equipar: " + es.format(n=st[k]),
                            "Equip: " + en_.format(n=st[k]), "p", cls="tt-eq"))
    return "".join(filas)
