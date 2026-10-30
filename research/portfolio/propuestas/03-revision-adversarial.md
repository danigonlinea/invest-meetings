---
title: "Revisión adversarial — propuesta B (consolidada agresiva)"
date: 2026-10-30
type: portfolio-review
category: finance
tags: [cartera, fondos, rebalanceo, adversarial, rock, myinvestor]
status: final
related: [research/portfolio/propuestas/02-propuesta-consolidada-100k.md, research/portfolio/cartera-actual.md]
---

# Revisión adversarial — 30/10/2026

> Ataque a la propuesta B (`02-propuesta-consolidada-100k.md`) y a la cartera de partida. Los
> hallazgos de §3 y §7 son los que gobiernan la propuesta A (`01-propuesta-moderada-90k.md`).

**Objeto:** atacar (no describir) la cartera actual de 70.000 € (9 fondos) y la propuesta del
documento `02-propuesta-consolidada-100k.md` (70.000 € manuales + 30.000 € en Rock de MyInvestor).
**Datos:** fichas MyInvestor MCP a 28/10/2026 (TER, rentabilidades, volatilidad, allocation,
top países/sectores) + factsheets 30/09/2026 para TIR/duración + macro del audit (BCE 2,50%,
inflación 3,8%, €STR 2,44%).

---

## 1. Veredicto en una línea

La propuesta acierta el diagnóstico (hay demasiada liquidez para un horizonte largo) y se
equivoca en la justificación: **vende un ahorro de costes de 453 €/año cuando lo que en
realidad hace es mover 43.000 € de renta fija a bolsa, con la bolsa en máximos y el propio
documento describiendo un entorno de riesgo elevado**. Y la ejecución, tal como está escrita
("vender"), cuesta ~2.600 € en impuestos que un traspaso evitaría.

---

## 2. Ataque a la cartera actual (70.000 €)

| ISIN | Fondo | € | TER | 3a anual | 1a | Vol 3a |
|---|---|---:|---:|---:|---:|---:|
| IE00BL1GVT98 | Neuberger Short Duration Euro Bond U | 22.000 | 0,38% | +4,38% | −0,16% | 1,93% |
| LU1694789451 | DNCA Alpha Bonds A | 13.000 | 1,31% | +4,12% | +1,95% | 2,00% |
| LU1623762843 | Carmignac Credit A | 12.000 | 1,20% | +6,31% | −1,69% | 3,62% |
| FR0000989626 | Groupama Trésorerie IC | 10.000 | 0,07% | +2,98% | +2,21% | 0,26% |
| ES0140794001 | Gamma Global A | 8.000 | 0,95% | +9,10% | +6,93% | 2,28% |
| ES0165243025 | MyInvestor Value C | 2.000 | n/p (+9% éxito) | n/a | +17,69% | 17,76% (1a) |
| LU1598719752 | Cobas International P | 1.000 | **2,33%** | +26,38% | +28,41% | 12,34% |
| IE00018YKVN0 | NB Next Gen Space Economy | 1.000 | **1,90%** | n/a | +2,64% | 35,75% (1a) |
| LU1815002040 | UBS MSCI China All Shares | 1.000 | 0,30% | +6,88% | −12,48% | 19,31% |

**TER ponderado real 0,793% → 555 €/año.** (El audit decía 0,774%; la diferencia está en
TERs mal tomados: Cobas 1,73% vs **2,33%** real, Space 1,72% vs **1,90%**, Groupama 0,16% vs
**0,07%**, Gamma 0,86% vs **0,95%**, NB 0,36% vs **0,38%**).

### 2.1 Lo indefendible

1. **81,4% en RF/monetario con rendimiento real negativo** (€STR 2,44% vs inflación 3,8%):
   cada año que pasa cuesta ~1,4% sobre 57.000 € = **~800 €/año de poder adquisitivo**.
   Diagnóstico correcto, sin discusión.
2. **Gamma Global no es un mixto defensivo, es un fondo de bonos basura concentrado**: 8.000 €,
   81% bonos corporativos, 70 emisores, energía/GNL/shipping, Ghana y Grecia en el top-6 de
   países, y un 61% de "futuros/forward" en la allocation. Con TIR 8,07% y duración 2,16 es
   rentable, pero el riesgo de emisor concreto no está diversificado. 8.000 € es demasiado.
