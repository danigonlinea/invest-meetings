# Cómo se montan agentes autónomos que entregan trabajo en Claude

**Alcance.** Este informe sale del vídeo `invest-dev-docs-explained-anthropic-engineers-ai-agents-claude-opus.txt`, del canal Dev Docs Explained. La reunión dura 1 hora 34 minutos 46 segundos. Dos ingenieros de Anthropic explican Claude Managed Agents, un producto gestionado para correr agents en la nube. La charla cubre la arquitectura del harness, la separación de cerebro y manos, las credenciales, la memoria, las skills, los outcomes, el modo dreaming, los despliegues y las evaluaciones. La segunda mitad es un taller con un desk de research y una ronda larga de preguntas. La pista es automática, en inglés, sin etiquetas de hablante.

## Resumen en una página

- Un agent es un modelo en un bucle con tools. El harness es la capa que envuelve al modelo para hacer esas llamadas. (00:06)
- El harness codifica suposiciones sobre el modelo. Las suposiciones caducan cuando sale un modelo nuevo. (09:10)
- La primera arquitectura metía todo en un contenedor. El equipo la llama "un pet": una entidad con nombre y cuidada a mano. (04:04)
- La segunda arquitectura separa tres interfaces: session, cerebro y manos. Todo pasa a ser reemplazable, como "cattle". (05:41)
- Las credenciales nunca entran en el sandbox. Un proxy reenvía la llamada e inyecta el token. El modelo nunca ve el token. (07:04)
- El event log de la session es append only. La estrategia de compactación decide qué entra en el contexto y qué no. (07:47)
- El cambio de arquitectura bajó el tiempo hasta el primer token un 90 por ciento. (08:25)
- Una task se define con un outcome: tarea, rúbrica y máximo de iteraciones. Un subagente verifica el resultado. (32:07)
- El modo dreaming analiza transcripts de los últimos 30 días y reescribe el memory store. Está en vista previa. (53:01)
- Correr evaluaciones es el único modo de saber si el agent funciona. Un resultado del 100 por cien suele indicar un problema mal definido. (79:55)

## Arquitectura de un agente autónomo

### La capa de harness

El harness es una capa que envuelve al modelo. Hace las llamadas a tools en un bucle. Gestiona el contexto y el estado de la session. Encapsula todo lo que el modelo no puede hacer.

El harness toma estas decisiones. Decide cuándo hacer un context reset. Decide qué eventos entran en el contexto. Decide qué hacer cuando una tool falla. Administra las suposiciones sobre cada modelo.

Un ejemplo del hablante. Sonnet 4.5 tenía "context anxiety". Cuando sentía el final del límite de contexto, intentaba cerrar la tarea muy rápido. Un harness para Sonnet 4.5 añadía un context reset. Opus 4.5 no tenía esa limitación. El reset dejó de ser necesario. El harness debe encapsular estas suposiciones y actualizarlas con cada modelo nuevo. (01:31)

En el producto, "harness" significa el bucle de ejecución de tools. Gestiona el contexto y el estado de la session. Otros constructores llaman harness a la coordinación de varios agents y sessions. (58:30)

### Session, cerebro y manos

El agent pasó a ser tres interfaces separadas. (05:48)

- La **session** es un log append only de todo lo que pasó en la session. La session es la unidad de trabajo. (03:34)
- El **cerebro** es el harness o agent loop, junto con Claude. (05:41)
- Las **manos** son los sandboxes, las llamadas a tools y las llamadas a MCP. Se aprovisionan a demanda. Desaparecen cuando termina el trabajo. Si se pierde un sandbox, se levanta otro. (05:48)

El hablante usa la frase "one brain can reach many hands". Un cerebro llega a muchos sandboxes. Puede llamar a un contenedor, a la VPC de un cliente o a un servidor MCP. Todas las manos son intercambiables. (08:47)

### El cambio de arquitectura y su efecto

La primera arquitectura metía todo en el contenedor. La session, el harness y la ejecución del sandbox vivían dentro. No había fronteras de servicio que diseñar. Las ediciones de ficheros eran como llamadas al sistema. (03:30 y 03:58)

