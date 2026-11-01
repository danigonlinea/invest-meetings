---
title: "Cartera: cómo funciona esta carpeta"
date: 2026-11-01
type: reference
category: finance
tags: [cartera, indice, proceso]
status: living
---
# Cartera: cómo funciona esta carpeta

La cartera personal, dentro de `finance/`. El resto de material financiero (vídeos, webinars,
informes) está en las otras subcarpetas de `finance/`.

## Dos documentos vivos… más un anexo de investigación

| Fichero | Rol | ¿Se edita? |
| --- | --- | --- |
| `cartera-actual.md` | **Fotografía congelada** del estado real: saldos, pesos, ISIN, TER, TIR, duración, Rock y consolidado de 90.000 €. Fuente de verdad | **No.** Un cambio de saldos genera `cartera-actual-YYYY-MM-DD.md` |
| `propuesta-actual.md` | **La cartera vigente**: modelo que decide el % de RV, cartera final con ISIN e importes, órdenes, métricas, coste de la decisión, ejecución, diagnóstico y qué se descarta | **Sí**, es el documento de trabajo |
| `propuesta-alternativa.md` | **Anexo de investigación, no una cartera paralela**: dos carteras posibles sobre la vigente —mínima (REITs indexados al 0,17%, 5.000 €) y ampliada (10 fondos manuales: + Fundsmith 1,09% y Comgest Growth Europe 1,59%)— con pesos, financiación y ocho fuentes. Nace del barrido del catálogo MyInvestor del 01/11/2026 | **No mientras no se adopte.** Si se adopta, sus conclusiones pasan a `propuesta-actual.md` y el fichero **se borra** (`git rm`) |

El anexo existe porque el usuario pidió conservar la investigación con nombres, ISIN, TER y pesos; su
ciclo de vida es corto a propósito: **o se incorpora a la propuesta, o se descarta y desaparece**. Una
tercera cartera permanente volvería a dejar dos documentos con dos cifras de la misma cartera.

El diagnóstico, el veredicto frente a las fuentes y las revisiones adversariales **no viven en
ficheros aparte**: sus conclusiones están dentro de la propuesta (§2, §5, §7, §8) y el debate que las
produjo, en el historial de git. Un documento por rol evita las dos verdades: la carpeta llegó a tener
tres ficheros con cifras distintas de la misma cartera.

## Estado a 31/10/2026

- **Cartera:** 107.000 € totales = 10.000 € de colchón (Groupama, fuera de la cartera) + 97.000 €
  invertibles (67.000 € manuales, con 7.000 € de aportación nueva, + 30.000 € en Rock).
- **Situación de partida (90k):** 31,6% de renta variable, 68,4% de renta fija, 0,746% de TER y 17
  posiciones.
- **Propuesta (cerrada):** **50,0% de RV / 50,0% de RF**, 0,655% de TER y 17 posiciones. Emergentes al
  10%, dos fondos value (5.000 + 5.000) y small caps en 3.700. Mueve 25.000 € por traspaso (0 € de
  impuestos) + 7.000 € de aportación, en 11 órdenes y tres tandas. Caída esperada ≈ −21,5%.
- **Pendiente antes de la primera orden:** los **gastos mensuales** (el colchón de 10.000 € nunca se
  dimensionó contra un dato real) y confirmar que se aguanta el −21,5%. Comisiones verificadas el
  31/10: 0,00% de reembolso en los cinco fondos que salen; entrada 0,00% salvo el Neuberger («hasta
  3%», máx. 297 €). Falta ver en pantalla la comisión de la clase S de iShares EM.
- **Decisión abierta (anexo del 01/11):** si se añade el bloque de activos reales de
  `propuesta-alternativa.md` —iShares Developed Real Estate (IE00BDRK7P73, 0,17%)— y si la cartera se
  queda en la **versión mínima** (5.000 €, 17 posiciones, 632 €/año) o pasa a la **ampliada** (10 fondos
  manuales, con Fundsmith 3.000 € al 1,09% y Comgest Growth Europe 2.500 € al 1,59%; 19 posiciones,
  662 €/año, USA 37,6% de la RV). Antes de ejecutarlo hay que verificar el reembolso de Vanguard
  Small-Cap, Fidelity Europe, MyInvestor Value y Cobas, y la entrada de los tres fondos nuevos.

## Reglas de esta carpeta

- Un dato se escribe una vez: la foto en `cartera-actual.md`, la decisión y su porqué en
  `propuesta-actual.md`. Ningún fichero replica la tabla de posiciones del otro.
- Toda propuesta se ejecuta por **traspaso** entre fondos armonizados, nunca por reembolso.
- Nada se mueve sin verificar antes la clase del fondo y su coste real en la plataforma.
