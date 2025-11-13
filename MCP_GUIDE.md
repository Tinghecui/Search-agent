# 🔌 MCP Server 使用指南

## 📋 简介

本项目已集成 **Model Context Protocol (MCP)** 服务器，可以在 Claude Desktop 或其他支持 MCP 的应用中直接通过对话交互使用财务分析功能。

### MCP 是什么？

MCP (Model Context Protocol) 是 Anthropic 推出的开放协议，让 AI 助手能够安全地访问本地工具和数据源。通过 MCP，Claude 可以：
- 📊 实时获取公司财务数据
- 🤖 使用 AI 进行深度分析
- 💬 通过自然对话完成复杂分析任务

## 🚀 快速开始

### 1. 安装 MCP 依赖

```bash
# 激活虚拟环境
source venv/bin/activate  # Mac/Linux
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install mcp>=0.9.0
```

### 2. 配置 Claude Desktop

在 Claude Desktop 配置文件中添加 MCP 服务器配置：

**Mac/Linux**: `~/.config/claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "financial-analysis": {
      "command": "/Users/YOUR_USERNAME/Desktop/boomreal/Search-agent/venv/bin/python",
      "args": [
        "/Users/YOUR_USERNAME/Desktop/boomreal/Search-agent/mcp_server.py"
      ],
      "env": {
        "ANTHROPIC_API_KEY": "your-api-key-here",
        "ANTHROPIC_BASE_URL": "https://claudecode.boomreal.ai/api"
      }
    }
  }
}
```

**重要**: 替换上面的路径为你的实际路径！

### 3. 重启 Claude Desktop

配置完成后，重启 Claude Desktop 应用。

### 4. 开始使用

在 Claude Desktop 中，你现在可以直接对话：

```
你: 帮我获取大洋电机的财务数据
你: 分析一下卧龙电机的盈利能力
你: 对比大洋电机和卧龙电机，哪个更值得投资？
```

## 🛠️ 可用工具

MCP 服务器提供以下 7 个工具：

### 1. `get_financial_data`
获取公司财务数据

**参数**:
- `company_name`: 公司名称（大洋电机 或 卧龙电机）
- `years`: 获取最近几年的数据（默认3年）

**示例**:
```
获取大洋电机最近3年的财务数据
```

### 2. `get_research_reports`
获取公司研报和新闻

**参数**:
- `company_name`: 公司名称
- `years`: 获取最近几年的数据（默认3年）

**示例**:
```
查看卧龙电机的最新研报
```

### 3. `analyze_financial_data`
AI 深度分析财务数据

**参数**:
- `company_name`: 公司名称
- `years`: 分析最近几年的数据（默认3年）

**示例**:
```
帮我深度分析大洋电机的财务状况
```

### 4. `analyze_research_reports`
AI 分析研报和新闻

**参数**:
- `company_name`: 公司名称
- `years`: 分析最近几年的数据（默认3年）

**示例**:
```
分析市场对卧龙电机的看法
```

### 5. `compare_companies`
对比两家公司

**参数**:
- `company1`: 第一家公司名称
- `company2`: 第二家公司名称
- `years`: 对比最近几年的数据（默认3年）

**示例**:
```
对比大洋电机和卧龙电机的投资价值
```

### 6. `generate_investment_report`
生成完整投资报告

**参数**:
- `company_name`: 公司名称
- `years`: 报告涵盖最近几年的数据（默认3年）

**示例**:
```
生成大洋电机的完整投资分析报告
```

### 7. `answer_question`
回答关于公司的问题

**参数**:
- `question`: 你的问题
- `company_name`: 相关公司（可选）

**示例**:
```
大洋电机的营收增长趋势如何？
卧龙电机的资产负债率健康吗？
这两家公司哪个更稳健？
```

## 💬 对话示例

### 示例 1: 基础查询

```
你: 帮我查一下大洋电机的最新财务数据

Claude: [调用 get_financial_data 工具]

# 大洋电机 财务数据

共 12 条记录，时间范围: 2022-12-31 至 2025-09-30

## 最新财务指标

- 报告期: 2025-09-30
- 营业收入: 91.80 亿元
- 净利润: 8.45 亿元
- 净资产收益率(ROE): 9.00%
- 资产负债率: 45.21%
- 每股收益(EPS): 0.35 元

[更多详细数据...]
```

