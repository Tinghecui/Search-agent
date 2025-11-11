"""
Claude Financial Analysis Agent
使用 Anthropic Claude API 进行财务分析
"""

import os
import json
from typing import List, Dict, Optional, Any
import anthropic
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()


class FinancialAgent:
    """财务分析 Agent"""

    def __init__(self):
        """初始化 Agent"""
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.base_url = os.getenv('ANTHROPIC_BASE_URL')
        self.model = os.getenv('LLM_MODEL', 'claude-sonnet-4-5-20250929')

        if not self.api_key:
            raise ValueError("未找到 ANTHROPIC_API_KEY 环境变量")

        # 初始化 Anthropic 客户端
        self.client = anthropic.Anthropic(
            api_key=self.api_key,
            base_url=self.base_url
        )

        logger.info(f"财务分析 Agent 初始化成功，使用模型: {self.model}")

    def analyze_financial_data(self, company_name: str, financial_data: Dict) -> str:
        """
        分析财务数据

        Args:
            company_name: 公司名称
            financial_data: 财务数据

        Returns:
            分析结果
        """
        logger.info(f"开始分析 {company_name} 的财务数据...")

        prompt = f"""请作为一位专业的财务分析师，分析以下公司的财务数据：

公司名称：{company_name}

财务数据：
{json.dumps(financial_data, ensure_ascii=False, indent=2)}

请从以下几个方面进行深入分析：

1. 盈利能力分析
   - 营业收入趋势
   - 净利润变化
   - 毛利率和净利率水平
   - 盈利质量评估

2. 偿债能力分析
   - 资产负债率
   - 流动比率
   - 速动比率
   - 债务结构分析

3. 运营能力分析
   - 总资产周转率
   - 应收账款周转率
   - 存货周转率

4. 成长能力分析
   - 营收增长率
   - 净利润增长率
   - 净资产增长率

5. 投资价值分析
   - 净资产收益率(ROE)
   - 每股收益(EPS)
   - 市盈率水平（如果有）
   - 投资建议

请用中文给出详细、专业的分析报告，重点突出关键财务指标和投资建议。"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            analysis = message.content[0].text
            logger.info(f"{company_name} 财务数据分析完成")
            return analysis

        except Exception as e:
            logger.error(f"分析财务数据时出错: {str(e)}")
            return f"分析出错: {str(e)}"

    def analyze_research_reports(self, company_name: str, reports: List[Dict]) -> str:
        """
        分析研报内容

        Args:
            company_name: 公司名称
            reports: 研报列表

        Returns:
            分析结果
        """
        logger.info(f"开始分析 {company_name} 的研报...")

        # 整理研报信息
        report_summary = []
        for report in reports[:10]:  # 只分析前10条
            report_summary.append({
                'title': report.get('title', ''),
                'institution': report.get('institution', ''),
                'date': report.get('date', ''),
                'rating': report.get('rating', ''),
                'summary': report.get('summary', report.get('content_preview', ''))
            })

        prompt = f"""请作为一位专业的投资分析师，分析以下关于 {company_name} 的研究报告：

研报信息：
{json.dumps(report_summary, ensure_ascii=False, indent=2)}

请从以下角度进行综合分析：

1. 市场共识
   - 各机构的评级分布
   - 主流观点和分歧点
   - 投资逻辑总结

2. 关键投资主题
   - 主要投资亮点
   - 潜在风险因素
   - 行业地位和竞争优势

3. 业绩预期
   - 机构对业绩的预期
   - 增长驱动因素
   - 不确定性因素

4. 投资建议综合
   - 基于研报的综合投资建议
   - 适合的投资者类型
   - 关注要点

