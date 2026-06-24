---
name: option-trade-summarizer-skill
description: 提取期权交易记录截图（OCR），通过 Python 脚本进行结构化统计、计算交易成本，并生成多维可视化 HTML 报告。
---

# 期权交易记录可视化与汇总助手

当用户要求进行期权归纳、汇总或可视化分析时，请严格按照以下工作流执行：

## 0. 获取截图数据
- 如果用户在对话框中直接上传了图片，请直接解析上传的图片。
- **默认设置**：如果用户未指定具体的截图文件，请主动查看 `~/Downloads/trade/` 目录下的图片文件（如 `.png`, `.jpg`），并取该目录下的文件作为分析的数据源。

## 1. 数据提取 (OCR & JSON 保存)
仔细识别并提取图片中的每一行交易记录。**不要在回复中输出长篇 Markdown 表格**，而是将提取的数据结构化为标准的 JSON 格式。

必须提取并清洗以下字段：
- `name`: 原始合约名称，如“科创50沽 7月1900”
- `underlying`: 标的名称 (从 name 中拆解，如“科创50”或“创业板ETF”)
- `option_type`: 期权类型 ("购" 或 "沽")
- `expiry`: 到期月份 (如“7月”或“9月”)
- `strike`: 行权价 (数值，如 1900)
- `type`: 交易类型方向，如“买平”、“卖开”
- `price`: 成交价 (浮点数)
- `quantity`: 成交量 (整数)

**数据校验要求**：
提取过程中，检查每行 `quantity` 是否超过 100，`price` 是否有离谱的极大/极小值。如果发现明显由于模糊导致的 OCR 错误，请先暂停并在回复中与用户核对异常数据。

若无异常，请将所有数据写入 JSON 文件（注意创建对应日期的目录）：
`~/outputs/option-trade-summarizer-skill/<YYYY-MM-DD-描述>/raw_data.json`

JSON 格式示例：
```json
[
  {
    "name": "科创50沽 7月1900",
    "underlying": "科创50",
    "option_type": "沽",
    "expiry": "7月",
    "strike": 1900,
    "type": "卖开",
    "price": 0.0621,
    "quantity": 10
  }
]
```

## 2. 调用处理脚本
在保存好 `raw_data.json` 之后，使用终端工具运行内置的 Python 脚本。该脚本负责计算金额、交易成本（买入收取 1.7 元/张，卖出 0 元），并生成交互式 HTML 报告：

```bash
python ~/.agents/skills/option-trade-summarizer-skill/scripts/generate_report.py ~/outputs/option-trade-summarizer-skill/<YYYY-MM-DD-描述>/raw_data.json
```

## 3. 回复用户
脚本执行成功并自动用浏览器打开 HTML 页面后，简单地用 1-2 句话向用户总结“数据已解析，可视化报告已在浏览器中打开”，无需重复输出具体数据。