Luego el equipo "decouple the brains from the hands". (05:41) El resultado medido: el tiempo hasta el primer token bajó alrededor de un 90 por ciento. El cerebro solo levanta el sandbox cuando lo necesita. No espera a que el contenedor arranque para devolver el primer token. (08:25)

### El "pet" y por qué la primera arquitectura fallaba

El hablante usa la metáfora de pet y cattle de la vieja infraestructura. Dice: "pet is when you essentially have a named and handtended entity. When it gets sick, you have to nurture it back to life. Otherwise, you basically cannot afford to lose it." (04:12) Y añade: "what we had with our initial setup was essentially a pet". (04:04)

Tres fallos del pet:

1. Depurar era difícil. Todo corría dentro del contenedor. Un paquete perdido y un contenedor muerto se veían igual. Había que entrar por websocket para depurar.
2. Investigar era difícil. Los datos del cliente vivían en esos contenedores. No había forma de entrar a depurar.
3. Conectar con un MCP en la VPC del cliente exigía emparejar redes o enviar el harness al cliente. (04:20)

Con la separación, cada componente se volvió "cattle". Cada pieza es reemplazable. Cuando el sandbox muere, el cerebro decide si lo levanta otra vez. Cuando el harness muere, se levanta una instancia nueva y lee el event log. El trabajo continúa desde el último evento. Lo único que se protege es el session log. (06:17)

## Credenciales, sandbox y seguridad

La regla central: las credenciales nunca entran en el sandbox. El hablante dice: "credentials never entered our sandbox". (07:04)

En la arquitectura anterior, la credencial vivía dentro del sandbox. Eso aumentaba la exposición a prompt injection.

En la arquitectura nueva, el sandbox llama a un proxy cuando necesita un token. El proxy inyecta el token antes de llamar al endpoint externo o al MCP externo. El modelo nunca ve la credencial ni el token. El hablante lo explica así: el usuario no puede hacer prompt injection para pedir los tokens, imprimirlos o escribirlos en un fichero. "You can never do that because cloud actually never sees your your tokens." (07:19 y 07:32)

El reenvío pasa por un proxy externo. El `.txt` no usa la frase `onward proxy` en ningún punto. El término exacto del hablante es "routed through a proxy that would inject your token". El nombre `onward proxy` queda como no verificado en el transcript. (07:21)

El producto añade el concepto de **vaults** para producción. El vault guarda un secreto en una variable de entorno. En lugar del secreto real, se pone un placeholder. Claude usa el placeholder. Anthropic lo cambia por el valor real en el egress. El cambio solo ocurre en los dominios que el usuario autoriza. Si el secreto es solo para el SEC, no se inyecta para anthropic.com. El hablante dice "entropic.com" por Anthropic. (38:26 y 38:45)

Las vaults también funcionan con OAuth. Se crea un vault, se le da un nombre y un ID. El ID se adjunta a la session. (39:35)

## Memoria

El **memory store** es un almacén de larga duración. Se comparte entre sessions. Varias sessions aprenden sobre instrumentos financieros distintos y comparten ese conocimiento. (30:54)

Datos del memory store:

- Es una entidad independiente. Se adjunta a la session cuando hace falta. (59:10)
- Se pueden adjuntar varios memory stores a la misma session. El hablante propone un store a nivel de usuario y otro a nivel de organización. (45:17)
- La memoria persiste entre sessions. Es "state", no solo contexto. (59:00)
- El contenido se escribe al terminar la tarea. En el taller, el agent escribe una nota por empresa en la memoria y un scorecard en un fichero. (33:40)
- Los datos están en la infraestructura de Anthropic. Todo es API. El usuario puede extraer las memorias y llevarlas a otro sistema. (44:20)

La session guarda cada evento. Nada se descarta. La estrategia de compactación decide qué parte del log entra en el contexto. El hablante liga la memoria a la acción del agent, no al contexto del modelo. (07:47)

El informe no encuentra la frase "memory graph" en el audio. Tampoco aparece "mapa de memoria". El título del capítulo 3 dice "memory graphs", pero la pista no lo dice. La organización de la memoria como store compartido es lo que describe el hablante. (inferida)

