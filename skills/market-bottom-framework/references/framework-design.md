# Framework Design

How to turn "where's the bottom?" into a layered framework with defensible thresholds.

## 1. Layers are questions, not indicators

A layer earns its place by answering a question no other layer answers. If two layers ask
the same thing, one is redundant.

| Layer type | Question it answers | Typical content |
|---|---|---|
| **Necessary condition** | what must be true for a bottom to be possible at all? | price depth, drawdown size, regime |
| **Leading condition** | what exhausts before price does? | leverage, forced-selling proxies, positioning |
| **Core confirmation** | what proves *new demand* arrived? | stablecoin supply, fund flows, issuance |
| **Quality metric** | what describes the *rebound* rather than the bottom? | participation breadth, dispersion, rotation |
| **Environment gate** | what invalidates everything else if it breaks? | credit spreads, systemic risk, policy shock |
| **Upside bonus** | what sets the rebound's height and duration? | new narratives, new category formation |

Order them by **causal time sequence**: necessary → leading → confirmation → quality →
environment → bonus. A reader should be able to trace the causal chain from the diagram
alone.

## 2. The threshold-evidence ladder

Every threshold you intend to act on carries one of these labels, and the label appears in
the deliverable:

| Label | Test it must pass | How to phrase it |
|---|---|---|
| **Validated** | pre-registered rule, fixed basket, baseline comparison, published false-positive rate, tested out of sample | "rule R, basket B, hit rate H vs baseline H0, out-of-sample" — the only tier that may carry a position instruction |
| **Backtested** | measured on the subject market's own history, in the condition where it is used | "X% of historical bottoms had this reading; median A" |
| **Descriptive** | a fact recomputed from raw data by an implementation independent of the one that produced it | "recomputed from [artifact]; recompute log at [path]" |
| **Prior** | logically sound, no testable data available | "assumes X; stated as an assumption" |
| **Market-priced** | someone else's number | "market-implied: X% (not our estimate)" |

Two constraints that keep the ladder honest:

- **Backtested requires independent cases.** Examples drawn from one liquidity regime are
  one case with several observations — they share the confound, so the effective sample is
  far below the count of examples. When cases cluster, the tier drops to Prior and the
  count is reported as "n observations across m regimes".
- **State the tier the document actually reaches.** If nothing is Validated, say that in the
  deliverable rather than letting the reader assume the ladder was climbed.

**A label of "refuted" is also valid** and must be published for any threshold you tried and
retired. This is the highest-value content in the whole document — it tells the reader what
the framework *cannot* do.

## 3. Choosing the subject market's universe

The subject market needs its own broad, liquid, long-history universe. Building one:

1. **Get a ranked list** from a source that defines the universe, not from a hand-picked
   list (e.g. market-cap ranking from an aggregator, index membership from the provider).
2. **Intersect with what is actually tradeable** on a venue you can price reliably.
3. **Exclude instruments that distort breadth**: stablecoins (they don't fall), commodity
   proxies, leveraged/inverse tokens (their price is mechanically derived).
4. **Filter by minimum history** so each asset contributes a comparable amount, and
   **report how many were dropped** — silent drops hide a shrinking denominator.
5. **Record the survivorship caveat explicitly**: a universe built from today's winners
   excludes the losers, which historically *inflates* measured breadth. State the direction
   of the bias, not just its existence.

## 4. Testing a metric: the sequence that works

```
1. State what the metric is supposed to predict, numerically, in advance.
2. Measure it at every historical turning point.
3. Ask: is the reading structurally extreme at every turning point?
   (If yes, it is a restatement of "the market fell", not new information.)
4. Test it unconditionally: does it separate the labeled classes?
5. Test it CONDITIONALLY: holding the variable you already use, does it add anything?
6. If it fails as an identifier, try the CHANGE from the trough instead of the level.
7. Publish both what it gets right and what it misses, with sample sizes.
```

Step 5 is the one most often skipped, and it is the one that catches the worst errors. A
metric can look useful in aggregate and be useless in the exact regime you care about.

## 5. Distinguishing "trend health" from "turning point"

A level can be genuinely predictive of *forward returns* while being useless as a *turning
point detector*. These are different jobs and the distinction matters:

| Job | What the level tells you | When it works |
|---|---|---|
| Turning-point detection | "the turn is here" | the level must be extreme **at** the turn |
| Trend health | "the prevailing direction is more likely to continue" | the level must differ **between** regimes |

If a metric's high values occur *after* turns (because high participation means the rally
is already underway), then it is a trend-health metric, and using it as a bottom
confirmation is causal inversion — the signal fires when you are already late.

Say this plainly in the deliverable. It is a common trap and readers cannot see it without
being told.

## 6. The theory document's job

The conclusion report says *what* the call is. The theory document says *why it is
trustworthy*. It must contain:

1. The problem the framework addresses, and why the obvious approach fails
2. The layer taxonomy with each layer's question
3. Each threshold: value, derivation, sample size, evidence label
4. **Refuted thresholds** and what replaced them
5. Known limitations, split into:
   - data limits (what you could not obtain)
   - statistical limits (sample size, survivorship, in-sample)
   - structural limits (what this framework fundamentally cannot see)
6. How to reproduce: script names, dependency order, raw data locations

The dependency order matters and must be stated — scripts that consume one another's output
run out of order silently and produce stale numbers that look fine.

## 7. Tail-mechanism classes differ between markets

Porting a framework across markets means **rebuilding the factor set**, not translating
it: the dominant tail mechanism differs by market class, and a factor set carried over
from the reference market will look complete while missing an entire layer.

| Subject market | Dominant tail mechanism | Where its probability can live |
|---|---|---|
| Equities | macro / credit / geopolitical shock | forward curves, policy pricing, prediction markets |
| Crypto | mechanism failure — depeg, exploit, exchange or custodian insolvency, bridge failure, stablecoin run | protocol-level history, on-chain and counterparty evidence; largely NOT derivatives |

Two rules follow.

1. **The reference market stays a transmission input.** Its factors say how a shock
   would arrive; they never supply the subject market's tail base rate.
2. **No market price for the mechanism means a base rate, not an implied distribution.**
   When the mechanism class has no derivative or prediction-market price, build a
   historical base-rate table with an explicit denominator — events per exposure-year —
   rather than borrowing an implied distribution from a price path. Without a
   denominator the number cannot be compared with anything.

| Field | What to record |
|---|---|
| mechanism class | the failure type itself |
| event date | the settlement date, not the announcement date |
| denominator | exposure at risk over the same span (assets-years, bridges-years, custodians-years) |
| loss severity | measured in the affected asset, not in the announcing headline |
| survivor note | assets/bridges/custodians that failed without ever being in the sample |

## 8. What the reader should be able to do afterwards

A good framework lets the reader:

- disagree with a specific threshold and see what changes (thresholds are visible and
  parameterized, not buried in code)
- update the data without re-deriving the logic (the pipeline is scripted and ordered)
- see exactly where the framework is weak (limits are stated, not implied)
- trust the numbers without opening a JSON file (readable views exist)
- verify the whole thing themselves (reproduction instructions exist)