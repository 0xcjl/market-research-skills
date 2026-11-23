# Metric Definitions and Their Traps

Every number that reaches the report needs a written definition. These are the definitions
that most often go wrong, and the mechanism behind each failure.

## 1. Period return — the base is the close BEFORE the period

```
year return for Y   = close(last trading day of Y)   / close(last trading day of Y-1)   - 1
YTD                 = close(latest session)          / close(last trading day of prior year) - 1
```

**Trap:** using the first bar *inside* the period as the base. This looks right — it is the
period's opening close — but it (a) drops the prior year's final close, so the figure is
off by one session's move, and (b) breaks the compounding identity between periods, so
`2026 YTD` and `2025` no longer reconcile with a cumulative total.

**Verification:** assert the identity `cum = (1 + ret_prev) * (1 + ret_ytd) - 1` against a
directly computed cumulative return. If it fails, the bases are wrong.

**Trap:** the data starts too late to supply the base close (e.g. a series beginning
2024-01-01 has no 2023 close). Then the earliest full year is 2025. Label 2024 partial or
drop the column — do not substitute the first available close and call it a year return.

**Trap:** `at(2025,1,1)` vs `at(2024,12,31)` as the base. These are different sessions and
give different answers. Pick one convention, state it, and use it everywhere.

## 2. Drawdown — always name the reference peak

```
drawdown from a peak = current / peak - 1     (negative)
```

Three different peaks, three different numbers:

| Peak | Definition | Typical use |
|---|---|---|
| All-time high | max over the full cached history | "how far from its high" |
| 52-week high | max over the last ~252 sessions | "how bad is this year" |
| YTD high | max since the year's first session | "the year's slide so far" |

Report each as its own labeled column. A drawdown column that does not name its peak is
not a checkable claim.

Also keep distinct:

- **current drawdown** = today vs the peak
- **max drawdown within a period** = the worst peak-to-trough inside the window

These answer different questions and are frequently confused for each other.

Always carry the peak's **date** — a reader needs to know whether the peak was 3 weeks or
14 months ago.

## 3. Moving averages

`MA200` needs 200 sessions of history *before* the window you report on. If the series
starts later, the first MA200 values are computed on a partial window and are not comparable
to the later ones. Either warm up the series or label the early values.

## 4. Correlation and beta

- Compute on **returns**, not price levels. Two trending series have a high level
  correlation that carries no information.
- Align on the intersection of dates. Crypto trades weekends, equities don't; a naive
  positional join (index i with index i) silently pairs different days. Inner-join on the
  date key and report the surviving sample size.
- Report the window definition explicitly: "120 sessions" and "120 calendar days" are
  different windows and produce different coefficients. When a checker reports a mismatch,
  **first test whether it is a definition difference** — a window-length disagreement
  explains the number; only then hunt for an error.

## 5. Lead-lag

Compute the peak date of each series per cycle and compare. Do **not** assert a general
rule. The relationship has not been stable across cycles — in the sessions where this was
tested, one cycle was synchronous and another had one asset leading by tens of days while
a third showed a lead spanning most of a year. The honest deliverable is the per-cycle
table plus "no stable lead", and it directly answers a user's assumption about who turns
first.

When testing "did asset A lead asset B by k days", shift the date keys by k sessions and
recompute the correlation at each lag, then report the lag profile. A single lag test is a
single number with no confidence.

## 6. Tail-risk and black-swan probability

Give a **probability range** with named triggers, not a point estimate:

| Layer | Shape |
|---|---|
| Base case | range + what would confirm it |
| Trigger conditions | the observable that would move you to another layer |
| Unknowns | explicitly labelled — e.g. "prediction-market odds for this specific trigger do not exist" |

Anchor the range to observables you actually measured: volatility level versus its own
recent range, credit spread level and percentile, implied probabilities, and concentration
of losses in a small number of names.

## 7. Prediction-market odds as an evidence tier

- Odds are a **crowd estimate of a future event**, priced against real money. They say
  nothing about mechanism and they are not a fact.
- Convert price → probability and quote it with the market's liquidity. A near-zero-volume
  market is a typed number, not a crowd estimate.
- Cross-venue: the same question on two independent venues is worth far more than either
  alone.
- Read the resolution criteria before using an odd. A market resolving on "BTC below $55K
  at any point" and one resolving on "BTC close below $55K on 31 Dec" have different
  meanings; the number without its resolution rule is not usable.
- Never present an odds-implied probability as a forecast of your own. Label it as
  "prediction market implies X".

## 8. Cross-checks against third-party figures

When a news outlet publishes a move figure, treat it as a **cross-check** on your computed
value, and record whether they agree. Agreement between an independent implementation of
yours and a third party is meaningful evidence the number is right. Disagreement means
re-check both before publishing — it is never grounds to quietly change your number.

## 9. Display precision and tolerance

A report prints `$1,663` for `1663.16`. A verification check that demands equality with the
raw float will fail on correct data. Match the tolerance to the **displayed precision** of
the report, not to the precision of the underlying data.

The same applies to percentages: a report showing `-32.2%` should be checked against
`-32.2`, not against `-32.216`.

## 10. Naming the reference period on every column

A column header reading `2026 YTD` is unambiguous; a header reading `YTD` in a table that
also has `2025` is not. Put the period in the header, and put the as-of date in the table
caption or the report front matter. Every reader should be able to reconstruct the exact
computation from the header alone.
