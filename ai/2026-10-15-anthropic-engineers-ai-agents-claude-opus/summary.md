---
title: "Ingenieros de Anthropic: cómo se construyen los agentes de IA con Claude"
date: 2026-10-15
type: meeting-summary
category: ai
tags: [ai, meeting, transcript]
status: final
---

# Ingenieros de Anthropic: cómo se construyen los agentes de IA con Claude

- **Fecha:** 2026-10-15
- **Participantes:** Ingenieros de Anthropic (sin nombres identificados). Dos de ellos llevan el taller. Uno se llama Gabe. La otra voz se transcribe como "Brianka", "Bianca" y "Priyanka". La audiencia hace preguntas.
- **Canal:** Dev Docs Explained
- **Transcripción:** `invest-dev-docs-explained-anthropic-engineers-ai-agents-claude-opus.txt`
- **Duración:** 94 minutos 46 segundos
- **Temas:** Claude Managed Agents, agentes de IA, harness, contexto, skills, memoria, orquestación, dreaming, despliegues

> **Nota sobre la transcripción.** La transcripción viene de YouTube (pista automática, idioma inglés, formato json3). No incluye etiquetas de hablante porque el vídeo no las da. Toda la reunión se atribuye a `speaker-1`, una sola voz, aunque en realidad hablan varios ingenieros y la audiencia. El transcript conserva las marcas de tiempo y los errores de reconocimiento de voz, sobre todo en nombres propios y en términos técnicos. Las mayúsculas del párrafo anterior sobre los capítulos vienen de la descripción del vídeo, no del audio.

## Resumen ejecutivo

- Un agente es un modelo en un bucle con herramientas. El modelo decide, llama a herramientas y repite hasta terminar la tarea.
- Un harness es la capa que envuelve al modelo. Gestiona el contexto, ejecuta el bucle de herramientas y cubre lo que el modelo no puede hacer.
- El harness codifica suposiciones sobre el modelo. Las suposiciones caducan con cada modelo nuevo. Por eso Anthropic diseña interfaces que duran más que el harness.
- La primera arquitectura de Managed Agents metía todo en el contenedor. Produjo un "pet" difícil de depurar, con datos de cliente dentro.
- La segunda arquitectura separa el cerebro de las manos. La sesión es un registro de solo añadir, el harness es intercambiable y los sandboxes se crean bajo demanda.
- Las credenciales nunca entran en el sandbox. Un proxy inyecta el token en la salida, así que Claude nunca ve las credenciales.
- El cambio de arquitectura redujo el tiempo hasta el primer token en un 90 por ciento.
- El taller construye un agente que cuenta chistes, luego un desk de research con skills, subagentes, memoria compartida, outcomes y despliegues.
- Outcomes es el mecanismo de autosupervisión. El usuario define una tarea y una rúbrica. Un subagente verifica el resultado y el agente reintenta si falla.
- Dreaming es una vista previa de investigación. Analiza los transcripts y las memorias de varias sesiones y reescribe el memory store.
- Dreaming solo toca los memory stores hoy. Anthropic quiere extenderlo a skills, prompts y definiciones de agente.
- El consejo repetido es correr evaluaciones. Sin datos de calidad, un resultado del 100 por cien no significa nada.

## Temas tratados

### Introduction to Claude Managed Agents (00:00:00)

- La sesión empieza con la definición básica. Un agente es un modelo en un bucle con herramientas.
- El harness es una capa que envuelve al modelo y hace las llamadas a herramientas en bucle.
- El harness gestiona el contexto y encapsula todo lo que el modelo no puede hacer.
- Ejemplo citado. Sonnet 4.5 tenía "context anxiety". Cerca del límite de contexto intentaba cerrar la tarea rápido. El harness lo compensaba con un context reset.
- Opus 4.5 ya no tenía esa limitación, así que el context reset dejó de ser necesario. Esto muestra que las suposiciones del harness caducan.
- El agente necesita un sandbox o una computadora. Ahí ejecuta el código que escribe. Claude Code es un ejemplo de harness local.
- El código que escribe el agente no es de confianza. Puede tener errores. Hay que aislarlo en un contenedor y limitar el radio de daño.
- Recomendación: ejecutar cada tarea en un contenedor separado.
- Se anuncia el taller. La primera parte la da un ingeniero y la segunda parte la da Gabe.

