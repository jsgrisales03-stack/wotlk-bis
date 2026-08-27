# -*- coding: utf-8 -*-
"""Carga de los ficheros de datos del sitio."""
import glob
import json
import os

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(AQUI, "datos")
ASSETS = os.path.join(AQUI, "assets")

# Una build es un JSON con ranuras de equipo. Antes se descartaban por el
# nombre, y cada fichero de datos nuevo rompía la generación hasta acordarse
# de añadirlo a la lista: se reconocen por el contenido.


def _leer(nombre, por_defecto):
    ruta = os.path.join(DATOS, nombre)
    if not os.path.exists(ruta):
        return por_defecto
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def iconos():
    return _leer("iconos.json", {})




def talentos():
    """Reparto por árbol y glifos, por build."""
    return _leer("talentos.json", {})


def origenes():
    """De dónde sale cada objeto, por id."""
    return _leer("origenes.json", {})


def _es_build(ruta):
    """Un JSON es una build si trae el diccionario de ranuras de equipo."""
    try:
        with open(ruta, encoding="utf-8") as f:
            d = json.load(f)
    except (ValueError, OSError):
        return False
    return isinstance(d, dict) and isinstance(d.get("piezas"), dict)


def ids():
    """Identificadores de todas las builds, en orden."""
    return [os.path.basename(r)[:-5]
            for r in sorted(glob.glob(os.path.join(DATOS, "*.json")))
            if _es_build(r)]


def build(build_id):
    with open(os.path.join(DATOS, build_id + ".json"), encoding="utf-8") as f:
        return json.load(f)


def builds():
    """Todas las builds ya cargadas, en orden."""
    return [build(b) for b in ids()]
