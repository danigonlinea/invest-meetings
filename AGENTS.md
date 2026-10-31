# AGENTS.md

Guía de enrutado para Hermes y cualquier otro agente que trabaje en este repositorio.
El repositorio se llama `investing-meetings` y guarda transcripciones, resúmenes y análisis
de inversión y de IA.

**Regla de oro:** el repositorio tiene dos grandes carpetas, `finance/` y `ai/`. Decide la
carpeta por la **materia** de la pregunta antes de abrir nada. Leer un vídeo de IA para
contestar una pregunta de cartera es tiempo perdido.

## 1. Mapa del repositorio

```
finance/
  la-pizarra-de-andres/        vídeos de YouTube de La Pizarra de Andrés (mercados, fondos, cartera)
  myinvestor-webinars/         webinars y entrevistas de MyInvestor (Escuela MyInvestor)
    catalogo.md                catálogo generado: 141 webinars, con estado ingerido/pendiente
  el-arte-de-invertir/         canal El Arte de Invertir
  portfolio/                   LA CARTERA PERSONAL: estado, diagnóstico, propuestas
    README.md                  qué es cada fichero y cuál se puede editar
  reports/                     informes de canal, síntesis para el inversor, revisiones adversariales
  revisions/                   auditorías de resúmenes concretos
ai/
  la-pizarra-de-andres/        vídeos de IA del mismo canal (agentes, modelos, economía de la IA)
  reports/                     informes de canal de IA (se crea al primer informe)
  revisions/                   auditorías de resúmenes de IA (se crea al primer informe)
reference/                     glosario de ponentes y nombres + glosario técnico (transversal)
tools/                         scripts de apoyo (catálogo de webinars, generador de INDEX.md)
ytpipe/                        CLI que descarga la transcripción de YouTube
.agents/skills/                skills del agente
INDEX.md                       índice generado de todos los artefactos
```

Cada reunión o vídeo es una carpeta `YYYY-MM-DD-<slug>/` dentro de la subcarpeta de su
fuente, y contiene:

| Archivo | Contenido | ¿Se edita? |
| --- | --- | --- |
| `transcript.json` | Transcripción estructurada (fuente de verdad) | **Nunca** |
| `invest-<canal>-<slug>.txt` | Transcripción literal con marcas de tiempo | Solo si el usuario lo pide |
| `summary.md` | Resumen con frontmatter YAML | Sí, es el entregable |

## 2. Enrutado por tipo de pregunta

Orden de lectura: **este archivo → `INDEX.md` → el archivo concreto**. `INDEX.md` lista
ruta, tipo, categoría, fecha, título y tags de los 28+ artefactos; con eso basta para
elegir sin abrir el resto.

| Si el usuario pregunta por… | Ir a | Empezar por |
| --- | --- | --- |
| Su cartera, rebalanceo, traspasos, "¿qué hago con mi dinero?" | `finance/portfolio/` | `cartera-actual.md` → `diagnostico-2026-10-30.md` → `propuestas/01-propuesta-moderada-90k.md` |
| Un fondo, ETF o acción concreto que él tiene o le han recomendado | `finance/portfolio/` y luego `finance/la-pizarra-de-andres/` | La ficha del fondo en `cartera-actual.md` y después los `summary.md` que lo nombran |
| Macro, tipos, inflación, renta fija, mercados | `finance/la-pizarra-de-andres/` | El `summary.md` más reciente del tema; los informes de canal en `finance/reports/` |
| Gestoras, entrevistas a gestores, "qué dice MyInvestor" | `finance/myinvestor-webinars/` | `catalogo.md` → la carpeta del webinar concreto → `summary.md` |
| Visión consolidada del canal, discrepancias entre vídeos | `finance/reports/` | `informe-canal-la-pizarra-de-andres-*.md` y `sintesis-inversor-*.md` |
| Agentes de IA, LLMs, Claude, herramientas de IA | `ai/la-pizarra-de-andres/` | `summary.md` del vídeo que corresponda |
| Cómo se llama una persona, canal o entidad | `reference/glossary.md` | Tabla de ponentes |
| Terminología técnica (IA o finanzas) | `reference/glossary-technical.md` | — |