### Opus 5.5 architecture (00:07:45)

- Este capítulo cubre la primera arquitectura de Managed Agents, enviada en diciembre del año anterior a los clientes de acceso anticipado.
- La primera arquitectura metía el session log, el harness y la ejecución del sandbox dentro del contenedor.
- La ventaja era no tener fronteras de servicio. Todo era local y fácil de editar.
- El problema fue el "pet". Un pet es una entidad con nombre y cuidada a mano. Si se rompe, no se puede perder.
- La depuración era difícil. Un paquete perdido y un contenedor muerto se veían igual. Había que entrar por websocket.
- La investigación era difícil porque los datos del cliente vivían en esos contenedores.
- Conectar un MCP en la VPC del cliente exigía emparejar redes o enviar el harness al cliente.
- La segunda arquitectura separa el agente en tres interfaces. Sesión, cerebro y manos.
- La sesión es un registro de solo añadir. El cerebro es el harness o bucle de agente con Claude. Las manos son sandboxes y llamadas a herramientas MCP.
- Cada componente pasó a ser "cattle", intercambiable. Si muere el sandbox, el harness lo vuelve a levantar. Si muere el harness, otro lee el event log y continúa.
- Solo el session log se protege. Todo lo demás se puede reemplazar.
- Las credenciales nunca entran en el sandbox. Un proxy inyecta el token justo antes de llamar al endpoint externo.
- El modelo nunca ve los tokens. Por eso no se puede inyectar un prompt que pida imprimir las credenciales.
- El event log de solo añadir permite una estrategia de compactación flexible. Nunca se descarta ningún evento.
- El tiempo hasta el primer token bajó alrededor de un 90 por ciento. Claude no espera a que arranque el contenedor.
- Un cerebro puede alcanzar muchas manos. El bucle puede llamar a un sandbox, a la VPC del cliente o a un servidor MCP.
- La lección del capítulo: los harness codifican suposiciones y las suposiciones caducan.

### Skills, loops and memory graphs (00:23:40)

- Gabe toma el relevo. La demo usa un repositorio llamado research desk.
- El taller se hace en seis actos y usa Claude Code como interfaz de programación.
- El primer acto crea una interfaz de chat. La sesión se comunica por un flujo de eventos y un endpoint.
- El flujo usa SSE. El servidor escucha los eventos del agente y los reenvía al navegador.
- El segundo acto convierte al agente en un ecosistema multiagente. El agente reparte tareas a subagentes.
- El agente recibe una skill para llamar a la web de la SEC y leer formularios por ticker.
- El agente recibe un custom tool llamado dispatch analysis para lanzar varias sesiones.
- El agente puede referenciarse a sí mismo. La copia hereda el prompt y los esquemas, pero no el transcript.
- El tercer acto lanza una tarea asíncrona larga. La tarea analiza un instrumento financiero y devuelve un informe.
- El mecanismo se llama outcomes. El usuario define la tarea, la rúbrica y el número máximo de iteraciones.
- Un subagente verifica el trabajo contra la rúbrica. Si no se cumple, el agente lo intenta otra vez.
- La demo analiza Nvidia y produce un fichero JSON de scorecard. También actualiza la memoria.
- La consola muestra cada subagente como un hilo. Los subagentes terminan y avisan al agente principal.
- El cuarto acto monta un harness propio de orquestación. Un agente principal reparte un ticker por sesión y agrega los resultados.
- Las skills son artefactos vivos. Se pueden editar y las sesiones nuevas recogen el cambio.
- El memory store es compartido entre sesiones. Los agentes aprenden de distintos instrumentos financieros.
- La demo usa un patrón de mapa y reduce para analizar Google y Microsoft a la vez.
- El quinto acto crea despliegues. Un despliegue ejecuta sesiones de un agente con un horario y unos mensajes iniciales.
- La pregunta sobre Vaults se responde en este capítulo. Un vault guarda secretos y los inyecta por dominio permitido.
- Los secretos se guardan como marcador. El valor real se cambia en la salida solo para los dominios autorizados.
- El commit de skills y agentes se puede hacer con Ant CLI y ficheros YAML, con estilo Terraform.

