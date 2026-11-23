# Mechanical Verification — the pipeline-stage rules

The detailed form of the eleven rules that govern the mechanical-verification stage
of `market-bottom-framework`. `SKILL.md` §8 carries the always-on checklist; this
file carries the reasoning behind each rule.

Every rule here exists because breaking it shipped a wrong number at least once.
Read the section you need; the checklist in `SKILL.md` is the contract.

---

## The rules

Independent of the agents, run a script that checks:

- every analysis script runs clean, in dependency order
- artifacts exist, parse, and are non-empty
- the deliverable **file actually contains** the numbers the data produces
- the thresholds and claims in the prose match the artifacts
- prior deliverables were not modified

**A correct script with a stale report is a failed deliverable** — the file check is what
catches that.

### Make verification a pipeline stage, not a one-off

Verification improvised in a temp script does not survive: the script gets deleted, the
next refresh has no verifier, and the same class of defect ships again.

So: **the verifier lives with the pipeline**, is named `verify_pipeline.py`, and is listed
in the pipeline's own run order and in the delivered documentation. Run it from a
`tempfile.mkstemp(prefix="hermes-verify-")` path when you need an OS-safe run, but keep the
canonical copy in the project.

Three properties that matter more than the assertion count:

| Property | Why | Failure it prevents |
|---|---|---|
| **Independent implementation** — the verifier must NOT import the metric code it verifies | Sharing an implementation reproduces the bug instead of catching it | A wrong RSI/moving-average definition passes because both sides are wrong the same way |
| **Fails loudly on missing input** — a missing raw file aborts with the filename | A backtest over a silently smaller universe still produces plausible numbers | Results computed on 134 assets instead of 135, reported as 135 |
| **Asserts the corrections landed** — every defect the audit found must appear in BOTH the code and the prose | Otherwise "fixed" can mean "described in a note" | A report that still quotes a retracted number |

The verifier should also assert its own independence (that it imports nothing from the
modules it checks), so a future edit cannot quietly reintroduce shared code.

### Seal every series to the last fully-settled bar

A daily candle stamped with its OPEN time is still forming until the UTC day ends.
Reading it as a close is the single most common way a "current" number stops being
reproducible.

Diagnostic: **fetch the same series twice at different times and compare the last bar.**
If the close differs, you were reading a live candle — and each fetch would have been
published as "the current price".

Rule: a bar dated `d` is settled iff `d < today (UTC)`. Apply it to every series —
prices, breadth universes, funding — and use ONE as-of rule across the whole deliverable.
Two panels reading different cutoffs is its own defect.

Direction matters when you fix it: an unfinished candle has a close that moves, so it
can make conditions look *more* extreme than they are. Correcting it can move a headline
reading toward neutral. Say so explicitly in the report.

### Generate prose tables from the artifact

A hand-typed table of computed numbers drifts the moment the pipeline is re-run — and it
drifts silently: an off-by-one sample size, or one quantity printed as 43% in one
document and 44% in another (both from 43.5%).

Write a small generator that renders the table from the JSON artifact and splice it into
the report. Make the generator idempotent so it can be re-run without breaking the prose
around it.

**Make idempotency a checked property, and delete by a stable marker.** Two failures
reproduce reliably. (1) A generator that rewrites a block usually has to remove its own
previous output first; matching that output *by content* breaks the moment the content
changes — the old copy is then never matched, and every run appends another. Match on a
**stable marker line the generator always writes**, never on the rendered text. (2)
Removing the marker leaves its trailing blank line behind, so the file gains a blank
line per run and byte-comparison still fails. Strip the marker **and** the blank line
after it. Then assert byte-identical output across two consecutive runs, and put that
assertion in the **pipeline-wide** verifier for every generator — a focused verifier only
covers the generator someone remembered to write one for. Recipe:
`references/artifact-verification.md`.

Three details that matter:

| Detail | Why |
|---|---|
| ONE rounding convention across all tables and documents | A quantity that rounds differently in two files reads as two different findings |
| Render the aggregate row, not only the buckets | The pipeline drops buckets with n below a floor but still includes them in the headline aggregate — without the aggregate row the table does not add up to the headline beside it |
| Keep the generator in the pipeline's run order | A generator nobody runs is a generator that drifts |

Then assert in the verifier that a few representative rows in each document still match
the JSON. That converts "someone re-types a table" from a silent error into a loud one.

Two rules make that assertion actually cover the deliverable:

- **Derive the coverage from the artifact, not from a hand-written list.** A verifier that
  checks only the tables it knows about cannot see a table that was never wired in — a
  hand-typed quadrant table sitting next to three generated ones stays wrong forever
  while the verifier is green. Enumerate the tables the artifact produces, then assert
  each one exists in the document and each of its rows matches the artifact.
- **Assert the SAME quantity is equal across documents, not merely that each document is
  internally consistent.** Two renderers of one number with two rounding formats (`:.0f`
  in one, `:.1f` in the other) satisfy every per-document check and still disagree on
  screen. When you fix a rounding convention, change it in every generator that renders
  that quantity, then add a cross-document equality assertion for it.

### Check that a baseline was not silently degraded

When a source series starts later than the period you need, code often falls back to a
"nearby" date without saying so. A calendar-year return computed from the first close
of the year is NOT the same as one computed from the previous year-end close, and mixing
the two conventions across columns makes the years incomparable while every individual
number still looks plausible.

