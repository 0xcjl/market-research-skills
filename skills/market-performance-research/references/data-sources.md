# Data Sources — Endpoints, Shapes, Quirks

All recipes below were exercised against live endpoints. Re-verify shapes when a response
changes shape; treat field names here as a starting point, not a contract.

## Priority order

1. **Exchange / index / official statistics** — Nasdaq official API, FRED, Binance.
2. **Aggregator** — used for cross-checks and for series the primary source doesn't publish.
3. **Media** — for narrative context and for spotting which numbers to go verify. Never as
   the source of a figure that belongs in a table.

Never source an index constituent list or its weights from search results. Search results
for "Nasdaq 100 components" return stale, weighted-by-anything lists. Use the index
provider's own API.

## US equities and indices — Nasdaq official API

```
GET https://api.nasdaq.com/api/quote/{SYMBOL}/historical?assetclass=stocks&fromdate=YYYY-MM-DD&todate=YYYY-MM-DD
```

- `assetclass=stocks` for listed names; index symbols (e.g. the Nasdaq-100 index, SPX) may
  need a different `assetclass` — try `index` and fall back to `etf` via a proxy symbol.
- Response shape: `data.tradesTable.rows` — a list of per-day rows. Each row carries `date`
  formatted `MM/DD/YYYY` and `close` formatted like `$1,234.56`.
- **`close` can be the literal string `--`** on non-trading rows. Skip those rows; never
  coerce them to `0` — a single zero close silently corrupts every drawdown and
  correlation computed downstream.
- The `close` string may include `$` and thousands separators. Strip both before parsing.
- For long histories, request explicit `fromdate`/`todate` windows and cache each window's
  raw JSON separately. A single request for a multi-year window may be truncated.
- Query `limit`/`offset` on the list endpoints when the symbol universe is large.

Parsing sketch:

```python
import datetime, json

def load_nasdaq(path):
    d = json.load(open(path))
    rows = d["data"]["tradesTable"]["rows"]
    out = {}
    for r in rows:
        try:
            dt = datetime.datetime.strptime(r["date"], "%m/%d/%Y").date()
            c = float(str(r["close"]).replace("$", "").replace(",", ""))
        except (ValueError, KeyError, TypeError):
            continue          # covers the "--" rows
        out[dt] = c
    return out
```

## Crypto spot — Binance klines

```
GET https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=1000&startTime=<ms>
```

- Row layout: `0` openTime (ms), `1` open, `2` high, `3` low, `4` close, `5` volume,
  `6` closeTime (ms), `7` quoteVolume, …
- Page backwards with `startTime`/`endTime` to build multi-year daily history.
- Crypto trades weekends; equity indexes do not. Any cross-asset correlation must inner-join
  on dates and report the resulting sample size.

```python
def load_binance(path):
    rows = json.load(open(path))
    return {datetime.datetime.utcfromtimestamp(r[0] / 1000).date(): float(r[4]) for r in rows}
```

## Total crypto market cap — CoinGecko

- Current snapshot: `GET https://api.coingecko.com/api/v3/global`
- Historical total market cap series: the global market-cap chart endpoint. Cache the whole
  series; the peak-to-current decline is a headline number and must be recomputable.

## Macro and volatility — FRED

CSV download, no key needed for the graph endpoint:

```
GET https://fred.stlouisfed.org/graph/fredgraph.csv?id={SERIES_ID}
```

| Series | ID | Use |
|---|---|---|
| VIX close | `VIXCLS` | volatility regime; compare to its own 52-week high |
| US high-yield OAS | `BAMLH0A0HYM2` | credit stress; report as level + historical percentile |
| 10-year Treasury yield | `DGS10` | rates backdrop |

Parse the CSV with two columns (`observation_date`, value); the value column contains `.`
for missing observations — skip them rather than reading `.` as a float.

## Prediction markets

Polymarket Gamma/CLOB endpoints, double-encoded fields, and a ready CLI live in the
`research/polymarket` skill — read that instead of re-deriving them here.

Two working rules for this task:

- **Query the same question on a second independent venue** (Kalshi is the usual counterpoint).
  Two venues converging on a macro probability is a materially stronger signal than one.
  Kalshi has moved domains more than once — confirm the current public host before
  scripting it rather than trusting a remembered URL.
- **Check liquidity before quoting an odd.** A market with negligible volume is a number
  someone typed, not a crowd estimate; report it as such or drop it.

## Search-tool fallback

When a search tool ignores or mangles query parameters, pull the bulk result set once and
filter locally in Python instead of trying to coax the backend into a precise query. This
is also the right pattern when you need an exhaustive universe rather than a ranked one.

## Caching discipline

Write every raw response to disk on arrival and compute only from the cache:

- A report number must be traceable to a cached file, not to a live re-fetch.
- A source that fails halfway through must not change numbers already published.
- The independent-recomputation check needs the cache anyway — it is the shared input for
  both implementations, which is what makes the comparison meaningful.
