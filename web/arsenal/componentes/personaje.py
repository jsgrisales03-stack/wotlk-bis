# -*- coding: utf-8 -*-
"""Figura central de la ficha: el personaje renderizado con su equipo.

Si no hay render para esa build se cae al retrato de raza con el distintivo
de clase, y en último caso al icono de clase a tamaño completo.
"""
import os

from ..html import esc
from .icono import ic

RAZA_ARCHIVO = {
    "Orco": "orc", "Trol": "troll", "Elfo de sangre": "bloodelf",
    "Tauren": "tauren", "No-muerto": "scourge",
    "Humano": "human", "Elfo de la noche": "nightelf", "Enano": "dwarf",
    "Gnomo": "gnome", "Draenei": "draenei",
}
GENEROS = {"macho": "male", "hembra": "female"}


def archivo_personaje(raza, genero="macho"):
    """Nombre del PNG con el personaje renderizado, si lo hay para esa raza."""
    r = RAZA_ARCHIVO.get(raza)
    if not r:
        return ""
    base = {"orc": "orco", "troll": "trol", "bloodelf": "elfo-de-sangre",
            "tauren": "tauren", "scourge": "no-muerto"}.get(r, r)
    sufijo = "" if genero == "macho" else "-hembra"
    return f"{base}{sufijo}.png"


def retrato(raza, genero="macho"):
    """Icono del retrato de raza, o cadena vacía si la raza no está mapeada."""
    r = RAZA_ARCHIVO.get(raza)
    if not r:
        return ""
    return f"race_{r}_{GENEROS.get(genero, 'male')}"


def render(build_id, raza, genero, clase_icono, iconos, carpeta):
    """Devuelve (marcado, hay_personaje). Prefiere el render propio de la build."""
    archivo = ""
    if os.path.exists(os.path.join(carpeta, build_id + ".png")):
        archivo = build_id + ".png"
    else:
        generico = archivo_personaje(raza, genero)
        if generico and os.path.exists(os.path.join(carpeta, generico)):
            archivo = generico

    if archivo:
        return (f'<img class="personaje" src="assets/personajes/{archivo}"'
                f' alt="{esc(raza)}" loading="lazy">'), True

    icono_raza = retrato(raza, genero)
    if icono_raza and icono_raza in iconos:
        return ('<div class="retrato">'
                + ic(iconos, icono_raza, "race-ic", raza)
                + ic(iconos, clase_icono, "cl-badge", clase_icono)
                + "</div>"), False
    return ic(iconos, clase_icono, "cl-ic", clase_icono), False


CSS = """
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
.ctr-t{position:relative;z-index:1;text-align:center}
.ctr-t .race{font-size:12.5px;color:var(--tn);display:block}
.ctr-t .fac{font-size:9.5px;text-transform:uppercase;letter-spacing:2px;
  color:var(--dk);margin-top:2px;font-weight:600;display:block}
@media(min-width:1440px){
  .personaje{height:300px}
  .ctr.con-personaje .ctr-t{margin-top:206px}
}
@media(min-width:1800px){
  .personaje{height:344px}
  .ctr.con-personaje .ctr-t{margin-top:238px}
}
@media(max-width:980px){
  .ctr{order:1;padding:4px 0 10px}
}
/* Portátiles de pantalla baja: la ficha tiene que seguir entrando de una vez. */
@media(min-width:981px) and (max-height:860px){
  .personaje{height:228px}
  .ctr.con-personaje .ctr-t{margin-top:142px}
}
"""