Diferencia entre memoria y contexto. El contexto es la ventana que ve el modelo ahora. La memoria es un almacén fuera de la session. El agent decide qué recuperar del almacén. La compactación gobierna el contexto, no la memoria. (inferida a partir de 07:47 y 30:54)

## Contexto y context resets

El harness gestiona la ventana de contexto. El event log de la session es append only. Nada se descarta ni se reescribe. (07:47)

La **compactación** es flexible. El sistema elige una de dos vías. Puede resumir todo el event log y meter el resumen en el contexto. Puede tomar solo los últimos N eventos y meterlos. La decisión depende de la estrategia elegida. (07:47)

El **context reset** nace de una limitación de un modelo. Sonnet 4.5 sufría "context anxiety". Al acercarse al límite, cerraba la tarea muy rápido. Un reset evitaba ese cierre prematuro. Opus 4.5 no tenía esa limitación. El reset dejó de ser necesario. (01:31)

Qué sobrevive al reset. El log completo de la session sobrevive. La session sigue viva. Si el harness muere, se levanta otro y lee el event log. El trabajo continúa desde el último evento. (06:45)

Anthropic corre la compactación por el usuario. El hablante dice que se pueden correr sessions durante días. La session más larga vista en producción dura 10 horas. (55:51)

## Skills, prompts y loops

Una **skill** es un artefacto de instrucciones reutilizable. En el taller, la skill enseña al agent a llamar a la web del SEC. Describe el paquete de Python y el uso de la identidad EDGAR. (28:39)

Propiedades de las skills:

- Son artefactos vivos. Se pueden actualizar. (36:30)
- Cuando se actualiza una skill, las sessions nuevas que la referencian reciben la información nueva. (36:40)
- El bucle agéntico llama a tools hasta terminar la tarea. (00:06)

Los **subagentes** tienen su propio prompt, sus tools y sus permisos. El agent principal puede delegar en ellos. Un agent puede referenciarse a sí mismo. Así puede levantar una copia de sí mismo con el mismo prompt. (29:10)

Detalle importante. El subagente no recibe el transcript de la session. Solo recibe el prompt, la descripción de tools y los esquemas. (29:20)

El hablante desaconseja fijar la topología a mano. Dice que conviene quitar los límites y "let it cook". Dejar que Claude decida su mejor topología suele dar mejor resultado. (56:42)

### Patrón de mapa y reduce con el desk de research

El taller usa un desk de research. El patrón funciona así. (19:37)

1. El usuario habla con un agent principal.
2. El agent principal llama a una custom tool propia llamada `dispatch analysis`. (29:04)
3. Esa tool levanta una session por cada ticker.
4. Cada session usa su propio multi-agent y su propio outcome.
5. Todas las sessions comparten el memory store.
6. Al terminar, el agent principal agrega los resultados y da las puntuaciones. (50:10)

El hablante llama a esto "map produce", que significa map-reduce. El usuario construye su propio harness encima de Claude Managed Agents. (19:37)

## Outcomes y autosupervisión

Un **outcome** define una tarea con tres piezas. La tarea, una rúbrica y un máximo de iteraciones. El hablante dice: "Outcomes is how we've created self-supervision." (32:07)

El flujo del outcome:

1. El usuario envía un evento `user-defined outcome` con la rúbrica.
2. El agent principal ejecuta el trabajo. Puede usar subagentes.
3. Cuando cree que terminó, levanta un subagente verificador.
4. El verificador lee la rúbrica, el trabajo y los artefactos.
5. Si no cumple, el agent vuelve a intentarlo. Si cumple, entrega. (32:23)

Este es el punto que separa "entregar trabajo" de "solo ejecutar". El agent no para por su cuenta. Para cuando un verificador confirma la rúbrica. El ejemplo del taller es un scorecard de Nvidia con formato fijo. El verificador comprueba los números, la memoria y el fichero JSON. (35:16)

Dos límites. El outcome se define a nivel de session completa. No hay definición de sub-outcome por subagente. El outcome también sirve para sessions muy largas. Claude itera hasta cumplir la rúbrica. (46:26 y 60:26)

## Dreaming y orquestación

