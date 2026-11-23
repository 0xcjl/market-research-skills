# Narrative schema, dispatch briefs, verification briefs

## 1. The shared entry schema (paste verbatim into every brief)

Identical schema across disjoint windows is what makes the merged timeline comparable. Copy
this block into every dispatch brief unchanged.

```
### <narrative name>
- **Class**: main narrative / branch narrative / sub-branch
- **Timeline**: seed (YYYY-MM) -> ignition (YYYY-MM) -> peak (YYYY-MM) -> decay (YYYY-MM); ~N weeks total
- **Cycle phase at ignition**: bear bottom / bear rally / recovery / mid-bull / blow-off / unwind / bear chop; reference asset ~$X (source)
- **Triggers**: 1-3, each typed (tech milestone / product launch / exchange listing / macro liquidity / regulation / celebrity / crisis spillover)
- **Amplifiers**: social virality / public VC thesis / exchange listings / airdrop expectation / media
- **Peak performance**: 2-4 representative tokens + multiple + start-end dates (source each)
- **Decay cause**: liquidity drain / disproof / event blow-up / attention migration / regulation
- **Pre-peak signals**: 1-3, each with weeks-before-peak and its evidence label
- **Sources**: all URLs for this entry
```

What makes each field earn its place:

- **Class** separates a theme from a branch of a theme; branch → main promotion is itself a finding.
- **Cycle phase at ignition** is required — an entry without it cannot be compared across windows.
- **Triggers** are typed so trigger types can be counted across the whole history.
- **Peak performance** names the theme's own peak, not the market's peak.
- **Pre-peak signals** carry weeks-before-peak; an entry with none is incomplete for a playbook.

## 2. Dispatch brief template

Each brief is self-contained: a sub-agent sees none of the parent conversation.

> **Your window**: [START]–[END]. Cover the narratives that ignited, peaked or decayed inside
> it. Do not speculate outside it — another researcher owns those windows.
>
> **What you must cover**: [list of themes phrased as "must cover", not "the only ones"] — the
> point is to prevent omissions, not to force a list.
>
> **Shared entry schema**: paste the block from §1 verbatim.
>
> **Cycle spine to annotate against**: paste the anchor table (date / phase label / price) so
> your narratives land on the same cycle as everyone else's. Use these prices; do not
> recompute them.
>
> **Source rule**: every dated claim carries its URL on the same line. First-hand preferred
> (protocol docs, project blogs, exchange/provider APIs, regulator and exchange filings,
> original reporting). Aggregators are context, not proof. Label inference **推断**; label
> anything untraceable **未验证** and keep it visible rather than dropping it.
>
> **Method**: run at least [N] distinct searches before writing; write the file only after
> the evidence is in hand.
>
> **Output**: write to the absolute path [PATH]. Write no other file. Do not modify any other
> file.
>
> **Language**: write the findings in [LANGUAGE].

Dispatch one agent per window in parallel; the parent's own price-series work (§2 of the
skill) happens concurrently and is not delegated.

## 3. Verification briefs for timeline deliverables

The briefs in `research/market-bottom-framework` (recomputation / methodology / statistical
audit) assume a quantitative backtest. A timeline deliverable has no backtest to recompute;
the equivalent independence comes from re-deriving claims from sources and from attacking
the causal story. Use two agents with different scopes.

### Brief A — fact re-derivation

> You are an independent auditor. For each dated claim in the deliverable (dates, price
> multiples, token names, trigger events, phase labels, lead times), locate the source that
> supports it and decide whether that source actually supports it.
>
> **Deliverables under test**: [paths]
> **Measurement contract**: window unit, period-return base, as-of date, what "peak" means,
> what "lead time" means
>
> **Do**: for each claim, open the cited URL (or find a better first-hand one) and mark
> SUPPORTED / UNSUPPORTED / MISSTATED / UNVERIFIABLE, with the URL you actually checked. Pay
> special attention to claims that carry no URL, to lead-time numbers stated as facts, and to
> phase labels that contradict the spine.
>
> **Do not** modify the deliverable. Write a findings file with a table: id / location (by
> quoted text, not line number) / claim / verdict / evidence URL / note. End with the count by
> verdict.

### Brief B — causal and method attack

