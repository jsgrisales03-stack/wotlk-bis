# -*- coding: utf-8 -*-
"""
Genera la ficha HTML estilo panel de personaje WoW.
Todo visible en una pantalla, gemas en hover.

    python build.py dk-profano
"""
import json, os, sys, html

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(AQUI, "datos")

CALIDAD = {4: ("epic", "#a335ee"), 5: ("legendary", "#ff8000")}
COLOR_RANURA = {
    "Roja": "#e5484d", "Amarilla": "#f5d90a", "Azul": "#4a9eff",
    "Meta": "#d9b45b", "Prismática": "#c084fc",
}

CLASE_EN = {"Caballero de la Muerte": "Death Knight", "Sacerdote": "Priest"}
ESPEC_EN = {
    "Profano": "Unholy", "Sangre": "Blood", "Escarcha": "Frost",
    "Sombras": "Shadow", "Disciplina": "Discipline", "Sagrado": "Holy",
}
RAZA_EN = {"Orco": "Orc", "Trol": "Troll", "Elfo de sangre": "Blood Elf",
           "No-muerto": "Undead", "Tauren": "Tauren"}
FACCION_EN = {"Horda": "Horde", "Alianza": "Alliance"}

def esc(t): return html.escape(str(t), quote=True)

def ic(iconos, nombre, cls, alt=""):
    return f'<img class="{cls}" src="{iconos.get(nombre,"")}" alt="{esc(alt)}">'


def tooltip_html(p, iconos, lado):
    parts = []
    enc = p.get("encantamiento")
    if enc:
        parts.append(
            f'<div class="tt-row tt-ench">'
            f'{ic(iconos, enc["icono"], "tt-ic", enc["nombre"])}'
            f'<div><b>{esc(enc["nombre"])}</b><span>{esc(enc["efecto"])}</span></div></div>'
        )
    for g in p.get("gemas", []):
        c = COLOR_RANURA.get(g["ranura"], "#888")
        nota = f' <em>{esc(g["clave"])}</em>' if g.get("clave") else ""
        marca = ' <span class="tt-skip">↯</span>' if g.get("ignora_color") else ""
        parts.append(
            f'<div class="tt-row">'
            f'<span class="tt-dot" style="background:{c}"></span>'
            f'{ic(iconos, g["icono"], "tt-ic", g["gema"])}'
            f'<div><b>{esc(g["gema"])}</b>{marca}<span>{esc(g["efecto"])}{nota}</span></div></div>'
        )
    if not parts:
        return ""
    pos = "tt-right" if lado == "izq" else "tt-left" if lado == "der" else "tt-center"
    return f'<div class="tt {pos}">{"".join(parts)}</div>'


def slot(p, iconos, lado):
    cls, col = CALIDAD.get(p["calidad"], ("epic", "#a335ee"))
    h = '<i class="hb">H</i>' if p.get("heroico") else ""
    enc = p.get("encantamiento")
    enc_line = f'<span class="s-enc">{esc(enc["nombre"])}</span>' if enc else ""
    n_gems = len(p.get("gemas", []))
    dots = ""
    if n_gems:
        dots = '<span class="s-dots">' + "".join(
            f'<span class="sd" style="background:{COLOR_RANURA.get(g["ranura"],"#888")}"></span>'
            for g in p["gemas"]
        ) + '</span>'
    tt = tooltip_html(p, iconos, lado)
    has_tt = " has-tt" if tt else ""

    en_name = esc(p.get("en", p["nombre"]))
    return f"""<div class="slot {lado}{has_tt}">
  <div class="s-icon {cls}">{ic(iconos, p["icono"], "si", p["nombre"])}<b class="lv">{p["ilvl"]}</b>{h}</div>
  <div class="s-txt">
    <span class="s-name i18n" data-es="{esc(p["nombre"])}" data-en="{en_name}" style="color:{col}">{esc(p["nombre"])}</span>
    {enc_line}{dots}
  </div>
  {tt}
</div>"""


