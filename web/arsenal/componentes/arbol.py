# -*- coding: utf-8 -*-
"""La rejilla de talentos de una build, dibujada como en el juego.

Los tres árboles se ven siempre a la vez, uno al lado del otro, porque lo que
se quiere de un vistazo es dónde cayeron los puntos; esconder dos tercios tras
un carrusel obligaría a buscar lo que debería saltar a la cara. Al estrechar,
la casilla encoge en vez de apilarse: a veinte píxeles el icono ya no se
identifica, pero la mancha de casillas encendidas sigue contando la build, y
el nombre exacto lo da la banda de lectura al tocar.

Cada árbol es una rejilla de once filas por cuatro columnas. Las casillas
vacías se emiten igual —siete bytes— porque son las que le dan al árbol su
silueta, y de paso el orden del documento coincide con el visual, que es lo
que recorren el tabulador y el lector de pantalla.
"""
from .. import textos
from ..html import esc

# Nombre de los tres árboles por clase, en el orden en que los numera el juego.
ARBOLES = {
    "Caballero de la Muerte": [("Sangre", "Blood"), ("Escarcha", "Frost"),
                               ("Profano", "Unholy")],
    "Guerrero": [("Armas", "Arms"), ("Furia", "Fury"), ("Protección", "Protection")],
    "Paladín": [("Sagrado", "Holy"), ("Protección", "Protection"),
                ("Reprensión", "Retribution")],
    "Cazador": [("Bestias", "Beast Mastery"), ("Puntería", "Marksmanship"),
                ("Supervivencia", "Survival")],
    "Pícaro": [("Asesinato", "Assassination"), ("Combate", "Combat"),
               ("Sutileza", "Subtlety")],
    "Sacerdote": [("Disciplina", "Discipline"), ("Sagrado", "Holy"),
                  ("Sombras", "Shadow")],
    "Chamán": [("Elemental", "Elemental"), ("Mejora", "Enhancement"),
               ("Restauración", "Restoration")],
    "Mago": [("Arcano", "Arcane"), ("Fuego", "Fire"), ("Escarcha", "Frost")],
    "Brujo": [("Aflicción", "Affliction"), ("Demonología", "Demonology"),
              ("Destrucción", "Destruction")],
    "Druida": [("Equilibrio", "Balance"), ("Feral", "Feral Combat"),
               ("Restauración", "Restoration")],
}

# Nombre de la clase en español -> hoja de sprites y datos de la rejilla.
CLASE_SLUG = {
    "Guerrero": "warrior", "Paladín": "paladin", "Cazador": "hunter",
    "Pícaro": "rogue", "Sacerdote": "priest", "Caballero de la Muerte": "death-knight",
    "Chamán": "shaman", "Mago": "mage", "Brujo": "warlock", "Druida": "druid",
}

COLUMNAS = 4
FILAS = 11


def _casilla(t, puntos, sprite):
    """Una casilla con talento. Sin id: el diálogo copia esto con innerHTML.

    La traba de nivel no se pinta sobre el icono; la marca el carril, que es
    donde se lee sin tapar nada.
    """
    clases = ["t"]
    if puntos:
        clases.append("mx" if puntos >= t["max"] else "on")
    # El índice en la hoja de sprites se parte en columna y fila.
    col, fila = t["i"] % sprite["columnas"], t["i"] // sprite["columnas"]
    partes = [
        f'<button type="button" class="{" ".join(clases)}"',
        f' style="--x:{col};--y:{fila}">',
        f'<span class="i18n" data-es="{esc(t["es"])}" data-en="{esc(t["en"])}"></span>',
    ]
    # El galón sólo va donde hay puntos: en el panel del juego un talento sin
    # gastar no lleva número, y ponérselo a los cuarenta grises de una build
    # llena la rejilla de ruido y esconde justo lo que se busca.
    if puntos:
        partes.append(f'<b>{puntos}/{t["max"]}</b>')
    # La descripción sólo viaja para los talentos que la build usa: emitir las
    # sesenta y seis en los dos idiomas serían veinte kilobytes por página de
    # texto que casi nadie abre.
    if puntos:
        d = (t.get("d") or {}).get(str(puntos)) or {}
        if d.get("es") or d.get("en"):
            partes.append(f'<i class="d" data-es="{esc(d.get("es", ""))}"'
                          f' data-en="{esc(d.get("en", ""))}"></i>')
    partes.append("</button>")
    return "".join(partes)


