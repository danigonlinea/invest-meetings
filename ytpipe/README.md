# ytpipe

## Qué hace

ytpipe descarga la transcripción de un vídeo de YouTube. Luego escribe una carpeta de reunión.

El script escribe dos archivos:

1. La transcripción en texto plano.
2. Un archivo JSON con la estructura de la reunión.

El script no escribe el resumen. Otra herramienta escribe el resumen.

## Instalación

El script usa `uv`.

1. Instala `uv`.
2. Entra en la carpeta `ytpipe`.
3. Ejecuta este comando.

```bash
uv sync
```

## Uso

1. Ejecuta el comando con la URL del vídeo.

```bash
uv run ytpipe fetch <url>
```

## Salida

El script crea una carpeta con el nombre `<fecha>-<tema>`.

El script escribe estos archivos:

| Archivo | Contenido |
| --- | --- |
| `invest-<canal>-<tema>.txt` | La transcripción completa. |
| `transcript.json` | La transcripción con su estructura. |

Después otra herramienta escribe este archivo:

| Archivo | Contenido |
| --- | --- |
| `summary.md` | El resumen de la reunión. |

El archivo `transcript.json` tiene estas secciones:

| Sección | Contenido |
| --- | --- |
| `schema_version` | La versión del formato. |
| `kind` | El tipo de documento. |
| `source` | Los datos del vídeo y de la pista de subtítulos. |
| `stats` | Los recuentos de segmentos, trozos, hablantes y palabras. |
| `chunks` | Los trozos de texto con sus horas de inicio y de fin. |
| `segments` | Los segmentos con su hablante y sus horas. |
| `chapters` | Los capítulos del vídeo. La sección no existe si el vídeo no tiene capítulos. |
| `speakers` | La lista de hablantes. La sección no existe si el vídeo no tiene etiquetas de hablante. |

La sección `source` usa estos campos:

| Campo | Tipo | Contenido |
| --- | --- | --- |
| `url` | string | La URL del vídeo. |
| `video_id` | string | El identificador del vídeo. |
| `title` | string | El título del vídeo. |
| `description` | string | La descripción del vídeo. Una cadena vacía si YouTube no da descripción. |
| `channel` | string | El nombre del canal. |
| `uploader` | string | El nombre de quien sube el vídeo. |
| `uploader_id` | string | El identificador de quien sube el vídeo. |
| `upload_date` | string | La fecha de subida en formato `YYYY-MM-DD`. |
| `duration_seconds` | int | La duración del vídeo. |
| `language_code` | string | El código del idioma de la pista. |
| `language_name` | string | El nombre del idioma de la pista. |
| `subtitle_kind` | string | `manual` o `auto`. |
| `subtitle_format` | string | `json3` o `vtt`. |
| `has_speaker_labels` | bool | `true` si el vídeo da nombres de hablante. `false` en otro caso. |
| `fetched_at` | string | La hora de la descarga en UTC. |

La sección `stats` usa estos campos:

| Campo | Tipo | Contenido |
| --- | --- | --- |
| `segment_count` | int | El número de segmentos. |
| `chunk_count` | int | El número de trozos. |
| `speaker_count` | int | El número de hablantes. |
| `word_count` | int | El número de palabras de la transcripción. |
| `character_count` | int | El número de caracteres de la transcripción. |
| `time_span_seconds` | int | Los segundos entre el final del último segmento y el inicio del primero. |

La sección `chapters` usa estos campos:

| Campo | Tipo | Contenido |
| --- | --- | --- |
| `index` | int | La posición del capítulo. Empieza en cero. |
| `start` | float | El inicio del capítulo en segundos. |
| `start_iso` | string | El inicio del capítulo como `HH:MM:SS`. |
| `end` | float | El final del capítulo en segundos. |
| `end_iso` | string | El final del capítulo como `HH:MM:SS`. |
| `title` | string | El título del capítulo. |

La sección `speakers` usa estos campos:

| Campo | Tipo | Contenido |
| --- | --- | --- |
| `id` | string | El identificador del hablante. Por ejemplo `speaker-1`. |
| `name` | string o null | El nombre del hablante. YouTube no da nombres, así que el valor es `null`. |
| `label` | string | La etiqueta del hablante en los subtítulos. Una cadena vacía si no hay etiqueta. |
| `word_count` | int | El número de palabras del hablante. |

En la práctica YouTube no da etiquetas de hablante en los vídeos de este repositorio: `has_speaker_labels` vale `false` y la sección `speakers` no existe. `name` vale siempre `null`: el script nunca inventa nombres. Los nombres de los ponentes solo entran en el resumen, según la regla de atribución de `reference/glossary.md`.

La sección `chunks` usa estos campos:

