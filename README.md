# investing-meetings

Repositorio personal de vídeos, webinars, transcripciones y análisis de inversión e IA.

> **Agentes:** el enrutado por pregunta está en `AGENTS.md`. Este archivo es la referencia de
> estructura, convenciones y comandos.

## Estructura

```
finance/                        inversión y finanzas
  la-pizarra-de-andres/         vídeos del canal La Pizarra de Andrés
  myinvestor-webinars/          webinars y entrevistas de MyInvestor
    catalogo.md                 catálogo generado de los 141 webinars y su estado
  el-arte-de-invertir/          canal El Arte de Invertir
  portfolio/                    cartera personal: estado, diagnóstico y propuestas
    README.md                   qué es cada fichero y cuál se puede editar
  reports/                      informes de canal, síntesis y auditorías (el `type` los distingue)
ai/                             IA
  la-pizarra-de-andres/         vídeos de IA del mismo canal
  reports/                      se crea con el primer informe de IA
reference/                      glosario de ponentes y nombres, glosario técnico
tools/                          catálogo de webinars, generador de INDEX.md
ytpipe/                         CLI que descarga la transcripción de YouTube
.agents/skills/                 skills del agente
AGENTS.md · INDEX.md            enrutado · índice generado de artefactos
```

Cada vídeo o reunión es una carpeta `YYYY-MM-DD-<slug>/` dentro de la subcarpeta de su fuente:

| Archivo | Contenido | ¿Se edita? |
| --- | --- | --- |
| `transcript.json` | Transcripción estructurada (fuente de verdad) | **Nunca** |
| `invest-<canal>-<slug>.txt` | Transcripción literal con marcas de tiempo | Solo si lo pide el usuario |
| `summary.md` | Resumen con frontmatter YAML | Sí, es el entregable |

## Convenciones

- **Nombres de carpeta:** `YYYY-MM-DD-<slug-kebab-sin-acentos>`, ≤6 palabras tras la fecha.
- **Nombres de archivo:** `YYYY-MM-DD-<slug>.md`, kebab-case, sin acentos. Los resúmenes de
  reunión se llaman siempre `summary.md`.
- **Frontmatter YAML** obligatorio en todo `.md`:

  ```yaml
  ---
  title: "…"
  date: YYYY-MM-DD
  type: meeting-summary | channel-report | synthesis | revision | portfolio-audit
      | portfolio-snapshot | portfolio-diagnosis | portfolio-proposal
      | portfolio-analysis | portfolio-review | reference
  category: ai | finance | cross
  tags: [ … ]
  status: draft | final | living
  source: "…"        # opcional, URL del vídeo o de la reunión
  related: [ … ]     # opcional, rutas del repositorio
  ---
  ```

- Un artefacto = un tema. Para relacionar, usa `related:` en lugar de duplicar contenido.
- Tras crear, mover o borrar artefactos: `python3 tools/build_index.py`.

## Skills

Las skills viven en `.agents/skills/` (`ingest-meeting`, `ingest-channel`,
`ingest-webinars`); cuándo usar cada una, en `AGENTS.md`.

## Reports: qué es cada uno

`<categoria>/reports/` es la salida analítica. Cada documento tiene un trabajo distinto y ninguno
repite al otro.

| `type` | Qué contiene | Cuándo se escribe |
| --- | --- | --- |
| `channel-report` | **Acta de una tanda**: vídeos analizados, hilos comunes, discrepancias, riesgos, menciones con cifra y postura, qué se puede comprar. Solo hechos, con cita y minuto. | Al ingerir N vídeos de un canal |
| `synthesis` | **Juicio propio sobre un periodo**: foto en una página, dónde se contradicen, qué no dar por bueno, plan de acción y señales a vigilar. | Al cerrar un periodo o cuando hay dos o más tandas |
| `revision` | **Auditoría de resúmenes**: qué decía el resumen, qué dice la transcripción, qué se corrigió. | Tras una ingesta con revisión adversarial |

En `finance/portfolio/` viven además los documentos de cartera (`portfolio-snapshot`,
`portfolio-diagnosis`, `portfolio-analysis`, `portfolio-proposal`): cruzan las fuentes con las
posiciones reales y caducan con la cartera, por eso no están en `reports/`.

**Regla:** un dato se escribe una vez. El acta recoge el hecho y la síntesis lo interpreta, pero
no lo repite. Si dos documentos dicen lo mismo, sobra uno.

## Comandos

```bash
# transcripción de un vídeo suelto (siempre con --out)
uv run --project ytpipe ytpipe fetch <url> --out finance/<fuente> --no-open

# webinars de MyInvestor
python3 tools/myinvestor_webinars.py list        # TSV: id, título, post
python3 tools/myinvestor_webinars.py pendientes  # solo los que faltan por ingerir
python3 tools/myinvestor_webinars.py catalogo    # reescribe finance/myinvestor-webinars/catalogo.md

# índice del repositorio
python3 tools/build_index.py
```

No descargar en paralelo: YouTube responde con HTTP 429.