### Agent dreaming and orchestration (00:54:00)

- Dreaming es una vista previa de investigación. Es un experimento temprano.
- El usuario elige un memory store, un modelo y una ventana de tiempo, por ejemplo los últimos 30 días.
- Dreaming lanza una sesión con Managed Agents y varios subagentes. Cada uno analiza el transcript de otra sesión.
- Dreaming busca si el memory store guardó toda la información necesaria y si hubo problemas repetidos.
- En la demo, Dreaming detectó huecos en la skill creada y actualizó el memory store.
- Hoy Dreaming solo se limita a los memory stores. Anthropic quiere extenderlo a skills, prompts y definiciones de agente.
- Los despliegues son la forma de trabajo recurrente. Se define un agente, un horario y unos recursos.
- Los despliegues aceptan memory stores, repositorios de GitHub o ficheros en cada ejecución.
- La memoria persiste entre sesiones. El usuario elige qué memory store se adjunta a cada sesión.
- Se pueden adjuntar varios memory stores. Anthropic propone uno por usuario y otro por organización.
- Todo es API. El usuario puede sacar sus memorias y llevarlas a otro sistema.
- Los workspaces son la primitiva de separación. Un workspace agrupa agentes y da acceso a un grupo de personas.
- Anthropic reconoce que falta control de acceso por roles dentro del workspace. Está en la hoja de ruta.
- Se puede atender a varios clientes con un agente por cliente, un workspace por cliente o una organización por cliente.
- Hay un campo de metadatos en la sesión para mapear cada sesión con su cliente.
- Las sesiones largas se sostienen con la compactación. Se han visto sesiones de 10 horas en producción.
- El equipo recomienda correr evaluaciones propias. También usar las sesiones históricas como conjunto de datos.

### Reverse engineering (01:10:23)

- El título del capítulo viene de la descripción del vídeo. El audio no usa la expresión "reverse engineering".
- El tramo final es una ronda larga de preguntas y respuestas.
- Un asistente pregunta cómo desplegar el agente a escala. La respuesta: construir el producto propio y llamar a la API.
- Notion y Atlassian para Jira ya usan Managed Agents en producción.
- Otro asistente pregunta por la relación con Claude Code. La respuesta: es un harness propio, inspirado en el de Claude Code, pero genérico y no solo para código.
- Se aclara que no es "Claude en una caja". Es un producto de API e infraestructura.
- Un asistente pregunta por los modelos disponibles. De momento solo hay modelos de Claude.
- Un asistente pregunta por el aislamiento de clientes. La respuesta usa workspaces como primitiva.
- Un asistente pregunta por la revisión de código generado. Anthropic usa agentes que revisan las pull requests y buscan errores.
- Un asistente pregunta por la observabilidad. Se pueden exportar los eventos a un sistema propio, por ejemplo OTEL.
- Los agentes pueden correr en el sandbox y validar sus propios cambios. También se puede devolver un vídeo de la validación.
- Un asistente pide recursos de cómputo distintos, por ejemplo GPU. La respuesta: usar sandboxes autoalojados, como Modal.
- Anthropic no ofrece despliegue en instalaciones propias hoy. Lo está estudiando.
- La ronda termina con el aviso de que se acabó el tiempo y con el equipo disponible fuera de la sala.

## Cifras y datos citados

