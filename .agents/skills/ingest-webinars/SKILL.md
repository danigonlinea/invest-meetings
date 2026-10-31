---
name: ingest-webinars
description: Usar cuando el usuario pida webinars o entrevistas de MyInvestor (Escuela MyInvestor), "los webinars nuevos de MyInvestor" o pase una URL de blog.myinvestor.es/escuelamyinvestor/webinars. Lista el catálogo, salta lo ya ingerido, descarga la transcripción con ytpipe en finance/myinvestor-webinars/ y resume cada webinar con la skill ingest-meeting.
---

# Ingesta de webinars de MyInvestor

## Metadatos

Esta skill trabaja solo en este repositorio, el repositorio `investing-meetings`.

- Ruta de la skill: `.agents/skills/ingest-webinars/`.
- Ruta de las carpetas de webinar: `<project-root>/finance/myinvestor-webinars/YYYY-MM-DD-<topic-slug>/`.
- Ruta del catálogo: `<project-root>/finance/myinvestor-webinars/catalogo.md`. Lo genera el script; nunca se edita a mano.
- Ruta de los informes: `<project-root>/finance/reports/`. Ruta de las auditorías: `<project-root>/finance/revisions/`.
- Categoría: siempre `finance`. Fuente: siempre `myinvestor-webinars`.
- Al terminar, ejecuta `python3 tools/build_index.py` para regenerar `INDEX.md`.

Dependencias:

| Dependencia | Uso |
| --- | --- |
| `python3 tools/myinvestor_webinars.py` | Lista los webinars publicados, cuáles faltan y reescribe el catálogo. |
| `yt-dlp` | Da el título y la fecha de subida reales de cada vídeo de YouTube. |
| CLI `ytpipe` (`ytpipe/`, vía `uv`) | Descarga la transcripción y escribe la carpeta del webinar. |
| Skill `ingest-meeting` | Escribe el `summary.md` de cada webinar. No repitas su lista de secciones. |

La fuente es la página pública <https://blog.myinvestor.es/escuelamyinvestor/webinars/>
(paginada). El vídeo de YouTube solo vive en el HTML del listado
(`data-plyr-embed-id`) junto al enlace del post; el script ya resuelve ese emparejamiento.
El canal de YouTube es `MyInvestor España` (`UCc9nsd1tjDdw32wLcM5OOWQ`).

## Paso 1: Lee la petición

El agente necesita 3 datos.

1. Cuántos webinars ingerir. Valor por defecto: 3, empezando por los más recientes.
2. Si hay un filtro por tema o por gestora («los de renta fija», «la entrevista de Antonio Rico»).
3. La preferencia de idioma de subtítulos. Valor por defecto: la lista interna de `ytpipe` (ver `ytpipe/README.md`).

Pregunta al usuario solo cuando falte el número o el filtro sea ambiguo.

- No inventes nunca una fecha: la fecha de la carpeta es la de subida del vídeo, la da `ytpipe`.
- No inventes nunca un participante: sale de la descripción del vídeo y de la transcripción.

## Paso 2: Lista el catálogo

Ejecuta este comando y lee la salida (TSV: `video_id`, `título`, `post`).

```bash
python3 tools/myinvestor_webinars.py list
```

Para ver solo lo que falta por ingerir:

```bash
python3 tools/myinvestor_webinars.py pendientes
```

Aplica estas reglas.

- El orden de la salida es el del listado de MyInvestor: el webinar más reciente primero.
- Si el comando devuelve `no webinar found`, la página cambió de HTML. Para la ingesta y avisa al usuario; no inventes la lista.
- El catálogo muestra el estado `ingerido` o `pendiente` de cada webinar.

**Criterio de finalización:** puedes nombrar cuántos webinars hay, cuántos están ingeridos y cuáles son los N que vas a procesar.

## Paso 3: Salta los webinars ya ingeridos

Lee el campo `source.video_id` de cada `finance/myinvestor-webinars/*/transcript.json` antes de cualquier descarga.

```bash
grep -o '"video_id": "[^"]*"' finance/myinvestor-webinars/*/transcript.json
```

- Compara el identificador de cada webinar elegido con la lista de identificadores presentes.
- Salta el webinar que ya está ingerido y díselo al usuario.
- No vuelvas a descargar una carpeta existente. Si hace falta rehacerla, `ytpipe` exige `--force`, y antes hay que confirmarlo con el usuario.

## Paso 4: Descarga y transcribe

Entra en la raíz del repositorio y ejecuta este comando, un webinar cada vez.

```bash
uv run --project ytpipe ytpipe fetch "https://www.youtube.com/watch?v=<video_id>" --out finance/myinvestor-webinars --slug "<tema-real>" --no-open
```

Aplica estas reglas.

