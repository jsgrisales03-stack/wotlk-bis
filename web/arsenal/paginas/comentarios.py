# -*- coding: utf-8 -*-
"""Comentarios: de momento sólo anuncia lo que vendrá."""
from .. import textos
from ..html import bi, esc
from ..plantilla import documento


CSS = """
body{background:var(--bg);color:var(--tx);
  font:14px/1.5 Barlow,"Segoe UI",system-ui,sans-serif;
  min-height:100vh;display:flex;flex-direction:column}
.page{max-width:680px;margin:0 auto;padding:70px 24px;flex:1;width:100%;
  display:flex;flex-direction:column;align-items:center;text-align:center}
.icon-badge{width:54px;height:54px;border-radius:50%;background:var(--p);
  border:1px solid var(--ln2);display:flex;align-items:center;
  justify-content:center;font-size:23px;margin-bottom:20px}
.page h1{font:700 clamp(22px,3.5vw,30px)/1.2 Cinzel,Georgia,serif;
  color:#f0eaf8;margin-bottom:12px}
.lead{color:var(--tn);font-size:14.5px;line-height:1.7;max-width:52ch}
.lead strong{color:var(--tx)}
.status-pill{display:inline-flex;align-items:center;gap:6px;margin-top:24px;
  font-size:11px;letter-spacing:.5px;text-transform:uppercase;color:var(--go);
  background:var(--p);border:1px solid var(--ln);border-radius:14px;padding:6px 14px}
.status-pill .dot{width:6px;height:6px;border-radius:50%;background:var(--go)}
.channels{display:flex;flex-direction:column;gap:10px;margin-top:32px;
  width:100%;max-width:420px}
.channel{display:flex;align-items:center;justify-content:space-between;gap:10px;
  background:var(--p);border:1px solid var(--ln);border-radius:8px;
  padding:12px 16px;text-decoration:none;color:var(--tx);
  transition:border-color .15s,background .15s}
.channel:hover,.channel:focus-visible{border-color:var(--gr);background:#1c2620}
.channel-label{font-size:13px;font-weight:600}
.channel-hint{font-size:11px;color:var(--tn)}
.previsto{list-style:none;margin:30px auto 0;max-width:430px;width:100%;
  display:flex;flex-direction:column;gap:9px;text-align:left}
.previsto li{display:flex;align-items:flex-start;gap:10px;
  background:var(--p);border:1px solid var(--ln);border-radius:8px;
  padding:12px 15px;font-size:13px;color:var(--tx);line-height:1.45}
.pv-ic{color:var(--go);font-size:9px;line-height:1.9;flex:0 0 auto}
@media(max-width:600px){
  .page{padding:44px 18px}
  .channels{max-width:100%}
  .lead{font-size:13.5px}
}
"""


def construir():
    lead_es = ("Todavía no hay un sistema de comentarios conectado. Cuando lo activemos "
               "podrás <strong>dejar tu opinión, avisar de un dato incorrecto o pedir una "
               "build nueva</strong> desde cada especialización.")
    lead_en = ("No comment system is connected yet. Once it is live you'll be able to "
               "<strong>leave feedback, flag incorrect data or request a new build</strong> "
               "from any specialization page.")
    cuerpo = f"""<div class="page">
  <div class="icon-badge" aria-hidden="true">💬</div>
  {bi("Comentarios", "Comments", "h1")}
  <p class="lead i18n" data-es="{esc(lead_es)}" data-en="{esc(lead_en)}">{lead_es}</p>
  <p class="status-pill"><span class="dot" aria-hidden="true"></span>
    {bi("Próximamente", "Coming soon")}</p>
  <ul class="previsto">
    <li><span class="pv-ic" aria-hidden="true">◆</span>
      {bi("Señalar un dato incorrecto en cualquier ficha",
          "Flag incorrect data on any page")}</li>
    <li><span class="pv-ic" aria-hidden="true">◆</span>
      {bi("Proponer una alternativa de gema o encantamiento",
          "Suggest an alternative gem or enchant")}</li>
    <li><span class="pv-ic" aria-hidden="true">◆</span>
      {bi("Pedir una especialización o una variante de banda",
          "Request a specialization or raid variant")}</li>
  </ul>
</div>"""
    return documento(f"Comentarios · {textos.MARCA_ES}", CSS, cuerpo, "comentarios")