El **modo dreaming** es un analizador de sesiones pasadas. El usuario elige un memory store, un modelo y unas instrucciones. Usa un prompt por defecto si no da instrucciones. (53:01)

Cómo opera:

1. Toma los transcripts de los últimos 30 días.
2. Levanta una session con Claude Managed Agents.
3. Levanta varios subagentes para analizar cada transcript.
4. Comprueba si el memory store codificó toda la información necesaria.
5. Detecta problemas repetidos y huecos en las instrucciones.
6. Reescribe el memory store para mejorar las sessions futuras. (53:03)

En la demo, dreaming encuentra huecos en la skill del SEC. Actualiza la memoria para ampliar ese conocimiento. (54:10)

Estado y límite. Dreaming está en research preview, es decir, en vista previa. El límite actual: opera solo sobre memory stores. El hablante espera extenderlo a skills, prompts y definiciones de agent. Anthropic corre evaluaciones para medir la mejora de dreaming. (63:55 y 47:00)

## Despliegues, workspaces y operación

Un **deployment** corre sessions de un agent según un calendario. Toma una definición de agent, un horario y unos mensajes iniciales. Puede recibir memory stores, repos de GitHub o ficheros. El ejemplo del taller corre un memo semanal el primer día del mes. (51:24)

Persistencia. La memoria y el estado persisten entre sessions. La session es la unidad de trabajo. Días, semanas y meses de trabajo son posibles. Anthropic corre la compactación. (27:36 y 55:51)

La **primitiva de aislamiento** es el **workspace**. Se ponen clientes distintos en workspaces distintos. Luego se da acceso a usuarios concretos dentro de cada workspace. (57:46)

Uso real citado. Los agents externos de Notion corren sobre este producto. También hay integraciones con Atlassian y Jira. (72:05)

Cifras citadas:

- Duración de la session más larga en producción: 10 horas. (55:51)
- Número de sessions en producción: no verificado. El hablante solo dice que no hay límite, salvo rate limits. (70:00)
- Sessions que Anthropic levanta en paralelo para evaluar: 10.000. (79:40)
- Proveedores de sandbox citados: Modal, Daytona, E2B, Cloudflare. El audio dice "Purcell" por un proveedor no identificado, "Moto" por Modal y "EB2" por E2B. (24:56 y 89:04)

También existe Ant CLI, una CLI que envuelve la API. Permite recursos duraderos en YAML dentro del repositorio. Así se hace CI/CD de los agents. (76:18)

## Límites y carencias hoy

- No hay rewind ni roll-forward. Solo se puede pilotear el agent con mensajes nuevos. En palabras del hablante: "We don't currently have a way for like rewind and roll forward." (42:55)
- No hay session forking. El hablante dice: "session forking is essentially what you're asking for... it's on our road map". (43:02)
- No hay sub-outcome por subagente. "There is no currently support for like a sub outcome definition." (46:26)
- No hay flujo topológico ni grafo en la interfaz. "Not yet. Not yet." (56:54)
- No hay control de acceso por roles. Solo existe el workspace. El hablante dice: "we don't have any arvback controls on our level other than like workspace". La palabra real es RBAC. (69:22)
- No hay controles finos de compartición. No se puede compartir solo una parte de un recurso. (81:40)
- No hay on-prem. "We're not supporting onrem." La palabra real es on-prem. (84:52)
- No hay presupuesto por session. "That's not something we offered today." (41:57)
- No hay otro proveedor de memoria de serie. Hay que construir un MCP o una custom tool. (44:30)
- Los sandboxes gestionados son todos iguales. Para GPU o más memoria hay que usar un sandbox self-hosted. (88:40)
- No hay tunneling para probar la interfaz dentro del sandbox. (83:40)
- Solo se admiten modelos de Claude. "It's cloud models only for now." (67:10)
- No se pueden enviar mensajes mientras el modelo espera un custom tool result. La llamada devuelve un 400. (77:40)

## Hoja de ruta

