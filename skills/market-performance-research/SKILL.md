---
name: market-performance-research
description: Use when quantifying market performance, drawdown, and risk.
license: MIT
allowed-tools: Bash, Read, Write, WebFetch
metadata:
  version: 0.1.0
  author: Helen
  hermes:
    tags: [market-research, quant, drawdown, risk, crypto, equities, prediction-markets]
    category: research
    related_skills: [research/market-bottom-framework, research/market-narrative-cycle-research, research/polymarket, research/claim-verification, research/crypto-token-due-diligence, communication/agent-output-format-scan-first]
---

# Market Performance Research

Quantify how an index, a theme basket, or an asset class actually performed — YTD, from its
peak, tail-risk probability, and how it transmits into another asset class — from
authoritative price series, and publish numbers that survive independent recomputation.

## When to Use

- "今年涨跌幅多少" / "从最高点跌了多少" / "回撤多少" / "距年内高点还有多远"
- bubble, crash, or tail-risk probability for an index or a theme
- cross-asset transmission: "美股跌会不会带崩 BTC" / "谁先反转" / "会不会有黑天鹅"
- a forward market view that has to name a turning point
- any deliverable whose substance is a NUMBER (not a narrative)

## Not for

| Task | Use instead |
|---|---|
| qualitative company / competitive / market-sizing research | `market-research` |
| a cycle history of market themes/narratives + a forward monitoring playbook | `research/market-narrative-cycle-research` |
| on-chain token contract, tax, and liquidity risk | `research/crypto-token-due-diligence` |
| fact-checking a third party's claim | `research/claim-verification` |
| prediction-market API mechanics and endpoints | `research/polymarket` |
| output format, source-link placement, delivery location | `communication/agent-output-format-scan-first` |

## The rule that decides this task

Every number in the delivered report must be recomputable from cached raw data by an
**independent** implementation, and the delivered file must be checked to actually contain
those values.

A correct script with a stale report is a failed deliverable. The two fail separately, and
only the file check catches the second one — so the report file, not the script, is the
thing under test at the end.

## Workflow

### 1. Fix the measurement contract before fetching anything

Write these down first; ambiguity here is what produces wrong numbers later, not the data source.

| Item | Must be pinned |
|---|---|
| Universe | exact constituents + the source that defines them (index provider, not search) |
| As-of | the exact trading day the numbers describe |
| Periods | what "YTD", "this year", "from the high" each mean numerically |
| Peak reference | all-time high vs 52-week high vs year-to-date high — these are different numbers |
| Return convention | simple vs log, price-only vs total return |

### 2. Fix the analytical frame before fetching anything

A measurement contract says how to compute. An analytical frame says **what question the
report answers** — and a wrong frame makes a numerically correct report useless.

| Symptom | The frame is wrong |
|---|---|
| The user asks where the bottom is and the report is organised around the top | bottom-finding and top-finding are different analyses; a top-framed report never answers the question asked |
| The user names one more indicator and you add exactly that one | you have a point list, not a framework — a framework covers every layer you believe matters, named or not |
| One number per asset, no structural layer | it answers "what happened", not "what to expect next" |

Build the frame as layers before fetching. Each layer needs three things, or it is
decoration:

| Layer element | Requirement |
|---|---|
| Historical reference | what this layer read at prior comparable moments (past cycles, prior drawdowns) |
| Current reading | today's value, under the same definition as the historical reference |
| Criterion | the level at which this layer argues the bottom is in, and what would refute it |

State the frame in the report so the reader sees the reasoning structure, not just
numbers — then fill every layer from data. **Do not deliver a layer-by-layer drip of
whatever the user asks for next; that is the failure mode this step exists to prevent.**

**Theme breadth is layered, not aggregate.** A theme's supply chain bottoms in staggered
order; averaging hides that one layer is still making lows while another has already
turned. Compute per-layer (hardware / compute / software / application) as well as for
the whole theme.

**Bottom questions need the marginal question answered.** "How far down" is symmetric and
rarely the binding constraint. What determines a bottom is whether the *outflow* is
finished: liquidity drain, positioning unwind, forced selling, credit stress. Add those
asymmetric layers (liquidity, positioning, credit, rate path) even when the user asked
only about amplitude.

Turning-point specifics live in the sibling skill `market-bottom-framework`
(its framework-design reference) — bottom-finding rules are maintained in one
place so the two skills cannot drift apart.

### 3. Pull raw series from authoritative sources and cache them

- **Never** source an index constituent list, weights, or holdings from search results —
  they are stale and wrong. Use the index provider's own API.
- Cache every raw response to disk on arrival. All later computation reads the cache, so
  a later source failure cannot silently change a number that is already in the report.
- Prefer the exchange/index/official-statistics endpoint over aggregators; keep the
  aggregator only as a cross-check.

Endpoint recipes, response shapes, and provider quirks: `references/data-sources.md`.

### 4. Compute — with the metric definitions actually written down

