# -*- coding: utf-8 -*-
"""Marca del sitio y tablas de traducción.

Todo el texto que se muestra en dos idiomas vive aquí, para que añadir
una build no obligue a tocar más de un fichero.
"""

MARCA_ES = "Arsenal de Corona de Hielo"
MARCA_EN = "Icecrown Arsenal"

# ---------------------------------------------------------------- traducciones
CLASES = {
    "Caballero de la Muerte": "Death Knight",
    "Guerrero": "Warrior",
    "Paladín": "Paladin",
    "Cazador": "Hunter",
    "Pícaro": "Rogue",
    "Sacerdote": "Priest",
    "Chamán": "Shaman",
    "Mago": "Mage",
    "Brujo": "Warlock",
    "Druida": "Druid",
}

ESPECS = {
    "Profano": "Unholy", "Sangre": "Blood", "Escarcha": "Frost",
    "Armas": "Arms", "Furia": "Fury", "Protección": "Protection",
    "Reprensión": "Retribution", "Sagrado": "Holy",
    "Puntería": "Marksmanship", "Bestias": "Beast Mastery", "Supervivencia": "Survival",
    "Asesinato": "Assassination", "Combate": "Combat", "Sutileza": "Subtlety",
    "Disciplina": "Discipline", "Sombras": "Shadow",
    "Elemental": "Elemental", "Mejora": "Enhancement", "Restauración": "Restoration",
    "Arcano": "Arcane", "Fuego": "Fire",
    "Aflicción": "Affliction", "Demonología": "Demonology", "Destrucción": "Destruction",
    "Equilibrio": "Balance", "Feral — DPS": "Feral — DPS", "Feral — Tanque": "Feral — Tank",
}

RAZAS = {
    "Orco": "Orc", "Trol": "Troll", "Elfo de sangre": "Blood Elf",
    "No-muerto": "Undead", "Tauren": "Tauren", "Goblin": "Goblin",
}

FACCIONES = {"Horda": "Horde", "Alianza": "Alliance"}

# Retrato del personaje: nombre interno de la raza en los archivos del juego.

ROLES = {
    "DPS cuerpo a cuerpo — PvE": "Melee DPS — PvE",
    "DPS a distancia — PvE": "Ranged DPS — PvE",
    "Tanque — PvE": "Tank — PvE",
    "Sanador — PvE": "Healer — PvE",
}

RANURAS = {
    "Cabeza": "Head", "Cuello": "Neck", "Hombros": "Shoulders", "Espalda": "Back",
    "Pecho": "Chest", "Muñecas": "Wrists", "Manos": "Hands", "Cintura": "Waist",
    "Piernas": "Legs", "Pies": "Feet", "Anillo": "Ring", "Abalorio": "Trinket",
    "Arma": "Weapon", "Objeto secundario": "Off hand", "Vara": "Wand",
    "A distancia": "Ranged", "Sigilo": "Sigil", "Tótem": "Totem",
    "Ídolo": "Idol", "Libram": "Libram", "Escudo": "Shield",
}

COLORES_RANURA = {
    "Roja": "Red", "Amarilla": "Yellow", "Azul": "Blue",
    "Meta": "Meta", "Prismática": "Prismatic",
}

GEMAS = {
    "Rubí cárdeno llamativo": "Bold Cardinal Ruby",
    "Rubí cárdeno delicado": "Delicate Cardinal Ruby",
    "Rubí cárdeno rúnico": "Runed Cardinal Ruby",
    "Circón majestuoso sólido": "Solid Majestic Zircon",
    "Piedra de terror de guardián": "Guardian's Dreadstone",
    "Lágrima de pesadilla": "Nightmare Tear",
    "Diamante de asedio de tierra incansable": "Relentless Earthsiege Diamond",
    "Diamante de asedio de tierra austero": "Austere Earthsiege Diamond",
    "Diamante de llama celeste de ascuas": "Ember Skyflare Diamond",
    "Diamante de llama celeste revitalizante": "Revitalizing Skyflare Diamond",
}

