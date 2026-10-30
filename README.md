# investing-meetings

Repositorio personal de reuniones, vídeos y análisis de inversión (IA y finanzas).

## Mapa del repositorio

- `ai/` — reuniones y vídeos de inteligencia artificial. Cada subcarpeta es una reunión (`YYYY-MM-DD-<slug>/`) con `transcript.json`, `.txt` y `summary.md`.
- `finance/` — reuniones y vídeos de finanzas/inversión/economía (misma estructura).
- `research/` — artefactos analíticos standalone:
  - `research/reports/` — informes de canal, síntesis, revisiones adversariales.
  - `research/portfolio/` — auditorías de cartera.
  - `research/revisions/` — revisiones y auditorías de resúmenes.
- `reference/` — glosarios y material de referencia.
- `ytpipe/` — CLI para descargar transcripciones de YouTube.
- `.agents/skills/` — skills del agente (ingest-meeting, ingest-channel).

## Convenciones

- **Nombres de carpeta:** `YYYY-MM-DD-<slug-kebab-sin-acentos>`, ≤6 palabras tras la fecha.
- **Nombres de archivo:** `YYYY-MM-DD-<slug>.md`, kebab-case, sin acentos.
- **Frontmatter YAML** en todo `.md`: `title`, `date`, `type`, `category`, `tags`, `status` (y `related`/`source` cuando aplica). Permite filtrar sin leer el cuerpo.
- **Tipos (`type`):** `meeting-summary`, `channel-report`, `synthesis`, `revision`, `portfolio-audit`, `reference`.
- **Categorías (`category`):** `ai`, `finance`, `cross`.
- Un artefacto = un tema. Para temas relacionados, usar `related:` en el frontmatter en lugar de duplicar.

## Navegación para agentes IA

1. Lee `INDEX.md` primero: lista todos los artefactos con ruta, tipo, fecha, título y tags.
2. Filtra por `type`/`tags`/`date` en el frontmatter; abre solo los archivos relevantes.
3. Las reuniones viven en `ai/` y `finance/`; su resumen es `summary.md` dentro de la carpeta.
4. Los artefactos analíticos viven en `research/`.

## Skills

- `.agents/skills/ingest-meeting/` — ingesta de una reunión o vídeo individual.
- `.agents/skills/ingest-channel/` — ingesta de los últimos N vídeos de un canal de YouTube.

## Fuentes de verdad

- `transcript.json` es la fuente de verdad de cada reunión. No se reescribe.
- Los resúmenes (`summary.md`) se generan a partir de la transcripción y no inventan cifras.
