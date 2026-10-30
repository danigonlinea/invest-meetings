---
title: "Propuesta B — consolidada agresiva (100k, RV 63%)"
date: 2026-10-30
type: portfolio-proposal
category: finance
tags: [cartera, propuesta, rebalanceo, rock, agresivo, myinvestor]
status: con-erratas
related: [research/portfolio/propuestas/03-revision-adversarial.md, research/portfolio/cartera-actual.md]
---

# Propuesta B — consolidada agresiva (100.000 €) · 30/10/2026

> **Estado: no ejecutable tal cual.** Se conserva como alternativa de perfil agresivo y como
> material del debate. Tiene erratas aritméticas conocidas (ver §0) y su justificación de costes no
> se sostiene; el ataque completo está en `03-revision-adversarial.md`.

## 0. Erratas conocidas (leer antes que nada)

| Dónde | Dice | Real |
|---|---|---|
| Tabla final §4.3 | RV 67.000 € / 67,0% | **63.400 € / 63,4%** (las filas no suman) |
| Tabla final §4.3 | TOTAL 100.000 € | **99.000 €** — falta la fila de Cobas (1.000 €) |
| §4.3 y §6 | "RF + monetario 33.000 / 33%" | **35.600 € / 35,6%** |
| §6 | "USA ~14% del total" | **33,4% del total** (52,7% de la RV) |
| §4.6 | "duración media ~4,5 años" | **5,0 años** (y hoy son 3,8, no 2,5) |
| §5 Fase 1 | "Vender" 65.000 € | Debe ser **traspaso**: ~2.610 € de impuestos evitables |
| §4.2 punto 1 | "RV Global: hueco libre" | Rock ya tiene 15.900 € en large cap desarrollado: el MSCI World no añade compañías nuevas |

**Total:** 100.000 € · **Dos bloques:** cartera auditada (70.000 €, 9 fondos, control directo) + cartera indexada Rock de MyInvestor (30.000 €, 9 fondos, gestión automatizada).
**Plataforma:** MyInvestor · **Inversor:** español · **Horizonte:** largo plazo

> Nota clarificativa: el usuario tiene **además** de la cartera auditada el 30/10/2026 (70.000 €) una cartera indexada **Rock** de MyInvestor por 30.000 €. Ambas se complementan. Este documento consolida ambas para evitar duplicidades al rebalancear.

---

## 1. Cartera Rock de MyInvestor (30.000 €) — composición

Cartera indexada automatizada de perfil **agresivo** (riesgo 4/7), gestión pasiva, comisión total 0,41% (TER 0,11% + custodia 0,15% + gestión 0,15%). Rentabilidad acumulada desde 24/06/2020: +83,44%. YTD 2026: +12,57%.

### 1.1 Fondos subyacentes

| # | ISIN | Fondo | % Rock | € (sobre 30k) | Bloque | Divisa |
|---|------|-------|--------|---------------|--------|--------|
| 1 | IE00BYX5MX67 | Fidelity S&P 500 Index P-ACC-EUR | 33% | 9.900 € | RV USA large | EUR |
| 2 | LU2349459045 | Goldman Sachs Global Enhanced Index Sustainable Equity I Cap EUR | 14% | 4.200 € | RV Global SRI (enhanced) | EUR |
| 3 | IE0007471471 | Vanguard US Government Bond Index EUR Hedged | 12% | 3.600 € | RF USA (gobierno) | EUR hedged |
| 4 | IE00BYWYCC39 | iShares Emerging Markets Index D Acc EUR | 11% | 3.300 € | RV Emergentes | EUR |
| 5 | IE00B246KL88 | Vanguard 20+ Year Euro Treasury Index Fund | 10% | 3.000 € | RF Europa (20+ años) | EUR |
| 6 | IE00BYX5N771 | Fidelity MSCI Japan Index P-ACC-EUR | 9% | 2.700 € | RV Japón | EUR |
| 7 | IE00BYX5MD61 | Fidelity MSCI Europe Index P-ACC-EUR | 7% | 2.100 € | RV Europa | EUR |
| 8 | IE00BDZVHT63 | Fidelity MSCI Pacific ex-Japan P-ACC-USD | 2% | 600 € | RV Pacífico ex-Japón | USD |
| 9 | IE00B1G3DH73 | Vanguard US Equity Index EUR Hedged | 2% | 600 € | RV USA (hedged) | EUR hedged |

### 1.2 Composición por bloque (Rock)

