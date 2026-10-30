# Lookup: Fund and Company Search

When a meeting transcript mentions a fund or a company stock/action, the agent
should automatically search public sources and add the information to the
summary.md file.

## Detection

Scan the full transcript text (concatenated chunks) for mentions:

- Funds: `fondo`, `fund`, `ETF`, `SICAV`, `EAF`, `GESTIÓN`, `gestora`,
  `management`, `fund`.
- Stocks/actions: `acción`, `actions`, `stock`, `acciones`, `cotización`,
  `carta`, `título`, `bono`, `shares`, `company`, `empresa`, `compañía`,
  `holding`, `sociedad`.

## Sources

| Type | Source | URL pattern |
|---|---|---|
| Spanish funds | CNMV | `https://www.cnmv.es/portal/consultas/iic/fondo?lang=es&nif=<NIF>` |
| Spanish funds (search) | CNMV search | `https://www.cnmv.es/portal/consultas/iic/fondo/search?lang=es` |
| European funds | Wikipedia | `https://es.wikipedia.org/wiki/<fondo-name>` |
| Stock quotes | Yahoo Finance | `https://finance.yahoo.com/quote/<symbol>` |
| Companies | Wikipedia | `https://es.wikipedia.org/wiki/<company-name>` |
| Listed companies | CNMV | `https://www.cnmv.es/portal/consultas/iic/valor/search?lang=es` |

## Output format

Add a section `## Fondos y acciones mencionados` to summary.md with tables:

```
### Fondos de inversión

| Campo | Valor |
|---|---|
| Nombre del fondo | `<nombre>` |
| ISIN | `<ISIN>` |
| Gestor | `<gestor>` |
| Fecha de constitución | `<fecha>` |
| Categoría | `<categoría>` |
| Estrategia | `<estrategia>` |
| Comisiones | `<gestion>% (fija), <variable>% (variable)` |
| Patrimonio | `<patrimonio>` EUR |
| Rentabilidad | `<rentabilidad>` |
| Fuente | `<URL>` |
```

Rules:
- Do not invent data. If not found, write `no verificado` or `no disponible`.
- Try name variations if the first search fails.
- Record all sources and URLs for traceability.
