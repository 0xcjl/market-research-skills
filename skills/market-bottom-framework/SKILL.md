---
name: market-bottom-framework
description: Use when locating market bottoms with a layered framework.
license: MIT
allowed-tools: Bash, Read, Write, Edit, WebFetch
metadata:
  version: 0.2.0
  author: Helen
  hermes:
    tags: [market-research, bottom-finding, framework, backtest, crypto, equities, multi-agent-verification]
    category: research
    related_skills: [research/market-performance-research, research/market-narrative-cycle-research, research/polymarket, research/claim-verification, research/crypto-token-due-diligence, communication/agent-output-format-scan-first]
---

# Market Bottom Framework

Build a layered, evidence-backed framework for locating market bottoms — where the bottom is,
when it arrives, and what confirms it — and publish it with the reasoning, the threshold
justifications, and the failure conditions all visible.

## When to Use

- "帮我找底" / "底部在哪" / "什么时候反转" / "跌完了吗" / "现在能不能抄底"
- a bottom or top call that must name a level, a window, and a confirmation signal
- a layered framework where each layer answers a different question
- "不要我说一点你加一点，我要一个整体的分析框架"
- any deliverable that claims a threshold is justified

## Not for

| Task | Use instead |
|---|---|
| performance/drawdown stats with no bottom call | `market-performance-research` |
| a cycle history of market themes/narratives + a forward monitoring playbook | `research/market-narrative-cycle-research` |
| on-chain token contract, tax, and liquidity risk | `research/crypto-token-due-diligence` |
| fact-checking a third party's claim | `research/claim-verification` |
| prediction-market API mechanics | `research/polymarket` |
| output format, source links, delivery location | `communication/agent-output-format-scan-first` |

## The rule that decides this task

**A threshold you cannot show the evidence for is a guess wearing a number's clothes.**

Every threshold in the delivered framework must be traceable to one of the labels below, and
the label must be stated in the document:

| Label | Meaning | Where it comes from |
|---|---|---|
| **Descriptive** | a fact recomputed from raw data by an implementation independent of the one that produced it | the artifact plus the recompute log |
| **Backtested** | derived from the measured distribution at historical turning points | a backtest over the asset's own history |
| **Prior** | logically sound but no testable data | stated as an assumption, not a finding |
| **Market-priced** | someone else's number | labeled as such, never presented as your own |

One tier sits above all of them: **Validated** — a pre-registered rule, a fixed basket, a
baseline comparison and a published false-positive rate, tested out of sample. Only a
Validated rule may carry a position instruction. A framework whose rules stop at Backtested
must say so in the document, in those words, rather than letting the reader assume the
ladder was climbed.

**Backtested requires independent cases.** Examples drawn from one liquidity regime are one
case with several observations — they share the confound, so the effective sample is far
below the count of examples. When cases cluster, the tier drops to Prior and the count is
reported as "n observations across m regimes". A rule's strength is the number of
independent regimes it survives, not the number of charts it appears on.

And when a backtest **refutes** a threshold you designed, the threshold gets changed — not
defended. Design the test before you look at the result, and report the refutation as loudly
as the confirmation.

## Workflow

### 1. Fix the measurement contract

Pin before fetching: universe (exact constituents + the source that defines them), as-of
trading day, what each period means numerically, peak reference (ATH vs 52w vs YTD), return
convention, and the **window unit** (trading sessions vs calendar days — mixing these is
the single most common source of a wrong number).

Pin the **window direction** as well: for a window anchored at a turning point, state
whether it looks BACKWARD from the anchor (the 90 days leading into it) or FORWARD from
it (the 90 days after it). Both are legitimate and they differ in sign. Two people
checking the same published number can each be right, and a disagreement that looks like
a defect is really two conventions colliding — confirm the direction before you call
anything mismatched, and put the direction in the measurement contract you hand to an
auditor.

**Every filter against an external taxonomy must be proven to match.** A category
filter that returns zero rows is a filter bug far more often than an empty category: a
singular/plural mismatch in an API's own category label silently yields an empty set,
and every number derived from it is wrong while looking perfectly plausible. Assert a
non-zero — and where the taxonomy is known, an exact expected — match count for every
category filter, and log the raw label values you filter on so the next reader can see
what the source actually calls the thing.