| Bloque | % Rock | € (sobre 30k) | % del total (100k) |
|--------|--------|---------------|---------------------|
| RV USA (S&P 500 + Vanguard US) | 35% | 10.500 € | 10,5% |
| RV Global SRI (Goldman enhanced) | 14% | 4.200 € | 4,2% |
| RV Emergentes | 11% | 3.300 € | 3,3% |
| RV Japón | 9% | 2.700 € | 2,7% |
| RV Europa | 7% | 2.100 € | 2,1% |
| RV Pacífico ex-Japón | 2% | 600 € | 0,6% |
| RF USA (gobierno) | 12% | 3.600 € | 3,6% |
| RF Europa 20+ años (larga) | 10% | 3.000 € | 3,0% |
| **TOTAL** | **100%** | **30.000 €** | **30,0%** |

### 1.3 Observaciones sobre Rock

- **Cobertura global implícita:** USA 35% + Europa 7% + Japón 9% + EM 11% + Pacífico 2% + Global SRI 14% = cobertura amplia pero fragmentada (sin un fondo MSCI World puro).
- **Sesgo USA fuerte:** 35% de Rock = USA (S&P 500 + Vanguard US Equity). Esto es deliberado (perfil agresivo).
- **RF Europa 20+ años:** 10% de Rock en deuda de muy larga duración. Esto **contradice** la recomendación del audit ("no alargar duración nominal ahora"), pero es parte del diseño de la cartera Rock (perfil agresivo, horizonte >6 años). No se puede cambiar individualmente (gestión automatizada).
- **Clase de EM más cara:** IE00BYWYCC39 (clase D, TER 0,20%) vs IE000QAZP7L2 (clase S, TER 0,16%). La cartera Rock usa la clase D. Si el usuario quisiera optimizar, podría traspasar a la clase S, pero esto implicaría salir de la cartera Rock.
- **Goldman Enhanced Index SRI:** fondo de gestión semipasiva (enhanced index) con TER incluido en la comisión de la cartera. No es un fondo indexado puro.

---

## 2. Visión consolidada (100.000 €)

### 2.1 Cartera auditada (70.000 €) — estado actual

| ISIN | Fondo | € | % (sobre 70k) | Bloque |
|------|-------|---|---------------|--------|
| IE00BL1GVT98 | Neuberger Short Duration Euro Bond U | 22.000 | 31,4% | Monetario/RF corta |
| LU1694789451 | DNCA Invest Alpha Bonds A | 13.000 | 18,6% | RF flexible |
| LU1623762843 | Carmignac Portfolio Credit A | 12.000 | 17,1% | Crédito HY |
| FR0000989626 | Groupama Trésorerie IC | 10.000 | 14,3% | Monetario |
| ES0140794001 | Gamma Global, FI A | 8.000 | 11,4% | Mixto flexible (HY) |
| ES0165243025 | MyInvestor Value, FI C | 2.000 | 2,9% | RV value |
| LU1598719752 | Cobas International Fund P | 1.000 | 1,4% | RV value |
| IE00018YKVN0 | NB Next Gen Space Economy | 1.000 | 1,4% | RV temática |
| LU1815002040 | UBS MSCI China All Shares | 1.000 | 1,4% | RV China |

### 2.2 Consolidado por bloque (100.000 €)

| Bloque | Rock (30k) | Auditada (70k) | Total | % total |
|--------|-----------|----------------|-------|---------|
| RV USA (large cap) | 10.500 € | 0 € | 10.500 € | 10,5% |
| RV Global (MSCI World) | 0 € | 0 € (pendiente) | 0 € | 0% ⚠️ |
| RV Global SRI (enhanced) | 4.200 € | 0 € | 4.200 € | 4,2% |
| RV Europa | 2.100 € | 0 € (pendiente) | 2.100 € | 2,1% |
| RV Japón | 2.700 € | 0 € | 2.700 € | 2,7% |
| RV Emergentes | 3.300 € | 0 € | 3.300 € | 3,3% |
| RV Pacífico ex-Japón | 600 € | 0 € | 600 € | 0,6% |
| RV Value (small/mid Europa) | 0 € | 3.000 € | 3.000 € | 3,0% |
| RV China (satélite) | 0 € | 1.000 € | 1.000 € | 1,0% |
| RV Temática (Space) | 0 € | 1.000 € | 1.000 € | 1,0% |
| RV Small cap | 0 € | 0 € (pendiente) | 0 € | 0% ⚠️ |
| RF USA (gobierno) | 3.600 € | 0 € | 3.600 € | 3,6% |
| RF Europa 20+ (larga) | 3.000 € | 0 € | 3.000 € | 3,0% |
| RF flexible (DNCA) | 0 € | 13.000 € | 13.000 € | 13,0% |
| Crédito HY (Carmignac) | 0 € | 12.000 € | 12.000 € | 12,0% |
| Mixto flexible (Gamma) | 0 € | 8.000 € | 8.000 € | 8,0% |
| Monetario/RF corta | 0 € | 32.000 € | 32.000 € | 32,0% |
| Ligados a inflación | 0 € | 0 € (pendiente) | 0 € | 0% ⚠️ |
| RF IG corta/global | 0 € | 0 € (pendiente) | 0 € | 0% ⚠️ |
| Crédito IG euro | 0 € | 0 € (pendiente) | 0 € | 0% ⚠️ |

