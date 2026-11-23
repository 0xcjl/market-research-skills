# Building a Market Universe

For breadth and cross-sectional analysis, the universe is the measurement instrument. A
bad universe makes every downstream number wrong in ways that look fine.

## What makes a universe usable

| Requirement | Why |
|---|---|
| **Broad** | a 15–20 name universe measures nothing; aim for the largest liquid set with consistent history |
| **Liquid and priced by one venue** | mixing venues introduces basis noise into returns |
| **Ranked by an objective source** | a hand-picked list bakes in survivorship *and* selection bias toward known survivors |
| **Long history per member** | short histories shrink the denominator in exactly the historical periods you need |
| **Filtered for non-informative instruments** | stablecoins and commodity proxies distort every cross-sectional statistic |

## Concrete procedure (crypto example)

```
1. Venue listings:   exchangeInfo → all TRADING spot symbols with quote asset USDT
2. Universe ranking: aggregator market-cap ranking (top 500), NOT a manual list
3. Intersection:     keep symbols present in both
4. Exclusions:
     - stablecoins (they don't fall → inflate breadth)
     - commodity proxies (gold/silver tokens)
     - leveraged/inverse tokens (price is mechanically derived, not discovered)
5. History filter:   keep assets with >= N days of continuous klines
6. Report:           the count at each filter step, and the final count
```

The count at each step is not bookkeeping — it is how a reader checks whether the universe
is what the document claims.

## Survivorship bias: the direction matters

A universe built from **today's** top 500 excludes every asset that has since been
delisted, rugged, or fallen out of the top 500.

Effect on breadth readings: **historically inflated**. In a past bear market, the assets
that would have dragged breadth down are absent from today's list, so measured historical
breadth was higher than the breadth a participant actually experienced.

So when a backtest says "breadth was 0% at the bottom", the *real* breadth was likely even
lower. Direction of the bias:

| Measure | Effect of survivorship bias |
|---|---|
| historical breadth levels | **inflated** (true values lower) |
| breadth as a bottom identifier | **weakened** (the metric would have performed worse in real time) |
| sample of turning points | biased toward episodes in which the eventual winners' declines were shallower |

State the direction, not just the caveat. "There may be survivorship bias" is not
actionable; "historical breadth was likely lower than measured, so the bottom-identification
result is if anything conservative" is.

## Early-period denominator collapse

With a 200-day moving average, an asset contributes to breadth only after it has 200 days
of history. In a multi-year backtest, the denominator in early periods can be tiny
(reported examples show n=2 in 2018–2019).

Rules:

1. **Never report a breadth number without its denominator** (`n`).
2. **Exclude turning points where n is below a floor** (e.g. n < 20) from any statistical
   claim, and say how many were excluded.
3. If the excluded turning points are all in one era, note that the surviving sample is
   concentrated in a later, structurally different regime.

## A backfilled universe is a limitation you must escalate, not a caveat

A universe built from **today's** constituents and backfilled over history is the only
universe most pipelines can build, and it carries a bias that **no amount of
recomputation can remove**: the assets that delisted, rug-pulled, or fell out of the
ranking are absent from every historical period, not only the recent ones.

Two statements, only one of which is honest for a backfilled universe:

| Statement | When it is honest |
|---|---|
| "historical breadth may be inflated by survivorship; the bottom-identification result is if anything conservative" | you hold a **historical constituent snapshot**, so the bias is bounded and disclosable |
| "the universe is today's constituents backfilled; delisted assets cannot be recovered from this data, and a historical market-cap snapshot source is required to fix it" | the universe **is** backfilled — this is the correct statement |

The second is a **hard limitation**: name the source that would fix it, say plainly that
the current data cannot, and do not soften it into a footnote. A defect that cannot be
fixed with the data at hand is a scope boundary the reader must see, not a caveat that
dilutes the headline. Put it in the deliverable's limits section and in the delivery
summary — not only in the theory document.

## Caching and reproducibility

Fetch scripts must:

- **skip the network when the raw response is cached** — otherwise a source failure
  silently changes numbers already published in a report
- **write the raw response to disk verbatim** — analysis must run on the raw file, not on
  a re-fetch
- **report failures** rather than printing a success line for each symbol

A fetch script that prints "ok" for every symbol regardless of outcome will produce a log
that looks successful and a directory that is empty. Verify by checking the file count
after a run, not the log.