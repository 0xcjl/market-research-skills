# Early-warning playbook: layers, tests, dashboard

## 1. The layer stack

Order layers by causal time sequence: each layer answers a different question. A layer that
repeats another layer's question is redundant.

| Layer | Question | Typical instruments |
|---|---|---|
| Liquidity | is new money entering the system at all? | stablecoin supply growth, ETF net flows, exchange balances, net liquidity proxies |
| Market structure | is capital rotating from the leader into the crowd? | leader dominance, altseason index, total market cap ex-leaders, ETH/BTC, alt vs BTC volatility |
| Attention | is anyone talking about the theme, and how fast is it accelerating? | mindshare / social-share metrics, search trends, social post volume, prediction markets |
| Capital and institutional flow | who is committing size, and when? | public venture rounds and their thesis, exchange listing cadence, treasury and company filings |
| On-chain behaviour | are users actually doing the thing? | active and new addresses, contract deployments, DEX volume share, gas anomalies, smart-money holdings |

Liquidity is a precondition, not a trigger. Structure tells you rotation is possible.
Attention tells you a theme is forming. Capital flow tells you it is being sized. On-chain
behaviour tells you it is real rather than marketing. A theme usually needs all five, in
that order — and the playbook's edge lives in the gap between "forming" and "being sized".

## 2. Leading vs confirming — how to test it

A signal is **Leading** only if it moved before price in at least two independent historical
cases (different themes, different windows). Two cases is a floor, not proof; label it
Backtested only when the cases are documented with dates and sources.

"Independent" means independent of the *liquidity regime*, not merely different months.
Two themes that both ran on the same 2020–2021 easing impulse are one case with two
observations: the shared confound is what made both lead. When the supporting cases come
from one regime, the rule is a Prior and the document says how many regimes it survived
("3 observations across 2 regimes") rather than how many charts it appears on.

| Label | Test | Use |
|---|---|---|
| Leading | moved before price in ≥2 independent cases, with dates | entry timing |
| Confirming | moved with or after price | sizing and exit, never entry |
| Prior | sound reasoning, no testable case yet | hypothesis to monitor, not a rule |

A signal that is structurally extreme at every narrative peak (for example, social volume at
its maximum) is a **peak detector, not an entry signal**. Say so explicitly, or the playbook
will tell the reader to buy the top.

The test that matters most is the one that can fail: for each claimed leading signal, ask
what the signal looked like in the windows where narratives did NOT become hot. A signal
that never reads high in a quiet window is not a narrative detector.

## 3. Narrative lifecycle stages

| Stage | What it looks like | Signal set |
|---|---|---|
| Seed | one or two projects, no narrative, no attention | new contract deployments, first public venture round, first mention by a large account |
| Build | a basket of copycats, the community names the theme | mindshare rising, topic tag volume rising, listings clustering |
| Mainstream | the theme is understood by non-crypto press and institutions | index inclusion, treasury or ETF interest, derivative listings, institutional research |
| Overheated | price detached from usage; leverage and memes dominate | funding extremes, negative funding on dips, parabolic moves with no new functionality |
| Decay | a new narrative takes the attention; price breaks lower | attention migrates to the next theme; breadth narrows to the original leaders |

The playbook's value is the **Seed → Build** transition: that is where a theme can still be
bought before the mainstream. Mainstream is confirmation; Overheated is the exit signal.

## 4. Weekly dashboard template

One table per layer, plus a lifecycle read.

| Indicator | Source URL | Layer | Frequency | Reading | Class | Threshold to act | Failure mode |
|---|---|---|---|---|---|---|---|

Rules:
- Every row has a source URL a reader can open without an account.
- The Class column is populated (Leading / Confirming / Prior) — an unclassified row is decoration.
- The Failure mode column is mandatory: the condition under which the indicator lies (a metric that can be gamed, a source that stops publishing, a signal that only works in bull markets).
- Readings are stamped with their as-of date and use the last settled value.

## 5. Apply-to-present section template

> **Where the market is now** — as-of [date], phase [phase], [drawdown] from the [reference
> peak and its date].
>
> **Historical windows that resemble this** — which past windows shared this phase, and what
> happened in each.
>
> **Signals currently hot / cold** — each reading with its source and its class.
>
> **What would flip the read** — the observable that changes the phase call, and what would
> refute the playbook's rules.

Two rules for this section specifically:

- **Label the phase read as undetermined when it is.** A phase call made in real time from a
  shape is always fuzzier than the same call made in a retrospective; when the shape admits
  both "final low" and "mid-decline continuation", write "undetermined" and give the
  observable that would settle it. Deciding the phase because the reader wants an answer is
  the same failure as a threshold defended after its test refuted it.
- **Mark the priority order as a posture, not an output.** "Watch the building-type
  candidates first" is a risk-posture choice; say whose and why. Do not let it read as the
  model's ranking, and do not turn the list into an allocation instruction — the
  playbook's tiers usually do not reach the level that supports position sizing.

## 6. Failed / abandoned narrative discipline

Keep a second list beside the winners: narratives that were seeded, named, and died without
becoming a mainstream theme. For each: what seeded it, how long it lived, why it died.

Why it matters:
- The historical record is survivor-biased — retrospectives remember the winners.
- Without this list you cannot tell whether a leading signal predicts narratives or merely
  predicts that a theme became famous enough to be written about.
- Every rule derived from the merged winners set must be re-checked against it: does the
  signal also fire on the failures? If it never does, it is a fame detector, not a narrative
  detector.
