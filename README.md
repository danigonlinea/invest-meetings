# investing-meetings

Repositorio personal de vídeos, webinars, transcripciones y análisis de inversión e IA.

## Dos carpetas, dos materias

| Carpeta | Qué guarda |
| --- | --- |
| `finance/` | Inversión y finanzas: cartera personal, vídeos de La Pizarra de Andrés, webinars de MyInvestor, El Arte de Invertir, informes. |
| `ai/` | IA: agentes, modelos y economía de la IA. |

Dentro de cada categoría hay una subcarpeta por **fuente** (`la-pizarra-de-andres/`,
`myinvestor-webinars/`, `el-arte-de-invertir/`) y dentro una carpeta por reunión
`YYYY-MM-DD-<slug>/` con `transcript.json`, la transcripción `.txt` y `summary.md`.

- `finance/portfolio/` — la cartera personal: estado congelado, diagnóstico y propuestas.
- `finance/reports/`, `finance/revisions/` — informes de canal, síntesis y auditorías.
- `reference/` — glosarios (ponentes y nombres, terminología técnica).
- `tools/` — scripts de apoyo (catálogo de webinars, generador de `INDEX.md`).
- `ytpipe/` — CLI que descarga transcripciones de YouTube.

## Por dónde empieza un agente

1. **`AGENTS.md`** — enrutado: qué carpeta mirar según la pregunta, convenciones y reglas de
   precisión.
2. **`INDEX.md`** — índice generado de todos los artefactos (ruta, tipo, categoría, fecha,
   título, tags).
3. El archivo concreto (`summary.md`, informe o ficha de cartera).

## Convenciones

- **Nombres de carpeta:** `YYYY-MM-DD-<slug-kebab-sin-acentos>`, ≤6 palabras tras la fecha.
- **Nombres de archivo:** `YYYY-MM-DD-<slug>.md`, kebab-case, sin acentos. Los resúmenes de
  reunión se llaman siempre `summary.md`.
- **Frontmatter YAML** en todo `.md`: `title`, `date`, `type`, `category`, `tags`, `status`
  (y `related`/`source` cuando aplica). Permite filtrar sin leer el cuerpo.
- **Tipos (`type`):** `meeting-summary`, `channel-report`, `synthesis`, `revision`,
  `portfolio-audit`, `portfolio-snapshot`, `portfolio-diagnosis`, `portfolio-proposal`,
  `portfolio-analysis`, `portfolio-review`, `reference`.
- **Categorías (`category`):** `ai`, `finance`, `cross`.
- Un artefacto = un tema. Para temas relacionados, usar `related:` en el frontmatter en lugar
  de duplicar.
- Tras crear, mover o borrar artefactos: `python3 tools/build_index.py`.

## Skills

- `.agents/skills/ingest-meeting/` — resumen de una reunión o vídeo individual.
- `.agents/skills/ingest-channel/` — últimos N vídeos de un canal de YouTube + informe.
- `.agents/skills/ingest-webinars/` — webinars y entrevistas de MyInvestor.

## Utilidades

```bash
uv run --project ytpipe ytpipe fetch <url> --out finance/<fuente> --no-open
python3 tools/myinvestor_webinars.py list        # catálogo de webinars de MyInvestor
python3 tools/myinvestor_webinars.py pendientes  # webinars aún sin ingerir
python3 tools/build_index.py                     # regenera INDEX.md
```

## Fuentes de verdad

- `transcript.json` es la fuente de verdad de cada reunión. No se reescribe.
- Los resúmenes (`summary.md`) se generan a partir de la transcripción y no inventan cifras.
