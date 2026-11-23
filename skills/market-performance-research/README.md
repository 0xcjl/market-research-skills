# market-performance-research

> **English** | **[简体中文](./README.zh-CN.md)**

Quantify market performance, drawdown, and risk without inventing a number that was never computed.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Skill](https://img.shields.io/badge/Agent-Skill-orange.svg)](./SKILL.md)
[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](./SKILL.md)

---

## What It Does

Performance claims are easy to make and hard to defend: which baseline, which window, which return definition, which universe, which data snapshot.

**market-performance-research** fixes the measurement contract before any data is fetched, then holds to it:

1. **Contract first** — define the universe, the as-of date, the baseline, the return definition, and the settlement rule before pulling anything.
2. **Asymmetric framing** — a bottom question is not a symmetric "how far down" question; what determines a bottom is whether the *outflow* is finished (liquidity drain, positioning unwind, forced selling, credit stress).
3. **Authoritative sources, cached on arrival** — index constituents, weights, and holdings come from the provider's own API, never from search results. Every raw response is cached so a later source failure cannot silently change a number already in the report.
4. **Cross-validation** — every figure is checked against a second source or an independent recomputation before it reaches the prose.

## Why Use It

| | Without it | With it |
|---|---|---|
| **Annual returns** | Each column uses whatever baseline was convenient | One baseline rule, applied consistently to every period |
| **Current values** | A still-forming daily bar is read as a close | Unsettled bars are excluded; the as-of date is stated |
| **Drawdown** | Peak-to-trough computed against an arbitrary window | Peak, trough, and recovery measured on the same series |
| **Provenance** | Numbers typed into prose | Numbers generated from artifacts and asserted against them |

## Quick Start

```bash
git clone https://github.com/0xcjl/jialin-skills.git
cp -R jialin-skills/skills/market-performance-research ~/.agents/skills/market-performance-research
```

Read `SKILL.md` first. Reference files load on demand:

| File | Load it when |
|---|---|
| `references/data-sources.md` | Sourcing price, index, flows, rates, or volatility series, and their endpoint quirks |
| `references/metrics-and-pitfalls.md` | Defining a metric, or checking whether a definition has a trap in it |
| `templates/verify_report_numbers.py` | Building the independent-recomputation gate for a finished report |

## Requirements

- Python 3.10+ (standard library only)
- Network access to the data endpoints you choose to use

## Companion Skills

- `market-bottom-framework` — locating bottoms with a layered framework
- `market-narrative-cycle-research` — turning narrative cycles into early-warning rules
- `crypto-research` — evidence-based crypto project and token research

## License

MIT — see [LICENSE](LICENSE).
