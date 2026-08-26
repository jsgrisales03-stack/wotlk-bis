# -*- coding: utf-8 -*-
"""Carga de los ficheros de datos del sitio."""
import glob
import json
import os

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(AQUI, "datos")
ASSETS = os.path.join(AQUI, "assets")

# Ficheros de datos y soporte que no describen una build.
NO_BUILD = ("iconos", "stats-", "displayids", "origenes", "_")


def _leer(nombre, por_defecto):
    ruta = os.path.join(DATOS, nombre)
    if not os.path.exists(ruta):
        return por_defecto
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def iconos():
    return _leer("iconos.json", {})




def origenes():
    """De dónde sale cada objeto, por id."""
    return _leer("origenes.json", {})


def ids():
    """Identificadores de todas las builds, en orden."""
    salida = []
    for ruta in sorted(glob.glob(os.path.join(DATOS, "*.json"))):
        nombre = os.path.basename(ruta)
        if not nombre.startswith(NO_BUILD):
            salida.append(nombre[:-5])
    return salida


def build(build_id):
    with open(os.path.join(DATOS, build_id + ".json"), encoding="utf-8") as f:
        return json.load(f)


def builds():
    """Todas las builds ya cargadas, en orden."""
    return [build(b) for b in ids()]
