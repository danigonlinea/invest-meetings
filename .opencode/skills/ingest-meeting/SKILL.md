---
name: ingest-meeting
description: Usar cuando el usuario pegue una transcripción de reunión en el chat, cuando el usuario pase una URL de YouTube, o cuando una carpeta de reunión tenga un transcript.json sin summary.md. La skill escribe el resumen detallado, documenta los errores de reconocimiento de la transcripción y compara la reunión nueva con las anteriores.
---

# Ingesta de una reunión

## Metadatos

Esta skill trabaja solo en este repositorio, el repositorio `investing-meetings`.

- Ruta de la skill: `.opencode/skills/ingest-meeting/`.
- Ruta de las carpetas de reunión: `<project-root>/YYYY-MM-DD-<topic-slug>/`.

El nombre de la carpeta de reunión usa el patrón `YYYY-MM-DD-<topic-slug>`.

- Escribe el patrón en minúsculas.
- Escribe las palabras separadas por guiones.
- No escribas acentos.
- No escribas guiones bajos.
- Escribe 6 palabras como máximo después de la fecha.

## Paso 1: Pregunta los datos que faltan

La transcripción llega por una de estas dos rutas.

- El usuario pega la transcripción en el chat.
- El usuario ejecuta `ytpipe fetch <url>` y el archivo `transcript.json` ya existe en la carpeta de la reunión.

El agente necesita 4 datos.

1. La fecha de la reunión.
2. El tema de la reunión.
3. Los participantes.
4. La fuente de la transcripción.

Pregunta al usuario por los datos que faltan antes de escribir cualquier archivo.

- No inventes nunca una fecha.
- No inventes nunca a un participante.
- No inventes nunca una fuente.

Si la carpeta ya tiene `transcript.json`, el agente lee ese archivo. No pide la transcripción en el chat.

## Paso 2: Escribe la transcripción literal

Escribe el texto del usuario en el archivo `.txt` carácter por carácter.

- Conserva las marcas de tiempo.
- Conserva las palabras inglesas `seconds` y `minutes`.
- Conserva los acentos.
- Conserva el signo `€`.
- Conserva las marcas `¿` y `¡`.
- Conserva cada error de reconocimiento de la transcripción automática.
- Conserva cada nombre incorrecto. El resumen documenta esos nombres más tarde.
- No añadas una cabecera.
- No añadas un título.
- No añadas un pie de página.
- No corrijas la ortografía.

**Criterio de finalización:** ejecuta `wc -c` en el archivo y comunica el número de bytes.

## Paso 2 bis: Lee el transcript.json

Aplica este paso solo cuando la carpeta de la reunión ya tiene `transcript.json`. Si el usuario pegó la transcripción en el chat y la carpeta no tiene ese archivo, pasa al Paso 3.

Lee el archivo con `python3 -c` o con la herramienta `read`.

- No leas el archivo entero de una vez cuando el archivo pasa de 200.000 bytes.
- Lee primero `source`, `stats` y `speakers`.
- Lee después `chunks` grupo por grupo.

- `source` trae `title`, `channel`, `upload_date`, `duration_seconds`, `description`, `language_code` y `has_speaker_labels`.
- `has_speaker_labels` vale `false` cuando YouTube no da etiquetas de hablante. El agente lo dice en la nota del resumen.
- `chapters` es el índice del vídeo, con `title`, `start_iso` y `end_iso`. El agente lo usa como esquema del resumen. A veces no existe.
- `stats` trae `segment_count`, `chunk_count`, `speaker_count`, `word_count`, `character_count` y `time_span_seconds`.
- El agente usa `chunks` como unidad de lectura. Cada chunk trae `text`, `text_start`, `text_end`, `time_start_iso`, `time_end_iso` y `speakers`.
- El texto plano del vídeo sale de unir `chunks[].text` con un espacio. `text_start` y `text_end` son las posiciones en ese texto.
- El agente usa `segments` cuando necesita una cita exacta.

## Paso 3 bis: Busca fondos y acciones mencionados

Este paso se aplica cuando la reunión menciona fondos de inversión o acciones de empresas.

El agente analiza el texto completo del transcript (junto de todos los `chunks`) y busca:

1. **Fondos de inversión**: `fondo`, `fund`, `ETF`, `SICAV`, `EAF`, `GESTIÓN`, `gestora`, `management`.
2. **Acciones/empresas**: `acción`, `actions`, `stock`, `acciones`, `cotización`, `carta`, `título`, `bono`, `company`, `empresa`, `compañía`, `holding`, `sociedad`.

