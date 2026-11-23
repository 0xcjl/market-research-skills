# market-narrative-cycle-research

> **English** | **[简体中文](./README.zh-CN.md)**

Map narrative cycles into early-warning rules, so a story becomes a testable signal instead of a feeling.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Skill](https://img.shields.io/badge/Agent-Skill-orange.svg)](./SKILL.md)
[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)](./SKILL.md)

---

## What It Does

A narrative cycle is not a chart pattern — it is a repeated sequence of *claims* about the world, each with its own evidence, its own phase, and its own lead time before the next claim collapses.

**market-narrative-cycle-research** makes that sequence explicit and usable:

1. **A structured schema** — each narrative gets defined fields (claim, evidence class, phase, lead time, invalidation condition), so two narratives can actually be compared instead of merely juxtaposed.
2. **A cycle spine** — the sequence is assembled from primary sources, with each transition dated and sourced.
3. **Early-warning rules** — the cycle is converted into rules with thresholds, trigger conditions, and the conditions under which each rule stops working.

## Why Use It

| | Without it | With it |
|---|---|---|
| **A "cycle"** | A story told after the fact | A dated sequence with sourced transitions |
| **Comparability** | Each narrative described in its own terms | One schema, so narratives can be ranked against each other |
| **Lead time** | "This feels late" | Stated lead times, with the evidence that supports them |
| **Failure** | Rules quietly stop applying | Each rule carries its invalidation condition |

## Quick Start

```bash
git clone https://github.com/0xcjl/market-cycle-research-skills.git
cp -R market-cycle-research-skills/skills/market-narrative-cycle-research ~/.agents/skills/market-narrative-cycle-research
```

Read `SKILL.md` first. Reference files load on demand:

| File | Load it when |
|---|---|
| `references/narrative-schema-and-briefs.md` | Defining a narrative's fields, evidence classes, or writing the research brief |
| `references/early-warning-playbook.md` | Converting a cycle into rules, thresholds, and monitoring cadence |
| `scripts/fetch_cycle_spine.py` | Assembling the dated cycle spine from a source list |

## Requirements

- Python 3.10+ (standard library only)
- Network access to the sources you cite

## Companion Skills

- `market-bottom-framework` — locating bottoms with a layered framework
- `market-performance-research` — quantifying performance, drawdown, and risk
- `crypto-research` — evidence-based crypto project and token research

## License

MIT — see [LICENSE](LICENSE).