The two that most often go wrong:

- **Period return base = the last close strictly BEFORE the period starts.** Not the first
  bar inside the period. Getting this wrong shifts every annual/YTD figure and breaks the
  compounding identity between years.
- **Drawdown always names its reference peak and its date.** "Down 19%" is meaningless
  without "from the 2026-10-06 high".

Correlation, lead-lag, and tail-risk definitions: `references/metrics-and-pitfalls.md`.

### 5. Cross-check every number before writing prose

Recompute with a second, independent implementation (different library or independent
code path) reading the same cached raw data. Importing the analysis module does not count —
that re-tests the same code path and reproduces its bugs.

Assert on **the entity the number belongs to**, never on a whole section: a percentage that
is wrong for one asset is frequently correct for another in the same table.

For a read-only backtest audit, inspect write destinations before running and redirect generated artifacts to scratch without editing the original scripts. Compare those artifacts to the published snapshots, then independently recompute critical rows from raw inputs. Reproducibility is not validity: distinguish confirmed turning points, rolling new lows, and forward-return labels; align cross-asset windows on actual session dates, not row counts.

### 6. Cross-validate with prediction markets and official statistics

The user explicitly wants prediction-market odds as an evidence tier — "大家用钱在投票" —
because they price the *future*, which no historical series does. Use them, but bound them:

- Treat odds as **one input to a probability range**, never as the conclusion.
- Query the **same question on a second independent venue**. Two venues agreeing on a macro
  question is a genuine signal; one venue alone is thin. Disagreement is informative too.
- Check liquidity before treating an odd as information.
- Pair every probability with the observable trigger that would confirm or refute it.

### 7. Write the report showing the frontier

- Lead with the verdict, then the numbers table, then the mechanism.
- Present forward views as scenarios with probabilities, not a single point forecast.
- When the data contradicts the user's framing (e.g. an assumed lead-lag), show the
  computed table and say so — do not bend the analysis to the premise.
- Separate: verified facts / sourced claims / inferences / unknown.

### 8. Verify the delivered file, then deliver

Re-run the checks against the file as it sits in the delivery location, and confirm the
report contains the corrected values. If a check fails, decide whether the **assertion or the
artifact** is wrong before changing anything — a check that scans a whole section will
match legitimate values belonging to other rows.

Template harness: `templates/verify_report_numbers.py`.

## Pitfalls

| Pitfall | Correction |
|---|---|
| Constituents or weights taken from search results | Pull the list from the index provider's API; search for context only |
| Today's forming daily bar read as a close | Seal every series to the last fully-settled bar (a bar dated `d` is settled iff `d < today UTC`); flag the in-progress period as partial — a forming bar's close moves, so it can make a reading look more extreme than it is |
| Period return computed from the first bar inside the period | Base = last close before the period opens |
| Data too short to supply the base close | Label the earliest year partial, or drop it — never fabricate a base |
| "Down X%" without naming the peak and its date | Every drawdown names its reference peak + date |
| Drawdown from ATH mixed with drawdown from the year's high | Separate columns, separate labels |
| Correlation computed on price levels | Use returns, and align on the intersection of dates |
| Crypto/equity correlation sample silently smaller than expected | Inner-join drops non-overlapping days (crypto trades weekends) — state the sample size |
| Rolling window defined as "120 bars" in one place and "120 days" in another | Pick one, name it; treat a mismatch as a definition difference until proven otherwise |
| Crypto price and ETF flow use equal row counts but different dates | Join BTC closes to actual ETF observation dates. Sum all N flow rows or subtract the pre-window cumulative value; subtracting the first in-window cumulative value drops one flow. |
| Last 30 funding settlements labelled 30 days | Group by UTC calendar day before daily statistics; state treatment of the incomplete latest day. |
| RSI label says Wilder but the value does not match | Recompute both Wilder and the simple mean of the last 14 changes; agreement with the latter diagnoses a smoothing mismatch. |
| Lead-lag asserted as a general law | Compute it per cycle; the relationship has not been stable across cycles |
| Point forecast presented as fact | Scenario + probability + confirming trigger |
| Probability quoted from one thin market | Second venue, liquidity check, then probability range |
| Correct script, stale report file | Verify the delivered file's contents, not just the script's exit code |
- Report check scoped to a whole section | Scope assertions to the entity row |
| Release note says “fixed” but the report body still contains stale values | Check every current-value occurrence (tables, scenarios, captions, dashboard) independently; recognize explicitly historical before/after values without letting them excuse stale current copies |
| Snapshot category names differ from prose labels | Enumerate raw categories and distinguish literal bucket matches, normalized synonyms, and explicit inclusion lists before comparing protocol counts |

## Support files

- `references/data-sources.md` — verified endpoint recipes, response shapes, and provider quirks
- `references/metrics-and-pitfalls.md` — metric definitions and the traps in each
- `templates/verify_report_numbers.py` — starter harness for the independent-recomputation gate