> You are an independent methodology reviewer looking for problems. Do not manufacture
> findings; say "verified, no issue" where something holds.
>
> **Deliverables under test**: [paths]
> **Central claims to challenge**:
> A. Is any trigger presented as necessary when it was only sufficient?
> B. Is any leading signal evidenced by a single case? Is its label (Validated /
>    Backtested / Descriptive / Prior) honest? Do the supporting cases come from independent
>    liquidity regimes, or are several observations of one case?
> C. Is the sample survivors-only? Which failed or abandoned narratives are missing, and
>    would including them change the rules?
> D. Do the stated rhythms hold across the whole history, or only in the windows the author
>    highlighted? Can every aggregate claim be re-derived from a published item-level ledger?
> E. Are there rival explanations the deliverable never considers? Does any claim that two
>    things happened together also assert that one caused the other?
> F. Is any causal claim about an external event (a launch, a policy, a listing)
>    distinguishable from the market simply drifting into it?
> G. Does the document's evidence ceiling match its language — does any rule described as
>    Backtested carry a position instruction, a stage-two entry rule, or "only X works now"?
> H. Are the phase labels retrospective certainty dressed as live judgement? Would a
>    reader acting today know whether the phase is determined, and what would settle it?
> I. Are any conditions written so they cannot fail? If the condition never triggers, is the
>    rule falsifiable, and does it state the false-positive/false-negative calibration it
>    would need?
>
> **Output**: findings file with a table: id / location (quoted text) / problem type (causal
> overclaim / selection bias / unfalsifiable rule / missing counter-example / labelling
> mismatch / tier inflation / aggregate not re-derivable) / description / severity /
> suggested fix. Separate "must fix" from "could improve".

Both agents write findings to files. Read the files yourself, then give every finding a
disposition: fix, disclose, or dismiss with a reason. Never paste an auditor's proposed
replacement value into the deliverable — re-derive it against the artifact first.

## 4. Merging

1. Concatenate the entry blocks in window order.
2. Resolve duplicates — the same narrative claimed by two windows: keep the earlier window's
   entry and note the overlap.
3. Sort entries by ignition date inside each window.
4. Count trigger types and phases across the whole merged set. That count is the only part of
   the history that supports a rhythm claim, and it inherits the survivors-only bias. Count
   **independent onsets**, not rows — a catalyst that spawned five tokens is one event (§5).
5. Any claim you cannot source stays marked **未验证** in the delivered file.
6. Publish the merged set as the ledger artifact (§5) so step 4's counts stay checkable.

## 5. The merged ledger (published artifact)

The prose table is the deliverable; the ledger is the evidence behind it. Write both, and
publish the ledger next to the document so a reader can re-derive every aggregate.

```json
{
  "generated": "YYYY-MM-DD",
  "as_of": "YYYY-MM-DD",
  "n": 50,
  "narratives": [
    {"id": "n01", "name": "...", "class": "main",
     "ignition": "YYYY-MM", "peak": "YYYY-MM", "decay": "YYYY-MM",
     "cluster": "ai-agent-q1", "independent_onset": true,
     "sources": ["https://..."]}
  ],
  "gaps": [
    {"from": "YYYY-MM", "to": "YYYY-MM", "months": 6,
     "empty_months": 5, "phase_at_start": "...", "phase_at_end": "..."}
  ]
}
```

Rules the schema enforces:

- **`cluster`** — the event cluster a narrative belongs to (one catalyst spawning several
  tokens/themes). Without it, one event inflates the count that supports any rhythm claim.
- **`independent_onset`** — true only for the first narrative of a cluster, i.e. the first
  appearance of that idea. Re-ignitions, branches and continuations are false. Count
  independent onsets, not rows; a "narratives per phase" statistic computed on raw rows
  measures how many tokens a catalyst produced.
- **`gaps[].empty_months` vs `months`** — endpoint distance and intervening empty months
  differ by one. Record both; the empty-month count is what a "no narrative for N months"
  rule actually measures, and mixing the two silently shifts every gap by a month.
- **`phase_at_start` / `phase_at_end`** — the phase on both sides of the gap. This is what
  lets a reader test "gaps cluster in bear markets" instead of taking it on trust; when the
  ledger shows gaps ending inside a bull continuation, the rule is an environment alert
  with a stated false-positive rate, not a confirmation.

## 6. The audit disposition artifact

Both audit agents write findings files; the parent decides. Record the decisions in a file
beside the deliverable, not in chat — a finding closed only in the conversation is invisible
to the next reader and re-opens on every audit.

```markdown
| id | finding | verdict (fix / disclose / dismiss) | what changed |
|----|---------|-----------------------------------|--------------|
| M01 | ... | fix | §6 re-labelled as point estimate; flip example added |
| D01 | ... | disclose | §12 limitations now states effective sample < nominal |
```

A dismissal requires a stated reason — "wrong" is not a reason, "the spike window is
defined differently in this phase, here is the definition" is. When the audit's own data
contradicts a claim in the document, the claim is downgraded to the count that survives
and the counterexamples are published in the document itself, not only in this table.
