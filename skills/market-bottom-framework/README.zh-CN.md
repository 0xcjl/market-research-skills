# market-bottom-framework

> **[English](./README.md)** | **简体中文**

用分层框架定位市场底部，并在任何人读到结论之前先把结论证明一遍。

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Skill](https://img.shields.io/badge/Agent-Skill-orange.svg)](./SKILL.md)
[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)](./SKILL.md)

---

## 它解决什么

「现在是底部吗」这类分析通常栽在两种地方：找到一个说得通的故事就当结论；或者引用了一批没人复核过的数字。

**market-bottom-framework** 把两者都换成一条管线：

1. **分层框架** —— L1 价格结构、L2 参与度广度、L3 杠杆与仓位、L4 美元流动性、L5 信用与宏观压力、L6 新叙事与边际买家；层与层之间有明确的 AND / OR / 否决语义。
2. **阈值是论证出来的，不是断言的** —— 每个阈值都带证据、样本量，以及失效条件。
3. **独立验证** —— 至少两个不同 scope 的子代理，外加一道机械校验；校验器不得 import 它要检验的指标实现。
4. **可复算产物** —— 正文里的每个数字都由 JSON 产物生成，重跑不会让报告悄悄漂移。

## 为什么用它

| | 不用它 | 用它 |
|---|---|---|
| **框架** | 想到什么指标就往上堆 | 固定的层序，不会漏项 |
| **阈值** | 数字没有依据 | 每个阈值都写清证据、样本量与失效条件 |
| **广度** | 拿「70% 的币站上 200 日线」当底部规则 | 回测证明广度不能识别底部，于是降级为续跌风险过滤器 |
| **验证** | 同一个代理既写、又查、又自证 | 独立子代理 + 机械关卡；并用变异测试证明这道关卡确实会失败 |
| **可复算** | 表格手抄，每次重跑都漂移 | 表格由产物生成；校验器断言它仍然对得上 |

## 快速开始

```bash
git clone https://github.com/0xcjl/market-cycle-research-skills.git
cp -R market-cycle-research-skills/skills/market-bottom-framework ~/.agents/skills/market-bottom-framework
```

先读 `SKILL.md` —— 那是操作规程。参考文件按需加载：

| 文件 | 什么时候读 |
|---|---|
| `references/framework-design.md` | 设计层结构或评分语义时 |
| `references/market-universe-building.md` | 决定什么算「样本域」、以及如何去偏时 |
| `references/crypto-market-data-apis.md` | 找 crypto 价格、资金流、资金费率、未平仓量、链上数据时 |
| `references/mechanical-verification.md` | 校验环节的 11 条流水线规则（§8 的细则）|
| `references/artifact-verification.md` | 让报告里的数字可被独立复核时 |
| `references/verification-protocol.md` | 给独立验证子代理写任务书时 |

## 环境要求

- Python 3.10+（仅标准库，不需要第三方包）
- 能访问所选数据端点的网络
- 能派生子代理的 agent 运行时

## 配套技能

- `market-performance-research` —— 量化收益、回撤与风险
- `market-narrative-cycle-research` —— 把叙事周期转成早期预警规则
- `crypto-research` —— 有证据链的 crypto 项目与代币研究

## 许可

MIT，见 [LICENSE](LICENSE)。