**Huecos críticos (marcados con ⚠️):** RV Global puro, RV Small cap, Ligados a inflación, RF IG corta, Crédito IG euro — ninguno está cubierto ni por Rock ni por la cartera auditada actual.

---

## 3. Duplicidades y solapamientos identificados

### 3.1 Solapamientos directos (mismo fondo o índice)

| Fondo/índice | Rock | Auditada | Solapamiento |
|-------------|------|----------|--------------|
| Fidelity MSCI Europe (IE00BYX5MD61) | 2.100 € (7%) | 0 € (pero propuesto en rebalanceo) | ⚠️ Si compro más Europa, duplico |
| iShares Emerging Markets (IE00BYWYCC39 / IE000QAZP7L2) | 3.300 € (11%) | 0 € (pero propuesto en rebalanceo) | ⚠️ Si compro EM, duplico |
| Fidelity S&P 500 (IE00BYX5MX67) | 9.900 € (33%) | 0 € | ✅ Sin duplicidad (auditada no tiene USA) |

### 3.2 Solapamientos por bloque

| Bloque | Rock cubre | Auditada cubre | Duplicidad |
|--------|-----------|----------------|------------|
| RV USA | ✅ 10.500 € | ❌ No | Sin duplicidad |
| RV Europa | ✅ 2.100 € | ❌ No (pero propuesto) | ⚠️ Limitar compra adicional |
| RV Japón | ✅ 2.700 € | ❌ No | Sin duplicidad |
| RV Emergentes | ✅ 3.300 € | ❌ No (pero propuesto) | ⚠️ No comprar más EM |
| RV Global (MSCI World) | ❌ No (fragmentado) | ❌ No | ✅ Hueco libre |
| RV Small cap | ❌ No | ❌ No | ✅ Hueco libre |
| RF USA | ✅ 3.600 € | ❌ No | Sin duplicidad |
| RF Europa larga (20+) | ✅ 3.000 € | ❌ No | ⚠️ Tensión con "no alargar duración" |
| RF IG corta/global | ❌ No | ❌ No | ✅ Hueco libre |
| Crédito IG euro | ❌ No | ❌ No | ✅ Hueco libre |
| Ligados a inflación | ❌ No | ❌ No | ✅ Hueco libre |
| Monetario | ❌ No | ✅ 32.000 € | Sin duplicidad (pero exceso) |
| RV Value | ❌ No | ✅ 3.000 € | Sin duplicidad |
| RV China | ❌ No | ✅ 1.000 € | Sin duplicidad |
| RV Temática | ❌ No | ✅ 1.000 € | Sin duplicidad |

### 3.3 Puntos de tensión

1. **RF Europa 20+ años (Rock):** La cartera Rock tiene 3.000 € (3% del total) en Vanguard 20+ Year Euro Treasury. El audit recomendaba "no alargar duración nominal ahora". Esto es inherente al diseño de Rock (perfil agresivo) y no se puede cambiar individualmente. **Decisión:** mantener, pero compensar en la cartera auditada con RF de corta duración (IE0004ZP1ND3, duración 1-5 años) para equilibrar la duración media del total.

2. **Clase de EM más cara:** Rock usa IE00BYWYCC39 (clase D, TER 0,20%). La clase S (IE000QAZP7L2, TER 0,16%) es más barata. **Decisión:** si el usuario quiere optimizar costes, puede traspasar fuera de Rock a la clase S, pero pierde la gestión automatizada. Recomendación: mantener en Rock por simplicidad.

