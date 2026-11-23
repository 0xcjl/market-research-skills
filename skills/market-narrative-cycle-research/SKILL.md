---
name: market-narrative-cycle-research
description: Use when mapping narrative cycles into early-warning rules.
license: MIT
allowed-tools: Bash, Read, Write, WebFetch
metadata:
  version: 0.2.0
  author: Helen
  hermes:
    tags: [market-research, crypto, narrative, cycle, early-warning, multi-agent-research]
    category: research
    related_skills: [market-research, research/market-performance-research, research/market-bottom-framework, research/claim-verification]
---

# Market Narrative Cycle Research

Study how market themes are born, amplified, peaked and killed on a repeating cycle, then
publish a playbook that lets a reader catch the next theme **before** its price move.

## When to Use

- "每半年一轮热点叙事，把历来的怎么起来、怎么灭的挖出来"
- "做一份热点叙事抓取指南 / 早期预警清单"
- "AI 叙事为什么一直不冷？下一波在什么条件下起来？"
- "我想在涨起来之前抓到下一个叙事"
- any deliverable whose substance is a cycle history plus forward monitoring rules

## Not for

| Task | Use instead |
|---|---|
| quantifying one asset's returns / drawdown / tail risk | `research/market-performance-research` |
| locating a bottom with a layered framework | `research/market-bottom-framework` |
| qualitative company / competitor / market-sizing research | `market-research` |
| fact-checking one third-party claim | `research/claim-verification` |

## The rule that decides this task

**A chronology is not a playbook.** Every narrative entry must carry what was *observable
before it peaked* — with a lead time — or it contributes nothing to catching the next one
early.

And the user's cadence ("roughly every six months") is a **hypothesis to test**, not a binning
scheme to satisfy: measure the actual spacing between narrative peaks, report the
distribution, and say plainly where the rhythm holds and where it breaks. Forcing entries
into half-year buckets to match the user's impression is the failure mode this step exists
to prevent.

Use the evidence ladder from `research/market-bottom-framework` for every rule in the
playbook — **Descriptive** (a fact recomputed from raw data by an independent
implementation) / **Backtested** (measured distribution at historical turning points) /
**Prior** (sound but untested, or one narrative's recollection) / **Market-priced** (someone
else's number) — with **Validated** (pre-registered rule, fixed basket, baseline comparison,
published false-positive rate) sitting above them all. A rule that only one narrative's
memory supports is a Prior, not a finding.

Two rules about tiers decide how a playbook reads, and both come from audits that found
over-claiming:

- **Independence beats count.** "Moved before price in ≥2 cases" is a floor, not proof.
  Cases drawn from one liquidity regime are one case with several observations — they share
  the confound, so a rule built only on them is a Prior. Report how many independent regimes
  a rule survived, not how many charts it appears on.
- **A narrative playbook rarely reaches the top tier.** If no rule is Validated, the document
  must say so in those words and stop at observation and cross-confirmation — no position
  instructions, no "this is the entry point" language, and no "build a position when stage
  two is confirmed" phrasing. The apply-to-present section may still rank what to watch, but
  label that ranking as the author's risk posture, not as a model output.

## Workflow

### 1. Pin the measurement contract before dispatching anything

| Item | Pin it as |
|---|---|
| Period | exact date range, split into named sub-windows |
| Window unit | calendar days vs trading sessions — say which |
| Period return base | last close strictly BEFORE the window opens |
| As-of | last fully settled bar; today's forming bar excluded everywhere |
| Narrative unit | what counts as one narrative (a theme with its own basket) vs a branch of an existing theme |
| Peak reference | the theme's own peak, not the market's |
| Lead time | pre-peak signals expressed in weeks before the peak |

### 2. Build the cycle spine yourself, from a primary series

Before any researcher is dispatched, pull the price series and compute the spine: period
returns, per-window highs and lows, ATH and drawdown, and the phase each sub-window sits in
(bear bottom / recovery / mid-bull / blow-off / unwind / bear-side chop).

Take numbers from the exchange or provider series, not from search snippets — search results
for a recent price routinely disagree with the settled close, and every sub-agent annotating
against the spine must see the same one.

`scripts/fetch_cycle_spine.py` pulls daily klines from a public exchange API, caches the raw
CSV, computes the windows and anchors, seals to the last settled bar, and writes
`cycle_spine.json`.

### 3. Dispatch by time window, one shared schema

Split the history into disjoint sub-windows and give each researcher one. Disjoint windows
plus one identical entry schema is what makes the merged table comparable; overlapping
windows with free-form notes are not a timeline.

Each brief must be self-contained (sub-agents see none of this conversation) and carry:

1. the window and the entries it must cover
2. the shared entry schema, verbatim
3. the spine anchors to annotate against, so every researcher places its narratives on the same cycle
4. the source rule
5. the absolute output file path and the instruction to write nothing else

Template: `references/narrative-schema-and-briefs.md`.

### 4. Source rule for every entry

Every dated claim carries its URL on the same line. First-hand preferred: protocol docs,
project blogs, exchange/provider APIs, regulator and exchange filings, original reporting.
Aggregators are context, not proof. Inference is labelled **推断**; anything untraceable is
labelled **未验证** and stays visible rather than being quietly dropped.

### 5. Extract the pre-peak signals — the actual product

For each narrative, back-fill what was observable 1–3 months before the peak and how long
before. Candidate families: capital raising and public VC theses, developer activity, social
and search attention, exchange-listing confirmation, distribution channel (app store,
messaging app, wallet), on-chain new-address and contract-deployment acceleration, TVL and
volume-mix shifts.

