# market-narrative-cycle-research

> **[English](./README.md)** | **简体中文**

把叙事周期映射成早期预警规则 —— 让故事变成可检验的信号，而不是一种感觉。

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Skill](https://img.shields.io/badge/Agent-Skill-orange.svg)](./SKILL.md)
[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)](./SKILL.md)

---

## 它解决什么

叙事周期不是 K 线形态 —— 它是一串关于世界的**主张**的重复序列，每条主张都有自己的证据、自己的阶段、以及距离下一次主张崩塌的领先时间。

**market-narrative-cycle-research** 把这串序列显式化、可用化：

1. **结构化 schema** —— 每个叙事有明确字段（主张、证据类别、阶段、领先时间、失效条件），于是两个叙事可以真正被比较，而不只是被并排放着。
2. **周期主轴** —— 序列由一手来源拼出，每次转折都有日期和出处。
3. **早期预警规则** —— 周期被转成带阈值、触发条件，以及「这条规则从什么时候开始不再适用」的规则。

## 为什么用它

| | 不用它 | 用它 |
|---|---|---|
| **所谓的「周期」** | 事后的故事 | 有日期、有出处的转折序列 |
| **可比性** | 每个叙事各说各话 | 同一套 schema，叙事之间可排序 |
| **领先时间** | 「感觉已经晚了」 | 写明领先时间，以及支撑它的证据 |
| **失效** | 规则悄悄不再适用 | 每条规则都带失效条件 |

## 快速开始

```bash
git clone https://github.com/0xcjl/market-cycle-research-skills.git
cp -R market-cycle-research-skills/skills/market-narrative-cycle-research ~/.agents/skills/market-narrative-cycle-research
```

先读 `SKILL.md`。参考文件按需加载：

| 文件 | 什么时候读 |
|---|---|
| `references/narrative-schema-and-briefs.md` | 定义叙事字段、证据类别，或写研究任务书时 |
| `references/early-warning-playbook.md` | 把周期转成规则、阈值与监控节奏时 |
| `scripts/fetch_cycle_spine.py` | 从来源列表拼出带日期的周期主轴时 |

## 环境要求

- Python 3.10+（仅标准库）
- 能访问所引来源的网络

## 配套技能

- `market-bottom-framework` —— 用分层框架找底
- `market-performance-research` —— 量化收益、回撤与风险
- `crypto-research` —— 有证据链的 crypto 项目与代币研究

## 许可

MIT，见 [LICENSE](LICENSE)。