- Pasa siempre `--out finance/myinvestor-webinars`. Sin esa opción, `ytpipe` escribe la carpeta en la raíz del repositorio.
- El título del post de MyInvestor es genérico («Webinar del ciclo Aprende con las gestoras. Entrevista a …»). El `--slug` sale del **título real del vídeo**, que imprime `ytpipe` en su plan (`title :`) o que da `yt-dlp --print "%(title)s"`. Si el tema no se entiende, usa `<gestora>-<tema>` en 6 palabras como máximo, sin acentos.
- No ejecutes las descargas en paralelo: YouTube responde con HTTP 429. `ytpipe` ya reintenta tras un límite de peticiones.
- Cuando `ytpipe` falla con `no subtitle available`, el webinar no tiene pista de subtítulos. Repórtalo y sigue con el siguiente: no escribas un resumen sin transcripción.
- No edites nunca `transcript.json`.

**Criterio de finalización:** cada carpeta nueva guarda `transcript.json` y el `.txt`. Ejecuta `wc -c` en los dos y comunica los bytes.

## Paso 5: Escribe el resumen

Aplica la skill `.agents/skills/ingest-meeting/SKILL.md` a cada carpeta nueva.

- La skill `ingest-meeting` define las secciones de `summary.md`. No repitas esa lista aquí.
- En el frontmatter, `category: finance` y `source` con la URL del post de MyInvestor.

Añade 2 secciones más a cada `summary.md`, después de `## Citas textuales` y antes de las advertencias sobre la transcripción.

### `## Conclusiones para el inversor`

- De 3 a 8 viñetas.
- Cada viñeta es una conclusión que afecta a una cartera.
- Cada viñeta nombra al hablante que la sostiene.

### `## Tips para el inversor`

| Tip | Por qué | Acción |
| --- | --- | --- |
| Un consejo del hablante. | La razón que da el hablante y el minuto. | Un paso concreto y comprobable. |

Aplica estas reglas a las dos secciones.

- No escribas nunca un tip como consejo propio del agente.
- Marca cada inferencia con la palabra `inferida`.
- No inventes nunca una cifra que la transcripción no contenga.

### Interés comercial: obligatorio en esta fuente

MyInvestor comercializa los fondos de las gestoras que entrevista, y el invitado trabaja
para la gestora del fondo que presenta. Aplica las dos reglas siguientes sin excepción.

- Añade `(lo comercializa)` a cada vehículo que el invitado gestione o que MyInvestor distribuya.
- Añade una viñeta al principio de `## Conclusiones para el inversor` con el interés comercial del hablante (gestora, plataforma o ambas).

## Paso 5 bis: Audita el resumen antes de darlo por bueno

Contrasta cada `summary.md` con su transcripción. Busca, en este orden:

1. Conclusiones invertidas respecto a la frase del hablante.
2. Cifras que no aparecen en la transcripción.
3. Unidades y magnitudes (puntos básicos frente a porcentajes, `trillion` frente a billón).
4. Hedges eliminados.
5. Atribuciones sin etiquetas de hablante: `inferida` o `no atribuible con certeza`.

Corrige el `summary.md`. Si la auditoría da material propio, escribe el archivo en
`finance/revisions/`, nunca dentro de la carpeta del webinar.

## Paso 6: Actualiza el catálogo

```bash
python3 tools/myinvestor_webinars.py catalogo
```

El comando marca como `ingerido` los webinars con carpeta y rellena la ruta. Comprueba que
el contador de ingeridos subió en tantas unidades como webinars has procesado.

## Paso 7: Informe de la tanda (solo si el usuario lo pide)

Si el usuario pide comparar los webinars entre sí o sacar una conclusión consolidada,
escribe `finance/reports/informe-webinars-myinvestor-<YYYY-MM-DD>.md` con la estructura de
informe de canal de `ingest-channel` (vídeos analizados, hilos comunes, conclusiones, tips
priorizados, discrepancias, menciones con cifras y postura).

## Si delegas la ingesta a un subagente

- Pásale la carpeta del webinar ya descargada y pídele solo el `summary.md`.
- El Paso 6 (catálogo) y el Paso 8 (`INDEX.md`) los ejecuta el agente principal: son los
  que escriben fuera de la carpeta y un subagente con alcance limitado no debe tocarlos.

## Paso 8: Informa al usuario

Da al usuario una lista numerada de 8 a 12 puntos clave en el chat.

- Nombra cada carpeta y archivo creado.
- Di qué webinars saltaste por estar ya ingeridos y cuáles fallaron por falta de subtítulos.
- Ejecuta `python3 tools/build_index.py`.

## Guardarraíles

- Escribe solo dentro de `finance/myinvestor-webinars/`, `finance/revisions/` y `finance/reports/`.
- No toques ninguna carpeta de otro canal.
- No escribas nunca `transcript.json`.
- No inventes nunca una fecha, un hablante, una cifra ni una fuente.
- La skill nunca da consejo financiero: cada tip pertenece al hablante.
- Un webinar de MyInvestor es material comercial. El interés del hablante va visible en la misma fila, no en un aviso al final.
