# Multi-Agent Verification Protocol

The requirement in §6 of SKILL.md. Copy these briefs, fill the bracketed slots, and dispatch.

## Why this is mandatory

The failure mode is not a crashing script. It is **an assumption that survives every check
because the same mind produced both the claim and the test of the claim**. A single agent
that collects, analyses, writes, and verifies will do this reliably.

Independent agents fail in a different way — and that is the point: they fail *loudly and
early* rather than silently and permanently.

## Rules

1. **At least two agents**, with **different scopes**. Two agents checking the same thing
   is not independence.
2. **Different models where possible** — a different model family makes shared blind spots
   much less likely.
3. **Agents must not edit the deliverables.** They write findings to files; you decide.
4. **Give raw data paths WITH format descriptions.** An agent that guesses a format will
   report false mismatches, and you will waste a cycle chasing them.
5. **Give the measurement contract** — window unit, formula, baseline convention. Without
   it, "mismatch" is ambiguous.
6. **Read the findings files yourself.** A sub-agent's summary is a self-report.
7. **Every finding gets a disposition**: fixed, or dismissed with a stated reason.

## Dispatch mechanics

```python
delegate_task(tasks=[{
    "goal": "<one-line objective>",
    "option": "dev",            # avoid the 'fast' tier: it routes to a model
                                 # that may not support the service tier
    "context": "<the brief below>"
}])
```

If a dispatch fails with `service_tier 'fast' is not available`, set `"option": "dev"`.

Agents run in the background; results re-enter as new messages. Do not poll their
transcripts. Do work that doesn't depend on them, then end the turn.

When a finished agent cannot be resumed (`action="continue"` errors or returns nothing),
dispatch a **fresh** auditor instead of retrying the resume. A fresh auditor has no
anchoring on the previous round's findings, so it is usually the stricter check — and it
re-derives the numbers rather than re-checking the earlier list.

---

## Brief A — Independent recomputation

> You are an independent auditor. Recompute every number in these reports from raw data
> and determine whether any published figure disagrees with the source.
>
> **Deliverables under test**: [paths]
>
> **Raw data**: [paths, each with a format description — see below]
>
> **Numbers to verify**: [list, one per line, with the exact expected value]
>
> **Measurement contract**:
> - Window unit for time windows: trading sessions vs calendar days (state which)
> - RSI: [exact smoothing convention]
> - Moving average: [exact type and window]
> - Period return: [exact baseline convention]
> - Calendar-daily series (e.g. stablecoin supply): window unit is calendar days
>
> **Critical**: do NOT import any of the analysis modules. Re-implement from the raw data
> yourself — that is the only way to find bugs in those modules.
>
> **Output**: a runnable script at [path] that prints expected / recomputed / difference
> for each item and ends with a PASS/FAIL summary, plus a findings file.
>
> **Report**: one-line verdict on whether all numbers agree, then a table of any
> mismatches (item / published / recomputed / difference / likely cause). If there are no
> mismatches, state that and give the count of items verified. If a data file is missing
> or its format differs from the description, say so and skip that item — do not guess.

### Format descriptions to include

| Source | Format |
|---|---|
| Binance klines | `[[openTime_ms, open, high, low, close, volume, ...], ...]` — `close` is index 4 |
| Nasdaq official API | `{"data": {"tradesTable": {"rows": [{"date": "11/20/2026", "close": "$342.56"}, ...]}}}` — strip `$` and `,` |
| ETF flow tables | TSV; col 1 = date like `07 Nov 2026`; last col = net flow in $M, parentheses = negative |
| FRED CSV | `observation_date,<series>` header, then `YYYY-MM-DD,value` rows; `.` means missing |
| DefiLlama series | list of `{date: <unix seconds>, ...}`; stablecoin total is at `totalCirculatingUSD.peggedUSD` |
| Binance funding | list of `{fundingTime: <ms>, fundingRate: <float>}` |
| Binance OI | list of `{timestamp: <ms>, sumOpenInterestValue: <float>}` |

---

## Brief B — Methodology / logic audit

> You are an independent methodology reviewer. Your job is to find problems. Do not
> manufacture findings — if something checks out, say so.
>
> **Documents under review**: [paths]
>
> **The framework in one paragraph**: [layers, their order, and what each is supposed to
> answer]
>
> **Central claims to challenge**:
> A. Is the necessary-condition chain still complete after the revision, or can a layer now
>    be skipped? Does any conclusion actually rest on a single layer?
> B. Are the scenario probabilities and headline judgements stronger than the evidence
>    supports? What sample size would be needed to support that precision?
> C. Are the thresholds consistent with the historical readings the document itself cites?
>    (Check for a threshold that contradicts the data it is derived from.)
> D. Does the label definition used in the backtest introduce its own bias? Is any
>    conclusion drawn from a cell with too few samples to support it?
> E. Is survivorship bias disclosed, and is the stated direction of its effect correct?
> F. Do all documents agree on every shared number and table? Does any document still carry
>    a superseded version of a claim?
> G. Is the "reference market is context, not determinant" positioning actually followed
>    through, or does some conclusion quietly depend on it?
>
> **Raw data and scripts**: [paths] — you may run them, but do not modify the deliverables.
>
> **Output**: findings file with a table: id / location / problem type (logic contradiction /
> overclaiming / statistical trap / data inconsistency / misleading phrasing) / description
> / severity (high/medium/low) / suggested fix.
>
> **Report**: overall judgement on whether the revision holds, then problems ordered by
> severity. Separate "must fix" from "could improve". State "verified, no issue" for parts
> that check out.