3. **DNCA cobra 1,31% + 20% de éxito por un +4,12% anual a 3 años** y mantiene 29% en liquidez.
   Pagas comisión de gestión activa por un fondo que en la práctica es deuda pública con caja.
4. **Cobas: 1.000 € a TER 2,33%** (el más caro de la cartera) y entra en soft close: no se puede
   ampliar. Es una posición testimonial que no aporta y no escala.
5. **Space Economy: 1.000 €, TER 1,90%, volatilidad 35,7%, SRRI 5.** El 1,4% de la cartera con
   el 25% del riesgo. Peor: la ficha declara geografía "USA" y 58% USA / 44% industria.
6. **Cuatro posiciones ≤2.000 € (7,1% del dinero, 44% de las líneas)**: ruido operativo.
7. **La columna "3a" del audit mezcla anualizado y acumulado**: Cobas +101,87% y UBS +22,60%
   son acumulados, no anualizados (reales: **+26,4%** y **+6,9%** anual). Cualquier decisión
   tomada sobre esa tabla está sesgada a favor de Cobas y de China.

### 2.2 Lo que el audit ataca injustamente

- **Neuberger no es "exceso de liquidez"**: 22.000 €, duración 1,95, TIR 4,65% (YTW), rating
  medio A−, 0,38% de TER, 5★. Es el mejor carry/riesgo de toda la cartera y de toda la
  propuesta. Venderlo es el peor movimiento del plan (ver §3.2).
- **Carmignac a 3 años hace +6,31% con duración 4,0 y TIR 6,5%.** Su YTD es −2,0% y su 2022 fue
  −13,0%, sí, pero se le exige el comportamiento de un monetario a un fondo de crédito HY.
- **Groupama a 0,07% de TER no tiene nada que arreglar.** Es la liquidez más barata disponible.

---

## 3. Ataque a la propuesta

### 3.1 La tabla final no cuadra (errores verificados)

| Afirmación del documento | Realidad (suma de sus propias filas) |
|---|---|
| RV 67.000 € / 67,0% | **63.400 € / 63,4%** |
| RF + monetario 33.000 € / 33,0% | **35.600 € / 35,6%** |
| TOTAL 100.000 € | **99.000 €** |
| "USA ~14% del total" | **33,4% del total** (52,7% de la RV) |
| "duración media ~4,5 años" | **5,0 años** con la RF propuesta (hoy: 2,5) |
| "TER ponderado ~0,27%" | 0,225% con las fichas MCP (menor, no mayor) |

La fila que falta es **Cobas International (1.000 €)**: se mantiene en la fase 1 y desaparece de
la asignación final. Los 1.000 € que faltan son exactamente eso.

### 3.2 El "ahorro de costes" es 453 €/año. Los costes no son el argumento

- Manual: 555 €/año (0,793%) → 102 €/año (0,145%) = **−453 €/año**.
- Cartera completa: 678 €/año → 225 €/año = **−0,45% de 100.000 €**.
- Ese es todo el premio. 38 €/mes. No justifica una reestructuración de 65.000 €.

Y lo que se entrega a cambio en la parte de RF:

| Fondo vendido | Importe | TIR/YTW | Carry |
|---|---:|---:|---:|
| NB Ultra Short | 22.000 | 4,65% | 1.023 €/año |
| Carmignac Credit | 12.000 | 6,50% | 780 €/año |
| Gamma Global | 8.000 | 8,07% | 646 €/año |
| DNCA Alpha Bonds | 13.000 | 3,97% | 516 €/año |
| Groupama Trésorerie | 10.000 | 3,00% | 300 €/año |
| **Total vendido** | **65.000** | **5,02%** | **3.265 €/año** |

| Fondo comprado | Importe | Rend. esperado | Carry |
|---|---:|---:|---:|
| iShares Global Agg 1-5Y EUR H | 10.000 | ~1,5–2,0% | 180 €/año |
| iShares Euro Credit | 7.000 | ~3,4% | 238 €/año |
| iShares Euro Gov Inflation-Linked | 5.000 | ~0,5% real | 25 €/año |
| **Total RF nueva** | **22.000** | **~2,0%** | **443 €/año** |

