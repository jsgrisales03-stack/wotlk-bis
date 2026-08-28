# -*- coding: utf-8 -*-
"""Comentarios: un formulario que obliga a concretar de qué se habla.

Un comentario suelto («esto está mal») no sirve para arreglar nada. Los
desplegables encadenados —clase, especialización, sobre qué, y cuál— hacen que
cada mensaje llegue ya clasificado, y de paso le ahorran a quien escribe tener
que explicar el contexto.

Las listas de objetos y talentos de cada especialización viajan con la página
y el guion las filtra en el navegador: es un sitio estático, no hay a quién
preguntar.
"""
import json

from .. import datos, textos
from ..componentes.arbol import ARBOLES
from ..html import bi, esc
from ..plantilla import documento

# Dónde aterrizan los comentarios. Mientras ACCION esté vacía el formulario
# avisa de que no está conectado en vez de fingir que ha enviado.
#
# Hay dos destinos posibles y el guion se adapta solo:
#
#   Script de la hoja (recomendado)  ACCION es la URL terminada en /exec que
#     devuelve Apps Script al implementar `herramientas/comentarios-hoja.gs`.
#     CAMPOS se deja vacío: los campos viajan con su propio nombre.
#
#   Formulario de Google  ACCION es la URL del formulario terminada en
#     /formResponse, y CAMPOS asocia cada campo nuestro con el identificador
#     `entry.N` que Google le asigna.
#   Netlify (el que usamos)  El propio alojamiento recoge los envíos: no hace
#     falta servicio externo ni claves. Como el formulario se manda al mismo
#     dominio, además se puede leer la respuesta y saber de verdad si se ha
#     guardado, cosa que con un destino externo no se puede.
NETLIFY = True
FORMULARIO = "comentarios"

ACCION = ""
CAMPOS = {}
# Sólo si el script de la hoja tiene puesta una clave.
CLAVE = ""

TEMAS = [
    ("objeto", "Un objeto del equipo", "A gear item"),
    ("talento", "Un talento", "A talent"),
    ("glifo", "Los glifos", "The glyphs"),
    ("build", "La build en general", "The build overall"),
    ("sitio", "El sitio web", "The website"),
]


def _catalogo(talentos_datos, arboles):
    """Objetos y talentos de cada build, en los dos idiomas."""
    salida = {}
    for bid in datos.ids():
        d = datos.build(bid)
        objetos = []
        for clave in d["orden"]:
            p = d["piezas"].get(clave)
            if p:
                objetos.append([p["nombre"], p.get("en", p["nombre"])])

        talentos = []
        tal = (talentos_datos or {}).get(bid) or {}
        clase_en = None
        for esp, en in ARBOLES.get(d["clase"], []):
            clase_en = clase_en or en
        rejilla = arboles.get(_slug(d["clase"])) or {}
        indice = {}
        for a in rejilla.get("arboles", []):
            for c in a["casillas"]:
                if c:
                    indice[c["en"]] = c["es"]
        for nombre in sorted(tal.get("puntos") or {}):
            talentos.append([indice.get(nombre, nombre), nombre])

        salida[bid] = {
            "c": [d["clase"], textos.en(textos.CLASES, d["clase"])],
            "e": [d["especializacion"],
                  textos.en(textos.ESPECS, d["especializacion"])],
            "o": objetos,
            "t": talentos,
        }
    return salida


def _slug(clase):
    from ..componentes.arbol import CLASE_SLUG
    return CLASE_SLUG.get(clase, "")