3. **Goldman Enhanced Index SRI:** Fondo de gestión semipasiva (enhanced index) con TER incluido en la comisión total de la cartera (0,41%). No es un fondo indexado puro. **Decisión:** mantener como parte de Rock (diversificación SRI).

4. **Exceso de monetario (auditada):** 32.000 € (32% del total) en monetario/RF corta. El audit recomendaba reducir a 10-15%. Con Rock cubriendo RF USA + RF Europa larga, la cartera auditada necesita menos RF. **Decisión:** reducir monetario a ~7.000 € (7%) y redistribuir el resto.

---

## 4. Propuesta de rebalanceo consolidado

### 4.1 Principio: no duplicar, complementar

La cartera Rock (30.000 €) ya cubre:
- RV USA (large cap): 10.500 €
- RV Japón: 2.700 €
- RV Emergentes: 3.300 €
- RV Europa: 2.100 €
- RV Global SRI: 4.200 €
- RV Pacífico: 600 €
- RF USA: 3.600 €
- RF Europa larga: 3.000 €

**Por tanto, la cartera auditada (70.000 €) NO debe comprar:**
- RV USA (cubierto)
- RV Japón (cubierto)
- RV Emergentes (cubierto)
- RV Europa (cubierto parcialmente — solo añadir si se quiere más peso Europa)
- RF USA (cubierto)
- RF Europa larga (cubierto — y además contradice el audit)

**La cartera auditada (70.000 €) SÍ debe cubrir (huecos libres):**
- RV Global (MSCI World) — fondo puro, barato
- RV Small cap — diversificación de tamaño
- Ligados a inflación — protección contra inflación
- RF IG corta/global — compensar duración larga de Rock
- Crédito IG euro — mejorar rentabilidad sobre RF
- Monetario — liquidez (reducido)
- RV Value — tilt de valor (mantener/ajustar)
- RV China — satélite (mantener)
- RV Temática — satélite (valorar venta)

### 4.2 Rebalanceo de la cartera auditada (70.000 €)

**Mantener (no tocar):**
| Fondo | € actual | Acción |
|-------|---------|--------|
| MyInvestor Value | 2.000 € | Mantener (value tilt) |
| Cobas International | 1.000 € | Mantener (value tilt) |
| UBS China | 1.000 € | Mantener (satélite) |
| NB Space Economy | 1.000 € | Mantener (satélite, valorar venta) |
| **Subtotal mantener** | **5.000 €** | |

**Vender y redistribuir (65.000 €):**
| Fondo | € actual | Acción |
|-------|---------|--------|
| NB Ultra Short Euro | 22.000 € | Vender → redistribuir |
| DNCA Alpha Bonds | 13.000 € | Vender → redistribuir |
| Carmignac Credit | 12.000 € | Vender → redistribuir |
| Groupama Trésorerie | 10.000 € | Vender → consolidar en monetario barato |
| Gamma Global | 8.000 € | Vender → redistribuir |
| **Subtotal vender** | **65.000 €** | |

**Comprar con los 65.000 €:**
| # | ISIN | Fondo | TER | € | Bloque | Justificación |
|---|------|-------|-----|---|--------|---------------|
| 1 | IE000ZYRH0Q7 | iShares Developed World Index S Acc EUR | 0,06% | 20.000 € | RV Global | Núcleo principal, más barato del catálogo |
| 2 | IE00BDRK7L36 | iShares Europe Index D Acc EUR | 0,10% | 5.000 € | RV Europa | Complemento a Rock (que ya tiene 2.100 € en Europa) |
| 3 | IE00B42W4L06 | Vanguard Global Small-Cap Index EUR Acc | 0,29% | 5.000 € | RV Small cap | Diversificación de tamaño (Rock no tiene) |
| 4 | IE00BD0NC144 | iShares Euro Gov Inflation-Linked D Acc EUR | 0,10% | 5.000 € | Ligados a inflación | Protección inflación (Rock no tiene) |
| 5 | IE0004ZP1ND3 | iShares Global Agg 1-5Y Bond S Acc EUR H | 0,08% | 10.000 € | RF IG corta | Compensar duración larga de Rock |
| 6 | IE00BD0NC698 | iShares Euro Credit Bond Index D Acc EUR | 0,12% | 7.000 € | Crédito IG euro | Mejorar rentabilidad sobre RF |
| 7 | FR0000447823 | AXA Trésor Court Terme C | 0,05% | 7.000 € | Monetario | Liquidez (consolidar monetario) |
| 8 | ES0165243025 | MyInvestor Value (añadir) | 1,45%+ | 3.000 € | RV Value | Reforzar value tilt (total 5.000 €) |
| 9 | IE000ZYRH0Q7 | iShares Developed World Index (añadir) | 0,06% | 3.000 € | RV Global | Reforzar núcleo (total 23.000 €) |
| | | **TOTAL comprar** | | **65.000 €** | | |

