# -*- coding: utf-8 -*-
"""
Motor de estadísticas: suma las estadísticas de un conjunto completo.

El total de una build se compone de cuatro fuentes:
  1. Estadísticas base de cada objeto      -> datos/stats-items.json (extraído de Wowhead)
  2. Gemas engarzadas                       -> GEMAS
  3. Encantamientos aplicados               -> ENCANTAMIENTOS
  4. Bonificaciones de ranura                -> campo "bono_ranura" de cada pieza,
     que sólo cuenta si TODAS las gemas de esa pieza respetan el color de su ranura.
"""
import json, os, re

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(AQUI, "datos")

# --- Estadísticas reconocidas, en orden de presentación ---------------------
ETIQUETAS = {
    "fuerza":               ("Fuerza",                  "Strength"),
    "agilidad":             ("Agilidad",                "Agility"),
    "intelecto":            ("Intelecto",               "Intellect"),
    "espiritu":             ("Espíritu",                "Spirit"),
    "aguante":              ("Aguante",                 "Stamina"),
    "salud":                ("Salud",                   "Health"),
    "armadura":             ("Armadura",                "Armor"),
    "poder_ataque":         ("Poder de ataque",         "Attack power"),
    "poder_hechizos":       ("Poder con hechizos",      "Spell power"),
    "critico":              ("Crítico",                 "Crit rating"),
    "golpe":                ("Golpe",                   "Hit rating"),
    "celeridad":            ("Celeridad",               "Haste rating"),
    "pericia":              ("Pericia",                 "Expertise rating"),
    "penetracion_armadura": ("Pen. de armadura",        "Armor penetration"),
    "defensa":              ("Defensa",                 "Defense rating"),
    "esquiva":              ("Esquiva",                 "Dodge rating"),
    "parada":               ("Parada",                  "Parry rating"),
    "mp5":                  ("Maná cada 5 s",           "Mana per 5 sec"),
    "temple":               ("Temple",                  "Resilience"),
}

TODAS_PRIMARIAS = ("fuerza", "agilidad", "intelecto", "espiritu", "aguante")

# --- Estadísticas por gema -------------------------------------------------
GEMAS = {
    "Rubí cárdeno llamativo":                   {"fuerza": 20},
    "Rubí cárdeno rúnico":                      {"poder_hechizos": 23},
    "Rubí cárdeno rúnico delicado":             {"agilidad": 23},
    "Circón majestuoso sólido":                 {"aguante": 30},
    "Piedra de terror de guardián":             {"pericia": 10, "aguante": 15},
    "Lágrima de pesadilla":                     {k: 10 for k in TODAS_PRIMARIAS},
    "Diamante de asedio de tierra incansable":  {"agilidad": 21},
    "Diamante de asedio de tierra austero":     {"aguante": 32},
    "Diamante de llama celeste de ascuas":      {"poder_hechizos": 25},
    "Diamante de llama celeste revitalizante":  {"mp5": 11},
}