CSS = """
body{background:var(--bg);color:var(--tx);
  font:14px/1.5 Barlow,"Segoe UI",system-ui,sans-serif;
  min-height:100vh;display:flex;flex-direction:column}
.page{max-width:620px;margin:0 auto;padding:46px 22px 60px;flex:1;width:100%}
.cab{text-align:center;margin-bottom:30px}
.cab h1{font:700 clamp(22px,3.5vw,30px)/1.2 Cinzel,Georgia,serif;
  color:#f0eaf8;margin-bottom:10px}
.lead{color:var(--tn);font-size:14px;line-height:1.65;max-width:50ch;
  margin:0 auto}
.lead strong{color:var(--tx)}

.form{display:flex;flex-direction:column;gap:16px}
.campo{display:flex;flex-direction:column;gap:6px}
.campo>label{font:600 10.5px/1 Barlow,sans-serif;letter-spacing:1.3px;
  text-transform:uppercase;color:var(--go)}
.campo .pista{font-size:11.5px;color:var(--db)}
select,textarea,input[type=text]{width:100%;background:var(--p2);
  color:var(--tx);border:1px solid var(--ln2);border-radius:8px;
  padding:11px 12px;font:14px/1.4 Barlow,sans-serif;-webkit-appearance:none;
  appearance:none;transition:border-color .15s ease}
select:hover,textarea:hover,input[type=text]:hover{border-color:var(--db)}
select:focus-visible,textarea:focus-visible,input[type=text]:focus-visible{
  border-color:var(--gr);outline:2px solid var(--focus);outline-offset:1px}
/* El galón del desplegable va como fondo: los nativos no se pueden teñir. */
select{background-image:linear-gradient(45deg,transparent 50%,var(--db) 50%),
  linear-gradient(135deg,var(--db) 50%,transparent 50%);
  background-position:calc(100% - 18px) 50%,calc(100% - 13px) 50%;
  background-size:5px 5px,5px 5px;background-repeat:no-repeat;
  padding-right:34px}
select:disabled{color:var(--db);border-style:dashed;cursor:not-allowed;
  background-image:none}
textarea{min-height:118px;resize:vertical;line-height:1.55}
.cuenta{font-size:11px;color:var(--db);text-align:right}
.cuenta.pasado{color:var(--dk)}

.enviar{margin-top:4px;padding:13px 20px;border:1px solid var(--go);
  border-radius:8px;background:linear-gradient(180deg,#3a2f14,#241d0d);
  color:var(--go);font:600 13px/1 Barlow,sans-serif;letter-spacing:.6px;
  cursor:pointer;transition:background .15s ease,transform .1s ease}
.enviar:hover{background:linear-gradient(180deg,#4a3c1a,#2e2511)}
.enviar:active{transform:translateY(1px)}
.enviar:disabled{opacity:.5;cursor:not-allowed;transform:none}

.aviso{border:1px solid var(--ln);border-radius:8px;background:var(--p);
  padding:13px 15px;font-size:12.5px;line-height:1.55;color:var(--tn)}
.aviso b{color:var(--go)}
.resultado{display:none;border-radius:8px;padding:13px 15px;font-size:13px}
.resultado.ok{display:block;border:1px solid var(--gr);background:#14231a;
  color:#bff0d0}
.resultado.mal{display:block;border:1px solid var(--dk);background:#2a1418;
  color:#f0c0c8}

@media(max-width:600px){
  .page{padding:34px 16px 46px}
  select,textarea,input[type=text]{font-size:16px}  /* iOS no hace zoom */
}
"""

