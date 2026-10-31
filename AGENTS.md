# AGENTS.md

Enrutado para agentes. Repositorio `investing-meetings`: transcripciones, resúmenes y análisis
de inversión (`finance/`) e IA (`ai/`).

**Orden de lectura: este archivo → `INDEX.md` → el artefacto concreto.** Si el tema es la
cartera, añade `finance/portfolio/README.md` como cuarto paso.

## 1. Enrutado

| Pregunta del usuario | Ruta | Empezar por |
| --- | --- | --- |
| Su cartera, rebalanceo, traspasos, "¿qué hago con mi dinero?" | `finance/portfolio/` | `cartera-actual.md` → `diagnostico-*.md` → `propuesta-actual.md` |
| Un fondo, ETF o acción que tiene o le han recomendado | `finance/portfolio/` | Su ficha en `cartera-actual.md`, luego los `summary.md` que lo nombran |
| Macro, tipos, inflación, renta fija, mercados | `finance/la-pizarra-de-andres/` | `summary.md` más reciente del tema |
| Gestoras, entrevistas, "qué dice MyInvestor" | `finance/myinvestor-webinars/` | `catalogo.md` → carpeta del webinar → `summary.md` |
| Visión consolidada o discrepancias entre vídeos | `finance/reports/` | `informe-canal-*` y `sintesis-inversor-*` |
| Agentes de IA, LLMs, Claude | `ai/la-pizarra-de-andres/` | `summary.md` del vídeo |
| Nombre de una persona, canal o entidad | `reference/glossary.md` | Tabla de ponentes |
| Terminología (IA o finanzas) | `reference/glossary-technical.md` | — |

Si la pregunta cruza `finance/` y `ai/` (p. ej. "¿la burbuja de la IA afecta a mi cartera?"),
responde desde `finance/` y usa `ai/` solo como contexto.

Cada vídeo o reunión es una carpeta `YYYY-MM-DD-<slug>/` con `transcript.json` (fuente de
verdad, nunca se reescribe), la transcripción `.txt` y el `summary.md` que se entrega.
Nombres de carpeta, frontmatter YAML y comandos: `README.md`.

## 2. Reglas que no se negocian

- **Ninguna cifra sin respaldo** en la transcripción. Sin dato del hablante, el criterio va sin número.
- **Ninguna atribución inventada**: sin etiquetas de hablante, marca `inferida` o `no atribuible con certeza`.
- **Una mención no es una recomendación**: `recomienda` exige cita literal; si el hablante vende el producto, `(lo comercializa)` en la misma fila.
- **Hedges y magnitudes se conservan** ("si no me equivoco", `trillion` = billón).
- Cada tip pertenece a su hablante: el agente no da consejo financiero.
- Tras crear, mover o borrar artefactos: `python3 tools/build_index.py`.

## 3. Skills

- `ingest-meeting` — llega una transcripción y falta `summary.md`. Define las secciones del resumen.
- `ingest-channel` — "los últimos N vídeos de un canal" o un informe de canal.
- `ingest-webinars` — webinars o entrevistas de MyInvestor (lista el catálogo y salta lo ya ingerido).

Las tres escriben en `<categoria>/<fuente>/YYYY-MM-DD-<slug>/` y reutilizan `ingest-meeting`.

## 4. Más detalle

| Archivo | Contiene |
| --- | --- |
| `README.md` | Mapa completo, convenciones de nombres, frontmatter, comandos |
| `INDEX.md` | Todos los artefactos, con ruta, tipo, categoría, fecha, título y tags |
| `finance/portfolio/README.md` | Qué es cada fichero de la cartera y cuál se puede editar |
| `ytpipe/README.md` | Formato de `transcript.json` y opciones del CLI |
