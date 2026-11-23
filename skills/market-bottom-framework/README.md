# market-bottom-framework

> **English** | **[简体中文](./README.zh-CN.md)**

Locate market bottoms with a layered framework, and prove the result before anyone reads it.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Skill](https://img.shields.io/badge/Agent-Skill-orange.svg)](./SKILL.md)
[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)](./SKILL.md)

---

## What It Does

Most "is this a bottom?" analysis fails in one of two ways: it finds a plausible story and treats it as a conclusion, or it quotes numbers that nobody re-checked.

**market-bottom-framework** replaces both with a pipeline:

1. **A layered framework** — L1 price structure, L2 participation breadth, L3 leverage and positioning, L4 dollar liquidity, L5 credit and macro stress, L6 new narrative and marginal buyers — with an explicit AND/OR/veto semantics between layers.
2. **Thresholds that are argued, not asserted** — every threshold carries its evidence, its sample size, and the conditions under which it fails.
3. **Independent verification** — at least two subagents with different scopes, plus a mechanical verifier that must not import the metric code it checks.
4. **Reproducible artifacts** — every number in the prose is generated from a JSON artifact, so a re-run cannot silently drift from the report.

## Why Use It

| | Without it | With it |
|---|---|---|
| **Framework** | Indicators pile up as they are thought of | A fixed layer order, so nothing is missed |
| **Thresholds** | Numbers appear without justification | Each threshold states its evidence, sample size, and failure conditions |
| **Breadth** | "70% of coins are above their 200-day" as a bottom rule | Breadth re-classified as a continuation-risk filter after backtesting showed it does not identify bottoms |
| **Verification** | The same agent writes, checks, and certifies its own work | Independent agents plus a mechanical gate; mutation-tested to prove it can fail |
| **Reproducibility** | Prose numbers typed by hand, drifting on every re-run | Prose tables generated from artifacts; the verifier asserts they still match |

## Quick Start

```bash
git clone https://github.com/0xcjl/market-cycle-research-skills.git
cp -R market-cycle-research-skills/skills/market-bottom-framework ~/.agents/skills/market-bottom-framework
```

Read `SKILL.md` first — it is the operating procedure. The reference files load on demand:

| File | Load it when |
|---|---|
| `references/framework-design.md` | Designing the layer structure or the scoring semantics |
| `references/market-universe-building.md` | Choosing what counts as the universe, and de-biasing it |
| `references/crypto-market-data-apis.md` | Sourcing crypto prices, flows, funding, open interest, on-chain data |
| `references/mechanical-verification.md` | The eleven pipeline-stage rules behind the verification stage |
| `references/artifact-verification.md` | Making a report's numbers independently checkable |
| `references/verification-protocol.md` | Briefing an independent verification subagent |

## Requirements

- Python 3.10+ (standard library only — no third-party packages)
- Network access to the data endpoints you choose to use
- An agent runtime that can spawn independent subagents

## Companion Skills

- `market-performance-research` — measuring performance, drawdown, and risk
- `market-narrative-cycle-research` — turning narrative cycles into early-warning rules
- `crypto-research` — evidence-based crypto project and token research

## License

MIT — see [LICENSE](LICENSE).
