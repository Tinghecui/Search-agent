# 🤖 AI 财务分析助手

基于 Anthropic Claude 的智能财务数据采集和分析系统，专注于上市公司财报和研报的自动化分析。

## 📋 项目简介

本项目是一个完整的金融数据分析 Demo，展示了如何使用 Anthropic Claude Agent 进行财务数据的采集、分析和可视化。

### 主要功能

- 🕷️ **数据采集**: 自动爬取大洋电机、卧龙电机的财报和研报数据
  - 财报数据源：东方财富、巨潮资讯
  - 研报数据源：同花顺、雪球
  - 时间范围：最近3年数据

- 🤖 **AI 智能分析**: 基于 Claude Sonnet 4.5
  - 财务数据深度分析（盈利能力、偿债能力、运营能力、成长能力）
  - 研报内容智能解读
  - 公司对比分析
  - 投资价值评估

- 📊 **可视化展示**: Streamlit 交互式界面
  - 实时数据展示
  - 动态图表
  - 多维度对比
  - 交互式问答

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd Search-agent
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境变量**

项目已包含 `.env` 文件，内容如下：
```env
LLM_MODEL=claude-sonnet-4-5-20250929
ANTHROPIC_API_KEY=cr_0238962535704516c89d95c983281a1665d86a08ba7f9d0ebb2927c06c05d0ec
ANTHROPIC_BASE_URL=https://claudecode.boomreal.ai/api
```

4. **运行应用**
```bash
streamlit run app.py
```

应用将在浏览器中自动打开，默认地址：`http://localhost:8501`

## 📁 项目结构

```
Search-agent/
├── app.py                      # Streamlit 主应用
├── .env                        # 环境变量配置
├── requirements.txt            # 项目依赖
├── README.md                   # 项目文档
│
├── agent/                      # AI Agent 模块
│   ├── __init__.py
│   ├── financial_agent.py      # Claude Agent 核心
│   └── tools.py                # 财务分析工具函数
│
├── crawler/                    # 爬虫模块
│   ├── __init__.py
│   ├── report_crawler.py       # 财报爬虫
│   └── research_crawler.py     # 研报爬虫
│
├── utils/                      # 工具函数
│   ├── __init__.py
│   └── helpers.py
│
└── data/                       # 数据存储
    ├── reports/                # 财报数据
    ├── research/               # 研报数据
    └── cache/                  # 缓存数据
```

## 💡 使用指南

### 1. 数据总览

- 查看公司最新财务指标
- 浏览研报摘要
- 快速了解公司概况

### 2. 财务分析

- **趋势图表**: 营收、利润、ROE等指标的时间趋势
- **财务指标**: 关键财务数据一览
- **AI 分析**: Claude Agent 深度分析财务数据

### 3. 研报分析

- 浏览同花顺券商研报
- 查看雪球用户分析文章
- AI 智能解读市场观点

### 4. 公司对比

- 双公司关键指标对比
- 趋势对比分析
- AI 生成综合对比报告

### 5. 智能问答

- 向 AI 助手提问任何关于公司的问题
- 基于真实数据的专业回答
- 支持多轮对话

### 6. 投资报告

- 一键生成完整投资分析报告
- 包含财务分析、市场研究、估值分析等
- 支持报告下载

## 🔧 核心技术

### 数据采集

- **requests**: HTTP 请求
- **BeautifulSoup**: HTML 解析
- **pandas**: 数据处理

### AI 分析

- **Anthropic Claude API**: Claude Sonnet 4.5
- **自定义 Agent**: 财务分析专用 Agent
- **Tool Functions**: 丰富的财务分析工具

### 可视化

- **Streamlit**: Web 界面框架
- **Plotly**: 交互式图表
- **Pandas**: 数据表格

## 📊 数据源说明

### 财报数据

1. **东方财富网**
   - 主要财务指标
   - 财务报表数据
   - 实时更新

2. **巨潮资讯网**
   - 官方公告
   - 年报、季报
   - 权威可靠

### 研报数据

1. **同花顺**
   - 券商研报
   - 机构评级
   - 专业分析

2. **雪球**
   - 用户分析
   - 市场观点
   - 社区讨论

## 🎯 分析能力

### 财务分析维度

1. **盈利能力**
   - 营业收入趋势
   - 净利润变化
   - 毛利率/净利率
   - 盈利质量

2. **偿债能力**
   - 资产负债率
   - 流动比率
   - 速动比率
   - 债务结构

3. **运营能力**
   - 资产周转率
   - 应收账款周转
   - 存货周转

4. **成长能力**
   - 营收增长率
   - 利润增长率
   - CAGR 计算

5. **投资价值**
   - ROE 分析
   - EPS 趋势
   - 估值水平
   - 投资建议

## 🔒 注意事项

1. **数据准确性**:
   - 数据来自公开渠道，仅供参考
   - 建议以官方公告为准

2. **API 限制**:
   - 注意爬虫频率限制
   - 遵守网站使用条款

3. **投资风险**:
   - AI 分析仅供参考
   - 投资需谨慎，请独立决策

4. **隐私保护**:
   - 不要将 API Key 提交到公共仓库
   - 已在 `.gitignore` 中排除敏感文件

## 🛠️ 开发指南

### 添加新公司

在 `crawler/report_crawler.py` 和 `crawler/research_crawler.py` 中修改：

```python
self.company_codes = {
    '大洋电机': '002249',
    '卧龙电机': '600580',
    '新公司名': '股票代码'  # 添加新公司
}
```

### 自定义分析

在 `agent/tools.py` 中添加新的分析函数：

```python
@staticmethod
def your_custom_analysis(data):
    # 自定义分析逻辑
    pass
```

### 扩展数据源

在 `crawler/` 目录下创建新的爬虫模块。

## 📝 示例截图

### 数据总览
![数据总览](docs/screenshots/overview.png)

### 财务分析
![财务分析](docs/screenshots/financial.png)

### AI 对话
![AI 对话](docs/screenshots/qa.png)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 License

MIT License

## 🙏 致谢

- [Anthropic](https://www.anthropic.com/) - Claude AI
- [Streamlit](https://streamlit.io/) - Web 框架
- 各数据源平台

## 📧 联系方式

如有问题或建议，欢迎联系。

---

**免责声明**: 本项目仅用于技术演示和学习目的，不构成任何投资建议。投资有风险，入市需谨慎。
