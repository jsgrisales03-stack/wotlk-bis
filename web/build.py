# -*- coding: utf-8 -*-
"""Genera el sitio Arsenal de Corona de Hielo.

    python build.py              todas las páginas
    python build.py dk-sangre    sólo esas fichas

El trabajo real vive en el paquete arsenal/: este fichero sólo carga los datos,
recorre las builds y escribe el resultado.
"""
import os
import sys

from arsenal import datos, motor
from arsenal.paginas import comentarios, ficha, indice

AQUI = os.path.dirname(os.path.abspath(__file__))


def escribir(nombre, contenido):
    ruta = os.path.join(AQUI, nombre)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
    return os.path.getsize(ruta) // 1024


def main(argv):
    iconos = datos.iconos()
    items_stats = motor.cargar_items()
    origenes = datos.origenes()
    talentos = datos.talentos()

    if not items_stats:
        print("Aviso: falta datos/stats-items.json; las fichas saldrán sin totales.")
    if not origenes:
        print("Aviso: falta datos/origenes.json; no se mostrará la procedencia.")
    if not talentos:
        print("Aviso: falta datos/talentos.json; las fichas saldrán sin talentos.")

    objetivos = argv[1:] or datos.ids()
    for bid in objetivos:
        pagina = ficha.construir(bid, iconos, items_stats, origenes, talentos)
        print(f"  {bid}.html  {escribir(bid + '.html', pagina)} KB")

    if not argv[1:]:
        print(f"  index.html  {escribir('index.html', indice.construir(iconos))} KB")
        print(f"  comentarios.html  "
              f"{escribir('comentarios.html', comentarios.construir())} KB")
    print(f"Listo: {len(objetivos)} fichas.")


if __name__ == "__main__":
    main(sys.argv)