| Dato | Contexto |
|---|---|
| 90% | Reducción del tiempo hasta el primer token tras separar el cerebro de las manos |
| 4 | Modelo Opus 4 disponible en el ejemplo del agente que cuenta chistes |
| 4.5 | Versiones citadas como Sonnet 4.5 y Opus 4.5 (transcritas como "set 45" y "opus 45") |
| 3 | Interfaces del agente: sesión, cerebro y manos |
| 1 | Interfaz que se protege en la arquitectura nueva: el session log |
| 6 | Actos del taller (workshop) |
| 30 segundos | Espera del presentador antes de empezar el taller |
| 5 minutos | Tiempo que tarda en llegar el crédito de API, aunque el formulario diga uno o dos días |
| 10 mensajes | Mensajes que se pueden poner en cola para dirigir al agente |
| 10 | Tickers que un agente principal puede repartir en sesiones separadas |
| 100 | Tickers citados en la pregunta sobre analizar 100 valores a la vez |
| 10.000 | Sesiones y pods que Anthropic lanza en paralelo para sus evaluaciones |
| 10 horas | Duración de sesiones vistas en producción |
| 6 meses | Ejemplo de tarea diaria que el agente puede sostener sin desbordar la persistencia |
| 30 días | Ventana de sesiones que Dreaming analiza en la demo |
| 90 segundos | Ejemplo de una interpretación de subagente lanzada desde una interfaz propia |
| 400 | Código de error si se envía un mensaje mientras el agente espera un custom tool result |
| 100% | Puntuación de una evaluación mal definida según el equipo, y por qué no sirve |
| 9:00 am | Ejemplo de horario diario para un despliegue |
| 1 pm | Ejemplo de horario mensual para un despliegue el primer día del mes |
| 2026-10-15 | Fecha de subida del vídeo |
| 5686 | Duración del vídeo en segundos |
| 77 | Número de chunks del transcript |
| 2534 | Número de segmentos del transcript |

## Ideas y tesis

- **Ingeniera de Anthropic (nombre no identificado; atribución inferida del audio).** Un agente es un modelo en un bucle con herramientas. Esa es la definición mínima.
- **Ingeniera de Anthropic (atribución inferida).** El harness codifica suposiciones sobre el modelo. Las suposiciones caducan con cada modelo nuevo.
- **Ingeniera de Anthropic (atribución inferida).** Las interfaces deben durar más que el harness. Por eso el harness se puede cambiar sin tocar la arquitectura.
- **Ingeniera de Anthropic (atribución inferida).** Separar el cerebro de las manos convierte cada componente en algo intercambiable.
- **Ingeniera de Anthropic (atribución inferida).** Las credenciales no deben entrar nunca en el sandbox. Así no se pueden filtrar con un prompt injection.
- **Gabe (ingeniero de Anthropic; el nombre sale en el transcript, el resto de atribuciones es inferida).** Un registro de solo añadir permite cambiar la estrategia de compactación sin perder datos.
- **Gabe (atribución inferida).** Las skills son artefactos vivos. Se pueden mejorar y las sesiones nuevas recogen el cambio.
- **Gabe (atribución inferida).** Outcomes da autosupervisión. Un subagente revisa la rúbrica y el agente reintenta hasta cumplirla.
- **Gabe (atribución inferida).** El memory store es conocimiento compartido entre sesiones. Se pueden adjuntar varios.
- **Gabe (atribución inferida).** Dreaming reescribe el memory store a partir de los transcripts. De momento solo cubre memoria.
- **Gabe (atribución inferida).** Los despliegues son la forma de trabajo recurrente, con horario y recursos declarados.
- **Ingeniero de Anthropic (atribución inferida).** Managed Agents no es Claude Code metido en una caja. Es un harness propio para tareas generales.
- **Ingeniero de Anthropic (atribución inferida).** Los workspaces son la primitiva de separación. Falta control de acceso por roles.
- **Ingeniero de Anthropic (atribución inferida).** El consejo repetido es correr evaluaciones. Un 100 por cien sin buenos datos no significa nada.
- **Ingeniero de Anthropic (atribución inferida).** A medida que el modelo mejora, los límites y la ayuda del harness se desvanecen. El andamiaje de hoy no es el de mañana.
- **Asistente de la audiencia (atribución inferida).** La duda abierta es si un harness propio gana a una skill. El equipo responde que depende de la tarea.

