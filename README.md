# Market Research Skills

> **English** | **[简体中文](./README.zh-CN.md)**

Three portable Agent Skills for evidence-based market research — measuring performance, locating bottoms, and mapping narrative cycles.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/Agent-Skills-3-orange.svg)](./skills)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](./skills/market-performance-research)

---

## What These Are

Market research has a specific failure mode: a plausible story, a table of numbers nobody re-checked, and a conclusion that reads like certainty. These skills exist to make that outcome structurally hard.

| Skill | Use it for |
|---|---|
| [`market-performance-research`](skills/market-performance-research/) | Quantifying performance, drawdown, and risk. Fixes the measurement contract before any data is fetched — universe, as-of date, baseline, return definition, and the settlement rule — so "the YTD number" means one thing. |
| [`market-bottom-framework`](skills/market-bottom-framework/) | Locating bottoms with a layered framework: price structure, participation breadth, leverage and positioning, dollar liquidity, credit and macro stress, new narrative and marginal buyers. Every threshold is argued, not asserted. |
| [`market-narrative-cycle-research`](skills/market-narrative-cycle-research/) | Mapping narrative cycles into early-warning rules, with a dated cycle spine and per-rule invalidation conditions. |

They compose: **performance** measures, **narrative** explains the sequence, **bottom** combines both into a decision with confirmation signals and falsification conditions.

## What They Enforce

These are not style preferences. Each rule exists because breaking it shipped a wrong number at least once.

- **Independent verification is not optional.** At least two subagents with different scopes, plus a mechanical verifier that must *not* import the metric code it checks — a shared implementation reproduces the same bug on both sides of the test.
- **Every series is sealed to its last fully-settled bar.** A daily candle stamped with its open time is still forming until the UTC day ends; reading it as a close is the most common way a "current" number stops being reproducible.
- **Prose tables are generated from the artifacts.** Hand-typed tables drift silently. Generators delete their own previous output by a stable marker, and idempotency is asserted, not assumed.
- **Baselines are asserted by date, not by value.** A calendar-year return computed from the year's first close is not the same as one computed from the previous year-end.
- **Auditor findings are hypotheses, not replacements.** Re-derive each proposed value yourself; a value that does not reproduce locally is an error in the finding.

## Install

Copy the whole skill directory into your agent's skills location. Discovery rules and permissions differ by client, so read each skill's `README.md` and `SKILL.md` first.

```bash
git clone https://github.com/0xcjl/market-research-skills.git
# install one
cp -R market-research-skills/skills/market-bottom-framework ~/.agents/skills/market-bottom-framework
# or all three
for s in market-research-skills/skills/*/; do
  cp -R "$s" ~/.agents/skills/"$(basename "$s")"
done
```

Requirements: Python 3.10+ (standard library only) and network access to the data endpoints you choose.

## Layout

```text
market-research-skills/
├── README.md / README.zh-CN.md
├── LICENSE
└── skills/
    ├── market-bottom-framework/        # SKILL.md + references/
    ├── market-performance-research/     # SKILL.md + references/ + templates/
    └── market-narrative-cycle-research/# SKILL.md + references/ + scripts/
```

## Related

- [`0xcjl/jialin-skills`](https://github.com/0xcjl/jialin-skills) — the wider collection of these skills
- [`0xcjl/crypto-research`](https://github.com/0xcjl/crypto-research) — evidence-based crypto project and token research

## License

MIT — see [LICENSE](LICENSE). Each skill directory carries its own copy.
