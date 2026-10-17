---
name: ingest-channel
description: Usar cuando el usuario pida los vídeos nuevos de un canal de YouTube (por ejemplo, "los últimos 3 vídeos de @lapizarradeandres"), cuando el usuario pase una URL de canal que termine en /videos, o cuando el usuario pida un informe de canal. La skill descarga los vídeos con ytpipe, lee las pistas de subtítulos, escribe el resumen de cada vídeo con conclusiones y tips para el inversor, y escribe un informe del canal.
---

# Ingesta de un canal

## Metadatos

Esta skill trabaja solo en este repositorio, el repositorio `investing-meetings`.

- Ruta de la skill: `.opencode/skills/ingest-channel/`.
- Ruta de las carpetas de reunión: `<project-root>/YYYY-MM-DD-<topic-slug>/`.
- Ruta del informe: `<project-root>/informe-canal-<canal-slug>-<YYYY-MM-DD>.md`.

Dependencias:

| Dependencia | Uso |
| --- | --- |
| `uv` | Ejecuta el CLI `ytpipe`. |
| `yt-dlp` | Lista los vídeos del canal. |
| CLI `ytpipe` (`ytpipe/`) | Descarga la transcripción y escribe la carpeta de reunión. |
| Skill `ingest-meeting` | Escribe el resumen de cada vídeo. |

El número de vídeos por defecto es 3.

Esta skill reutiliza la skill `ingest-meeting`. No repite sus pasos. No copia su lista de secciones.

## Paso 1: Lee la petición

El agente necesita 3 datos.

1. El número de vídeos. Valor por defecto: 3.
2. La URL del canal.
3. La preferencia de idioma. Valor por defecto: la lista de idiomas interna de `ytpipe`. Ver `ytpipe/README.md`.

Pregunta al usuario solo cuando falta el número de vídeos o cuando falta el canal.

- No inventes nunca una fecha.
- No inventes nunca un idioma.

## Paso 2: Lista los vídeos nuevos

Ejecuta este comando. Cambia `<canal-url>` por la URL del canal y `<N>` por el número de vídeos.

```bash
yt-dlp --flat-playlist --playlist-end <N> --print "%(id)s\t%(title)s" "<canal-url>/videos"
```

Aplica estas reglas.

- La pestaña `/videos` lista el vídeo más nuevo primero. La opción `--playlist-end N` devuelve los N vídeos más nuevos.
- Cuando un título llega en inglés y el canal habla en español, vuelve a ejecutar `ytpipe fetch` con un `--slug` explícito.

## Paso 3: Salta los vídeos ya ingeridos

Lee el campo `source.video_id` de cada `<carpeta>*/transcript.json` del repositorio antes de cualquier descarga.

- El agente comprueba el identificador de cada vídeo nuevo contra la lista de identificadores ya presentes.
- El agente salta el vídeo cuya identificación ya está presente.
- El agente reporta al usuario cada vídeo que salta.

Ejemplo con `python3 -c`:

```bash
python3 -c "import glob,json; [print(p, json.load(open(p))['source']['video_id']) for p in glob.glob('*/transcript.json')]"
```

Ejemplo con `grep`:

```bash
grep -o '"video_id": "[^"]*"' */transcript.json
```

## Paso 4: Descarga y transcribe

Entra en la carpeta `ytpipe` y ejecuta este comando, un vídeo cada vez.

```bash
uv run ytpipe fetch <url> --no-open
```

Aplica estas reglas.

- No ejecutes las descargas en paralelo. YouTube responde con HTTP 429.
- `ytpipe` ya reintenta después de un límite de peticiones.
- Cuando `ytpipe` falla con `no subtitle available`, el vídeo no tiene pista de subtítulos. Reporta ese vídeo y continúa con el siguiente.
- No edites nunca `transcript.json`.

**Criterio de finalización:** cada carpeta descargada guarda `transcript.json` y el archivo `.txt`. Ejecuta `wc -c` en los dos archivos y comunica el número de bytes de cada uno.

## Paso 5: Escribe el resumen de cada vídeo