SCRIPT = """<script>
(function(){
  var D = window.__catalogo || {};
  var f = document.getElementById('coment');
  if (!f) return;
  var elClase = f.clase, elEspec = f.espec, elTema = f.tema, elCual = f.cual;
  var campoCual = document.getElementById('campo-cual');

  function idioma(){ return document.documentElement.lang === 'en' ? 1 : 0; }
  function txt(par){ return par[idioma()] || par[0]; }

  function vacia(sel, etiqueta){
    sel.innerHTML = '';
    var o = document.createElement('option');
    o.value = ''; o.textContent = etiqueta;
    sel.appendChild(o);
  }
  function llena(sel, opciones){
    opciones.forEach(function(par){
      var o = document.createElement('option');
      o.value = par.valor; o.textContent = par.texto;
      sel.appendChild(o);
    });
  }

  function clases(){
    var vistas = {}, salida = [];
    Object.keys(D).forEach(function(b){
      var c = D[b].c;
      if (!vistas[c[1]]) { vistas[c[1]] = 1; salida.push({valor: c[1], texto: txt(c)}); }
    });
    return salida.sort(function(a, b){ return a.texto.localeCompare(b.texto); });
  }

  function pintaClases(){
    var previo = elClase.value;
    vacia(elClase, idioma() ? 'Choose a class…' : 'Elige una clase…');
    llena(elClase, clases());
    elClase.value = previo;
  }
  function pintaEspecs(){
    var previo = elEspec.value;
    vacia(elEspec, idioma() ? 'Choose a spec…' : 'Elige una especialización…');
    var lista = [];
    Object.keys(D).forEach(function(b){
      if (D[b].c[1] === elClase.value) lista.push({valor: b, texto: txt(D[b].e)});
    });
    lista.sort(function(a, b){ return a.texto.localeCompare(b.texto); });
    llena(elEspec, lista);
    elEspec.disabled = !elClase.value;
    elEspec.value = previo;
    pintaCual();
  }
  function pintaCual(){
    var b = D[elEspec.value], t = elTema.value;
    var lista = [];
    if (b && t === 'objeto') lista = b.o;
    else if (b && t === 'talento') lista = b.t;
    campoCual.hidden = !lista.length;
    if (!lista.length) { elCual.value = ''; return; }
    var previo = elCual.value;
    vacia(elCual, idioma() ? 'Choose one…' : 'Elige cuál…');
    llena(elCual, lista.map(function(par){
      return {valor: par[1], texto: txt(par)};
    }));
    elCual.value = previo;
  }

  elClase.addEventListener('change', pintaEspecs);
  elEspec.addEventListener('change', pintaCual);
  elTema.addEventListener('change', pintaCual);

  // El conmutador de idioma cambia el atributo lang del documento; al verlo
  // se repintan las opciones, que las genera el guion y no el traductor.
  new MutationObserver(function(){
    pintaClases(); pintaEspecs();
  }).observe(document.documentElement, {attributes: true, attributeFilter: ['lang']});

  var texto = f.mensaje, cuenta = document.getElementById('cuenta'), TOPE = 1200;
  function midetexto(){
    var n = texto.value.length;
    cuenta.textContent = n + ' / ' + TOPE;
    cuenta.classList.toggle('pasado', n > TOPE);
    f.querySelector('.enviar').disabled = n > TOPE;
  }
  texto.addEventListener('input', midetexto);

  pintaClases(); pintaEspecs(); midetexto();

  f.addEventListener('submit', function(e){
    e.preventDefault();
    var caja = document.getElementById('resultado');
    var esNetlify = f.dataset.modo === 'netlify';
    if (!esNetlify && !f.dataset.accion) {
      caja.className = 'resultado mal';
      caja.textContent = idioma()
        ? 'The form is not connected yet — nothing was sent.'
        : 'El formulario aún no está conectado; no se ha enviado nada.';
      return;
    }
    var boton = f.querySelector('.enviar');
    boton.disabled = true;

    function bien(){
      caja.className = 'resultado ok';
      caja.textContent = idioma() ? 'Thanks! Your comment was sent.'
                                  : '¡Gracias! Tu comentario se ha enviado.';
      f.reset(); pintaEspecs(); midetexto();
    }
    function mal(){
      caja.className = 'resultado mal';
      caja.textContent = idioma() ? 'It could not be sent. Try again later.'
                                  : 'No se ha podido enviar. Inténtalo más tarde.';
      boton.disabled = false;
    }

    if (esNetlify) {
      // Va al propio dominio, así que la respuesta sí se puede leer: aquí se
      // sabe de verdad si el comentario quedó guardado.
      var cuerpo = new URLSearchParams(new FormData(f)).toString();
      fetch(location.pathname, {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: cuerpo
      }).then(function(r){ r.ok ? bien() : mal(); }).catch(mal);
      return;
    }

    // Destino externo: el script de la hoja acepta nuestros propios nombres,
    // un formulario de Google exige los suyos.
    var mapa = JSON.parse(f.dataset.campos || '{}');
    var datos = new FormData();
    ['clase', 'espec', 'tema', 'cual', 'mensaje', 'firma'].forEach(function(k){
      if (f[k]) datos.append(mapa[k] || k, f[k].value || '');
    });
    if (f.dataset.clave) datos.append('clave', f.dataset.clave);
    // Fuera de nuestro dominio la respuesta es opaca: se puede enviar, no leer.
    fetch(f.dataset.accion, {method: 'POST', mode: 'no-cors', body: datos})
      .then(bien).catch(mal);
  });
})();
</script>"""


