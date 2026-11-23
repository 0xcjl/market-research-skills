#!/usr/bin/env python3
"""Template: verify every number in a delivered market-research report.

Copy this file next to your cached raw data, fill in the loader + SECTIONS, and run it.
Exit code 0 = every assertion passed.

The template encodes four rules that make this gate actually work:

1. **Load from cached raw data, and re-implement the metric independently.** Do NOT import
   the analysis module that produced the report -- importing it re-tests the same code path
   and reproduces its bugs. Use a different implementation (numpy vs pure-python, or a
   separately written function) so a shared mistake has to be made twice to survive.

2. **Assert per entity row, never per section.** A percentage that is wrong for one asset
   is frequently correct for another asset in the same table, so a section-wide substring
   check both misses real errors and fires on correct data.

3. **Tolerance matches the report's DISPLAYED precision**, not the underlying precision.

4. **Also assert the delivered file contains the value.** A correct script and a stale
   report is the classic silent failure of this workflow.
"""

import json
import os
import sys

SCRATCH = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(SCRATCH, "outputs")          # where the deliverable actually lives
REPORT = os.path.join(OUT_DIR, "report.md")

fails = []


def ck(label, cond, detail=""):
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}{(' | ' + detail) if detail else ''}")
    if not cond:
        fails.append(label)


# --------------------------------------------------------------------------
# 1. Independent loaders over the cached raw data.
#    Rewrite for your sources. Keep them separate from the analysis code.
# --------------------------------------------------------------------------

def load_nasdaq(path):
    """Nasdaq official API daily history -> {date: close}."""
    import datetime
    d = json.load(open(path))
    rows = d["data"]["tradesTable"]["rows"]
    out = {}
    for r in rows:
        try:
            dt = datetime.datetime.strptime(r["date"], "%m/%d/%Y").date()
            c = float(str(r["close"]).replace("$", "").replace(",", ""))
        except (ValueError, KeyError, TypeError):
            continue          # covers "--" placeholder rows
        out[dt] = c
    return out


def load_klines(path):
    """Binance klines -> {date: close}."""
    import datetime
    return {datetime.datetime.utcfromtimestamp(r[0] / 1000).date(): float(r[4])
            for r in json.load(open(path))}


def last_on_or_before(series, day):
    ks = [k for k in sorted(series) if k <= day]
    return ks[-1] if ks else None


# --------------------------------------------------------------------------
# 2. Independent metric implementations.
# --------------------------------------------------------------------------

def period_return(series, start, end=None):
    """Return over [start, end] using the close BEFORE start as the base."""
    base = last_on_or_before(series, start)
    assert base is not None, f"no base close on or before {start}"
    last = last_on_or_before(series, end) if end else max(series)
    return (series[last] / series[base] - 1) * 100


def drawdown_from_peak(series, end=None):
    """Current drawdown vs the peak, plus the peak date."""
    ks = sorted(k for k in series if end is None or k <= end)
    peak_date = max(ks, key=lambda k: series[k])
    cur_date = ks[-1]
    return (series[cur_date] / series[peak_date] - 1) * 100, peak_date


# --------------------------------------------------------------------------
# 3. Expected values + entity-scoped assertions.
#    Fill these from the REPORT being checked, one row per entity.
# --------------------------------------------------------------------------

SECTIONS = {
    # entity -> {metric: (expected_value, tolerance)}
    "BTC": {
        "ytd_pct": (-32.2, 0.05),
        "from_peak_pct": (-18.4, 0.05),
    },
    "ETH": {
        "ytd_pct": (-21.0, 0.05),
    },
}


def report_row(text, entity):
    """Return the table row that belongs to ONE entity.

    Scoping the search to a single row is the whole point: a section-wide substring
    check matches other entities' legitimate values.
    """
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and cells[0].strip("*") == entity:
            return cells
    return None


def main():
    # ---- 1. scripts under test must run clean -------------------------
    # for script in ("analysis.py", "claims.py"):
    #     import subprocess
    #     p = subprocess.run([sys.executable, script], capture_output=True, text=True)
    #     ck(f"{script} exits 0", p.returncode == 0, p.stderr[:200])
    #     ck(f"{script} produced output", len(p.stdout.strip()) > 0)

    # ---- 2. recompute independently from the cache --------------------
    # series = load_nasdaq(os.path.join(SCRATCH, "NDX.json"))
    # got = period_return(series, date(2026, 1, 1))
    # ck("NDX YTD", abs(got - SECTIONS["NDX"]["ytd_pct"][0]) <= SECTIONS["NDX"]["ytd_pct"][1],
    #    f"got {got:.2f}")

    # ---- 3. the DELIVERED FILE contains the values --------------------
    # text = open(REPORT, encoding="utf-8").read()
    # for entity, metrics in SECTIONS.items():
    #     cells = report_row(text, entity)
    #     ck(f"{entity} row present", cells is not None)
    #     if cells:
    #         for metric, (expected, tol) in metrics.items():
    #             found = any(abs(float(re.sub(r"[^0-9.\-]", "", c)) - expected) <= tol
    #                         for c in cells if re.search(r"[-+]?[0-9.]+%?$", c))
    #             ck(f"{entity}.{metric} in report", found, f"expected {expected}")

    if not SECTIONS:
        print("  [SKIP] SECTIONS is empty -- fill it in before trusting this run.")
        return 0

    print("\n=== SUMMARY ===")
    if fails:
        print(f"FAILED -- {len(fails)} check(s):")
        for f in fails:
            print("   -", f)
        return 1
    print("PASSED -- every assertion held.")
    return 0


if __name__ == "__main__":
    import re
    sys.exit(main())