### 4.3 Asignación final consolidada (100.000 €)

| Bloque | Rock (30k) | Auditada (70k) | Total | % total |
|--------|-----------|----------------|-------|---------|
| RV USA (large cap) | 10.500 € | 0 € | 10.500 € | 10,5% |
| RV Global (MSCI World) | 0 € | 23.000 € | 23.000 € | 23,0% |
| RV Global SRI (enhanced) | 4.200 € | 0 € | 4.200 € | 4,2% |
| RV Europa | 2.100 € | 5.000 € | 7.100 € | 7,1% |
| RV Japón | 2.700 € | 0 € | 2.700 € | 2,7% |
| RV Emergentes | 3.300 € | 0 € | 3.300 € | 3,3% |
| RV Pacífico ex-Japón | 600 € | 0 € | 600 € | 0,6% |
| RV Value (small/mid Europa) | 0 € | 5.000 € | 5.000 € | 5,0% |
| RV Small cap | 0 € | 5.000 € | 5.000 € | 5,0% |
| RV China (satélite) | 0 € | 1.000 € | 1.000 € | 1,0% |
| RV Temática (Space) | 0 € | 1.000 € | 1.000 € | 1,0% |
| RF USA (gobierno) | 3.600 € | 0 € | 3.600 € | 3,6% |
| RF Europa 20+ (larga) | 3.000 € | 0 € | 3.000 € | 3,0% |
| RF IG corta/global | 0 € | 10.000 € | 10.000 € | 10,0% |
| Crédito IG euro | 0 € | 7.000 € | 7.000 € | 7,0% |
| Ligados a inflación | 0 € | 5.000 € | 5.000 € | 5,0% |
| Monetario | 0 € | 7.000 € | 7.000 € | 7,0% |
| **TOTAL** | **30.000 €** | **70.000 €** | **100.000 €** | **100%** |

### 4.4 Resumen por gran bloque

| Gran bloque | € | % |
|-------------|---|---|
| **Renta variable** | 67.000 € | 67,0% |
| **Renta fija + monetario** | 33.000 € | 33,0% |

Desglose RV:
| Sub-bloque RV | € | % del total |
|---------------|---|-------------|
| RV Global (MSCI World) | 23.000 € | 23,0% |
| RV USA | 10.500 € | 10,5% |
| RV Europa | 7.100 € | 7,1% |
| RV Value (small/mid) | 5.000 € | 5,0% |
| RV Small cap | 5.000 € | 5,0% |
| RV Global SRI | 4.200 € | 4,2% |
| RV Emergentes | 3.300 € | 3,3% |
| RV Japón | 2.700 € | 2,7% |
| RV China | 1.000 € | 1,0% |
| RV Temática (Space) | 1.000 € | 1,0% |
| RV Pacífico | 600 € | 0,6% |
| **Total RV** | **67.000 €** | **67,0%** |

Desglose RF + monetario:
| Sub-bloque RF | € | % del total |
|---------------|---|-------------|
| RF IG corta/global | 10.000 € | 10,0% |
| Monetario | 7.000 € | 7,0% |
| Crédito IG euro | 7.000 € | 7,0% |
| Ligados a inflación | 5.000 € | 5,0% |
| RF USA | 3.600 € | 3,6% |
| RF Europa 20+ (larga) | 3.000 € | 3,0% |
| **Total RF + monetario** | **33.000 €** | **33,0%** |

### 4.5 Costes estimados