def _arbol(indice, datos_arbol, nombres, puntos_por_nombre, sprite):
    """Un árbol: cabecera, carril de trabas y las cuarenta y cuatro casillas."""
    casillas = datos_arbol["casillas"]
    total = sum(puntos_por_nombre.get(t["en"], 0) for t in casillas if t)

    # Se recortan las filas finales que no tienen ni un talento: hay clases
    # cuya última fila queda vacía y dejaría un hueco muerto bajo el árbol.
    ultima = 0
    for i, t in enumerate(casillas):
        if t:
            ultima = i // COLUMNAS + 1
    filas = max(ultima, 1)

    rejilla = []
    for i, t in enumerate(casillas[:filas * COLUMNAS]):
        if not t:
            rejilla.append("<i></i>")
            continue
        rejilla.append(_casilla(t, puntos_por_nombre.get(t["en"], 0), sprite))

    carril = []
    for f in range(filas):
        falta = " no" if total < f * 5 else ""
        carril.append(f'<b class="{falta.strip()}"></b>' if falta else "<b></b>")

    es, en = nombres
    return (f'<section class="tal-arb" data-i="{indice}">'
            f'<h4><span class="i18n" data-es="{esc(es)}" data-en="{esc(en)}"></span>'
            f'<b>{total}</b></h4>'
            f'<div class="tal-cuerpo">'
            f'<div class="tal-rail">{"".join(carril)}</div>'
            f'<div class="tal-g">{"".join(rejilla)}</div>'
            f"</div></section>")


def render(clase, datos_build, arboles_clase):
    """El mapa de los tres árboles. Vacío si falta el detalle por talento."""
    puntos = (datos_build or {}).get("puntos")
    if not puntos or not arboles_clase:
        return ""
    nombres = ARBOLES.get(clase, [])
    sprite = arboles_clase["sprite"]
    slug = CLASE_SLUG.get(clase, "")
    trozos = []
    for i, a in enumerate(arboles_clase["arboles"]):
        par = nombres[i] if i < len(nombres) else (a["en"], a["en"])
        trozos.append(_arbol(i, a, par, puntos, sprite))
    return (f'<div class="tal-mapa" style="--hoja:url(assets/talentos/{slug}.jpg);'
            f'--sc:{sprite["columnas"]};--sf:{sprite["filas"]}">'
            f'{"".join(trozos)}</div>'
            '<p class="tal-banda i18n" data-es="Toca un talento para leerlo."'
            ' data-en="Tap a talent to read it."></p>')