**Write the unit into the artifact, not only into the prose.** A percentile computed over
500 observations is not "500 days" — with 8h bars it is ~167 days, and a document that
prints the observation count as a calendar unit inherits that error permanently, because
the wrong unit can never be re-derived from the artifact. Every windowed metric in the
JSON carries its own unit and span (`window: {unit: "period", n: 500, period_hours: 8,
calendar_days: 167}`), and the document renders the label from that field rather than
typing it. When two defensible windows exist (500 periods vs 500 calendar days), emit
BOTH as separate fields — the label error and the truncation error then stop being
reachable.

### 2. Build the frame as layers, not as a list

The user names some indicators. The framework must cover the layers you believe matter,
named or not. Order layers by **causal time sequence**, and give each layer a different
question to answer:

```
necessary condition  →  what must be true for a bottom to be possible
leading condition   →  what exhausts first (forced selling)
core confirmation   →  what proves new demand arrived
quality metric      →  what describes the rebound, not the bottom
environment gate    →  what invalidates everything else if it breaks
upside bonus        →  what sets the rebound's height
```

State each layer's **question**, not just its indicators. A layer whose question duplicates
another layer's is a redundant layer.

### 3. Choose the subject market before the reference market

The market you are analyzing supplies the thresholds. A reference market is a **transmission
factor**, never the threshold source.

| Mistake | Why it fails |
|---|---|
| Deriving a crypto breadth threshold from equity breadth | circular — crypto bottoms don't happen because equities bottomed |
| Using the reference market as the "core" layer | causality runs one way; the reference has no claim on the subject's timing |
| Building the subject's universe from the reference's constituents | different participant sets, different breadth |

If the subject market has no broad, liquid, long-history universe of its own, **build one**
before running any breadth test (see §5).

**Porting a framework across markets means rebuilding the factor set, not translating it.**
The dominant tail mechanism differs by market class — equities fail through macro, credit
and geopolitical shocks; crypto fails through mechanism failure (depeg, exploit,
insolvency, bridge). A framework carried over from the reference market will look
complete while missing an entire layer, and the reference market's factors stay
*transmission* inputs only, never the tail base rate. When the mechanism class has no
derivative or prediction-market price, the probability comes from a historical base-rate
table with an explicit denominator. Mechanism classes and the base-rate recipe:
`references/framework-design.md`; crypto data sources and their coverage limits:
`references/crypto-market-data-apis.md`.

### 4. Backtest every threshold you intend to publish

Minimum viable test for any threshold:

1. **Sample**: the subject market's own history, broad universe, longest available.
2. **Label**: what counts as success, defined numerically and in advance
   (e.g. "true bottom" = +15% within 120 days).
3. **Baseline comparison**: is the metric better than the alternative the framework already
   uses? If depth already predicts the outcome, a second metric adds nothing.
4. **Report both directions**: what the metric gets right AND what it misses.

**Always test the metric in the condition where it will actually be used.** A metric can
look useful unconditionally and be useless conditionally — e.g. a level that is near-zero
exactly when you need it to read high is a restatement of the thing you already know, not
new information.

### 5. If the metric can't identify the turning point, use its level differently

When a level is structurally extreme at every turning point (e.g. breadth sits at ~0% on
every bottom because everything is below its own moving average after a crash), then:

