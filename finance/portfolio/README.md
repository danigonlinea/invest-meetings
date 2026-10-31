---
title: "Cartera: cómo funciona esta carpeta"
date: 2026-10-31
type: reference
category: finance
tags: [cartera, indice, proceso]
status: living
---
# Cartera: cómo funciona esta carpeta

La cartera personal, dentro de `finance/`. El resto de material financiero (vídeos, webinars,
informes) está en las otras subcarpetas de `finance/`.

## Los cuatro documentos

| Fichero | Rol | ¿Se edita? |
| --- | --- | --- |
| `cartera-actual.md` | **Fotografía congelada** del estado real: saldos, pesos, TER, TIR, Rock y consolidado de 90.000 €. Fuente de verdad | **No.** Un cambio de saldos genera `cartera-actual-YYYY-MM-DD.md` |
| `diagnostico-2026-10-30.md` | **Qué está bien y qué está mal**: características de cada fondo, costes, fortalezas, debilidades, macro y criterios de decisión | Solo si cambia el diagnóstico |
| `propuesta-actual.md` | **La cartera vigente**: modelo que decide el % de RV, cartera final, movimientos exactos, métricas, coste de la decisión, ejecución y cuándo se recalcula | Sí, es el documento de trabajo |
| `analisis/videos-2026-10-30.md` | **Veredicto posición por posición** frente a lo que dicen las fuentes y lo que no justifican | Solo al añadir fuentes nuevas |

`archivo/` guarda lo descartado: la propuesta agresiva de 63% de RV y la revisión adversarial que la
tumbó. No hace falta leerlo para decidir; es la trazabilidad de por qué la propuesta actual es la que
es.

## Estado a 31/10/2026

- **Cartera:** 100.000 € totales = 10.000 € de colchón (Groupama, fuera de la cartera) + 90.000 €
  invertibles (60.000 € manuales + 30.000 € en Rock).
- **Situación:** 31,6% de renta variable, 68,4% de renta fija, 0,746% de TER y 17 posiciones.
- **Propuesta:** **54,9% de RV / 45,1% de RF**, 0,521% de TER y 16 posiciones, moviendo 26.000 € por
  traspaso (0 € de impuestos). Caída esperada ≈ −23% en un escenario tipo 2008.
- **Pendiente de decidir:** confirmar que se aguanta el −23% (si no, el modelo baja a 45% o 35%) y
  verificar comisiones de suscripción/reembolso y el TER real de MyInvestor Value C. **Sin órdenes de
  traspaso hasta entonces.**

## Reglas de esta carpeta

- Un dato se escribe una vez: la foto va en `cartera-actual.md`, el juicio en `diagnostico`, la
  decisión en `propuesta-actual`.
- Toda propuesta se ejecuta por **traspaso** entre fondos armonizados, nunca por reembolso.
- Nada se mueve sin verificar antes la clase del fondo y su coste real en la plataforma.