# --- Estadísticas por encantamiento ---------------------------------------
# Los que van vacíos son efectos activos o procs: no aportan estadística constante.
ENCANTAMIENTOS = {
    "Arcanum de tormento":                          {"poder_ataque": 50, "critico": 20},
    "Arcanum de misterios ardientes":               {"poder_hechizos": 30, "critico": 20},
    "Arcanum de alivio de gozo":                    {"poder_hechizos": 30, "mp5": 10},
    "Arcanum del adepto protector":                 {"aguante": 37, "defensa": 20},
    "Inscripción del hacha superior":               {"poder_ataque": 40, "critico": 15},
    "Inscripción de la tormenta superior":          {"poder_hechizos": 24, "critico": 15},
    "Inscripción del risco superior":               {"poder_hechizos": 24, "mp5": 8},
    "Inscripción del gladiador superior":           {"aguante": 30, "temple": 15},
    "Encantar capa: velocidad superior":            {"celeridad": 23},
    "Encantar capa: Armadura poderosa":             {"armadura": 225},
    "Encantar capa: sabiduría":                     {"espiritu": 10},
    "Encantar capa: Perforar con hechizos":         {},
    "Encantar pechera: estadísticas potentes":      {k: 10 for k in TODAS_PRIMARIAS},
    "Encantar pechera: supersalud":                 {"salud": 275},
    "Encantar brazales: asalto superior":           {"poder_ataque": 50},
    "Encantar brazales: aguante sublime":           {"aguante": 40},
    "Encantar brazales: poder con hechizos excelente": {"poder_hechizos": 30},
    "Encantar guantes: triturador":                 {"poder_ataque": 44},
    "Encantar guantes: poder con hechizos excepcional": {"poder_hechizos": 28},
    "Cincha de armadura reticulada":                {"armadura": 885},
    "Aceleradores de hipervelocidad":               {},
    "Hebilla de cinturón eterna":                   {},
    "Armadura de pierna de escama de hielo":        {"poder_ataque": 75, "critico": 22},
    "Armadura de pierna nerubiana":                 {"poder_ataque": 55, "critico": 15},
    "Armadura para pierna de pellejo de escarcha":  {"aguante": 55, "agilidad": 22},
    "Hilo de hechizo de zafiro":                    {"poder_hechizos": 50, "aguante": 30},
    "Encantar botas: asalto superior":              {"poder_ataque": 32},
    "Encantar botas: caminante del hielo":          {"golpe": 12, "critico": 12},
    "Encantar botas: vitalidad de los colmillarr":  {"aguante": 15},
    "Encantar botas: vitalidad superior":           {"mp5": 7},
    "Propulsiones de nitro":                        {"critico": 24},
    "Encantar arma: matanza mayor":                 {"poder_ataque": 110},
    "Encantar arma: poder con hechizos poderoso":   {"poder_hechizos": 63},
    "Encantar arma: mangosta":                      {},
    "Encantar arma a distancia: certeza mortal":    {"golpe": 40},
    "Encantar anillo: asalto":                      {"poder_ataque": 40},
    "Runa del cruzado caído":                       {},
    "Runa de la gárgola piel de piedra":            {"defensa": 25},
}

# --- Parser de texto "+N estadística" --------------------------------------
_ALIAS = [
    (r"(?:índice de )?golpe crítico|crítico",   "critico"),
    (r"penetración de armadura",                "penetracion_armadura"),
    (r"poder de ataque",                        "poder_ataque"),
    (r"poder con hechizos",                     "poder_hechizos"),
    (r"(?:índice de )?celeridad",               "celeridad"),
    (r"(?:índice de )?pericia",                 "pericia"),
    (r"(?:índice de )?defensa",                 "defensa"),
    (r"(?:índice de )?esquiva",                 "esquiva"),
    (r"(?:índice de )?parada",                  "parada"),
    (r"(?:índice de )?temple",                  "temple"),
    (r"(?:índice de )?golpe",                   "golpe"),
    (r"maná(?: cada 5 s(?:egundos)?|/5s)",      "mp5"),
    (r"fuerza",                                 "fuerza"),
    (r"agilidad",                               "agilidad"),
    (r"intelecto",                              "intelecto"),
    (r"espíritu",                               "espiritu"),
    (r"aguante",                                "aguante"),
    (r"armadura",                               "armadura"),
    (r"salud",                                  "salud"),
]
_RE_ALIAS = [(re.compile(pat, re.I), clave) for pat, clave in _ALIAS]
_RE_PAR = re.compile(r"\+(\d+)\s+([^+,;]+)")


def parsear(texto):
    """'+8 fuerza' -> {'fuerza': 8}.  '+10 a todas las estadísticas' -> las 5 primarias."""
    out = {}
    if not texto:
        return out
    if "todas las estad" in texto.lower():
        m = re.search(r"\+(\d+)", texto)
        if m:
            for k in TODAS_PRIMARIAS:
                out[k] = out.get(k, 0) + int(m.group(1))
        return out
    for m in _RE_PAR.finditer(texto):
        valor, resto = int(m.group(1)), m.group(2).strip()
        for rx, clave in _RE_ALIAS:
            if rx.search(resto):
                out[clave] = out.get(clave, 0) + valor
                break
    return out


def _sumar(acc, aporte):
    for k, v in aporte.items():
        if v:
            acc[k] = acc.get(k, 0) + v


