# Artifact Verification — the focused-verifier recipe

The per-generator verifier described in SKILL.md §8. A pipeline-wide verifier can only
see strings the document contains; a focused verifier sees whether the rendered table
still equals the artifact it came from.

## What a focused verifier asserts

Four layers, in this order. Each layer catches a class the others cannot.

| Layer | Asserts | Catches |
|---|---|---|
| **A. Generator behaviour** | runs clean; output byte-identical across two consecutive runs; a marker block appears exactly once | non-idempotent generators, duplicated blocks, accumulating blank lines |
| **B. Independent recompute** | every cell recomputed from the raw snapshot by your own implementation equals the rendered cell | stale cells, wrong formulas, wrong join keys, wrong direction |
| **C. Mutation test** | deliberately broken copies are detected | a verifier that cannot fail |
| **D. Cross-document** | the same quantity renders identically in every document that shows it | divergent rounding conventions, divergent labels |

## The hard rules

**Do not import the generator you are verifying.** Re-implement the metric from the raw
snapshot inside the verifier. Sharing an implementation reproduces the bug instead of
catching it — both sides are wrong the same way and the check passes.

**Derive coverage from the artifact, not from a hand-written list.** Enumerate the
tables the artifact produces and assert each one exists in the document and each of its
rows matches. A verifier that checks only the tables it knows about cannot see a table
that was never wired in.

**Assert the aggregate row, not only the buckets.** A pipeline drops buckets below an
n-floor but still includes them in the headline aggregate; without the aggregate row
the table does not add up to the number printed beside it.

## Layer A — idempotency

Byte-identical across two runs is the only test that matters, and it catches two
distinct defects that look identical from the outside.

```python
def snap(paths):
    return {p: open(p, "rb").read() for p in paths}

before = snap(deliverables)
run(generator)                      # first run
run(generator)                      # second run
after = snap(deliverables)
assert before == after, changed_deliverables(before, after)
```

The generator must **remove its own previous output** before writing. Match on a stable
marker, not on content:

```python
MARKER = "> **口径说明（2026-11-22）**"

kept, skip_blank = [], False
for ln in text.split("\n"):
    if ln.startswith(MARKER):
        skip_blank = True            # also drop the blank line after it
        continue
    if skip_blank and not ln.strip():
        skip_blank = False
        continue
    skip_blank = False
    kept.append(ln)
text = "\n".join(kept)
```

Content-matching is the trap: change the rendered text by one word and the old copy
is never found again, so every subsequent run appends another one. The marker must be
emitted verbatim by the generator and must not contain any computed value.

## Layer C — mutation test

A green run cannot distinguish a working check from a check that cannot fail. Break
copies, on purpose, and require detection.

```python
import os, shutil, subprocess, sys, tempfile

def detected(mutate, verifier, deliverables, extra_paths=()):
    d = tempfile.mkdtemp(prefix="hermes-mut-")
    for p in deliverables:
        shutil.copy(p, os.path.join(d, os.path.basename(p)))
    mutate(d)
    r = subprocess.run([sys.executable, verifier, d], capture_output=True)
    return r.returncode != 0        # 0 means the verifier MISSED it
```

Mutations worth running — one per assertion class:

- a single cell value changed to a plausible but wrong number
- a direction-dependent cell (leading vs lagging) put on the wrong side
- a sample-size column inflated
- a superseded reading written back

**Run every mutation on a copy.** The real deliverable must be byte-identical before
and after the mutation suite.

## Layer D — cross-document equality

Per-document consistency is not cross-document consistency. Two renderers of one
number with two rounding formats (`:.0f` in one, `:.1f` in the other) satisfy every
per-document check and still disagree on screen. Assert the equality directly:

```python
assert f"{value:.1f}" in doc_a and f"{value:.1f}" in doc_b
```

When you change a rounding convention, change it in **every** generator that renders
that quantity, then add the cross-document assertion.

## Layer A′ — the fix is load-bearing

A verifier that checks the artifact's *shape* cannot see a silent truncation. The
artifact parses, has the right schema, and every number in it is presentable — it is just
shorter, or computed over a smaller sample than it should be.

Two shapes recur, and both need a coverage assertion rather than a shape assertion:

| Shape | Coverage assertion |
|---|---|
| the source caps a response and returns the *tail* of a wide range, so "everything" silently yields only the most recent slice | the artifact's earliest observation is EARLIER than what one unchunked request returns |
| the full history exists but the pipeline loaded the short convenience file while the long file sat unused | the sample used is the LONGEST available — assert the count and the span, not just that a file was read |

Without these, the fix can stop working while every other check stays green.

## Rounding in verifiers

A verifier that recomputes a percentage with `round()` disagrees with a document rounded by
hand, and the disagreement looks like a data bug rather than a convention mismatch. Python's
`round()` is banker's rounding (216.50 → 216); humans expect half-up (216.50 → 217). Pick one
rule, state it, and apply it explicitly on both sides:

```python
from decimal import Decimal, ROUND_HALF_UP

def pct(x, nd=1):
    q = Decimal(1).scaleb(-nd)
    return (Decimal(str(x)) * 100).quantize(q, rounding=ROUND_HALF_UP)
```

Build the percentage from the **decimal string** of the ratio, never from a float product:
`0.145 * 100` is `14.499999999999998`, so half-up of a true 14.5 quantizes to 14 and the
verifier reports a false defect on a correct document. `Decimal(str(x))` first, then multiply
by 100 — that ordering is the whole fix.

When a rounding dispute appears between two windows of the same document, suspect the
convention before the data, and fix the rule once in a helper that both the generator and the
verifier import, rather than correcting each window by hand.

## Classifying a failure before touching the deliverable

A probe written in the same session as the fix has its own bugs. Re-read the failing
assertion first. Common verifier bugs:

| Symptom | Usually |
|---|---|
| matcher returns only the first table with a given header | it stops at the first match and ignores the rest |
| assertion written before the fix it checks | it tests the old direction |
| count mismatch | the generator's own output shape changed, not the deliverable |

Fixing a deliverable to satisfy a broken probe bakes the bug into the artifact. Decide
**verifier-bug or real-defect** per failure and record which.

## Editing the pipeline without breaking it

Batch text edits to import lines break in ways the file still parses: an import
landed after a trailing comment (so it is inert), or inside a docstring. After any
batch edit:

```bash
for f in edited.py; do
  python3 -c "import ast,sys; ast.parse(open('$f').read())" || echo "PARSE FAIL $f"
  python3 -m pyflakes "$f" 2>/dev/null || python3 -m py_compile "$f" || echo "IMPORT FAIL $f"
done
```

`pyflakes` catches undefined and unused names; `py_compile` catches syntax. A module
that parses but has an inert import still fails at the first call site, which is much
later and much more expensive to find.

Dead-code checks must scan the **whole tree**, not one file: a shared helper imported
by other modules looks uncalled when you only read the file that defines it. Collect
defined names and all referenced names across every file in the tree, then report
names that are defined and never referenced anywhere else.

## Where it lives

Keep the focused verifier next to the pipeline (not in a temp dir), list it in the
run order, and persist its output to a log — a verification whose output was deleted
cannot be re-checked by anyone, including you.

**Persist the script as well as the log, and do not delete it after a green run.** A run
whose only artifact is a chat message leaves nothing to re-check: nobody can tell whether
the assertions were real, and the changed files stay marked unverified. When the run
happens from a `tempfile.mkstemp(prefix="hermes-verify-")` path, leave the script at that
path — the OS prunes the temp directory on its own, so removing it buys nothing — and
copy it beside the persisted log.