Guard: assert the baseline DATE, not just the resulting value. If the needed baseline is
missing, extend the history (a longer series) rather than substituting a nearby date.
Cross-check two independent sources on their overlap before splicing them.

### Assert the fix is load-bearing

A silent-truncation fix is invisible to every ordinary check. The artifact still parses,
still has the right schema, still looks plausible — it is just shorter, or computed over
a smaller sample than it should be, and every number remains perfectly presentable.

Two shapes recur:

| Shape | Symptom |
|---|---|
| **Response-window truncation** — a source caps a response and returns the *tail* of a wide range, so "give me everything" silently yields only the most recent slice | the series starts later than it should; the array length looks plausible |
| **Wrong-subset selection** — the full history exists, but the pipeline loaded the short convenience file and computed on it while the long file sat unused | a percentile labelled with a unit the window never spanned |

The guard in both cases asserts **coverage**, not shape:

- assert the artifact's earliest observation is EARLIER than what a single unchunked
  request returns — if the chunking regresses, this fails
- assert the sample used is the LONGEST available, not the one that happened to be
  loaded — assert the count and the span, not just that a file was read
- assert the window unit the artifact declares matches the unit the document prints

Without these, the fix can stop working while every other check stays green.

### Update the prose after a recompute — anchor every replacement

When a recompute changes numbers, the prose has to change with it. The obvious mechanic
— string-replace the old value with the new one — corrupts the document, because **the
same literal can mean different things in different contexts**.

Concretely, one literal can be simultaneously the *current* drawdown from the high AND
the MA200 deviation of a *historical* bottom two years earlier. A global replace
rewrites the historical record with a current reading, and the result still looks
plausible, so nothing downstream flags it.

Rules:

1. List every occurrence of the old value **with its surrounding context** before
   touching anything.
2. Replace by **context anchor** (the sentence, the table cell, the line), not by value.
3. Assert the expected hit count per anchor. A count of 0 or 2 means the anchor is
   wrong — stop, do not widen the pattern.
4. **Historical readings are frozen.** A number describing a past event does not change
   because today's pipeline was re-run.

### Add a focused verifier per generator, and give it teeth

A single pipeline-wide verifier that asserts "the document contains string X" cannot see a
table whose numbers are wrong — the string is present, the value is stale, the check
passes. Once documents are rendered from artifacts, add a **focused** verifier per
generator that asserts the rendered table equals the artifact, row by row, and that
re-running the generator changes nothing (byte-identical output).

A verifier that has never been observed to fail has not been tested. Take **copies** of
the deliverable in a temp dir, deliberately break one thing at a time — a cell value, a
direction-dependent cell, a sample-size column, a reverted reading — and require the
verifier to exit non-zero on each mutation. A surviving mutation is a hole in the
verifier, and you found it before a reader did. Never mutate the real deliverable.

When a focused verifier reports failures, **classify each failure as verifier-bug or
real-defect before changing anything**. A probe written in the same session as the fix
has its own bugs — a table matcher that stops at the first header silently ignores the
second table with the same header, and an assertion written before the fix it checks
tests the wrong direction. Fixing a deliverable to satisfy a broken probe bakes the bug
into the artifact. Re-read the failing assertion first; only then touch the deliverable.

### Treat the auditor's findings as a timestamped snapshot

An auditor reads the files as they were when it read them. If you keep editing while it
works, a large share of its findings are already fixed, partially fixed, or about to be
contradicted by your next run. **Never write an auditor's replacement value into a
deliverable verbatim** — re-derive each one from the artifact yourself; a proposed value
that does not reproduce locally is an error in the finding, not a new truth.

Before concluding that a published number is wrong, re-check **your own direction**: a
window anchored backward from a turning point and the same window anchored forward differ
in sign, so a reversed direction turns a correct number into an enormous apparent error.
Confirm the anchor direction, then the unit, then the value. Briefs and the reading
procedure: `references/verification-protocol.md`.

### The verification run is the last gate

A verification pass that ran **before** your last edit proves nothing about the code you
are delivering. Any edit after the run — a cleanup, a line-wrap fix, a refactor — re-opens
the gate.

End-of-session order: finish every edit including cleanup → run the verifier → deliver.
If you clean up after the run, re-run, and say in the delivery which run the evidence
comes from.

### Label the verification honestly

A one-shot research pipeline has no canonical test/lint/build command, so an ad-hoc
assertion script is **not** "the test suite is green". Report what it asserts, how many
assertions, the exit code, and where the log is persisted. Persist the log: a
verification whose output was deleted cannot be re-checked by anyone, including you.

**Persist the script too, and do not delete it after a green run.** A run whose only
artifact is a chat message leaves nothing to re-check: nobody can tell whether the
assertions were real, and the changed files stay marked unverified. Keep the canonical
copy with the pipeline; when the run happens from a
`tempfile.mkstemp(prefix="hermes-verify-")` path, **leave the script at that path** —
the OS prunes the temp directory on its own, so deleting it buys nothing — and copy it
next to the persisted log.

### Guard a shared implementation against being re-copied

Converging duplicated helpers onto one shared module is only half the job. Without a
guard the next edit copies the helper back and the two drift silently. Add an assertion
that **fails** when a module both defines a helper locally and imports the shared one.