- Bifurcación de session. Los clientes la han pedido. "It's on our road map." (43:02)
- Control de acceso por roles. El hablante dice que "RBAC is on our road map". (58:08)
- Presupuesto de tokens y de dinero por session. Está en exploración: "We are exploring the idea of what it means to do like budget tighter budget controls." (41:57)
- Extender dreaming a skills, prompts y definiciones de agent. Hoy solo toca memory stores. (47:00)
- Mejorar el soporte multi-tenant sobre workspaces. (69:00)
- Flujos topológicos o de grafo en la interfaz. "Maybe soon." (56:54)
- On-prem. El hablante dice que lo consideran en serio para clientes enterprise. (85:10)

## Cómo aplicarlo en un proyecto propio

1. Define cada tarea como una session. La session es la unidad de trabajo. (capítulo 1, 00:03:34)
2. Separa session, cerebro y manos. No metas el harness dentro del sandbox. (capítulo 1, 00:05:41)
3. Levanta cada sandbox a demanda y deséchalo al terminar. (capítulo 1, 00:05:48)
4. Ejecuta cada tarea en un contenedor aparte para limitar el radio de impacto. (capítulo 1, 00:02:56)
5. No dejes que la credencial entre en el sandbox. Usa un vault y un proxy que inyecte el token en el egress. (capítulo 1, 00:07:04)
6. Guarda cada evento en un log append only. Deja que la compactación decida qué entra en el contexto. (capítulo 1, 00:07:47)
7. Adjunta un memory store compartido a las sessions que deban aprender juntas. (capítulo 3, 00:30:54)
8. Define cada tarea con un outcome: rúbrica y máximo de iteraciones. (capítulo 3, 00:32:07)
9. Deja que un subagente verificador revise la rúbrica y los artefactos antes de entregar. (capítulo 3, 00:35:16)
10. Empieza con un agent y una skill. Sube a multi-agent cuando haga falta. (capítulo 3, 00:28:39)
11. Usa la lógica de map-reduce para muchos elementos. Una session por elemento y agregación al final. (capítulo 3, 00:19:37)
12. Programa el trabajo recurrente con deployments. (capítulo 4, 00:51:24)
13. Corre evaluaciones con datos de calidad antes de confiar en el agent. (capítulo 5, 01:19:55)
14. Usa un workspace por cliente cuando haya requisitos legales de separación de datos. (capítulo 5, 01:25:00)

## Evaluaciones y datos

El consejo central: correr evaluaciones. El hablante dice: "Our best recommendation would be to run evals on your agent with like different types of tasks that you want the agent to perform." (60:18)

La calidad del dato decide todo. El hablante dice: "garbage in garbage out". Un problema mal definido da un resultado del 100 por cien sin significado. El equipo lo vio en sus propias evaluaciones. Un 100 por cien no prueba nada si la rúbrica es floja. (79:55 y 80:02)

Dos prácticas:

- Iterar sobre los datos y definir bien el problema.
- Usar las sessions históricas como conjunto de datos. Puntuar los resultados para medir al modelo. (80:40)

Anthropic tiene tooling interno. Levanta 10.000 sessions en paralelo sobre distintos conjuntos de datos. Con eso ajusta prompts y borra suposiciones del harness con cada modelo nuevo. (79:40)

El outcome ayuda aquí. El usuario define la rúbrica exacta y un máximo de iteraciones. El agent verifica el resultado contra esa rúbrica. (60:26)

## Citas textuales

1. "agent is basically uh a model in a loop with tools." (00:06) El hablante define qué es un agent, antes de hablar del harness.
2. "Harness is typically like a layer that wraps around the model that helps you make these tool calls in a loop." (01:03) Definición de harness.
3. "what happened was we realized we adopted a pet." (04:04) El equipo reconoce el fallo de la primera arquitectura.
4. "what we decided that we wanted to essentially decouple the brains from the hands." (05:41) El pivote de arquitectura.
5. "credentials never entered our sandbox." (07:04) Regla de seguridad de la arquitectura nueva.
6. "That way the model never sees your credentials or your tokens." (07:23) Por qué el proxy inyecta el token.
7. "we were able to bring down the TAM to force token by about 90%." (08:25) El efecto medido del cambio.
8. "harnesses encode assumptions and assumptions can go stale." (09:10) La lección central del capítulo de arquitectura.
9. "Outcomes is how we've created self-supervision." (32:07) Cómo se autosupervisa el agent.
10. "we've seen 10-hour sessions in production uh from some of our users." (55:51) La session más larga citada.
11. "garbage in garbage out." (79:55) La calidad del dato de evaluación.
12. "We are exploring the idea of what it means to do like budget tighter budget controls." (41:57) Estado del control de gasto por session.