| Campo | Tipo | Contenido |
| --- | --- | --- |
| `index` | int | La posición del trozo. Empieza en cero. |
| `text_start` | int | La posición del inicio del trozo en el texto plano. |
| `text_end` | int | La posición del final del trozo en el texto plano. |
| `time_start_iso` | string | La hora del inicio del trozo como `HH:MM:SS`. |
| `time_end_iso` | string | La hora del final del trozo como `HH:MM:SS`. |
| `speakers` | array | Los identificadores de los hablantes del trozo. Sin nombres repetidos y en orden. |
| `text` | string | El texto del trozo. |

Las posiciones `text_start` y `text_end` son índices del texto plano. El texto plano se obtiene al unir el texto de cada trozo con un solo espacio.

La sección `segments` usa estos campos:

| Campo | Tipo | Contenido |
| --- | --- | --- |
| `index` | int | La posición del segmento. Empieza en cero. |
| `speaker` | string o null | El identificador del hablante. El valor es `null` si el vídeo no da etiquetas. |
| `start` | float | El inicio del segmento en segundos. |
| `end` | float | El final del segmento en segundos. |
| `text` | string | El texto del segmento. |

El texto aparece dos veces. El texto de cada trozo sirve para leer. El texto de cada segmento sirve para citar la hora exacta.

## Elegir un idioma

1. Pide la lista de pistas disponibles.

```bash
uv run ytpipe languages <url>
```

2. Lee el código de la pista.
3. Pasa el código al comando de descarga.

```bash
uv run ytpipe fetch <url> --lang <código>
```

El script usa estos idiomas si el usuario no elige uno:

1. `es`
2. `es-ES`
3. `es-419`
4. `en`
5. `en-US`
6. `en-GB`

El script elige la pista en este orden.

1. El script busca primero en las pistas manuales de todos los idiomas pedidos.
2. El script usa el orden de los idiomas pedidos.
3. El script busca en las pistas automáticas si no hay ninguna pista manual.
4. El script usa el número de segmentos solo si dos pistas del mismo idioma y del mismo tipo existen.

## CLI

El script tiene dos subcomandos. Cada subcomando hace una tarea.

| Subcomando | Tarea |
| --- | --- |
| `fetch` | Descarga la transcripción y escribe la carpeta de la reunión. |
| `languages` | Muestra todas las pistas de subtítulos del vídeo. |

### `ytpipe fetch <url>`

Este subcomando hace el trabajo principal.

Opciones:

| Opción | Valor por defecto | Contenido |
| --- | --- | --- |
| `--date YYYY-MM-DD` | La fecha de subida del vídeo | La fecha de la reunión. |
| `--slug TEXT` | Diez palabras del título | El tema de la carpeta. |
| `--out DIR` | La raíz del proyecto | La carpeta padre donde el script escribe. |
| `--lang CODE` | La lista de idiomas interna | Un código de idioma. Repite la opción para más códigos. |
| `--chunk-chars N` | `1200` | El tamaño aproximado de cada trozo. |
| `--force` | Desactivada | Sobrescribe la carpeta si ya existe. |
| `--open` | Activada en macOS | Abre la carpeta al final con el comando `open`. |
| `--no-open` | | No abre la carpeta. |
| `--dry-run` | Desactivada | Muestra el plan y los metadatos. No escribe nada. |

El script para si la carpeta ya existe y `--force` está ausente.

El script muestra un bloque con el plan antes de escribir. Después muestra un bloque con el resultado.

El script no muestra la traza del error. La variable `YTPIPE_DEBUG` vale `1` para ver la traza.

Si no hay ninguna pista en los idiomas pedidos, el script sale con código 1, no escribe la carpeta y el error sugiere ejecutar `ytpipe languages <url>` para ver las pistas que sí existen.

Ejemplo completo:

```bash
uv run ytpipe fetch https://www.youtube.com/watch?v=dQw4w9WgXcQ --lang es --chunk-chars 1200 --dry-run
```

Quita `--dry-run` para escribir la carpeta.

### `ytpipe languages <url>`

Este subcomando muestra una línea por cada pista de subtítulos. Cada línea tiene el código, el nombre y el tipo. El tipo es `auto` o `manual`.

```bash
uv run ytpipe languages https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

## Lo que el script no hace

El script no escribe el resumen. La skill `ingest-meeting` escribe el archivo `summary.md` en un paso aparte.

## La carpeta de la reunión

La skill `ingest-meeting` define la carpeta. La carpeta contiene tres archivos:

1. `invest-<canal>-<tema>.txt`
2. `transcript.json`
3. `summary.md`

## Pruebas

1. Ejecuta este comando desde la carpeta `ytpipe`.

```bash
uv run pytest -q
```