| Componente | Coste anual estimado |
|------------|---------------------|
| Rock (30.000 € × 0,41%) | 123 € |
| Auditada RV Global (23.000 × 0,06%) | 13,80 € |
| Auditada RV Europa (5.000 × 0,10%) | 5,00 € |
| Auditada RV Small cap (5.000 × 0,29%) | 14,50 € |
| Auditada Value (5.000 × 1,45%+) | ~72,50 € + success fee |
| Auditada China (1.000 × 0,30%) | 3,00 € |
| Auditada Space (1.000 × 1,72%) | 17,20 € |
| Auditada RF IG corta (10.000 × 0,08%) | 8,00 € |
| Auditada Crédito IG (7.000 × 0,12%) | 8,40 € |
| Auditada Inflación (5.000 × 0,10%) | 5,00 € |
| Auditada Monetario (7.000 × 0,05%) | 3,50 € |
| **Total coste anual estimado** | **~274 €** |
| **TER ponderado (excl. success fees)** | **~0,27%** |

vs. TER ponderado actual de la cartera auditada: 0,774% → reducción del ~65%.

### 4.6 Duración y riesgo consolidado

| Métrica | Valor |
|---------|-------|
| Duración media ponderada (RF) | ~4,5 años (compensada: Rock 20+ años + auditada 1-5 años) |
| Rating medio de cartera (RF) | A (mix de IG soberano + corporativo) |
| Volatilidad estimada (cartera total) | ~12-14% (RV 67% con vol ~15-20%, RF 33% con vol ~2-5%) |
| Max drawdown estimado | −25% a −30% (en crisis severa, por el peso en RV) |

---

## 5. Acciones de ejecución (orden sugerido)

### Fase 1 — Vender (liberar 65.000 €)
1. Vender NB Ultra Short Euro (22.000 €)
2. Vender DNCA Alpha Bonds (13.000 €)
3. Vender Carmignac Credit (12.000 €)
4. Vender Groupama Trésorerie (10.000 €)
5. Vender Gamma Global (8.000 €)

### Fase 2 — Comprar (invertir 65.000 €)
6. Comprar iShares Developed World Index S (IE000ZYRH0Q7) — 23.000 €
7. Comprar iShares Europe Index D (IE00BDRK7L36) — 5.000 €
8. Comprar Vanguard Global Small-Cap EUR (IE00B42W4L06) — 5.000 €
9. Comprar iShares Euro Gov Inflation-Linked (IE00BD0NC144) — 5.000 €
10. Comprar iShares Global Agg 1-5Y (IE0004ZP1ND3) — 10.000 €
11. Comprar iShares Euro Credit Bond Index (IE00BD0NC698) — 7.000 €
12. Comprar AXA Trésor Court Terme (FR0000447823) — 7.000 €
13. Añadir a MyInvestor Value (ES0165243025) — 3.000 €

### Fase 3 — Ajustes finales
14. Valorar venta de NB Space Economy (1.000 €) → redistribuir a RV Global o Value
15. Valorar si mantener UBS China (1.000 €) o consolidar en RV Global
16. Verificar que no hay solapamiento entre Rock y la cartera auditada post-rebalanceo

### Fase 4 — Mantenimiento
17. Revisar anualmente la asignación consolidada
18. Rebalancear si algún bloque se desvía >5% del objetivo
19. Monitorizar costes de Rock (comisión 0,41%) vs fondos directos

---

## 6. Notas importantes

- **No vender Rock:** La cartera Rock está gestionada automáticamente y tiene un track record excelente (+83,44% desde 2020). No tiene sentido desmontarla.
- **Complementar, no duplicar:** La cartera auditada cubre los huecos que Rock no cubre (RV Global puro, small cap, inflación, RF corta, crédito IG, monetario).
- **Duración compensada:** Rock tiene RF Europa 20+ años (duración larga). La cartera auditada tiene RF IG corta (1-5 años). La duración media ponderada del total (~4,5 años) es razonable.
- **Coste total:** TER ponderado ~0,27% (excl. success fees de Value y Space). Muy competitivo para una cartera diversificada global.
- **Diversificación geográfica:** USA ~14% (Rock 10,5% + auditada 0%), Europa ~9,8% (Rock 2,1% + auditada 7,7%), Japón 2,7%, EM 3,3%, Global 23%, China 1%, Pacífico 0,6%. Bien diversificada.
- **Diversificación de tamaño:** Large cap (USA + global) + small cap (5%) + value (small/mid Europa 5%). Buena cobertura de tamaños.

---

*Nota creada el 30/10/2026. Parte de `research/portfolio/cartera-actual.md`.*
*Datos de Rock: MyInvestor MCP (search_portfolios). Datos de fondos: MyInvestor MCP (search_funds).*
*Dato clave: la cartera Rock tiene 30.000 € adicionales que NO estaban incluidos en la auditoría original (70.000 €).*