## Preguntas abiertas y temas pendientes

- No hay rewind ni roll forward de una sesión. La bifurcación de sesión está en la hoja de ruta y sin fecha.
- No existe presupuesto por sesión ni límite de tokens por sesión. Anthropic lo estudia, pero no lo ofrece hoy.
- No hay definición de outcome por subagente. La rúbrica vive a nivel de sesión completa.
- Dreaming sigue en vista previa de investigación. Su efecto final sobre el resultado se mide con evaluaciones externas.
- No hay control de acceso por roles dentro de un workspace. Solo existe la separación por workspace.
- No hay permisos finos para compartir un recurso en parte. El recurso se comparte entero dentro del workspace.
- No hay despliegue en instalaciones propias. Anthropic lo está considerando sin fecha.
- Los sandboxes que ofrece Anthropic son todos iguales. Para GPU o más memoria hay que usar un proveedor externo.
- No hay herramienta de túneles para inspeccionar la interfaz del agente desde fuera.
- No hay todavía un flujo gráfico de topología de agentes. El equipo dice "todavía no".
- No se aclara el provider transcrito como "Purcell", ni el término transcrito como "heperagg".
- No se da cifra de uplift de Dreaming. Solo se dice que hay mejoras en clientes.
- La revisión del código que generan los agentes queda como pregunta abierta. Anthropic dice que sigue explorando.

## Citas textuales

- "agent is basically uh a model in a loop with tools" — definición inicial del agente (00:00:00).
- "Harness is typically like a layer that wraps around the model that helps you make these tool calls in a loop to get you the outcome for the task" — definición de harness (00:00:00).
- "our set 45 model had something what we called uh context anxiety" — ejemplo de limitación del modelo que el harness compensaba (00:00:00).
- "we decided that we wanted to essentially decouple the brains from the hands" — cambio de arquitectura (00:04:46).
- "credentials never entered our sandbox" — regla de seguridad de la arquitectura nueva (00:07:04).
- "we were able to bring down the TAM to force token by about 90%" — mejora del tiempo hasta el primer token; la expresión correcta es "time to first token" (00:08:12).
- "harnesses encode assumptions and assumptions can go stale" — lección central del capítulo de arquitectura (00:08:12).
- "one brain can reach many hands" — descripción de las manos intercambiables (00:08:12).
- "I don't think anybody's writing code by hand" — Gabe, al explicar que usa un agente de código (00:19:01, atribución inferida).
- "Outcomes is how we've created self-supervision" — mecanismo de autosupervisión (00:30:54).
- "you can send that 10 messages at a time and it's fine" — mensajes en cola para dirigir al agente (00:42:03).
- "We don't currently have a way for like rewind and roll forward" — respuesta sobre corregir el historial (00:42:03).
- "session forking is essentially what you're asking for" — función en la hoja de ruta (00:42:03).
- "today the dreaming is constrained to uh memory stores" — alcance actual de Dreaming (00:45:28).
- "We we are running compaction for you so that you can run these for days" — sesiones largas (00:55:18).
- "We've seen 10-hour sessions in production uh from some of our users" — duración real vista (00:55:18).
- "the main thread is idle while the sub agents were doing work" — patrón de coordinación (01:29:17, atribución inferida).
- "The boring answer is just run evals and and evaluate these things" — respuesta sobre harness grueso o fino (01:01:15).
- "not just clock in a box" — comparación con Claude Code; el audio dice "clock" por Claude (01:04:56).
- "garbage in garbage out" — consejo sobre datos para evaluaciones (01:19:45).
- "yeah it's cloud models only for now" — restricción de modelos (01:10:23, atribución inferida).
- "we're not supporting onrem" — respuesta sobre instalación propia; el audio dice "onrem" por on-prem (01:24:27).
- "let claude just let it cook" — sobre quitar restricciones al agente (01:29:17, atribución inferida).

