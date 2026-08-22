# Proyecto WoW — Wrath of the Lich King (LochRaven)

Proyecto de consulta sobre **World of Warcraft: Wrath of the Lich King**. El usuario juega
principalmente **Caballero de la Muerte**: Profano (DPS PvE) y Sangre (Tanque PvE).
Personaje base: **LochRaven**.

## Cómo responder

1. **Siempre en español.** Nombres de objetos, hechizos, gemas y encantamientos en su
   localización española, con el nombre en inglés entre paréntesis solo si ayuda a buscar
   en una base de datos.
2. **La guía manda.** `guia-wow.md` es la fuente maestra del proyecto y contiene decisiones
   ya tomadas. No las contradigas por costumbre; si crees que algo está desactualizado o es
   discutible, dilo explícitamente y explica por qué, pero no cambies la decisión sin que el
   usuario lo pida.
3. **Distingue siempre el contexto.** Profano PvE ≠ Sangre/Tanque PvE ≠ JcJ. Las gemas y
   encantamientos de PvE de la guía no valen para arena sin adaptar (temple, penetración
   de hechizos, control).
4. **Avisa cuando la respuesta dependa de la versión.** Wrath original vs **WotLK Classic**
   vs servidor privado **3.3.5a** difieren en: botín, emblemas, mazmorras de recuperación,
   tasas de experiencia, disponibilidad de objetos y costes de vendedor. Las mecánicas de
   objetos y los principios de gemado son mucho más estables que esos sistemas.
5. **No inventes cifras.** Si un valor exacto (límite de golpe, coste, nivel de objeto, ID)
   no está en la guía, dilo y búscalo en Wowhead antes de afirmarlo.
6. Si la pregunta va más allá de la guía, respóndela igual con conocimiento general de
   Wrath, dejando claro qué parte viene de la guía y qué parte no.

## Fuentes

- `guia-wow.md` — guía maestra en español (progresión, zonas, mazmorras, bandas, stats,
  gemas, encantamientos, DK Profano, DK Sangre, nombres LochR, glosario).
- `fuente/guia-wow.docx` — original en Word. Si se actualiza una recomendación, se cambia
  aquí y en el Markdown para no dejar copias contradictorias.
- **Wowhead WotLK**: https://www.wowhead.com/wotlk — referencia externa principal.
  Las páginas índice son muy JS y devuelven poco; las fichas concretas funcionan mejor:
  - Objeto: `https://www.wowhead.com/wotlk/es/item=<id>`
  - Hechizo: `https://www.wowhead.com/wotlk/es/spell=<id>`
  - Guías: `https://www.wowhead.com/wotlk/guide/...`
  Usa `es` en la ruta para obtener los nombres en español.
- **Tooltips en crudo** (lo más fiable para stats exactas, verificado):
  `https://nether.wowhead.com/wotlk/es/tooltip/item/<id>` y `.../tooltip/spell/<id>`.
  Las fichas normales de Wowhead no exponen el tooltip al descargarlas; esta ruta sí.

## Referencia rápida — LochRaven

### DK Profano (DPS PvE)

| Elemento | Elección |
|---|---|
| Meta | Diamante de asedio de tierra incansable |
| Roja | Rubí cárdeno llamativo (+20 fuerza) |
| Azul | Lágrima de pesadilla (+10 a todo, prismática) |
| Amarilla | Ametrino grabado si falta golpe; si no, fuerza pura o fuerza/celeridad según bonus |
| Cabeza | Arcanum de tormento (Espada de Ébano) |
| Hombros | Inscripción del hacha superior (Hijos de Hodir) |
| Capa | Encantar capa: velocidad superior (+23 celeridad) |
| Pecho | Encantar pechera: estadísticas potentes (+10 a todo) |
| Piernas | Armadura de pierna de escama de hielo |
| Arma | Runa del cruzado caído |

Prioridad de stats: golpe hasta el objetivo de la configuración → fuerza → celeridad →
crítico → penetración de armadura → pericia → poder de ataque.

### DK Sangre (Tanque PvE)

| Elemento | Elección |
|---|---|
| Meta | Diamante de asedio de tierra austero (+32 aguante, +2% armadura) |
| Azules | Circón majestuoso sólido (+30 aguante) |
| Cabeza | Arcanum del adepto protector (Cruzada Argenta) |
| Hombros | Inscripción del gladiador superior |
| Capa | Encantar capa: Armadura poderosa (+225 armadura) |
| Brazales | Encantar brazales: aguante sublime (+40 aguante) |
| Piernas | Armadura para pierna de pellejo de escarcha |
| Botas | Vitalidad de los colmillarr; alternativa Entereza superior |
| Arma 2M | Runa de la gárgola piel de piedra |

Objetivo defensivo clásico: **540 de defensa** para inmunidad práctica a críticos de jefes.

### Nombres de personaje

Patrón: **LochR + animal que empiece por R**. Base LochRaven. Trabajados: LochRattler,
LochRay, LochRaptor, LochRhino, LochRook. Ver sección 14 de la guía para el catálogo completo.

## Sub-proyecto: fichas de build (`web/`)

Mini web de consulta. Una ficha por personaje/especialización: cada pieza del equipo con
nombre en español, gemas y encantamientos. Nada más — sin rotaciones, sin talentos.

```
web/
├── build.py              generador: python build.py <id>
├── datos/
│   ├── iconos.json       iconos del juego en base64 (compartido)
│   └── <id>.json         datos de una build
└── <id>.html             salida autocontenida
```

Fichas existentes: `dk-profano` (LochRaven, ICC 25 heroico con Agonía de Sombras).

**Para añadir una build nueva:** crear `datos/<id>.json` con la misma forma que
`dk-profano.json` y ejecutar `python build.py <id>`. Si aparecen iconos nuevos hay que
añadirlos a `iconos.json` (descargar de `https://wow.zamimg.com/images/wow/icons/large/<icono>.jpg`
y guardar como data URI base64).

**Flujo de datos verificado — usar siempre este, no la memoria:**
1. ID del objeto: `https://www.wowhead.com/wotlk/search/suggestions-template?q=<nombre+en+inglés>`
   devuelve JSON con `id`, `icon`, `quality` y el nivel de objeto en `pinDescription`.
   Filtrar por nivel de objeto, porque las piezas de tier repiten nombre entre versiones.
2. Nombre español, ranuras y bono: `https://nether.wowhead.com/wotlk/es/tooltip/item/<id>`.
   Las ranuras salen de `socket-(red|yellow|blue|meta|prismatic)`; el bono, de
   `Bono de ranura: ...` (ojo: es "Bono", no "Bonificación").
3. Encantamientos: mismo endpoint con `/tooltip/spell/<id>` cuando no existen como objeto.

Los iconos van incrustados en base64 a propósito: la página funciona sin conexión y sin
depender de dominios externos.