ENCANTAMIENTOS = {
    "Arcanum de tormento": "Arcanum of Torment",
    "Arcanum de misterios ardientes": "Arcanum of Burning Mysteries",
    "Arcanum de alivio de gozo": "Arcanum of Blissful Mending",
    "Arcanum del adepto protector": "Arcanum of the Stalwart Protector",
    "Inscripción del hacha superior": "Greater Inscription of the Axe",
    "Inscripción de la tormenta superior": "Greater Inscription of the Storm",
    "Inscripción del risco superior": "Greater Inscription of the Crag",
    "Inscripción del gladiador superior": "Greater Inscription of the Gladiator",
    "Encantar capa: velocidad superior": "Enchant Cloak — Greater Speed",
    "Encantar capa: armadura poderosa": "Enchant Cloak — Mighty Armor",
    "Encantar capa: sabiduría": "Enchant Cloak — Wisdom",
    "Encantar capa: perforar con hechizos": "Enchant Cloak — Spell Piercing",
    "Encantar pechera: estadísticas potentes": "Enchant Chest — Powerful Stats",
    "Encantar pechera: supersalud": "Enchant Chest — Super Health",
    "Encantar brazales: asalto superior": "Enchant Bracers — Greater Assault",
    "Encantar brazales: aguante sublime": "Enchant Bracers — Major Stamina",
    "Encantar brazales: poder con hechizos excelente": "Enchant Bracers — Superior Spellpower",
    "Encantar guantes: triturador": "Enchant Gloves — Crusher",
    "Encantar guantes: poder con hechizos excepcional": "Enchant Gloves — Exceptional Spellpower",
    "Cincha de armadura reticulada": "Reticulated Armor Webbing",
    "Aceleradores de hipervelocidad": "Hyperspeed Accelerators",
    "Hebilla de cinturón eterna": "Eternal Belt Buckle",
    "Armadura de pierna de escama de hielo": "Icescale Leg Armor",
    "Armadura de pierna nerubiana": "Nerubian Leg Armor",
    "Armadura para pierna de pellejo de escarcha": "Frosthide Leg Armor",
    "Hilo de hechizo de zafiro": "Sapphire Spellthread",
    "Encantar botas: asalto superior": "Enchant Boots — Greater Assault",
    "Encantar botas: caminante del hielo": "Enchant Boots — Icewalker",
    "Encantar botas: vitalidad colmillarr": "Enchant Boots — Tuskarr's Vitality",
    "Encantar botas: vitalidad superior": "Enchant Boots — Greater Vitality",
    "Propulsiones de nitro": "Nitro Boosts",
    "Encantar arma: matanza mayor": "Enchant 2H Weapon — Massacre",
    "Encantar arma: poder con hechizos poderoso": "Enchant Weapon — Mighty Spellpower",
    "Encantar arma: mangosta": "Enchant Weapon — Mongoose",
    "Mira buscacorazones": "Heartseeker Scope",
    "Encantar anillo: asalto": "Enchant Ring — Assault",
    "Runa del cruzado caído": "Rune of the Fallen Crusader",
    "Runa de la gárgola piel de piedra": "Rune of the Stoneskin Gargoyle",
    # mejoras de profesión que aparecen en las capturas de referencia
    "Bordado de tejido de luz": "Lightweave Embroidery",
    "Bordado de guardia de espada": "Swordguard Embroidery",
    "Bordado de resplandor oscuro": "Darkglow Embroidery",
    "Base de tejido flexible": "Flexweave Underlay",
    "Cinturón de fragmentación": "Frag Belt",
    "Generador de pulso electromagnético personal": "Personal Electromagnetic Pulse Generator",
    "Disco de amplificación mental": "Mind Amplification Dish",
    "Forro de pelaje de poder con hechizos": "Fur Lining — Spell Power",
    "Forro de pelaje de aguante": "Fur Lining — Stamina",
    "Encantar escudo: intelecto superior": "Enchant Shield — Greater Intellect",
    "Encantar arma: Rabiar": "Enchant Weapon — Berserking",
    "Encantar arma: drenador de sangre": "Enchant Weapon — Blood Draining",
    "Hilo de hechizo luminoso": "Brilliant Spellthread",
    "Encantar pechera: espíritu sublime": "Enchant Chest — Major Spirit",
    "Refuerzo para armadura boreal pesado": "Heavy Borean Armor Kit",
}

