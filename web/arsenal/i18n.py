# -*- coding: utf-8 -*-
"""Conmutador de idioma: intercambia los data-es/data-en de la página."""

SCRIPT_I18N = """<script>
(function(){
  var KEY = 'wotlk-lang';
  function aplicar(l){
    document.documentElement.lang = l;
    document.querySelectorAll('.i18n').forEach(function(el){
      var v = el.getAttribute('data-' + l) || el.getAttribute('data-es') || '';
      if (v.indexOf('<') !== -1) el.innerHTML = v; else el.textContent = v;
    });
    document.querySelectorAll('[data-i18n-title]').forEach(function(el){
      var v = el.getAttribute('data-title-' + l);
      if (v) el.setAttribute('title', v);
    });
    document.querySelectorAll('.lang-switch button').forEach(function(b){
      b.setAttribute('aria-pressed', String(b.dataset.lang === l));
    });
    try { localStorage.setItem(KEY, l); } catch (e) {}
  }
  document.querySelectorAll('.lang-switch button').forEach(function(b){
    b.addEventListener('click', function(){ aplicar(b.dataset.lang); });
  });
  var guardado;
  try { guardado = localStorage.getItem(KEY); } catch (e) {}
  var actual = guardado === 'en' ? 'en' : 'es';
  aplicar(actual);
  // El diálogo copia nodos ya traducidos; al cambiar de idioma hay que
  // volver a pasar por ellos.
  window.__idioma = function(l){ actual = l || actual; aplicar(actual); return actual; };
})();
</script>"""