## Preguntas abiertas

- ¿Cuántas sessions corren en producción y con qué distribución de duración? El vídeo no da la cifra.
- ¿Cómo se gradúan las tareas de los subagentes si no hay sub-outcome?
- ¿Cómo se evita que varios agents entren en bucle y gasten tokens sin control, si no hay presupuesto por session?
- ¿Cómo cambia el reparto entre harness grueso y skills gruesas cuando sale un modelo nuevo?
- ¿Cómo se mide el efecto real de dreaming si cada iteración puede ir en una dirección distinta?
- ¿Cuándo llega on-prem y con qué forma?
- ¿Cómo se resuelve el cuello de botella de revisar miles de PR generados por agents?
- ¿Qué proveedor es "Purcell" en la lista de sandboxes?

## Advertencias sobre la transcripción y los datos

Cada una de estas entradas se comprueba contra el `.txt` antes de escribirla.

- El audio nunca dice "Opus 5.5". El título del capítulo 2 lo dice, pero la pista dice "Opus 45" y "Opus 4". La lectura correcta es Opus 4.5. (01:49)
- El audio nunca dice "memory graphs". El título del capítulo 3 lo dice, pero la pista habla de "memory store". (30:54)
- "cloud", "claw" y "clock" aparecen por Claude. Ejemplos: "cloud managed agents", "claw console", "cloud tag", "clock in a box".
- "TAM to force token" significa time to first token. La bajada es de un 90 por ciento. (08:25)
- "map produce" significa map-reduce. (19:37)
- "cell supervision" significa self-supervision. (35:16)
- "edgger identifier" significa EDGAR identifier. (23:19)
- "arvback" y "arbback" significan RBAC. Aparecen a las 69:22 y a las 58:08.
- "onrem" significa on-prem. (84:52)
- "Moto" significa Modal. "EB2" significa E2B. (89:04)
- "Purcell" es un proveedor de sandbox no identificado. Candidato probable: Cloudflare. No verificado. (25:01)
- "Brianka" y "Bianca" son la misma persona. Las dos formas aparecen a las 25:26 y a las 26:13, y señalan a la primera ponente. (26:13)
- "Priyanka" aparece solo como nombre de ejemplo en un escenario de Slack. (89:43) No está probado que sea la misma persona que Brianka y Bianca. La identificación queda como inferida.
- "sonnet 45" y "opus 45" significan Sonnet 4.5 y Opus 4.5. (01:31 y 01:49)
- "sunet five" significa Sonnet five. La frase completa es "the android just released the sunet five". "android" significa Anthropic. (72:53)
- "sis calls" significa syscalls, llamadas al sistema. (03:58)
- "grap" significa grep. (13:07)
- "MVAR" significa env var, variable de entorno. (38:56)
- "entropic.com" significa anthropic.com. (39:01)
- "OOTH" y "ooth" significan OAuth. (39:35)
- "m.ample" y "m.local" significan .env.example y .env.local. (22:35)
- "buni" significa bun. (20:55)
- "heperagg" es un término no identificado, probablemente una librería de memoria con grafos. No verificado. (65:16)
- "Ant CLI" y "ANCLI"/"ANC" nombran la misma CLI. La forma exacta queda como no verificada. (76:18 y 76:39)
- "cloud code" y "claw console" nombran Claude Code y la consola de Claude. (02:28 y 66:50)
- "co-work" parece nombrar un producto de Claude para agents personales. La forma exacta queda como no verificada. (73:19)
- "SAS" significa SaaS. (68:40)
- La pista no tiene etiquetas de hablante. Las atribuciones de voz son inferidas por el contenido.
- El hablante dice "50" en "sonnet 45" y "opus 45". La puntuación decimal se pierde en la transcripción.