## Advertencias sobre la transcripción

La transcripción es automática. Tiene errores de reconocimiento de voz. Los más relevantes:

- "cloud" es "Claude". Aparece en todo el texto. Ejemplos: "cloud managed agents" es Claude Managed Agents; "cloud code" es Claude Code; "cloud platform" es la plataforma de Claude.
- "claw" y "clock" también son "Claude". "platform.claw.com" es platform.claude.com. "not just clock in a box" es "not just Claude in a box".
- "set 45" y "sonnet 45" son Sonnet 4.5. "opus 45" y "Opus45" son Opus 4.5.
- "sunet five" es Sonnet 5. El tramo "the android just released the sunet five" atribuye el lanzamiento a Android. Por contexto, el emisor es Anthropic. La frase correcta es "Anthropic just released Sonnet 5".
- "grap" es grep. El tramo es "read, write, grap, etc.".
- "sis calls" es syscalls. El tramo es "File edits were essentially just like sis calls.".
- "appendon" es append-only. Aparece como "appendon log" y "appendon session log".
- "TAM to force token" es "time to first token". El tramo es "we were able to bring down the TAM to force token by about 90%".
- "m.ample file" es `.env.example`. "amp.local" y "m.local" son `.env.local`.
- "buni" es bun. El tramo es "run npm install or buni". "bun rundev" es `bun run dev`.
- "edgger identifier" es EDGAR identifier. "Edgar identities" es EDGAR identity.
- "mpm package" es npm package. El tramo es "you have to pick mpm package".
- "entropic.com" es anthropic.com. El tramo es "cloud tries to use it for entropic.com".
- "oth" y "OOTH" son OAuth. El tramo es "ooth credentials for piece". La palabra "piece" no se identifica.
- "arbback" y "arvback" son RBAC. Significa control de acceso por roles.
- "onrem" es on-prem. Significa instalación propia del cliente.
- "multi-tenency" es multi-tenancy.
- "aent" y "aents" son agent y agents. Aparecen como "multi- aent", "sub aents" y "sub aentic".
- "map produce" es map-reduce. El tramo habla de un patrón de reparto y agregación.
- "cell supervision" y "self-s supervision" son self-supervision.
- "thick hardness, thin harness, thick skills" contiene un error. Por contexto, es "thick harness, thin harness, thick skills".
- "MVAR" es env var. El tramo es "my super secret MVAR".
- "Moto" es Modal y "EB2" es E2B. Son proveedores de sandbox citados como "Moto or EB2, Daytona".
- "Purcell" no se identifica. Aparece en la lista de proveedores de sandbox junto a Modal y Daytona.
- "heperagg" no se identifica. El tramo es "experiment with things like uh heperagg" sobre memorias.
- "oneP offering" no se identifica. El tramo es "we have like a oneP offering uh that we run on".
- "cloud tag" y "cloud co-work" no se identifican del todo. Parecen nombres de productos de Claude. "co-work" aparece también como "cowork" y "co-work".
- "oh pager duty" es un artefacto de reconocimiento. Se cuela al final de una frase sobre la nueva versión del agente.
- "Brianka", "Bianca" y "Priyanka" son la misma persona. La transcripción escribe su nombre de tres formas en tres momentos distintos.
- Los nombres Gabe, Travis y Rohan aparecen una vez cada uno. Son personas reales del taller.
- Los títulos de los capítulos son de la descripción del vídeo. El audio nunca dice "Opus 5.5", "memory graphs" ni "reverse engineering". La búsqueda de "5.5" en el transcript da cero resultados. El único modelo con versión citada en el audio es el 4 y el 4.5.
- "Nvidia", "Google" y "Microsoft" son solo ejemplos de tickers de la demo técnica. No hay datos de inversión.
- Esta sección de fondos y acciones no aplica. La reunión es una charla técnica de IA. Las empresas citadas son contexto de una demo, no una recomendación de inversión.