El resto (43.000 €) va a bolsa, y ahí sí hay retorno esperado (earnings yield ~5,3% sobre el
MSCI World a 18,7x). **Conclusión: el plan no es de reducción de costes, es de subida de RV.
Presentarlo como lo primero es lo que lo hace malo, porque oculta la decisión que sí importa.**

### 3.3 Los tres fondos nuevos de RF son un downgrade, no una mejora

1. **iShares Global Agg 1-5Y EUR Hedged (10.000 €): +0,03% a 1 año.** Es deuda global a 1-5 años
   con 36% USA y 12,5% China, cubierta a EUR. El coste de cobertura de USD a EUR se come
   íntegro el cupón (diferencial de tipos ~2%). Resultado: rinde como un monetario euro pero
   con riesgo de crédito soberano de EEUU y China. Frente al 4,65% del Neuberger que sustituye,
   son **~2,9 pp menos de carry sobre 10.000 €**.
2. **iShares Euro Gov Inflation-Linked (5.000 €): −0,88% a 12 meses, −0,92% anual a 5 años.**
   Duración real ~7,6 años. Es el activo más largo de la cartera manual nueva, y se compra
   justo cuando el documento dice "no alargar duración" y advierte de que el BCE puede subir
   en diciembre. Como seguro contra inflación tiene sentido; como "mejora" de rentabilidad, no.
3. **iShares Euro Credit (7.000 €): −1,58% a 12 meses, −1,14% anual a 5 años.** Rinde ~3,4%
   frente al 6,5% de TIR del Carmignac que sustituye. Se gana calidad crediticia (IG vs BBB−),
   eso es cierto, pero se paga con ~3 pp de rentabilidad esperada sobre 12.000 €.

**La duración no baja: sube.** RF actual 2,5 años → RF propuesta 5,0 años. Con +100 pb de tipos,
el impacto pasa de −1.012 € a −1.766 €. El documento afirma que la RF corta "compensa" la
duración larga de Rock (20+ años); lo que hace en realidad es **doblar la duración media**.

### 3.4 El "hueco de RV global" no existe: ya está cubierto por Rock

Rock tiene 15.900 € en large cap desarrollado (S&P 500 9.900 + Vanguard US 600 + Europa 2.100 +
Japón 2.700 + Pacífico 600). El MSCI World son las mismas 1.300 empresas, con 72% en USA.

**Comprar 23.000 € de MSCI World añade 0 € de exposición nueva a compañías.** No es un hueco,
es una reponderación. La frase "RV Global: 0 € ⚠️ hueco crítico" del documento confunde
"no hay un fondo llamado World" con "no hay exposición".

Consecuencia real de la propuesta, calculada por look-through:

| Región | % de la cartera | % de la RV | Referencia ACWI |
|---|---:|---:|---:|
| USA | 33,4% | 52,7% | 63% |
| Europa | 16,8% | 26,5% | 15% |
| Japón | 5,0% | 7,9% | 5% |
| Emergentes | 4,3% | 6,8% | 10% |

Dos consecuencias que contradicen al documento: (a) el sesgo no es "USA 14%", es USA 33% y
**Europa sobreponderada 11 pp**; (b) **emergentes queda infraponderada al 6,8% de la RV**
—justo el bloque que mejor lo ha hecho (iShares EM: +20,5% anual a 3 años, +21,1% YTD)—
mientras el documento dice "no comprar más EM porque Rock ya tiene".

### 3.5 Ejecución: "vender" cuesta ~2.600 € que no hace falta pagar

La fase 1 dice "vender" 65.000 €. En España, **traspaso entre fondos armonizados no tributa**;
reembolso sí. Con una plusvalía latente del 20% (13.000 €), el hachazo es ~2.610 €
(19% hasta 6.000 + 21% hasta 50.000). Todos los fondos implicados son UCITS armonizados: se
puede traspasar sin pasar por caja. **Es un error de redacción con coste real.**

Además, dos importes a verificar antes de mover nada: Groupama Trésorerie declara hasta **4% de
reembolso**, y Neuberger hasta **3% de suscripción**. En MyInvestor suelen ser 0, pero si no lo
son, el plan se come el ahorro de 10 años de comisiones en una sola operación.