### 示例 2: AI 分析

```
你: 帮我深度分析大洋电机的盈利能力和成长性

Claude: [调用 analyze_financial_data 工具]

根据大洋电机最近3年的财务数据，我为您进行如下深度分析：

## 一、盈利能力分析

### 1. 营业收入趋势
大洋电机的营业收入呈现持续增长态势...

### 2. 净利润变化
净利润从 2022 年的 4.27 亿增长至 2025Q3 的 8.45 亿...

[详细的 AI 分析报告...]
```

### 示例 3: 公司对比

```
你: 对比一下大洋电机和卧龙电机，帮我分析哪个投资价值更高

Claude: [调用 compare_companies 工具]

# 大洋电机 vs 卧龙电机 投资价值对比分析

## 一、规模对比
- 大洋电机: 营收 91.80 亿，净利润 8.45 亿
- 卧龙电机: 营收 119.67 亿，净利润 8.19 亿

## 二、盈利能力对比
...

[详细的对比分析报告...]
```

## 🔧 高级配置

### 自定义环境变量

你可以在配置文件中设置更多环境变量：

```json
{
  "mcpServers": {
    "financial-analysis": {
      "command": "...",
      "args": ["..."],
      "env": {
        "ANTHROPIC_API_KEY": "your-key",
        "ANTHROPIC_BASE_URL": "your-base-url",
        "LLM_MODEL": "claude-sonnet-4-5-20250929",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### 使用不同的 Python 解释器

如果你想使用系统 Python 而不是虚拟环境：

```json
{
  "mcpServers": {
    "financial-analysis": {
      "command": "/usr/bin/python3",
      "args": [
        "/path/to/Search-agent/mcp_server.py"
      ]
    }
  }
}
```

## 🐛 故障排查

### 问题 1: MCP 服务器无法启动

**检查**:
1. Python 路径是否正确
2. mcp_server.py 路径是否正确
3. 虚拟环境是否激活并安装了依赖

**解决**:
```bash
# 测试服务器是否能运行
source venv/bin/activate
python mcp_server.py
```

### 问题 2: 工具调用失败

**可能原因**:
- API Key 未配置或无效
- 网络连接问题
- AKShare 数据获取失败

**解决**:
检查 Claude Desktop 的日志文件：
- Mac: `~/Library/Logs/Claude/mcp*.log`
- Windows: `%APPDATA%\Claude\Logs\mcp*.log`

### 问题 3: 数据不准确

**说明**:
- 财务数据来自 AKShare（同花顺）
- 如果 AKShare 不可用，会自动降级到模拟数据
- 模拟数据仅用于演示

**解决**:
确保网络畅通，AKShare 可以正常访问

## 📚 更多资源

- [MCP 官方文档](https://modelcontextprotocol.io/)
- [Claude Desktop 下载](https://claude.ai/download)
- [AKShare 文档](https://akshare.akfamily.xyz/)

## 🎯 最佳实践

### 1. 明确的问题描述

好的提问方式：
```
✅ 帮我分析大洋电机2023-2025年的盈利能力变化趋势
✅ 对比大洋电机和卧龙电机的资产负债率，哪个更健康？
✅ 生成大洋电机的完整投资报告，重点关注成长性
```

避免模糊的提问：
```
❌ 分析一下
❌ 怎么样？
❌ 好不好？
```

### 2. 分步骤深入分析

对于复杂分析，可以分步进行：
```
1. 先获取财务数据
2. 然后深度分析
3. 再查看市场研报
4. 最后生成投资报告
```

### 3. 利用 AI 能力

MCP 结合了 Claude 的理解能力，你可以：
- 问开放式问题
- 要求总结要点
- 比较历史趋势
- 预测未来走向（基于历史数据）

## 🎉 开始使用

现在你已经了解了如何使用 MCP Server 进行财务分析！

打开 Claude Desktop，开始对话吧：

```
你: 帮我分析一下大洋电机的投资价值
```

Claude 会自动调用合适的工具，为你提供专业的财务分析！