---

## Brief C — Statistical & engineering audit of the backtests

> You are an independent statistical and engineering reviewer. Find technical defects in the
> data pipeline.
>
> **Scripts and outputs under review**: [paths]
>
> **Methodology as claimed** (verify it is actually implemented):
> [each definition, stated precisely]
>
> **Check specifically**:
> A. **Look-ahead bias** — the asset universe is today's constituents applied to a
>    historical period (survivorship); are assets correctly excluded before their listing
>    date; is the denominator tiny in early periods; does the document assess the effect?
>    Is MA200 unavailability in early dates skewing the denominator?
> B. **Window-unit consistency** — is "N days later" calendar or trading days? Does it
>    match the other windows in the same analysis?
> C. **Sample adequacy** — for each cited conclusion, is the cell's n large enough? Should a
>    significance test (Fisher exact / chi-square) be run before claiming a difference?
>    How should a Wilson interval behave at n=1?
> D. **Engineering** — do all scripts use the same universe? Does the set of turning-point
>    dates match across scripts? Does any script silently drop data without reporting how
>    much? Do the outputs contain enough to reproduce each conclusion, or only aggregates?
> E. **Reproducibility** — if a cached raw file is deleted, does the script fail loudly or
>    silently degrade? Is the cache guard correct?
>
> **You may**: run these scripts (they write JSON to [allowed output dir]), write your own
> check scripts under [your own dir], create/delete temp files under your own dir.
> **You must not**: modify the analysis scripts or any deliverable file.
>
> **Output**: findings file with a table: id / location (script:line or json field) /
> problem type (look-ahead / window mismatch / insufficient sample / engineering defect /
> reproducibility) / description / severity / suggested fix.
>
> **Report**: overall judgement on whether the backtest's conclusions can be relied on.
> Separate "methodologically fatal" from "limitation to disclose" from "engineering
> improvement". Verify and state what is correct.

---

## Reading the results

### Group before you fix

Findings usually collapse into a handful of **root causes**, not one defect each. Sort
them into groups first, then fix each root cause once — a shared loader, a shared window
convention, a shared baseline rule. Patching N symptoms individually leaves the root
cause in place and guarantees a fifth finding of the same kind later.

### Re-derive the auditor's count

The auditor's own tally may disagree with what its raw output contains — it may have
counted one of two tables, or summarised 88 failing rows as "44 items". Before acting on
a number, re-derive it from the raw findings file.

Then check each group by recomputation yourself: **a whole group can be false positives**,
and you cannot tell which groups are real by reading the auditor's verdict alone. Fix the
groups that recompute as defects, disclose the ones that are real but already handled,
dismiss the rest with a stated reason.

For each finding, decide explicitly:

| Disposition | Meaning |
|---|---|
| **Fix** | change the deliverable or script, then re-verify |
| **Disclose** | the finding is real but the deliverable already handles it — or add a note |
| **Dismiss (with reason)** | the agent's finding is wrong; state why in the delivery notes |

Never silently drop a finding. If an agent's finding is right and you dismissed it, the
deliverable is worse for having been "verified".

### The findings are a snapshot of a moving target

An auditor reads the files as they were when it read them. If you keep editing while
it works, a large share of its findings are already fixed, partially fixed, or about
to be contradicted by your next run.

**Never write an auditor's replacement value into a deliverable verbatim.** Procedure:

1. Turn the findings into (old value → proposed value) pairs.
2. Read the CURRENT file and re-derive each number from the artifact yourself.
3. Recompute the auditor's proposed value independently. A proposed value that does
   not reproduce locally is an error in the finding, not a new truth.
4. Apply the fix **in the generator**, not by string-replacing the report.
5. Classify each finding: already fixed (no-op) / real defect (fix at the generator) /
   unit or convention difference (disclose) / false positive (dismiss with a reason).

Check your own direction before calling a published number wrong. A window anchored
backward from a turning point and the same window anchored forward differ in sign, so
a reversed direction turns a correct number into an enormous apparent error — and an
auditor that inherits your stated convention inherits it too. Confirm the anchor
direction, then the unit, then the value.

Auditor findings also drift by line number. Match on **value plus context**, not on
`file:line` — a line number from a snapshot that has since been edited points at
unrelated text.

### Third layer: your own mechanical check

The agents read; you compute. Write a verification script that:

1. Runs every analysis script in dependency order, asserts exit code 0
2. Asserts every artifact exists, parses, and is non-empty
3. Re-derives the published numbers from raw data **independently** (numpy + stdlib only,
   never importing the analysis modules)
4. Asserts the deliverable file **contains** those numbers
5. Asserts the thresholds and claims in prose match the artifacts
6. Asserts prior deliverables are unmodified

Keep the canonical verifier with the pipeline (`verify_pipeline.py`) and list it in the
pipeline's own run order. When you need an OS-safe run path, copy it to a temp path with
a `hermes-verify-` prefix — but the canonical copy stays, and the run's output is
persisted to a log file. A verification whose output was deleted cannot be re-checked by
anyone, including you.

Run it **after your final edit**. A pass that predates the last cleanup or refactor
proves nothing about the code you deliver; if you touch anything after a green run,
re-run before delivering and say which run the evidence comes from.

Layer 3 catches what layers 1–2 cannot: prose that describes an older version of a
correct analysis.