Aplica la skill `ingest-meeting` en `.opencode/skills/ingest-meeting/SKILL.md` para cada carpeta.

- La skill `ingest-meeting` define la lista de secciones de `summary.md` y el nombre del archivo. No repitas esa lista aquí.

Añade 2 secciones a cada `summary.md`. Pon las dos secciones después de `## Citas textuales` y antes de la sección de advertencias sobre la transcripción.

### `## Conclusiones para el inversor`

- Una lista de viñetas de 3 a 8 elementos.
- Cada elemento es una conclusión del vídeo que afecta a una cartera.
- Cada elemento nombra al hablante cuando la transcripción da etiquetas de hablante.

### `## Tips para el inversor`

Una tabla Markdown con estas columnas.

| Tip | Por qué | Acción |
| --- | --- | --- |
| Un consejo del hablante. | La razón que da el hablante. | Un paso concreto y comprobable. |

Aplica estas reglas a la sección `## Tips para el inversor`.

- Escribe el minuto del vídeo en la celda `Por qué` cuando hay una hora de `segments` disponible.
- Atribuye cada tip a su hablante.
- No escribas nunca un tip como consejo propio del agente.
- Marca cada inferencia con la palabra `inferida`.
- No inventes nunca una cifra que la transcripción no contiene.

## Paso 6: Escribe el informe del canal

Escribe el informe en la raíz del repositorio con este nombre: `informe-canal-<canal-slug>-<YYYY-MM-DD>.md`. La fecha es la fecha de la ejecución.

Escribe estas secciones, en este orden.

1. Un título y una lista de viñetas de metadatos. La lista contiene el canal, la fecha de la ejecución, el número de vídeos y el número de carpetas leídas.
2. `## Vídeos analizados`, una tabla con estas columnas.

| Fecha | Título | Duración | Carpeta |
| --- | --- | --- | --- |
| `<YYYY-MM-DD>` | `<título>` | `<duración>` | `<carpeta>` |

3. `## Hilos comunes`. Los temas que se repiten entre los vídeos.
4. `## Conclusiones consolidadas para el inversor`.
5. `## Tips priorizados para el inversor`, una tabla con estas columnas.

| Prioridad | Tip | Fuente |
| --- | --- | --- |
| `alta`, `media` o `baja` | `<tip>` | `<vídeo>` y `<minuto>` |

6. `## Discrepancias entre vídeos`. Una viñeta por desacuerdo, o la frase `No hay discrepancias.`.
7. `## Riesgos que menciona el canal`.
8. `## Fondos y acciones mencionados en el canal`. Une las tablas que ya guardan los resúmenes. No repitas la búsqueda que ya hizo `.opencode/skills/ingest-meeting/LOOKUP.md`.

Aplica estas reglas al escribir el informe.

- Lee cada `summary.md` antes de escribir el informe.
- No inventes nunca un dato.
- No repitas un tip que ningún resumen guarda.
- Marca cada inferencia con la palabra `inferida`.

## Paso 7: Informa al usuario

Da al usuario una lista numerada de 8 a 12 puntos clave en el chat.

- Escribe la lista en el chat.
- No escribas la lista en un archivo.
- Nombra cada archivo que la ejecución creó.

## Guardarraíles

- Escribe solo dentro de las carpetas de reunión nuevas y del archivo de informe nuevo.
- No toques ninguna otra carpeta de reunión.
- No escribas nunca `transcript.json`.
- No inventes nunca una fecha, un hablante, una cifra ni una fuente.
- La skill nunca da consejo financiero. Cada tip pertenece al hablante.
- Reporta cada vídeo sin pista de subtítulos. No escribas un resumen sin transcripción.

## Convenciones

Usa este patrón para el nombre del informe: `informe-canal-<canal-slug>-<YYYY-MM-DD>.md`.

Las reglas del nombre de la carpeta de reunión las definen `ytpipe` y `ingest-meeting`. No las repitas aquí.

- `ytpipe` define el patrón `YYYY-MM-DD-<topic-slug>` de la carpeta.
- La skill `ingest-meeting` define la lista de secciones de `summary.md`.

Ejecuta las descargas una tras otra. Nunca en paralelo.