请用中文给出专业、客观的分析总结。"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            analysis = message.content[0].text
            logger.info(f"{company_name} 研报分析完成")
            return analysis

        except Exception as e:
            logger.error(f"分析研报时出错: {str(e)}")
            return f"分析出错: {str(e)}"

    def compare_companies(self, company1_data: Dict, company2_data: Dict) -> str:
        """
        对比两家公司

        Args:
            company1_data: 公司1的数据
            company2_data: 公司2的数据

        Returns:
            对比分析结果
        """
        company1_name = company1_data.get('company_name', '公司1')
        company2_name = company2_data.get('company_name', '公司2')

        logger.info(f"开始对比 {company1_name} 和 {company2_name}...")

        prompt = f"""请作为一位专业的投资分析师，对比分析以下两家公司：

公司1：{company1_name}
数据：
{json.dumps(company1_data, ensure_ascii=False, indent=2)}

公司2：{company2_name}
数据：
{json.dumps(company2_data, ensure_ascii=False, indent=2)}

请从以下维度进行详细对比：

1. 规模对比
   - 营业收入规模
   - 资产规模
   - 市场地位

2. 盈利能力对比
   - 净利润水平
   - 盈利能力指标（ROE、净利率等）
   - 盈利质量

3. 成长性对比
   - 营收增长率
   - 利润增长率
   - 成长可持续性

4. 财务健康度对比
   - 资产负债率
   - 现金流状况
   - 风险水平

5. 投资价值对比
   - 估值水平
   - 投资性价比
   - 风险收益比

6. 综合评价
   - 各自的优势和劣势
   - 适合的投资策略
   - 投资建议

请用中文给出专业、客观、详细的对比分析报告。"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            analysis = message.content[0].text
            logger.info(f"{company1_name} 和 {company2_name} 对比分析完成")
            return analysis

        except Exception as e:
            logger.error(f"对比分析时出错: {str(e)}")
            return f"分析出错: {str(e)}"

    def answer_question(self, question: str, context: Dict) -> str:
        """
        回答关于公司的问题

        Args:
            question: 用户问题
            context: 上下文数据（财务数据、研报等）

        Returns:
            回答
        """
        logger.info(f"回答问题: {question}")

        prompt = f"""你是一位专业的财务分析师和投资顾问。基于以下数据回答用户的问题。

可用数据：
{json.dumps(context, ensure_ascii=False, indent=2)}

用户问题：{question}

请给出专业、准确、详细的回答。如果数据不足以回答问题，请说明需要什么额外信息。"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            answer = message.content[0].text
            logger.info("问题回答完成")
            return answer

        except Exception as e:
            logger.error(f"回答问题时出错: {str(e)}")
            return f"回答出错: {str(e)}"

    def generate_investment_report(self, company_name: str, all_data: Dict) -> str:
        """
        生成综合投资报告

        Args:
            company_name: 公司名称
            all_data: 所有数据（财务数据、研报等）

        Returns:
            投资报告
        """
        logger.info(f"生成 {company_name} 的综合投资报告...")

        prompt = f"""请作为一位资深投资分析师，基于以下全部数据，为 {company_name} 生成一份完整的投资分析报告。

完整数据：
{json.dumps(all_data, ensure_ascii=False, indent=2)}

报告应包含以下部分：

# {company_name} 投资分析报告

## 一、公司概况
- 基本信息
- 主营业务
- 行业地位

## 二、财务分析
- 盈利能力分析
- 偿债能力分析
- 运营能力分析
- 成长能力分析

## 三、市场研究
- 机构研报观点汇总
- 市场评级分布
- 投资逻辑分析

## 四、竞争优势
- 核心竞争力
- 护城河分析
- 风险因素

## 五、估值分析
- 当前估值水平
- 历史估值对比
- 合理估值区间

## 六、投资建议
- 投资评级
- 目标价位（如适用）
- 投资策略
- 风险提示

请生成一份专业、全面、客观的投资分析报告，用中文撰写。"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=8192,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            report = message.content[0].text
            logger.info(f"{company_name} 投资报告生成完成")
            return report

        except Exception as e:
            logger.error(f"生成报告时出错: {str(e)}")
            return f"生成报告出错: {str(e)}"


if __name__ == "__main__":
    # 测试代码
    agent = FinancialAgent()

    # 测试数据
    test_data = {
        'company_name': '大洋电机',
        'financial_summary': {
            '营业收入': '150亿元',
            '净利润': '12亿元',
            '总资产': '300亿元',
            '净资产收益率': '15%'
        }
    }

    # 测试财务分析
    print("="*50)
    print("测试财务分析")
    print("="*50)
    result = agent.analyze_financial_data('大洋电机', test_data)
    print(result)