# Texto de efecto ES -> EN. Cubre gemas, encantamientos y bonificaciones de ranura.
EFECTOS = {
    # gemas
    "+20 fuerza": "+20 Strength",
    "+20 agilidad": "+20 Agility",
    "+23 poder con hechizos": "+23 Spell power",
    "+30 aguante": "+30 Stamina",
    "+10 pericia, +15 aguante": "+10 Expertise, +15 Stamina",
    "+10 a todas las estadísticas": "+10 to all stats",
    "+21 agilidad, +3% daño crítico": "+21 Agility, +3% crit damage",
    "+32 aguante, +2% armadura": "+32 Stamina, +2% armor",
    "+25 poder con hechizos, +2% intelecto": "+25 Spell power, +2% Intellect",
    "+11 maná/5s, +3% curación crítica": "+11 mana/5s, +3% crit healing",
    # encantamientos
    "+50 poder de ataque y +20 índice de golpe crítico": "+50 Attack power and +20 crit rating",
    "+30 poder con hechizos y +20 índice de golpe crítico": "+30 Spell power and +20 crit rating",
    "+30 poder con hechizos y +10 maná cada 5 segundos": "+30 Spell power and +10 mana per 5 sec",
    "+37 aguante y +20 defensa": "+37 Stamina and +20 Defense",
    "+40 poder de ataque y +15 índice de golpe crítico": "+40 Attack power and +15 crit rating",
    "+24 poder con hechizos y +15 índice de golpe crítico": "+24 Spell power and +15 crit rating",
    "+24 poder con hechizos y +8 maná cada 5 segundos": "+24 Spell power and +8 mana per 5 sec",
    "+30 aguante y +15 temple": "+30 Stamina and +15 Resilience",
    "+23 celeridad": "+23 Haste rating",
    "+225 armadura": "+225 Armor",
    "+10 espíritu": "+10 Spirit",
    "+35 penetración de hechizos": "+35 Spell penetration",
    "+275 salud": "+275 Health",
    "+50 poder de ataque": "+50 Attack power",
    "+40 aguante": "+40 Stamina",
    "+30 poder con hechizos": "+30 Spell power",
    "+44 poder de ataque": "+44 Attack power",
    "+28 poder con hechizos": "+28 Spell power",
    "+885 armadura": "+885 Armor",
    "+340 celeridad durante 12 s, cada minuto": "+340 Haste for 12 s, once per minute",
    "+1 ranura de gema": "+1 gem socket",
    "+75 poder de ataque y +22 crítico": "+75 Attack power and +22 crit rating",
    "+55 poder de ataque y +15 crítico": "+55 Attack power and +15 crit rating",
    "+55 aguante y +22 agilidad": "+55 Stamina and +22 Agility",
    "+50 poder con hechizos y +30 aguante": "+50 Spell power and +30 Stamina",
    "+32 poder de ataque": "+32 Attack power",
    "+12 índice de golpe y +12 índice de golpe crítico": "+12 Hit rating and +12 crit rating",
    "+15 aguante y velocidad menor": "+15 Stamina and minor run speed",
    "+7 maná y +7 salud cada 5 segundos": "Restores 7 mana and 7 health every 5 sec",
    "+24 índice de golpe crítico y ráfaga de velocidad": "+24 crit rating and a speed burst",
    "+110 poder de ataque": "+110 Attack power",
    "+63 poder con hechizos": "+63 Spell power",
    "+120 agilidad ocasional y celeridad de ataque": "Chance for +120 Agility and attack speed",
    "+40 índice de golpe crítico a distancia": "+40 ranged crit rating",
    "+40 poder de ataque": "+40 Attack power",
    "Probabilidad de sanar un 3% y aumentar la fuerza total un 15% durante 15 s":
        "Chance to heal 3% and raise total Strength by 15% for 15 sec",
    "+25 defensa y +2% de aguante total": "+25 Defense and +2% total Stamina",
    "+110 poder de ataque (arma a dos manos)": "+110 Attack power (two-handed weapon)",
    "+23 índice de celeridad": "+23 Haste rating",
    "+44 poder de ataque (Ingeniería: aceleradores)":
        "+44 Attack power (Engineering: accelerators)",
    "+75 poder de ataque y +22 índice de golpe crítico":
        "+75 Attack power and +22 crit rating",
    "Sanación y poder de ataque ocasional": "Chance to heal and gain attack power",
    # notas de engarce
    "Activa meta": "Activates meta",
    "Hebilla": "Belt buckle",
    "Activa el requisito azul y amarillo de la gema meta":
        "Meets the meta gem's blue and yellow requirement",
    "Añade una ranura de gema adicional": "Adds an extra gem socket",
    "Ranura extra de la hebilla": "Extra socket from the belt buckle",
    # efectos de las mejoras de profesión
    "Probabilidad de +295 poder con hechizos durante 15 s":
        "Chance for +295 Spell power for 15 sec",
    "Probabilidad de +400 poder de ataque durante 15 s":
        "Chance for +400 Attack power for 15 sec",
    "Probabilidad de restaurar 400 p. de maná": "Chance to restore 400 mana",
    "Probabilidad de +400 poder de ataque a costa de armadura":
        "Chance for +400 Attack power at the cost of armor",
    "Probabilidad de acumular Reserva de sangre al golpear":
        "Chance to build Blood Reserve on hit",
    "Permite lanzar una bomba de fragmentación cada 6 min":
        "Lets you throw a frag bomb every 6 min",
    "Aturde a las unidades mecánicas cercanas": "Stuns nearby mechanical units",
    "+23 agilidad y caída lenta": "+23 Agility and slow fall",
    "+45 aguante y control mental cada 10 min": "+45 Stamina and mind control every 10 min",
    "+25 intelecto": "+25 Intellect",
    "+76 poder con hechizos": "+76 Spell power",
    "+102 aguante": "+102 Stamina",
    "+15 espíritu": "+15 Spirit",
    "+18 aguante": "+18 Stamina",
    "+50 poder con hechizos y +20 espíritu": "+50 Spell power and +20 Spirit",
    "+40 índice de golpe crítico a distancia": "+40 ranged crit rating",
}

ORIGENES = {
    "Encantamiento": "Enchanting",
    "Herrería": "Blacksmithing",
    "Peletería": "Leatherworking",
    "Sastrería": "Tailoring",
    "Ingeniería": "Engineering",
    "Encantamiento / Ingeniería": "Enchanting / Engineering",
    "Forja de runas, Acherus": "Runeforging, Acherus",
    "Caballeros de la Espada de Ébano": "Knights of the Ebon Blade",
    "Hijos de Hodir, Exaltado": "Sons of Hodir, Exalted",
    "Hijos de Hodir, Reverenciado": "Sons of Hodir, Revered",
    "Cruzada Argenta, Reputado": "Argent Crusade, Honored",
    "Kirin Tor, Reverenciado": "Kirin Tor, Revered",
    "Acuerdo del Reposo del Dragón, Reverenciado": "Wyrmrest Accord, Revered",
    "Vendedores JcJ": "PvP vendors",
}


def en(tabla, valor):
    """Traducción al inglés con reserva al propio valor español."""
    return tabla.get(valor, valor)