def resumen_gemas(d):
    cuenta = {}
    for p in d["piezas"].values():
        for g in p.get("gemas", []):
            k = (g["gema"], g["icono"], g["efecto"])
            cuenta[k] = cuenta.get(k, 0) + 1
    return sorted(cuenta.items(), key=lambda kv: -kv[1])


CSS = r"""
:root{
  --bg:#0a090e;--p:#13111a;--p2:#1a1722;--ln:#2a2536;--ln2:#362f45;
  --tx:#ddd8e8;--tn:#918aa5;--db:#6a6380;--gr:#40d97e;--go:#d9b45b;
  --ep:#a335ee;--lg:#ff8000;--dk:#c41e3a;
}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--tx);
  font:13px/1.45 Barlow,"Segoe UI",system-ui,sans-serif;
  font-variant-numeric:tabular-nums;height:100vh;overflow:hidden;
  display:flex;flex-direction:column}
.page{max-width:1280px;width:100%;margin:0 auto;padding:0 12px;
  flex:1;display:flex;flex-direction:column}

/* header */
header{text-align:center;padding:18px 0 6px;flex:0 0 auto}
header h1{font:700 clamp(22px,3.5vw,34px)/1.1 Cinzel,Georgia,serif;
  color:#f0eaf8;letter-spacing:.4px}
.spec-lab{font-size:14px;letter-spacing:4px;text-transform:uppercase;
  color:var(--go);margin-top:5px;font-weight:500}

/* paperdoll */
.pd{flex:1;display:grid;
  grid-template-columns:1fr minmax(140px,220px) 1fr;
  grid-template-rows:1fr auto;
  gap:0;min-height:0;padding:8px 0 0}
.col{display:flex;flex-direction:column;gap:4px;justify-content:center;
  padding:0;min-height:0}
.col-l{align-items:flex-end}
.col-r{align-items:flex-start}

/* center */
.ctr{grid-row:1/2;grid-column:2/3;display:flex;flex-direction:column;
  align-items:center;justify-content:center;position:relative;padding:8px}
.ctr-bg{position:absolute;inset:0;border-radius:10px;
  background:radial-gradient(ellipse 80% 55% at 50% 45%,#1a1428,var(--bg))}
.ctr-bg::before{content:"";position:absolute;inset:0;
  background:radial-gradient(circle at 50% 46%,rgba(80,220,140,.06),transparent 55%)}
.ctr-bg::after{content:"";position:absolute;
  width:120px;height:120px;left:50%;top:46%;transform:translate(-50%,-50%);
  border-radius:50%;border:1px solid rgba(80,220,140,.1);
  box-shadow:0 0 50px rgba(80,220,140,.04)}
.cl-ic{width:64px;height:64px;border-radius:50%;position:relative;z-index:1;
  border:2px solid rgba(80,220,140,.22);box-shadow:0 0 24px rgba(80,220,140,.08)}
.ctr-t{position:relative;z-index:1;text-align:center;margin-top:10px}
.ctr-t .race{font-size:13px;color:var(--tn)}
.ctr-t .fac{font-size:10px;text-transform:uppercase;letter-spacing:2px;
  color:var(--dk);margin-top:2px;font-weight:600}

/* bottom row */
.bot-row{grid-column:1/4;display:flex;justify-content:center;
  gap:6px;flex-wrap:wrap;padding:6px 0 0;flex:0 0 auto}

/* slot */
.slot{display:flex;gap:8px;align-items:center;
  background:var(--p);border:1px solid var(--ln);border-radius:7px;
  padding:6px 10px;max-width:310px;width:100%;position:relative;
  transition:border-color .15s,background .15s;cursor:default}
.slot.has-tt:hover{border-color:var(--ln2);background:var(--p2)}
.slot.izq{flex-direction:row-reverse;text-align:right}
.slot.btm{max-width:220px}
.s-icon{position:relative;flex:0 0 auto}
.si{width:36px;height:36px;display:block;border-radius:5px;border:2px solid var(--ln2)}
.epic .si{border-color:var(--ep)}
.legendary .si{border-color:var(--lg)}
.lv{position:absolute;left:50%;transform:translateX(-50%);bottom:-6px;
  background:#08070b;border:1px solid var(--ln2);border-radius:3px;
  font-size:9.5px;padding:0 4px;color:var(--go);font-weight:700;
  line-height:14px;font-style:normal}
.hb{position:absolute;top:-4px;right:-4px;
  background:#3d2246;color:#e3a9ff;border-radius:2px;
  font-size:8px;padding:0 3px;font-weight:700;font-style:normal;
  border:1px solid #5a3570;line-height:13px}
.s-txt{min-width:0;flex:1}
.s-name{display:block;font-size:12.5px;font-weight:600;line-height:1.25}
.s-enc{display:block;font-size:10.5px;color:var(--gr);font-weight:500;
  margin-top:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.s-dots{display:flex;gap:3px;margin-top:3px}
.slot.izq .s-dots{justify-content:flex-end}
.sd{width:7px;height:7px;border-radius:1.5px;transform:rotate(45deg)}

/* tooltip on hover */
.tt{display:none;position:absolute;z-index:100;
  background:#1c1928;border:1px solid var(--ln2);border-radius:8px;
  padding:10px 12px;width:280px;box-shadow:0 8px 32px rgba(0,0,0,.6);
  pointer-events:none}
.slot.has-tt:hover .tt{display:block}
.tt-right{left:calc(100% + 10px);top:50%;transform:translateY(-50%)}
.tt-left{right:calc(100% + 10px);top:50%;transform:translateY(-50%)}
.tt-center{bottom:calc(100% + 8px);left:50%;transform:translateX(-50%)}
.tt-row{display:flex;gap:8px;align-items:flex-start;padding:5px 0;
  border-bottom:1px solid rgba(255,255,255,.04)}
.tt-row:last-child{border-bottom:0}
.tt-ic{width:24px;height:24px;border-radius:4px;flex:0 0 auto;
  border:1px solid var(--ln2)}
.tt-dot{width:8px;height:8px;border-radius:2px;transform:rotate(45deg);
  flex:0 0 auto;margin-top:8px}
.tt-row div{min-width:0;flex:1}
.tt-row b{display:block;font-size:12.5px;font-weight:600;color:#d5cee3;line-height:1.3}
.tt-row span{display:block;font-size:11.5px;color:var(--tn);line-height:1.35}
.tt-row em{color:var(--go);font-style:normal;font-size:11px}
.tt-ench b{color:var(--gr)}
.tt-skip{color:#d99b3c;font-size:11px}

/* footer */
footer{flex:0 0 auto;text-align:center;font-size:10.5px;color:#47425a;
  padding:8px 0 12px}

/* lang switch */
.lang-switch{position:fixed;top:14px;right:14px;z-index:200;
  display:flex;gap:2px;background:var(--p);border:1px solid var(--ln);
  border-radius:20px;padding:3px}
.lang-switch button{border:0;background:transparent;color:var(--tn);
  font:600 11px/1 Barlow,sans-serif;padding:5px 11px;border-radius:16px;
  cursor:pointer;letter-spacing:.5px}
.lang-switch button.active{background:var(--ln2);color:#f0eaf8}

/* responsive */
@media(max-width:860px){
  body{overflow:auto;height:auto}
  .pd{grid-template-columns:1fr;grid-template-rows:auto;gap:6px}
  .col{align-items:stretch!important;gap:4px}
  .col-l{order:1}.ctr{order:0;min-height:120px;grid-column:auto;grid-row:auto}
  .col-r{order:2}.bot-row{order:3;grid-column:auto}
  .slot,.slot.izq{flex-direction:row;text-align:left;max-width:100%}
  .slot.izq .s-dots{justify-content:flex-start}
  .slot.btm{max-width:100%}
  .tt-left,.tt-right{left:0;right:auto;top:calc(100% + 6px);transform:none}
}
"""