- it is **not** a bottom identifier — say so, and retire it as one
- its **change from the trough** is often the usable signal
- its **absolute level** may still work as a *context* filter (e.g. "low breadth + shallow
  drop = still falling") — verify that separately

A metric used in the wrong role is worse than no metric: it produces confident
recommendations that are structurally impossible to time correctly.

### 6. Verify with independent agents — this is not optional

**A single agent that collects, analyses, writes, and verifies its own work will inherit its
own assumptions into its own validation.** This is the failure mode that matters: not that
the code crashes, but that the same blind spot survives every check because the same mind
produced the claim and the test of the claim.

**Requirement**: spawn at least **two** independent sub-agents for verification, with
**different scopes** so they check different failure modes:

| Agent | Scope | Must NOT |
|---|---|---|
| **Recomputation** | re-derive every published number from raw data using a fresh implementation | import any of your analysis modules |
| **Methodology** | attack the framework's logic: contradictions, overclaiming, causal inversion, evidence strength | edit the deliverables — report findings only |

Recommended third: **statistical audit** of the backtests themselves (look-ahead bias,
survivorship bias, sample size, window-unit consistency).

Give each agent: the deliverable paths, the raw data paths with **format descriptions**,
the exact numbers to check, the **measurement contract** (window units, formulas), and an
explicit instruction that it must not modify the deliverables. Instruct agents to write
findings to files so you can read them in full rather than through a summary.

These briefs assume a **quantitative backtest** to recompute. A timeline or narrative
deliverable has no backtest, so the equivalent independence comes from re-deriving dated
claims against their cited sources and from attacking the causal story — use the adapted
fact-re-derivation and causal-attack briefs shipped with
`research/market-narrative-cycle-research` (its narrative-schema-and-briefs support file).

**A sub-agent's report is a self-report, not a verified fact.** Read the findings files
yourself. Then decide, per finding: fix it, or record why not. A finding you dismiss must
have a stated reason.

**Then run your own mechanical check** as a third layer. It catches what reading does not:
numbers that drifted between the data and the prose.

### 7. Publish for a reader, not for a parser

Machine-readable artifacts are working files, not deliverables. **A reader who cannot open
JSON must still be able to use everything.**

| Deliverable | Purpose |
|---|---|
| Conclusion report | the call, the evidence, the scenarios, the confirmation checklist |
| **Theory/threshold document** | each layer's question, each threshold's evidence label, the reasoning, the known limits |
| **Human-readable data views** | every JSON rendered as tables; the numbers a reader acts on |
| **Data-file guide** | what each artifact is, what each field means, how to query it yourself |
| Machine artifacts (JSON) | reproducibility; reference them in the guide |

State in the theory document which thresholds were **refuted** and what replaced them. A
framework that only shows its working parts hides exactly the part a reader needs to judge
it.

### 8. Mechanical verification before delivery

Independent of the agents, run a script that checks:

- every analysis script runs clean, in dependency order
- artifacts exist, parse, and are non-empty
- the deliverable **file actually contains** the numbers the data produces
- the thresholds and claims in the prose match the artifacts
- prior deliverables were not modified

**A correct script with a stale report is a failed deliverable** — the file check is what
catches that.

Eleven rules govern this stage. Each one is not a preference; each one exists because
breaking it shipped a wrong number once. Full prose: `references/mechanical-verification.md`.

1. **Verification is a pipeline stage, not a one-off.** The verifier lives with the
   pipeline, is named `verify_pipeline.py`, and is listed in the pipeline's own run order
   and in the delivered documentation.
2. **The verifier must not import the metric code it verifies.** A shared implementation
   reproduces the same bug on both sides of the check. The verifier should also assert its
   own independence.
3. **Seal every series to the last fully-settled bar.** A bar dated `d` is settled iff
   `d < today (UTC)`. One as-of rule across the whole deliverable.
4. **Generate prose tables from the artifact.** Hand-typed tables drift silently.
5. **Make idempotency a checked property, and delete by a stable marker** — never by the
   rendered content, and strip the trailing blank line with the marker.
6. **Check that a baseline was not silently degraded.** Assert the baseline DATE, not just
   the resulting value.
7. **Assert the fix is load-bearing.** A silent-truncation fix is invisible to every
   ordinary check; assert coverage, not shape.
8. **Update prose after a recompute by context anchor, never by value.** The same literal
   can mean different things in different contexts; historical readings are frozen.
9. **Add a focused verifier per generator, and give it teeth.** A verifier never observed
   to fail has not been tested — mutate copies of the deliverable and require a non-zero
   exit on each.
10. **Treat an auditor's findings as a timestamped snapshot.** Never write an auditor's
    replacement value into a deliverable verbatim; re-derive it. And re-check your own
    anchor direction before calling a number wrong.
11. **The verification run is the last gate, and it must be labelled honestly.** Any edit
    after the run re-opens the gate. An ad-hoc assertion script is not "the test suite is
    green" — report what it asserts, how many assertions, the exit code, and where the
    log and the script are persisted. Do not delete the script after a green run.
Reporting shape

- Conclusion first; then the evidence; then the limits.
- Separate **facts** / **historical reference** / **inference** / **subjective scenario weights**
  explicitly. Scenario weights are judgment, and must be labeled as such.
- For each threshold: the value, the source of the number, the evidence label.
- State which tier the document's rules actually reach — and, when none is Validated, say so
  plainly so the reader does not mistake a Backtested threshold for a tradeable rule.
- Give **falsification conditions** — what would prove the call wrong, and what to watch.
- Give a **monitoring checklist**: indicator, current reading, threshold to flip, data source,
  how often to check.

## Pitfalls

| Pitfall | Guard |
|---|---|
| Threshold tuned on the same history it is validated on | state that it is in-sample; prefer out-of-sample or disclose |
| Metric that is mechanically extreme at every turning point | test it in the condition where it will be used |
| Reference market's breadth used for the subject market | build the subject's own universe |
| Confident scenario percentages from a small sample | label as subjective judgment, give ranges |
| One agent verifying its own work | two independent agents, different scopes, findings to files |
| **Verifier imports the metric code it verifies** | re-implement independently in the verifier; a shared bug passes on both sides |
| **Verifier lives only in a temp script** | keep a canonical `verify_pipeline.py` with the pipeline; list it in the run order |
| **Missing raw input silently shrinks the sample** | abort with the filename; never continue on a smaller universe |
| **Retracted numbers still quoted in the prose** | assert old values appear only inside correction notes |
| Report numbers correct but prose describing an older version | mechanical check that the prose matches the artifacts |
| Deliverable is JSON-only | human-readable views for every artifact |
| Threshold defended after its test refutes it | change the threshold; report the refutation |
| Causal inversion (leading indicator asserted as confirmation) | state which direction the evidence supports |
| "Improvement over the previous report" that silently changes the framework | version the framework; list what changed and why |
| **Reading a still-forming daily candle as a close** | seal every series to the last fully-settled bar; see below |
| **Two panels of the same report using different cutoffs** | one as-of rule for the whole deliverable |
| **Prose tables hand-typed from computed numbers** | generate the tables from the artifact; a hand-typed table drifts |
| **A metric labelled with the wrong unit** (periods vs days, events vs sessions) | name the window and the count explicitly |
| **Baseline silently degraded when the source series starts late** | assert the baseline date; fall back to a longer history, not to a nearby date |
| **Global string replace of a changed number** | anchor replacements by context and assert hit counts; historical readings are frozen |
| **Verification run predates the last edit** | run the verifier after the final edit; a pre-edit pass proves nothing about the delivered code |
| **Duplicated helper copied back after DRY convergence** | assert no module defines a helper it also imports from the shared module |
| **Verifier that has never been observed to fail** | mutate copies of the deliverable; require a non-zero exit on each mutation |
| **Category filter against an external taxonomy matches zero rows** | assert a non-zero / expected match count; log the raw category labels |
| **Auditor's replacement value written in verbatim** | re-derive from the artifact; the auditor's snapshot predates your edits |
| **Dead-code check run one file at a time** | scan the whole tree — a shared helper looks uncalled from inside one file |
| **Batch text edits to import lines** | re-import every edited module and confirm each name it uses resolves |
| **Verification script deleted after a green run** | leave it at the `hermes-verify-` path and persist a copy beside the log |
| **Truncation / wrong-subset fix with no coverage assertion** | assert the artifact reaches further back than the unchunked request, and that the sample used is the longest available |
| **Window unit typed into the prose instead of the artifact** | emit unit + count + calendar span in the JSON; render the label from it |
| **Framework carried to a new market with the old factor set** | rebuild it for that market's tail-mechanism class — see the mechanism-class rule in §3 |
| **Example count used as sample size** | count independent regimes, not charts; clustered cases demote the tier |
| **Aggregate claim never re-derived from the item-level ledger** | publish the ledger; re-derive the aggregate from it, downgrade to the surviving count and publish the counterexamples |
| **A tier label that reads as permission to trade** | only a Validated rule may carry a position instruction; state plainly which tier ceiling the document reaches |
| **Partial-period return published under a full-period label** | name the base date and the window end; a YTD figure computed from the prior year-end close is not the half-year figure |
| **Percent recomputed with float arithmetic in a verifier** | use `Decimal` with an explicit rounding rule on both sides — `0.145 * 100` is `14.499999999999998`, so half-up of 14.5 rounds to 14 |

## References

- `references/mechanical-verification.md` — the eleven pipeline-stage rules behind §8
- `references/framework-design.md` — layer taxonomy, threshold-evidence ladder, worked example
- `references/verification-protocol.md` — the multi-agent verification briefs, verbatim
- `references/artifact-verification.md` — focused-verifier recipe: idempotency, mutation test, cross-document equality
- `references/market-universe-building.md` — building a broad, survivorship-aware universe
- `references/crypto-market-data-apis.md` — crypto tail-risk data sources: Deribit DVOL/options window quirks, prediction-market coverage limits, base-rate denominators