# market-performance-research

> **[English](./README.md)** | **简体中文**

量化市场表现、回撤与风险 —— 不编造一个从未被计算过的数字。

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Skill](https://img.shields.io/badge/Agent-Skill-orange.svg)](./SKILL.md)
[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](./SKILL.md)

---

## 它解决什么

业绩类结论最容易讲、最难 defend：基期取哪个？窗口多长？收益怎么定义？样本域是谁？数据是哪一份快照？

**market-performance-research** 在抓任何数据之前先把口径钉死，然后守住它：

1. **先定口径** —— 样本域、数据截止日、基期、收益定义、封口规则，先写清楚再动手。
2. **不对称提问** —— 找底不是对称的「还能跌多少」问题；决定底部的是**流出是否结束**（流动性抽离、仓位平掉、强制抛售、信用压力）。
3. **权威源 + 落盘缓存** —— 指数成分、权重、持仓一律走提供方自己的 API，绝不从搜索结果来。每个原始响应都缓存，避免之后源挂了却悄悄改掉报告里已经写好的数字。
4. **交叉验证** —— 每个数字在进正文之前，都要被第二来源或独立重算复核过。

## 为什么用它

| | 不用它 | 用它 |
|---|---|---|
| **年度收益** | 每一列随手选个基期 | 统一基期规则，套用到所有区间 |
| **当期读数** | 把还在走的当日 K 线当收盘价读 | 排除未封口 K 线，写明数据截止日 |
| **回撤** | 在随手选的窗口里算峰谷 | 峰、谷、修复在同一序列上量 |
| **来源可追** | 数字手抄进正文 | 数字由产物生成，并被断言校验 |

## 快速开始

```bash
git clone https://github.com/0xcjl/jialin-skills.git
cp -R jialin-skills/skills/market-performance-research ~/.agents/skills/market-performance-research
```

先读 `SKILL.md`。参考文件按需加载：

| 文件 | 什么时候读 |
|---|---|
| `references/data-sources.md` | 找价格、指数、资金流、利率、波动率序列，以及端点的坑 |
| `references/metrics-and-pitfalls.md` | 定义指标，或检查某个定义是否埋着陷阱时 |
| `templates/verify_report_numbers.py` | 为成稿搭独立重算关卡时 |

## 环境要求

- Python 3.10+（仅标准库）
- 能访问所选数据端点的网络

## 配套技能

- `market-bottom-framework` —— 用分层框架找底
- `market-narrative-cycle-research` —— 把叙事周期转成早期预警规则
- `crypto-research` —— 有证据链的 crypto 项目与代币研究

## 许可

MIT，见 [LICENSE](LICENSE)。