### Fuentes de búsqueda

| Tipo | Fuente | URL / método |
|---|---|---|
| Fondos españoles | CNMV | `https://www.cnmv.es/portal/consultas/iic/fondo?lang=es&nif=<NIF>` |
| Fondos internacionales | Wikipedia | `https://es.wikipedia.org/wiki/<nombre>` |
| Acciones de empresas | Yahoo Finance | `https://finance.yahoo.com/quote/<symbol>` |
| Empresas | Wikipedia | `https://es.wikipedia.org/wiki/<nombre>` |
| Valores cotizados | CNMV | `https://www.cnmv.es/portal/consultas/iic/valor/search?lang=es` |

### Proceso

1. Extrae el texto completo del transcript.
2. Busca nombres de fondos y empresas (usando las palabras clave anteriores).
3. Para cada nombre encontrado, hace una petición a la fuente pública adecuada.
4. Guarda los resultados en la parte de abajo.
5. Añade una tabla con la información al resumen.

### Formato de la sección `## Fondos y acciones mencionados`

```markdown
### Fondos de inversión

| Campo | Valor |
| --- | --- |
| Nombre del fondo | `<nombre>` |
| ISIN | `<ISIN>` |
| Gestor | `<gestor>` |
| Fecha de constitución | `<fecha>` |
| Categoría | `<categoría>` |
| Estrategia | `<estrategia>` |
| Comisiones | `<gestion>% (fija), <variable>% (variable)` |
| Patrimonio | `<patrimonio>` EUR |
| Rentabilidad | `<rentabilidad>` |
| Fuente | `<URL>` |

### Acciones de empresas

| Campo | Valor |
| --- | --- |
| Nombre de la empresa | `<nombre>` |
| Sector | `<sector>` |
| Código de cotización | `<código>` |
| ISIN | `<ISIN>` |
| Rentabilidad media anual | `<rentabilidad>%` |
| Volatilidad | `<volatilidad>%` |
| Dividendo | `<dividendo>` |
| Fuente | `<URL>` |
```

### Criterio de finalización

- Cada nombre detectado aparece en la sección.
- No se inventan datos. Si no se encuentra un dato, se escribe `no verificado`.
- El agente registra la URL de cada fuente consultada. Cada segment trae `index`, `speaker`, `start`, `end` y `text`.
- Cuando `speakers` no existe, el vídeo tiene una sola voz. El agente lo dice en la nota y atribuye todo a `speaker-1`.
- Cuando `speakers` existe, el agente usa el campo `id` de cada entrada. El campo `name` vale `null` porque YouTube no da nombres.
- El campo `segments[].speaker` vale `null` cuando el vídeo no tiene etiquetas. El agente nunca inventa un hablante.

No escribas en el resumen ningún número que no aparezca en `transcript.json` o en el texto de la transcripción.

**Criterio de finalización:** el agente puede nombrar la fecha, el canal, la duración, el número de hablantes y el número de capítulos sin abrir ningún otro archivo.

## Paso 3: Escribe el resumen

Escribe `summary.md` con estas secciones, en este orden.

1. Un título y una lista de viñetas de metadatos.
   - La lista contiene la fecha, los participantes, el canal, el nombre del archivo de transcripción, la duración y los temas.
2. Una nota en formato de cita de bloque sobre la transcripción.
   - La nota dice que no hay etiquetas de hablante cuando hay una sola voz.
   - La nota dice que las marcas de tiempo se conservan.
   - La nota dice que hay errores de reconocimiento.
3. `## Resumen ejecutivo`, con 8 o 12 viñetas. Cada viñeta contiene una sola idea.
4. `## Temas tratados`, con un encabezado `###` por tema. Cada tema contiene 3 o 10 viñetas.
5. `## Cifras y datos citados`, una tabla Markdown de dos columnas. La primera columna se llama `Dato`. La segunda columna se llama `Contexto`.
6. `## Ideas y tesis`, una viñeta por tesis. Pon al hablante en negrita al principio de cada viñeta.
7. `## Preguntas abiertas y temas pendientes`, una viñeta por pregunta sin resolver.
8. `## Citas textuales`, cada cita entre comillas dobles. Pon una raya larga detrás de la cita. Escribe el contexto después de la raya larga.
9. `## Fondos y acciones mencionados` (opcional, solo si el transcript menciona fondos o acciones). Ver `Paso 3 bis` para el proceso de búsqueda.

