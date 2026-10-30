---
name: ingest-meeting
description: Usar cuando el usuario pegue una transcripción de reunión en el chat, cuando el usuario pase una URL de YouTube, o cuando una carpeta de reunión tenga un transcript.json sin summary.md. La skill escribe el resumen detallado, documenta los errores de reconocimiento de la transcripción y compara la reunión nueva con las anteriores.
---

# Ingesta de una reunión

## Metadatos

Esta skill trabaja solo en este repositorio, el repositorio `investing-meetings`.

- Ruta de la skill: `.agents/skills/ingest-meeting/`.
- Ruta de las carpetas de reunión: `<project-root>/<categoria>/YYYY-MM-DD-<topic-slug>/`.
- Ruta de los informes y artefactos analíticos: `<project-root>/research/reports/`, `<project-root>/research/portfolio/`, `<project-root>/research/revisions/`.
- Ruta de las referencias: `<project-root>/reference/`.
- Todo artefacto `.md` lleva frontmatter YAML (title, date, type, category, tags, status). Ver `README.md` del repositorio.
- El agente elige la categoría por el tema de la reunión antes de crear la carpeta.
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
- El agente usa `segments` cuando necesita una cita exacta. Cada segment trae `index`, `speaker`, `start`, `end` y `text`.
- Cuando `speakers` no existe, el vídeo tiene una sola voz. El agente lo dice en la nota y atribuye todo a `speaker-1`.
- Cuando `speakers` existe, el agente usa el campo `id` de cada entrada. El campo `name` vale `null` porque YouTube no da nombres.
- El campo `segments[].speaker` vale `null` cuando el vídeo no tiene etiquetas. El agente nunca inventa un hablante.

No escribas en el resumen ningún número que no aparezca en `transcript.json` o en el texto de la transcripción.

**Criterio de finalización:** el agente puede nombrar la fecha, el canal, la duración, el número de hablantes y el número de capítulos sin abrir ningún otro archivo.

## Paso 3 bis: Busca fondos y acciones mencionados

Este paso se aplica cuando la reunión menciona fondos de inversión o acciones de empresas.

El agente analiza el texto completo del transcript (la unión de todos los `chunks`) y busca:

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
3. Para cada nombre, localiza la frase donde aparece y anota el minuto.
4. Guarda la cifra que el hablante asocia a ese nombre: precio sobre valor en libros, PER, dividendo, descuento sobre activos, comisión, CDS, probabilidad, rentabilidad.
5. Determina la postura del hablante hacia ese nombre con una frase literal.
6. Para cada fondo, hace una petición a la fuente pública adecuada.
7. Escribe la sección con el formato de abajo.

### Formato de la sección `## Fondos y acciones mencionados`

La sección responde tres preguntas sin abrir la transcripción: qué se nombra, con qué cifras y qué opina el hablante. Cuatro subsecciones, en este orden.

#### `### Vehículos con identificador`

Fondos, ETF, SICAV y bonos con nombre o ISIN.

| Nombre | Tipo | ISIN o ticker | Clase | Comisión o coste | Cifra clave del hablante | Postura | Minuto |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<nombre>` | fondo, ETF, bono | `<ISIN>` o `no verificado` | `<clase>` | `<dato>` o `no verificado` | `<la cifra que dice>` o `sin cifras` | `<postura>` | `<mm:ss>` |

Después de la tabla, una ficha por fondo con los campos públicos: gestor, fecha de constitución, categoría, estrategia, patrimonio, rentabilidad y fuente. Si el vídeo no nombra ningún vehículo, escribe una línea con ese hecho en lugar de una fila con guiones.

#### `### Acciones y empresas con cifras`

| Empresa | Ticker | Cifra que da el hablante | Contexto de la mención | Postura | Minuto |
| --- | --- | --- | --- | --- | --- |
| `<nombre>` | `<ticker>` o `no verificado` | `<cifra>` | `<qué se decía de ella>` | `<postura>` | `<mm:ss>` |

#### `### Menciones sin cifras`

Una viñeta por nombre que aparece sin ningún número asociado: `<nombre>` — qué se dijo y en qué minuto.

#### `### Lo que el vídeo descarta y por qué`

