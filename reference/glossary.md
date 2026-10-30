---
title: "Glosario"
date: 2026-10-11
type: reference
category: cross
tags: [glosario, terminologia]
status: final
---
# Glosario de ponentes y nombres

Índice de personas, canales, entidades y variaciones de escritura que aparecen en las reuniones del repositorio `investing-meetings`. Sirve para indexar nombres y ponentes futuros y mantener estandarizados los nombres y las atribuciones en los resúmenes (`summary.md`) y en las transcripciones.

## ¿Cómo añadir una entrada?

Cuando aparezca un nuevo ponente en una reunión futura:

1. Añade una fila/entrada en la tabla de **Ponentes** con:
   - **Nombre** (forma canónica que se usará en el resumen).
   - **Rol** (autor, presentador, entrevistador, invitado, autor de libro, etc.).
   - **Canal / contexto** (si está claro).
   - **Aparece en** (fecha de la reunión, o fecha + nombre de la traducción).
   - **Notas** (variantes de transcripción, ambigüedad de nombre, supuestos que convenga confirmar).
2. Si el ponente ya estaba en el glosario, actualiza solo su fila (añade la nueva fecha en la columna "Aparece en", no crees una entrada duplicada).
3. Si el ponente solo aparece en una reunión y luego no vuelve, se puede dejar en la tabla con un marcador de "sola aparición".

> Regla de oro: en un resumen, el nombre canónico del ponente va siempre escrito de la misma manera, y cualquier variante de transcripción va en la sección "Advertencias sobre la transcripción" y en esta tabla.

## Ponentes

| Nombre canónico | Rol | Canal / contexto | Aparece en | Notas |
|---|---|---|---|---|
| Andrés | Autor y presentador del canal "La Pizarra de Andrés". Hace videos y charlas sobre inversiones. | "La Pizarra de Andrés" | 2026-10-09 (monólogo, autor); 2026-10-07 (entrevistador) | En 2026-10-07 el nombre "Andrés" lo usan ambas partes (el entrevistador lo llama al invitado al inicio y el invitado lo llama al entrevistador en la segunda mitad). Por eso la atribución de turno en ese encuentro es inferencial y va marcada como "(inferida)". |
| Javier (también "Jorge") | Invitado / gestor de inversiones. Aparece como autor del libro *Lo que saben los que saben*. | El Arte de Invertir (asociado; el resumen no lo declara explícitamente) | 2026-10-07 | El nombre "Javier" lo usa el entrevistador al invitado (es la única voz que lo llama así). El nombre "Jorge" aparece en el slug del fichero `invest-jorge-la-pizarra-andres.txt`. La correlación Jorge ↔ Javier es inferida. |
| Comet | Invitado del episodio de SpaceX (El Arte de Invertir). | "El Arte de Invertir" | 2026-05-20 | En la transcripción aparece como "Nicomer", "Comic", "come to". La forma canónica es "Comet". |
| Presentador (El Arte de Invertir) | Presentador del canal El Arte de Invertir. No tiene nombre explícito en la transcripción del episodio de SpaceX. | "El Arte de Invertir" | 2026-05-20 | Solo se referencia como "presentador". No colocar nombre propio que no esté en la transcripción. |
| Mike Bird | Autor del libro *The Land Trap*. No es ponente, es referenciado en el resumen de Javier. | — | 2026-10-07 | Solo citar su nombre y obra. |
| Stephen Penman | Profesor de la Universidad de Columbia, fuente del método de los beneficios residuales. | — | 2026-10-07 | Referenciado en el resumen de Javier. |

## Canales

| Canal | Propietario / frecuente | Descripción |
|---|---|---|
| La Pizarra de Andrés | Andrés | Videos y charlas de inversión, con estilo de monólogo y "pizarra". Aparece en 2026-10-09. |
| El Arte de Invertir | Presentador (sin nombre confirmado); invitados como Comet y Javier | Episodios y charlas de inversiones con invitados, interviews y análisis. Aparece en 2026-05-20 y 2026-10-07. |

## Variaciones de transcripción (errores de reconocimiento)

Tabla de variaciones detectadas. Cada una debe aparecer en la sección "Advertencias sobre la transcripción" de su resumen correspondiente.

| Transcripción | Nombre correcto |
|---|---|
| Nicomer / Comic / come to | Comet |
| Iron Mosque / Elon Mosk / Elon Mosco / Elon M / Ilon / Mosk / Mosco / Mosque | Elon Musk |
| Space X | SpaceX |
| XI, Xi, xAI, ex, EX | xAI |
| Grock, Grock de AI | Grok |
| Ecostar | EchoStar |
| Gey / besos / Jeos | Bezos (Jeff) |
| Bolaris Aerob | Volaris |
| Lockit Martin | Lockheed Martin |
| Yobi o Fly | Joby |
| ASS, Asts, AST Space Mobile | AST Space Mobile |
| One Web | OneWeb |
| Rocketlabs, Rocket Laab | Rocket Lab |
| Vitso | Vistage |
| Daniel Fogel | Daniel Fogel (apellido no confirmado) |
| Weightbot White / Walter Isackson | Walter Isaacson |
| Jack Dors, Jack Dory | Jack Dorsey |
| Alan Casís | Alan Casís (correcto) |
| Sunder Pichy | Sundar Pichai |
| Charlie Monger | Charlie Munger |
| reality distortion feel | reality distortion field |

## Aclaraciones alcanzables (en investigación)

Lista de puntos que el resumen debe marcar como inferencia, no como dato hablado:

| Punto | Reunión | Estado |
|---|---|---|
| "11 veces" hace referencia a "equivalente a México", no a Meta. Meta sí aparece en el vídeo, pero la comparativa del 11x es de "equivalente a México". | 2026-05-20 | Confirmar que el resumen diga "equivalente a México" |
| EBITDA 7.500–8.000, FCF ~5.000, xAI fusion 1.25 billones, proyección 20.000 millones, "300" del siguiente de Musk (transcrito como "300, ¿no?") | 2026-05-20 | Estimaciones del presentador, irán etiquetadas como "(estimación)" |
| "1929 y 1972" del resumen de Andrés viene de "crack de 29" + "29 y el 72" (Japón). Correxir a "entre el crack de 1929 y 1972". | 2026-10-09 | Pendiente de ajuste |
| "39–41%" de las 10 mayores del S&P 500 → transcripción dice "43 de cada 100 € ... en torno al 40". Usar "43% (en torno al 40%)" o redondear explícitamente. | 2026-10-09 | Pendiente de ajuste |
| Canal del encuentro Javier/Andrés no está declarado explícitamente en su resumen (solo el de El Arte de Invertir en 2026-05-20). | 2026-10-07 | Confirmar canal |
| "Javier" ↔ "Jorge" (slug del fichero) | 2026-10-07 | Confirmar nombre exacto del invitado |