Aplica estas reglas al escribir el resumen.

- Escribe el resumen en español.
- Mantén las frases cortas.
- Atribuye cada tesis a su hablante.
- Marca cada inferencia sobre el hablante con la palabra `inferida`.
- No inventes nunca una cifra que el transcript no contiene.
- Saca cada número del resumen del transcript.
- El agente usa `source.description` del vídeo para los temas. Esa descripción suele traer la agenda y la lista de valores.

**Criterio de finalización:** comprueba que cada sección de la lista anterior existe en el archivo.

## Paso 4: Documenta los errores de reconocimiento

Escribe una sección `## Advertencias sobre la transcripción` como la última parte del resumen.

> El agente puede nombrar la fecha, el canal, la duración, el número de hablantes y el número de capítulos sin abrir ningún otro archivo.

> Los nombres de fondos y acciones buscados en el `Paso 3 bis` se escriben en su propia sección (`## Fondos y acciones mencionados`) antes de esta sección.

Aplica estas reglas al escribir el resumen.

- Escribe el resumen en español.
- Mantén las frases cortas.
- Atribuye cada tesis a su hablante.
- Marca cada inferencia sobre el hablante con la palabra `inferida`.
- No inventes nunca una cifra que el transcript no contiene.
- Saca cada número del resumen del transcript.
- El agente usa `source.description` del vídeo para los temas. Esa descripción suele traer la agenda y la lista de valores.

**Criterio de finalización:** comprueba que cada sección de la lista anterior existe en el archivo.

## Paso 5: Muestra los puntos clave

Al final de la ejecución, da al usuario una lista numerada de 8 o 12 puntos clave.

- Escribe la lista en el chat.
- No escribas la lista en un archivo.
- Dile al usuario qué archivos creaste.
- Dile al usuario si el texto pegado y el archivo guardado tienen alguna diferencia.

## Paso 6: Verifica el resumen

Lee el archivo `summary.md` después de escribirlo. El agente que escribe puede meter palabras corruptas dentro de una palabra.

- Busca palabras que mezclen español e inglés dentro de la misma palabra. Usa `grep -n -E '[a-zñáéíóú]+(recently|developer|Opinions|Escape|imagin es|irmado)[a-zñáéíóú]*' summary.md`.
- Busca números pegados a palabras, por ejemplo `Esadeveloperuntería`.
- Busca una puntuación sin espacio, por ejemplo `garantizado.Japón`.
- Corrige cada caso. Cambia solo la palabra rota.

**Criterio de finalización:** el comando devuelve 0 líneas, y el agente informa del resultado.

## Convenciones

Usa este patrón para el nombre del archivo de transcripción: `invest-<guest>-<channel>-<host>-<topic-slug>.txt`.

Usa `invest-andres-la-pizarra-<slug>.txt` cuando Andrés es el único hablante.

Usa `summary.md` como nombre del resumen.

- Escribe el nombre `summary.md` en inglés.
- La carpeta anterior del repositorio ya usa ese nombre.

Una carpeta de reunión guarda `transcript.json`, la transcripción y `summary.md`.

La transcripción conserva el nombre que escribió `ytpipe`.

- El JSON no tiene `full_text`. El texto plano sale de unir los `chunks`.

`transcript.json` lo escribe `ytpipe`. El agente nunca reescribe ese archivo.

Abre la carpeta en Finder con `open` cuando termina la ejecución.

## Guardarraíles

Lee los otros archivos `summary.md` antes de escribir el resumen nuevo.

- El enlace con las reuniones anteriores ayuda al agente.
- El agente puede marcar dónde discrepan dos hablantes.
- Escribe solo dentro de la carpeta nueva.
- No toques ninguna otra carpeta de reunión.
- El agente informa al usuario si cambió el transcript. La transcripción automática suele traer errores de reconocimiento.
- El agente nunca borra `transcript.json`. Ese archivo es la fuente de la verdad para el resumen.
- El agente nunca corrige el JSON. Si el JSON tiene un error, el agente lo dice al usuario y deja el archivo intacto.

Usa el texto pegado tal cual cuando el texto ya está normalizado.

Cuando el usuario pida corregir un error de reconocimiento, cambia el transcript.

Registra el cambio en la sección `## Advertencias sobre la transcripción` del resumen.
