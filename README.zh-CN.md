# Market Research Skills

> **[English](./README.md)** | **简体中文**

三个可移植的 Agent Skill —— 量化表现、定位底部、映射叙事周期。

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/Agent-Skills-3-orange.svg)](./skills)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](./skills/market-performance-research)

---

## 这是什么

市场研究有一个特定的失败模式：一个说得通的故事、一批没人复核过的数字、和一个读起来像确定性的结论。这三个技能的存在，就是为了让这个结局在结构上难以发生。

| 技能 | 适合做什么 |
|---|---|
| [`market-performance-research`](skills/market-performance-research/) | 量化收益、回撤与风险。抓任何数据之前先把口径钉死 —— 样本域、数据截止日、基期、收益定义、封口规则 —— 让「今年以来的数字」只指一件事。|
| [`market-bottom-framework`](skills/market-bottom-framework/) | 用分层框架找底：价格结构、参与度广度、杠杆与仓位、美元流动性、信用与宏观压力、新叙事与边际买家。每个阈值都是论证出来的，不是断言的。|
| [`market-narrative-cycle-research`](skills/market-narrative-cycle-research/) | 把叙事周期映射成早期预警规则，带带日期的周期主轴，以及每条规则的失效条件。|

三者可以组合：**performance** 负责度量，**narrative** 负责解释序列，**bottom** 把两者合成一个带确认信号和证伪条件的决策。

## 它们强制什么

这不是风格偏好。每条规则都因为违反它就曾经至少发布过一次错误数字。

- **独立验证不是可选项。** 至少两个不同 scope 的子代理，外加一道机械校验；且校验器**不得** import 它要检验的指标实现 —— 共享实现会让同一个 bug 在检查的两侧一起复现。
- **每条序列都封口到最后一根已结算的 K 线。** 以开盘时间戳标记的日 K 在 UTC 日结束前仍在形成；把它当收盘价读，是「当前读数」失去可复现性最常见的原因。
- **正文表格由产物生成。** 手抄表格会悄悄漂移。生成器按稳定标记删除自己的上一版输出，幂等是被断言的，不是被假设的。
- **基期按日期断言，不按数值断言。** 用年内首个收盘价算出的年度收益，和用上一年末收盘价算出的不是一回事。
- **审计结论是待验证假设，不是替换值。** 每个建议值都要自己重算；本地复现不出来的值，是结论本身错了。

## 安装

把整个技能目录放进你的 agent 技能目录。各客户端的发现规则与权限不同，请先读每个技能的 `README.md` 与 `SKILL.md`。

```bash
git clone https://github.com/0xcjl/market-research-skills.git
# 装一个
cp -R market-research-skills/skills/market-bottom-framework ~/.agents/skills/market-bottom-framework
# 或者三个都装
for s in market-research-skills/skills/*/; do
  cp -R "$s" ~/.agents/skills/"$(basename "$s")"
done
```

环境要求：Python 3.10+（仅标准库），以及能访问所选数据端点的网络。

## 目录结构

```text
market-research-skills/
├── README.md / README.zh-CN.md
├── LICENSE
└── skills/
    ├── market-bottom-framework/        # SKILL.md + references/
    ├── market-performance-research/     # SKILL.md + references/ + templates/
    └── market-narrative-cycle-research/# SKILL.md + references/ + scripts/
```

## 相关项目

- [`0xcjl/jialin-skills`](https://github.com/0xcjl/jialin-skills) —— 更大范围的技能合集
- [`0xcjl/crypto-research`](https://github.com/0xcjl/crypto-research) —— 有证据链的 crypto 项目与代币研究

## 许可

MIT，见 [LICENSE](LICENSE)。每个技能目录各带一份。