def construir(talentos_datos=None, arboles=None):
    cat = _catalogo(talentos_datos or datos.talentos(), arboles or datos.arboles())

    # Netlify localiza el formulario al desplegar leyendo estos atributos, y
    # descarta los envíos que rellenen el campo señuelo: los robots lo
    # rellenan porque no ven que está oculto, las personas no.
    if NETLIFY:
        # `data-modo` es marca nuestra: Netlify borra sus propios atributos al
        # desplegar —ya han cumplido— y el guion se quedaba sin saber que el
        # formulario estaba conectado.
        atributos = (f'name="{esc(FORMULARIO)}" method="POST" data-modo="netlify"'
                     ' data-netlify="true" netlify-honeypot="bot-field"')
        ocultos = (f'<input type="hidden" name="form-name" value="{esc(FORMULARIO)}">'
                   '<p hidden><label>No rellenar'
                   ' <input name="bot-field" tabindex="-1" autocomplete="off">'
                   '</label></p>')
    else:
        atributos = ocultos = ""

    lead_es = ("Cuéntanos qué mejorarías. Los desplegables sirven para que el "
               "comentario llegue <strong>ya situado</strong>: qué clase, qué "
               "especialización y sobre qué pieza o talento hablas.")
    lead_en = ("Tell us what you would improve. The dropdowns make each comment "
               "arrive <strong>already pinned down</strong>: which class, which "
               "specialization, and which item or talent you mean.")

    # La clase i18n es la que el conmutador busca; sin ella estas opciones se
    # quedaban en español al pasar a inglés.
    temas = "".join(
        f'<option class="i18n" value="{c}" data-es="{esc(es)}" '
        f'data-en="{esc(en)}">{esc(es)}</option>'
        for c, es, en in TEMAS)

    cuerpo = f"""<div class="page">
  <div class="cab">
    {bi("Comentarios", "Comments", "h1")}
    <p class="lead i18n" data-es="{esc(lead_es)}" data-en="{esc(lead_en)}">{lead_es}</p>
  </div>

  <form class="form" id="coment" {atributos}
        data-accion="{esc(ACCION)}"
        data-campos="{esc(json.dumps(CAMPOS, separators=(",", ":")))}"
        data-clave="{esc(CLAVE)}" novalidate>{ocultos}
    <div class="campo">
      <label for="clase">{bi("Clase", "Class", "span")}</label>
      <select id="clase" name="clase" required></select>
    </div>

    <div class="campo">
      <label for="espec">{bi("Especialización", "Specialization", "span")}</label>
      <select id="espec" name="espec" required disabled></select>
    </div>

    <div class="campo">
      <label for="tema">{bi("¿Sobre qué?", "What about?", "span")}</label>
      <select id="tema" name="tema" required>{temas}</select>
    </div>

    <div class="campo" id="campo-cual" hidden>
      <label for="cual">{bi("¿Cuál?", "Which one?", "span")}</label>
      <select id="cual" name="cual"></select>
    </div>

    <div class="campo">
      <label for="mensaje">{bi("Tu comentario", "Your comment", "span")}</label>
      <textarea id="mensaje" name="mensaje" required
        data-i18n-ph
        data-ph-es="Qué cambiarías y por qué. Si es un dato incorrecto, cuéntanos cuál es el bueno."
        data-ph-en="What you would change and why. If a value is wrong, tell us the right one."></textarea>
      <p class="cuenta" id="cuenta">0 / 1200</p>
    </div>

    <div class="campo">
      <label for="firma">{bi("Tu nombre o nick", "Your name or nick", "span")}</label>
      <input type="text" id="firma" name="firma" maxlength="40">
      <p class="pista i18n" data-es="Opcional. Sirve para responderte dentro del juego."
         data-en="Optional. Only so we can reply to you in game."></p>
    </div>

    <button type="submit" class="enviar">{bi("Enviar comentario", "Send comment", "span")}</button>
    <p class="resultado" id="resultado" role="status" aria-live="polite"></p>
  </form>

  <p class="aviso i18n" style="margin-top:22px"
     data-es="No pedimos correo ni contraseña, y no se guarda nada en tu navegador. Lo único que viaja es lo que escribas aquí."
     data-en="We ask for no email and no password, and nothing is stored in your browser. The only thing sent is what you type here."></p>
</div>
<script>window.__catalogo = {json.dumps(cat, ensure_ascii=False, separators=(",", ":"))};</script>"""

    titulo = f"{textos.MARCA_ES} — Comentarios"
    # El guion va al final del documento: necesita el catálogo ya declarado y
    # los campos del formulario ya presentes.
    return documento(titulo, CSS, cuerpo, "comentarios", {}, guion_extra=SCRIPT)