### 3.6 Complejidad: 19 posiciones para un patrimonio de 100.000 €

Manual final: 10 fondos (23.000 + 10.000 + 7.000 + 7.000 + 5.000 ×4 + 1.000 ×3 con Cobas) +
Rock 9 fondos = **19 líneas**, de las cuales 5 por debajo de 2.000 €. Para 100.000 €, 5–8 fondos
cubren el 95% de la diversificación. La propuesta añade 9 fondos nuevos y mantiene los 4
satélites de 1.000 € "para valorar".

---

## 4. Lo que la propuesta acierta (steelman)

- **El problema es la liquidez, no los fondos.** 81,4% en RF/caja con tipos reales negativos es
  el único error grave de la cartera actual. Eso está bien visto.
- **Bajar Gamma de 8.000 € es correcto** por concentración de emisor, no por TER.
- **Consolidar 4 monetarios/crédito en 1–2 vehículos** simplifica de verdad.
- **No tocar Rock es la decisión correcta:** 0,41% todo incluido (TER 0,11% + custodia 0,15% +
  gestión 0,15%) por 9 fondos indexados es difícil de batir comprando por separado. Su
  track record (+83,44% desde 24/06/2020, 10,1% anualizado) y sus 2022 (−15,5%) vs índice
  (−13,2%) son coherentes con un 78/22.
- **Los fondos indexados elegidos son los correctos** (TER 0,06–0,12%). El problema no son los
  fondos, es la dosis y el momento.

---

## 5. Las tres decisiones que faltan (y que cambian el veredicto)

1. **¿Cuánto de esos 100.000 € es fondo de emergencia?** El plan deja 7.000 € en monetario
   (7%). Si el colchón de 3–6 meses de gastos tiene que salir de ahí, el plan es inviable tal
   cual: el monetario se queda fuera de la cartera y se dimensiona por gastos, no por porcentaje.
2. **¿Perfil y horizonte?** El audit fija objetivo 40–50% RV ("conservador-moderado"); la
   propuesta ejecuta 63–67% RV (perfil agresivo, "mínimo 6 años" como Rock). Son dos carteras
   distintas y el documento usa la etiqueta de una con los números de la otra.
3. **¿Se tolera una caída del −25/−30%?** Con 63% RV, un 2008 replica da ≈ −28%. Hoy la cartera
   caería ~−10%. **El plan multiplica por 3,4 el riesgo de mercado.** Si la respuesta no es un
   sí sin matices, el 67% no es la cartera.
4. (Operativa) **¿Los importes siguen siendo 70k/30k?** Los cálculos están hechos sobre los
   saldos del 30/10.

---

## 6. Alternativas con importes exactos

### Opción A — Conservador-moderado (coherente con el audit: RV 45%)

Sin duplicar nada, sin alargar duración, sin tocar Rock, sin ILB ni Global Agg.

| Bloque | Fondo / ISIN | € | TIR/rend. |
|---|---|---:|---:|
| Monetario (colchón, fuera del cálculo de RV) | AXA Trésor Court Terme · FR0000447823 (0,05%) | 10.000 | 2,44% |
| RF corta IG | Neuberger Short Duration · IE00BL1GVT98 (0,38%) | 22.000 | 4,65% |
| RF flexible govt | DNCA Alpha Bonds · LU1694789451 (1,31%) | 10.000 | 3,97% |
| Crédito | Carmignac Credit · LU1623762843 (1,20%) | 8.000 | 6,50% |
| Crédito HY (recortado) | Gamma Global · ES0140794001 (0,95%) | 5.000 | 8,07% |
| RV emergentes | iShares EM clase S · IE000QAZP7L2 (0,16%) | 5.000 | — |
| RV small cap | Vanguard Global Small-Cap · IE00B42W4L06 (0,29%) | 4.000 | — |
| RV value Europa | MyInvestor Value · ES0165243025 (+9% éxito) | 6.000 | — |
| | **Total manual** | **70.000** | |
| Rock | sin cambios | 30.000 | |

**Movimientos exactos (23.000 € de origen, todo por traspaso):**