Si la pregunta cruza las dos carpetas (por ejemplo, "¿la burbuja de la IA afecta a mi
cartera?"), abre primero `finance/` (la decisión de cartera es lo que se responde) y usa
`ai/` solo como contexto.

## 3. Convenciones de nombres y frontmatter

- **Carpeta:** `YYYY-MM-DD-<slug-kebab-sin-acentos>`, 6 palabras como máximo tras la fecha.
- **Archivos de análisis:** `YYYY-MM-DD-<slug>.md`. Los resúmenes de reunión se llaman
  siempre `summary.md`.
- **Frontmatter YAML obligatorio** en todo `.md`:
  ```yaml
  ---
  title: "…"
  date: YYYY-MM-DD
  type: meeting-summary | channel-report | synthesis | revision | portfolio-audit | portfolio-snapshot | portfolio-diagnosis | portfolio-proposal | portfolio-analysis | portfolio-review | reference
  category: ai | finance | cross
  tags: [ … ]
  status: draft | final | living
  ---
  ```
- Un artefacto = un tema. Para relacionar, usa `related:` con rutas del repositorio; no
  dupliques contenido.
- Tras crear, mover o borrar artefactos: `python3 tools/build_index.py` para regenerar
  `INDEX.md`.

## 4. Skills disponibles

| Skill | Cuándo usarla |
| --- | --- |
| `.agents/skills/ingest-meeting/SKILL.md` | Hay una transcripción nueva (pegada o ya descargada) y falta `summary.md`. Define las secciones del resumen y las reglas de precisión. |
| `.agents/skills/ingest-channel/SKILL.md` | El usuario pide "los últimos N vídeos de un canal de YouTube" o un informe de canal. Usa `ytpipe` y escribe un informe en `finance/reports/` o `ai/reports/`. |
| `.agents/skills/ingest-webinars/SKILL.md` | El usuario pide webinars o entrevistas de MyInvestor (Escuela MyInvestor). Lista el catálogo, salta lo ya ingerido, descarga con `ytpipe` en `finance/myinvestor-webinars/` y resume cada uno. |

Las tres skills escriben dentro de la subcarpeta de la fuente:
`<categoria>/<fuente>/YYYY-MM-DD-<slug>/`.

## 5. Reglas de precisión (no negociables)

- **Ninguna cifra sin respaldo** en `transcript.json` o en el texto de la transcripción.
  Si el hablante no da el dato, el resumen escribe el criterio sin número.
- **Ninguna atribución inventada.** Sin etiquetas de hablante (`has_speaker_labels: false`),
  la atribución se marca `inferida` o `no atribuible con certeza`.
- **Una mención no es una recomendación.** `recomienda` exige cita literal; si el hablante
  vende el producto, se anota `(lo comercializa)` en la misma fila.
- **Hedges y magnitudes se conservan** ("si no me equivoco", "me lo invento", `trillion`
  frente a billón).
- **`transcript.json` nunca se reescribe** y el `.txt` solo cambia si el usuario lo pide.
- La skill no da consejo financiero: cada tip pertenece a su hablante.

## 6. Comandos

```bash
# transcripción de un vídeo suelto (siempre con --out)
uv run --project ytpipe ytpipe fetch <url> --out finance/<fuente> --no-open

# listado de webinars de MyInvestor (TSV: id, título, post)
python3 tools/myinvestor_webinars.py list
python3 tools/myinvestor_webinars.py pendientes      # solo los que faltan por ingerir
python3 tools/myinvestor_webinars.py catalogo        # reescribe finance/myinvestor-webinars/catalogo.md

# índice del repositorio
python3 tools/build_index.py
```

No descargar en paralelo: YouTube responde con HTTP 429.