Classify each signal **Leading** (moved before price in ≥2 cases that are independent —
different themes AND different liquidity regimes; clustered cases demote it to Prior),
**Confirming** (moved with or after price — useful for sizing, useless for entry), or
**Prior**.

Keep a **failed / abandoned narrative list** beside the winners. Narratives get catalogued
from the survivors — what a retrospective remembered is what got written down — so a playbook
fitted only to winners will promise leading signals that do not lead.

### 6. Build the playbook as layers

The monitoring layer stack (liquidity → market structure → attention → capital and
institutional flow → on-chain behaviour), the narrative lifecycle stages, the weekly
dashboard shape and the apply-to-present section are in
`references/early-warning-playbook.md`. Each layer states: question, indicator, source URL,
check frequency, leading-vs-confirming, the historical case that validates it, and its
failure mode.

### 7. Apply the playbook to the present, as a dated section

The user buys a playbook to act on now. Close with where the market sits on the spine
(as-of date, phase, drawdown), which historical windows that resembles, and which signals
currently read hot or cold — each with its source.

### 8. Verify before publishing

- Two independent agents, different scopes: one re-derives the dated claims from first-hand
  sources and flags any claim whose cited URL does not support it; the other attacks the
  causal claims for overclaiming, selection bias and unfalsifiable rules. Both write findings
  to files; briefs in `references/narrative-schema-and-briefs.md`.
- Read the findings files yourself and give every finding a disposition — fix, disclose, or
  dismiss with a stated reason. A sub-agent's report is a self-report, not a fact.
- Then your own mechanical pass: every URL in the delivered file resolves, every table row
  matches the artifact, every lead time is in weeks and consistent with the timeline it hangs
  on, and every number in the prose matches the JSON.
- Publish the item-level ledger (`narrative_ledger.json`) beside the document — one row per
  narrative with its window, class, event-cluster tag and independent-onset flag, plus the
  gap rows — and make every aggregate claim in the document re-derivable from it. When the
  ledger contradicts an aggregate you already wrote ("all gaps fall in bear markets"),
  downgrade the aggregate to the count that survives, publish the counterexamples in the
  document, and demote the rule to the lower tier. Schema and the empty-month vs
  endpoint-distance distinction: `references/narrative-schema-and-briefs.md` §5.
- Persist the audit dispositions as an artifact (`audit_dispositions.md`): finding id,
  verdict, what changed, and the reason for any dismissal. A finding dispositioned only in
  chat is not dispositioned — the next reader cannot see why it was closed. Format:
  `references/narrative-schema-and-briefs.md` §6.

## Pitfalls

| Pitfall | Correction |
|---|---|
| The deliverable is a well-sourced chronology | Every entry carries a pre-peak signal with lead time, or it is not a playbook |
| Leading signals drawn only from the winners | Keep the failed / abandoned narrative list; survivors-only samples overfit the signal set |
| A rule recalled from one narrative presented as a law | Label Backtested / Prior / Market-priced; one recollection is a Prior |
| Calendar-month distances treated as counts of complete empty months | Distinguish endpoint distance from intervening empty months, log the real-time alert date, and handle unfinished tail gaps separately; otherwise the historical hit count need not describe the deployed rule. |
| The user's stated rhythm forced onto the table | Measure the actual spacing and report where the rhythm breaks |
| Search snippets used for prices and recent events | Use the exchange/provider series for numbers; search only to locate sources |
| Today's forming bar read as a close | Seal every series to the last fully settled bar; label in-progress windows partial |
| A partial window's return quoted as a window return | Mark the window partial and state its end date |
| Overlapping sub-agent windows, free-form outputs, hand-merged | Disjoint windows + one shared schema + mechanical merge |
| Sub-agent brief assumes conversation context | Briefs are self-contained: window, schema, anchors, source rule, output path |
| The findings file trusted from its summary | Read the file in full; disposition each finding |
| Branch narratives folded into their parent theme | Keep branch vs main distinct — branch → main promotion is itself a signal |
| "This theme is structurally different" asserted without a case | Same measurement contract for every theme; the exception is a claim to be tested, not a premise |
| Narrative activity counted as independent onsets | Count first-ignitions, not news items or re-ignitions; tag each row with its event cluster and publish the ledger so the count is checkable |
| An aggregate claim ("all gaps fall in bear markets") that the item-level ledger contradicts | Re-derive the aggregate from the ledger; downgrade it to the surviving count, publish the counterexamples, and demote the rule |
| Examples from one liquidity regime treated as independent cases | Count independent regimes, not charts; clustered examples demote the rule to Prior |
| A density or ranking statistic computed on retrospectively labelled phases | Disclose boundary sensitivity and give a flip example where a different boundary changes the ranking |
| Apply-to-present section recommends an action with no stated risk posture | Label it as the author's posture under a stated preference, not a model output |
| Conditions written so they cannot fail ("if X then Y") | Stage them in time, number them, and pair each with the false-positive/false-negative calibration it would need |
| Audit findings dispositioned in chat only | Persist the disposition table with a reason for every dismissal |

## Support files

- `references/narrative-schema-and-briefs.md` — entry schema, dispatch brief template, verification briefs for timeline deliverables, merged-ledger schema (§5), audit disposition format (§6)
- `references/early-warning-playbook.md` — layer stack, leading-vs-confirming test, lifecycle stages, dashboard and apply-to-present templates
- `scripts/fetch_cycle_spine.py` — pull daily klines, cache, compute windows and anchors, seal to the last settled bar