| Origen | € | Destino |
|---|---:|---|
| DNCA (13.000 → 10.000) | 3.000 | AXA Trésor |
| Carmignac (12.000 → 8.000) | 4.000 | AXA Trésor |
| Gamma (8.000 → 5.000) | 3.000 | AXA Trésor |
| Groupama (10.000 → 0) | 10.000 | AXA Trésor |
| Cobas (1.000 → 0) | 1.000 | iShares EM |
| Space (1.000 → 0) | 1.000 | Vanguard Small Cap |
| China (1.000 → 0) | 1.000 | iShares EM |

Resultado: **RV 15.000 manual + 23.400 Rock = 38.400 € = 38,4% del total (42,7% del capital
invertible si los 10.000 de monetario son el colchón) · RF 45.000 € · monetario 10.000 € ·
duración RF ~2,6 años · 8 fondos manuales + 9 de Rock.**

Contrapartida honesta: **el TER apenas baja, de 0,793% a ~0,67% (555 → 470 €/año)**, porque se
mantiene el carry. Ese es el precio de no regalar rentabilidad: esta opción no es una mejora de
costes, es una mejora de asignación. Si lo que se quiere es bajar el TER un 70%, hay que aceptar
el 63% de RV de la propuesta y su drawdown del −28%.

### Opción B — Agresivo (RV 65%), pero por etapas y sin disfrazarlo de ahorro

Aquí el MSCI World **sí** hace falta (Rock solo aporta 23.400 € de RV; para llegar a 65.000 hay
que duplicar, y duplicar con un índice barato es la forma correcta de hacerlo). Lo que cambia:

- Entrada **escalonada en 9–12 meses**, no de golpe, con S&P 500 a 18,7x fwd y el propio audit
  describiendo "concentración IA", HY en "flashing yellow" y BCE con sesgo restrictivo.
- Nada de Global Agg 1-5Y EUR H ni ILB: **22.000 € se quedan en Neuberger (4,65%) en lugar de
  ~2%**. Eso son ~580 €/año de carry que se regalan sin comprar diversificación real.
- Mantener como mínimo Carmignac 6.000 y Gamma 5.000: son las únicas posiciones con TIR >6,5%.
- Sin satélites de 1.000 €: China y Space fuera (China ya está dentro de EM al 19%).
- Asumir por escrito: drawdown esperado −28%, 2022 habría sido −20/−22% en vez de −15,5%.

---

## 7. Resumen de hallazgos

| # | Hallazgo | Severidad |
|---|---|---|
| 1 | La tabla final suma 99.000 € y omite Cobas; RV real 63,4%, no 67% | Alta |
| 2 | El ahorro justificado es 453 €/año; el cambio real es +43.000 € de RV | Alta |
| 3 | "Vender" en vez de "traspasar": ~2.610 € de impuestos evitables | Alta |
| 4 | El "hueco de RV global" no existe: MSCI World = mismo large cap que Rock | Alta |
| 5 | La duración de la RF sube de 2,5 a 5,0 años, contra su propia tesis | Alta |
| 6 | 22.000 € a Global Agg 1-5Y H (≈2%) sustituyen 22.000 € a 4,65% | Alta |
| 7 | "USA ~14%" vs 33,4% real; Europa 26,5% de la RV; EM 6,8% | Media |
| 8 | 19 posiciones y 5 microlíneas para 100.000 € | Media |
| 9 | TER mal tomados en el audit (Cobas 2,33% vs 1,73%) y columna 3a mezclada | Media |
| 10 | Groupama 4% reembolso / NB 3% suscripción sin verificar antes de operar | Media |
| 11 | Falta el fondo de emergencia en todo el análisis | Alta |

---

## 8. Fuentes

- MyInvestor MCP (`get_funds`, `search_portfolios`, 28/10/2026): TER, rentabilidades YTD/1A/3A/5A,
  volatilidad, allocation, top países/sectores, comisiones de éxito, soft-close.
- `search_portfolios`: Rock — composición, 78/22, comisión 0,11+0,15+0,15, serie anual 2008-2026.
- Factsheets 30/09/2026 vía audit: TIR/YTW, duración modificada, rating medio, max drawdown.
- Fiscalidad española: traspaso entre fondos armonizados no tributa (LIRPF); tramos del ahorro
  19/21/23/27/30 aplicados al reembolso.