def cargar_items():
    ruta = os.path.join(DATOS, "stats-items.json")
    if not os.path.exists(ruta):
        return {}
    with open(ruta, encoding="utf-8") as f:
        return {int(k): v for k, v in json.load(f).items()}


def bonificacion_activa(pieza):
    """La bonificación de ranura sólo cuenta si ninguna gema ignora el color de su ranura."""
    gemas = pieza.get("gemas", [])
    if not gemas:
        return False
    return not any(g.get("ignora_color") for g in gemas)


def calcular(build, items_stats):
    """Devuelve (totales, desglose) de un conjunto completo."""
    totales, desglose = {}, {"objetos": {}, "gemas": {}, "encantamientos": {}, "bonificaciones": {}}

    for pieza in build["piezas"].values():
        base = items_stats.get(pieza["id"], {})
        aporte = {k: v for k, v in base.items() if k in ETIQUETAS}
        _sumar(totales, aporte)
        _sumar(desglose["objetos"], aporte)

        for gema in pieza.get("gemas", []):
            g = GEMAS.get(gema["gema"]) or parsear(gema.get("efecto"))
            _sumar(totales, g)
            _sumar(desglose["gemas"], g)

        enc = pieza.get("encantamiento")
        if enc:
            e = ENCANTAMIENTOS.get(enc["nombre"])
            if e is None:
                e = parsear(enc.get("efecto"))
            _sumar(totales, e)
            _sumar(desglose["encantamientos"], e)

        if bonificacion_activa(pieza):
            b = parsear(pieza.get("bono_ranura"))
            _sumar(totales, b)
            _sumar(desglose["bonificaciones"], b)

    # El aguante se convierte en salud: 10 p. de salud por punto.
    if totales.get("aguante"):
        totales["salud"] = totales.get("salud", 0) + totales["aguante"] * 10

    return totales, desglose


# --- Qué estadísticas destacar según el rol --------------------------------
PERFILES = {
    "tanque":   ["aguante", "salud", "armadura", "defensa", "esquiva", "parada",
                 "fuerza", "agilidad", "poder_ataque", "critico", "pericia", "golpe"],
    "sanador":  ["intelecto", "poder_hechizos", "espiritu", "mp5", "critico",
                 "celeridad", "aguante", "salud"],
    "caster":   ["poder_hechizos", "intelecto", "critico", "golpe", "celeridad",
                 "espiritu", "aguante", "salud"],
    "fuerza":   ["fuerza", "poder_ataque", "critico", "golpe", "celeridad",
                 "pericia", "penetracion_armadura", "aguante", "salud"],
    "agilidad": ["agilidad", "poder_ataque", "critico", "golpe", "celeridad",
                 "pericia", "penetracion_armadura", "aguante", "salud"],
}

# Una estadística primaria con un valor residual (sólo aportado por gemas
# híbridas) es ruido: se oculta si no llega a esta fracción de la mayor.
UMBRAL_PRIMARIA = 0.12


def perfil_de(build, totales=None):
    rol = (build.get("rol") or "").lower()
    if "tanque" in rol:
        return "tanque"
    if "sanador" in rol:
        return "sanador"

    if totales:
        sp = totales.get("poder_hechizos", 0)
        fisico = max(totales.get("fuerza", 0), totales.get("agilidad", 0))
        if sp > fisico:
            return "caster"
        return "fuerza" if totales.get("fuerza", 0) >= totales.get("agilidad", 0) else "agilidad"

    principal = (build.get("gemas_clave", {}).get("roja") or {}).get("efecto", "")
    if "hechizos" in principal:
        return "caster"
    return "agilidad" if "agilidad" in principal else "fuerza"


def visibles(totales, perfil):
    """Claves a mostrar, en orden, ya filtradas de ruido."""
    mayor = max((totales.get(k, 0) for k in TODAS_PRIMARIAS), default=0)
    fuera = set()
    if mayor:
        for k in TODAS_PRIMARIAS:
            v = totales.get(k, 0)
            if v and v < mayor * UMBRAL_PRIMARIA:
                fuera.add(k)
    return [k for k in PERFILES[perfil]
            if totales.get(k) and k not in fuera]