CSS = """
/* El mapa de los tres árboles. La casilla encoge con la ventana en una sola
   expresión, sin puntos de corte: así el paso de 2560 a 320 es continuo y no
   hay ningún ancho intermedio donde el diseño se rompa. */
.tal-mapa{--g:3px;--rail:16px;--cmax:40px;
  --c:clamp(16px,calc((100vw - 120px)/13),var(--cmax));
  display:flex;justify-content:center;gap:clamp(6px,2vw,14px);
  margin-top:14px;padding-top:12px;border-top:1px solid var(--ln);
  /* Sin `overflow` a propósito. Poner `overflow-x:auto` de red arrastra el
     eje vertical a `auto`, y como el galón del último rango asoma tres
     píxeles por debajo de la rejilla, el navegador sacaba una barra vertical
     entera para dos píxeles de nada. El ancho ya lo garantiza el `clamp`. */
  padding-bottom:4px}
.tal-arb{flex:0 0 auto;min-width:0}
/* `width:0` con `min-width:100%` deja que la cabecera ocupe el ancho de la
   columna sin contarse para calcularlo: si no, un nombre largo como
   "RESTAURACIÓN" ensancha el árbol más que su propia rejilla. */
.tal-arb h4{display:flex;align-items:baseline;gap:5px;margin-bottom:7px;
  width:0;min-width:100%;overflow:hidden;
  font:600 9.5px/1 Barlow,sans-serif;letter-spacing:1.1px;text-transform:uppercase;
  color:var(--db)}
/* Si falta anchura se acorta el nombre, nunca la cifra: el nombre se
   adivina, el numero de puntos es el dato. */
.tal-arb h4 span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
  min-width:0}
.tal-arb h4 b{flex:0 0 auto;font-size:13px;color:var(--tn);
  font-variant-numeric:tabular-nums}
.tal-arb[data-i] h4 b{margin-left:auto}

.tal-cuerpo{display:flex;gap:4px}
/* El carril numera las trabas de nivel: 0, 5, 10… Sale de un contador CSS,
   así que no cuesta un solo byte de datos ni de marcado. */
.tal-rail{display:grid;grid-auto-rows:var(--c);gap:var(--g);width:var(--rail);
  counter-reset:tr -5}
.tal-rail b{counter-increment:tr 5;display:flex;align-items:center;
  justify-content:flex-end;padding-right:3px;
  font:600 8.5px/1 Barlow,sans-serif;color:var(--tn);
  border-right:2px solid var(--ln2);font-variant-numeric:tabular-nums}
.tal-rail b::after{content:counter(tr)}
.tal-rail b.no{color:var(--db);border-right-style:dashed}

.tal-g{display:grid;grid-template-columns:repeat(4,var(--c));
  grid-auto-rows:var(--c);gap:var(--g)}
.tal-g>i{display:block}

.t{position:relative;padding:0;border:1px solid var(--ln);border-radius:5px;
  background:var(--p2);cursor:pointer;-webkit-appearance:none;appearance:none;
  transition:transform .12s ease,border-color .12s ease}
/* El icono va en un pseudoelemento y no en el botón porque `filter` se hereda
   a todo el subárbol: puesto en el botón, el galón de rango saldría gris
   también y el estado "sin puntos" perdería su señal más legible. */
.t::before{content:"";position:absolute;inset:1px;border-radius:4px;
  background-image:var(--hoja);
  background-size:calc(var(--sc)*100%) calc(var(--sf)*100%);
  background-position:calc(var(--x)*100%/(var(--sc) - 1))
                      calc(var(--y)*100%/(var(--sf) - 1));
  filter:grayscale(1) brightness(.45)}
/* Los tres estados no dependen sólo del color: cambia el relleno del galón y
   el grosor del borde, y el número está siempre escrito. */
.t.on{border-color:#6d5a2e}
.t.on::before,.t.mx::before{filter:none}
.t.mx{border-color:var(--go);
  box-shadow:0 0 0 1px rgba(217,180,91,.28),0 0 10px -3px rgba(217,180,91,.5)}
.t>span{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}
.t>.d{display:none}
.t>b{position:absolute;right:-2px;bottom:-3px;z-index:2;min-width:17px;
  padding:0 2px;border-radius:3px;border:1px solid var(--ln2);
  background:var(--p2);color:var(--tn);
  font:600 8.5px/12px Barlow,sans-serif;font-variant-numeric:tabular-nums}
.t.on>b{color:var(--tx);border-color:#6d5a2e}
.t.mx>b{background:var(--go);color:#17140b;border-color:var(--go)}
.t[aria-pressed="true"]{box-shadow:0 0 0 2px var(--focus)}

/* Banda de lectura: en un móvil un globo flotante siempre acaba tapando
   justo lo que acabas de tocar. */
.tal-banda{min-height:42px;margin-top:11px;padding:9px 11px;
  border:1px solid var(--ln);border-radius:8px;background:var(--p);
  font-size:11.5px;line-height:1.45;color:var(--tn)}
.tal-banda b{color:var(--go);font-weight:600}

/* En pantallas bajas el árbol encoge en vez de empujar los glifos fuera y
   obligar a desplazar el diálogo entero. */
@media(max-height:900px){.tal-mapa{--cmax:34px}}
@media(max-height:780px){
  .tal-mapa{--cmax:25px;margin-top:9px;padding-top:8px}
  .tal-banda{min-height:34px;margin-top:8px;padding:7px 10px;font-size:11px}
}
@media(max-height:660px){
  .tal-mapa{--cmax:21px;margin-top:7px;padding-top:6px}
  .tal-banda{min-height:30px;margin-top:6px}
  .tal-arb h4{margin-bottom:4px}
}

@media(hover:hover){
  .t:hover{transform:scale(1.08);border-color:var(--go);z-index:3}
}
/* El carril de trabas es lo primero que sobra cuando falta anchura: la
   progresión se sigue leyendo en la propia forma del árbol. */
@media(max-width:620px){
  .tal-mapa{--rail:0px}
  .tal-rail{display:none}
}
/* Por debajo de esto el galón tapa más icono del que deja ver; el rango pasa
   a leerse en la banda, que es donde de todas formas se mira en táctil. */
@media(max-width:400px){
  /* A esta anchura cada pixel de hueco se lo quita al icono: se aprietan los
     huecos para que los tres arboles entren enteros sin desplazamiento. */
  .tal-mapa{--g:2px;gap:5px}
  .tal-arb h4{font-size:8px;letter-spacing:.4px}
  .t>b{display:none}
  .t.mx{box-shadow:0 0 0 1px var(--go)}
}
"""

# El diálogo copia el panel con innerHTML, así que no hay dónde enganchar
# oyentes antes de tiempo: se delega en el documento.
SCRIPT = """<script>
(function(){
  var SIN = {es:'Esta build no gasta puntos aqui.', en:'This build spends no points here.'};
  document.addEventListener('click', function(e){
    var t = e.target.closest ? e.target.closest('.t') : null;
    if (!t) return;
    var raiz = t.closest('.modal-cuerpo') || document;
    var banda = raiz.querySelector('.tal-banda');
    if (!banda) return;
    raiz.querySelectorAll('.t[aria-pressed]').forEach(function(x){
      x.removeAttribute('aria-pressed');
    });
    t.setAttribute('aria-pressed', 'true');
    var n = t.querySelector('span'), d = t.querySelector('.d'), r = t.querySelector('b');
    var rango = r ? ' <i>' + r.textContent + '</i>' : '';
    ['es', 'en'].forEach(function(l){
      // Si falta la descripcion en un idioma se cae al otro antes que al
      // texto de reserva: mas vale leerla en ingles que no leerla.
      var otro = l === 'es' ? 'en' : 'es';
      var texto = d && (d.getAttribute('data-' + l) || d.getAttribute('data-' + otro));
      banda.setAttribute('data-' + l,
        '<b>' + (n ? n.getAttribute('data-' + l) : '') + '</b>' + rango
        + (texto ? ' &mdash; ' + texto : (d ? '' : ' &mdash; ' + SIN[l])));
    });
    if (window.__idioma) window.__idioma();
  });
})();
</script>"""