Una viñeta por nombre que el hablante rechaza o critica: `<nombre>` — motivo y minuto.

#### Valores de `Postura`

Usa exactamente uno.

| Valor | Cuándo |
| --- | --- |
| `recomienda` | Solo si hay una frase en la que el hablante lo recomienda. |
| `en cartera` | El hablante dice que lo tiene o que lo ha comprado. |
| `idea a estudiar` | Lo presenta como candidato sin posición. |
| `ejemplo negativo` | Lo usa para explicar qué no comprar. |
| `criticado por caro` | Lo compara por coste o por valoración. |
| `neutro` | Se nombra sin juicio. |

Añade `(lo comercializa)` cuando el hablante vende el vehículo que describe.

### Criterio de finalización

- Cada nombre detectado aparece una sola vez, en la subsección que le toca.
- Cada fila con cifras contiene la cifra literal del hablante y su minuto.
- `recomienda` solo aparece cuando hay una cita que lo sostiene.
- No se inventan datos. Si falta un dato público, se escribe `no verificado`; si el hablante no da cifra, `sin cifras`.
- El agente registra la URL de cada fuente consultada.

## Paso 3: Escribe el resumen

Antes de escribir el cuerpo, abre el archivo con un bloque de frontmatter YAML:

```yaml
---
title: "<título del vídeo o reunión>"
date: <YYYY-MM-DD>
type: meeting-summary
category: <ai o finance>
tags: [<temas principales>]
status: final
---
```

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
9. `## Fondos y acciones mencionados` (opcional, solo si el transcript menciona fondos o acciones). Usa el formato enriquecido de `Paso 3 bis`: qué se nombra, con qué cifras y con qué postura. Una tabla de nombres no basta.

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

Escribe una sección `## Advertencias sobre la transcripción` como la última parte del resumen. La sección `## Fondos y acciones mencionados` del Paso 3 bis va justo antes.

Aplica estas reglas a esta sección.

- Abre un encabezado `###` por tipo de error: nombres propios, palabras corruptas y marcas de tiempo.
- Escribe una viñeta por error. Cada viñeta da la forma que aparece en la transcripción y la forma correcta.
- Añade el minuto cuando `segments` da la hora del error.
- No inventes nunca una corrección. Si no puedes confirmar la forma correcta, escribe `no verificado`.
- Deja la transcripción intacta salvo que el usuario pida corregirla. Ver `## Guardarraíles`.

**Criterio de finalización:** la sección existe, es la última del archivo, y cada error corregido en el Paso 6 aparece en ella.

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

### Reglas de precisión

- No inventes nunca una cifra dentro de un tip. Si el hablante no da el número, escribe el criterio sin número: «reducir las fuentes», no «dos o tres gestores».
- No atribuyas una frase a un hablante cuando el audio no trae etiquetas y el contexto es ambiguo. Escribe `no atribuible con certeza` en vez de elegir un nombre.
- Comprueba la magnitud de las cifras del audio: «trillón» en una charla en español suele ser el *trillion* inglés, es decir, un billón. Anota la forma del audio y la equivalencia.
- Conserva los hedges del hablante («si no me equivoco», «me lo invento», «no sé cuáles son»). Suprimirlos endurece la tesis y falsea el resumen.
- Revisa las conclusiones del resumen contra la transcripción: es donde más se invierte el énfasis de lo que dijo el invitado.
- No conviertas una descripción en instrucción de cartera. Si la acción la deduce el agente, escribe `inferida` en la celda.
- Una mención no es una recomendación. Usa `recomienda` solo con la frase que lo diga; si el hablante lo tiene, es `en cartera`; si lo usa como ejemplo de lo que no compra, es `ejemplo negativo`.
- Cada nombre propio de empresa o fondo lleva la cifra que el hablante le asocia y el minuto. Un nombre sin cifra va a `### Menciones sin cifras`, no a la tabla.
- Cuando el hablante vende el producto que describe, escríbelo al lado: `(lo comercializa)`. El lector tiene que ver el interés en la misma fila, no en un aviso al final.

Usa el texto pegado tal cual cuando el texto ya está normalizado.

Cuando el usuario pida corregir un error de reconocimiento, cambia el transcript.

Registra el cambio en la sección `## Advertencias sobre la transcripción` del resumen.