IZQUIERDA = ["head", "neck", "shoulder", "back", "chest", "wrist"]
DERECHA = ["hands", "waist", "legs", "feet", "ring1", "ring2"]


def construir(build_id):
    d = json.load(open(os.path.join(DATOS, build_id + ".json"), encoding="utf-8"))
    iconos = json.load(open(os.path.join(DATOS, "iconos.json"), encoding="utf-8"))

    abajo = d["orden"][12:]
    col_l = "".join(slot(d["piezas"][s], iconos, "izq") for s in IZQUIERDA)
    col_r = "".join(slot(d["piezas"][s], iconos, "der") for s in DERECHA)
    bot = "".join(slot(d["piezas"][s], iconos, "btm") for s in abajo)
    clase_icono = d.get("clase_icono", "spell_deathknight_classicon")
    cl_icon = ic(iconos, clase_icono, "cl-ic", d["clase"])
    raza_es = d.get("raza", "Orco")
    faccion_es = d.get("faccion", "Horda")

    clase_es, espec_es = d["clase"], d["especializacion"]
    clase_en = CLASE_EN.get(clase_es, clase_es)
    espec_en = ESPEC_EN.get(espec_es, espec_es)
    footer_es = "Iconos: World of Warcraft © Blizzard Entertainment. Datos verificados contra Wowhead WotLK Classic."
    footer_en = "Icons: World of Warcraft © Blizzard Entertainment. Data verified against Wowhead WotLK Classic."

    return f"""<meta charset="utf-8">
<title>{esc(clase_es)} · {esc(espec_es)}</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Barlow:wght@400;500;600&display=swap">
<style>{CSS}</style>
<div class="lang-switch">
  <button data-lang="es">ES</button>
  <button data-lang="en">EN</button>
</div>
<div class="page">

<header>
  <h1 class="i18n" data-es="{esc(clase_es)}" data-en="{esc(clase_en)}">{esc(clase_es)}</h1>
  <div class="spec-lab i18n" data-es="{esc(espec_es)}" data-en="{esc(espec_en)}">{esc(espec_es)}</div>
</header>

<div class="pd">
  <div class="col col-l">{col_l}</div>
  <div class="ctr">
    <div class="ctr-bg"></div>
    {cl_icon}
    <div class="ctr-t">
      <div class="race i18n" data-es="{esc(raza_es)}" data-en="{esc(RAZA_EN.get(raza_es, raza_es))}">{esc(raza_es)}</div>
      <div class="fac i18n" data-es="{esc(faccion_es)}" data-en="{esc(FACCION_EN.get(faccion_es, faccion_es))}">{esc(faccion_es)}</div>
    </div>
  </div>
  <div class="col col-r">{col_r}</div>
  <div class="bot-row">{bot}</div>
</div>

<footer class="i18n" data-es="{esc(footer_es)}" data-en="{esc(footer_en)}">{esc(footer_es)}</footer>

</div>
<script>
(function(){{
  var KEY='wotlk-lang';
  function apply(l){{
    document.documentElement.lang = l;
    document.querySelectorAll('.i18n').forEach(function(el){{
      el.textContent = l==='en' ? (el.getAttribute('data-en')||el.getAttribute('data-es')) : el.getAttribute('data-es');
    }});
    document.querySelectorAll('.lang-switch button').forEach(function(b){{
      b.classList.toggle('active', b.dataset.lang===l);
    }});
    localStorage.setItem(KEY, l);
  }}
  document.querySelectorAll('.lang-switch button').forEach(function(b){{
    b.addEventListener('click', function(){{ apply(b.dataset.lang); }});
  }});
  apply(localStorage.getItem(KEY) || 'es');
}})();
</script>"""


if __name__ == "__main__":
    bid = sys.argv[1] if len(sys.argv) > 1 else "dk-profano"
    salida = os.path.join(AQUI, bid + ".html")
    with open(salida, "w", encoding="utf-8") as f:
        f.write(construir(bid))
    print(f"Generado: {salida} ({os.path.getsize(salida)//1024} KB)")
