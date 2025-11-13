#!/usr/bin/env python3
"""
MCP Server for Financial Analysis
提供财务数据查询和分析的 MCP 工具
"""

import asyncio
import json
import logging
import sys
from typing import Any

# 添加项目路径
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from mcp.server.stdio import stdio_server

from crawler.report_crawler import FinancialReportCrawler
from crawler.research_crawler import ResearchReportCrawler
from agent.financial_agent import FinancialAgent

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化组件
financial_crawler = FinancialReportCrawler()
research_crawler = ResearchReportCrawler()

try:
    financial_agent = FinancialAgent()
    logger.info("Financial Agent 初始化成功")
except Exception as e:
    logger.error(f"Financial Agent 初始化失败: {e}")
    financial_agent = None

# 创建 MCP 服务器
app = Server("financial-analysis-server")

# 支持的公司列表
SUPPORTED_COMPANIES = ["大洋电机", "卧龙电机"]


@app.list_tools()
async def list_tools() -> list[Tool]:
    """列出所有可用的工具"""
    return [
        Tool(
            name="get_financial_data",
            description="获取公司的财务数据，包括营业收入、净利润、ROE等关键财务指标",
            inputSchema={
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": "string",
                        "description": f"公司名称，支持: {', '.join(SUPPORTED_COMPANIES)}",
                        "enum": SUPPORTED_COMPANIES
                    },
                    "years": {
                        "type": "number",
                        "description": "获取最近几年的数据，默认3年",
                        "default": 3
                    }
                },
                "required": ["company_name"]
            }
        ),
        Tool(
            name="get_research_reports",
            description="获取公司的研报和新闻数据",
            inputSchema={
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": "string",
                        "description": f"公司名称，支持: {', '.join(SUPPORTED_COMPANIES)}",
                        "enum": SUPPORTED_COMPANIES
                    },
                    "years": {
                        "type": "number",
                        "description": "获取最近几年的数据，默认3年",
                        "default": 3
                    }
                },
                "required": ["company_name"]
            }
        ),
        Tool(
            name="analyze_financial_data",
            description="使用 AI 对公司财务数据进行深度分析，包括盈利能力、偿债能力、运营能力等",
            inputSchema={
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": "string",
                        "description": f"公司名称，支持: {', '.join(SUPPORTED_COMPANIES)}",
                        "enum": SUPPORTED_COMPANIES
                    },
                    "years": {
                        "type": "number",
                        "description": "分析最近几年的数据，默认3年",
                        "default": 3
                    }
                },
                "required": ["company_name"]
            }
        ),
        Tool(
            name="analyze_research_reports",
            description="使用 AI 分析公司的研报和新闻，总结市场观点和投资建议",
            inputSchema={
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": "string",
                        "description": f"公司名称，支持: {', '.join(SUPPORTED_COMPANIES)}",
                        "enum": SUPPORTED_COMPANIES
                    },
                    "years": {
                        "type": "number",
                        "description": "分析最近几年的数据，默认3年",
                        "default": 3
                    }
                },
                "required": ["company_name"]
            }
        ),
        Tool(
            name="compare_companies",
            description="对比分析两家公司的财务数据和投资价值",
            inputSchema={
                "type": "object",
                "properties": {
                    "company1": {
                        "type": "string",
                        "description": f"第一家公司名称，支持: {', '.join(SUPPORTED_COMPANIES)}",
                        "enum": SUPPORTED_COMPANIES
                    },
                    "company2": {
                        "type": "string",
                        "description": f"第二家公司名称，支持: {', '.join(SUPPORTED_COMPANIES)}",
                        "enum": SUPPORTED_COMPANIES
                    },
                    "years": {
                        "type": "number",
                        "description": "对比最近几年的数据，默认3年",
                        "default": 3
                    }
                },
                "required": ["company1", "company2"]
            }
        ),
        Tool(
            name="generate_investment_report",
            description="生成公司的完整投资分析报告，包括财务分析、市场研究、估值分析等",
            inputSchema={
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": "string",
                        "description": f"公司名称，支持: {', '.join(SUPPORTED_COMPANIES)}",
                        "enum": SUPPORTED_COMPANIES
                    },
                    "years": {
                        "type": "number",
                        "description": "报告涵盖最近几年的数据，默认3年",
                        "default": 3
                    }
                },
                "required": ["company_name"]
            }
        ),
        Tool(
            name="answer_question",
            description="基于公司的财务数据和研报，回答关于公司的任何问题",
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "关于公司的问题"
                    },
                    "company_name": {
                        "type": "string",
                        "description": f"相关的公司名称（可选），支持: {', '.join(SUPPORTED_COMPANIES)}",
                        "enum": SUPPORTED_COMPANIES + ["所有公司"]
                    }
                },
                "required": ["question"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """处理工具调用"""

    try:
        if name == "get_financial_data":
            company_name = arguments["company_name"]
            years = arguments.get("years", 3)

            logger.info(f"获取 {company_name} 的财务数据...")
            data = financial_crawler.get_financial_summary(company_name, years)

            if data.empty:
                return [TextContent(
                    type="text",
                    text=f"未能获取 {company_name} 的财务数据"
                )]

            # 格式化数据为表格
            result = f"# {company_name} 财务数据\n\n"
            result += f"共 {len(data)} 条记录，时间范围: {data['报告期'].iloc[0]} 至 {data['报告期'].iloc[-1]}\n\n"
            result += "## 最新财务指标\n\n"

            latest = data.iloc[-1]
            result += f"- 报告期: {latest['报告期']}\n"
            result += f"- 营业收入: {latest.get('营业收入(亿元)', 'N/A')} 亿元\n"
            result += f"- 净利润: {latest.get('净利润(亿元)', 'N/A')} 亿元\n"
            result += f"- 净资产收益率(ROE): {latest.get('净资产收益率(%)', 'N/A')}%\n"
            result += f"- 资产负债率: {latest.get('资产负债率(%)', 'N/A')}%\n"
            result += f"- 每股收益(EPS): {latest.get('每股收益(元)', 'N/A')} 元\n\n"

            result += "## 历史数据\n\n"
            result += data.tail(5).to_markdown(index=False)

            return [TextContent(type="text", text=result)]

        elif name == "get_research_reports":
            company_name = arguments["company_name"]
            years = arguments.get("years", 3)

            logger.info(f"获取 {company_name} 的研报数据...")
            data = research_crawler.crawl_all_research(company_name, years)

            if not data:
                return [TextContent(
                    type="text",
                    text=f"未能获取 {company_name} 的研报数据"
                )]

            result = f"# {company_name} 研报和新闻\n\n"

            # 新闻
            if data.get('tonghuashun'):
                result += f"## 新闻 ({len(data['tonghuashun'])} 条)\n\n"
                for i, news in enumerate(data['tonghuashun'][:5], 1):
                    result += f"{i}. **{news['title']}**\n"
                    result += f"   - 日期: {news.get('date', 'N/A')}\n"
                    result += f"   - 摘要: {news.get('summary', 'N/A')}\n\n"

            # 雪球文章
            if data.get('xueqiu'):
                result += f"\n## 雪球文章 ({len(data['xueqiu'])} 条)\n\n"
                for i, article in enumerate(data['xueqiu'][:5], 1):
                    result += f"{i}. **{article['title']}**\n"
                    result += f"   - 作者: {article.get('author', 'N/A')}\n"
                    result += f"   - 日期: {article.get('date', 'N/A')}\n"
                    result += f"   - 点赞: {article.get('likes', 'N/A')} | 评论: {article.get('comments', 'N/A')}\n\n"

            return [TextContent(type="text", text=result)]

        elif name == "analyze_financial_data":
            if not financial_agent:
                return [TextContent(
                    type="text",
                    text="AI 分析功能不可用，请检查配置"
                )]

            company_name = arguments["company_name"]
            years = arguments.get("years", 3)

            logger.info(f"AI 分析 {company_name} 的财务数据...")
            data = financial_crawler.get_financial_summary(company_name, years)

            if data.empty:
                return [TextContent(
                    type="text",
                    text=f"未能获取 {company_name} 的财务数据"
                )]

            analysis = financial_agent.analyze_financial_data(
                company_name,
                data.to_dict('records')
            )

            return [TextContent(type="text", text=analysis)]

        elif name == "analyze_research_reports":
            if not financial_agent:
                return [TextContent(
                    type="text",
                    text="AI 分析功能不可用，请检查配置"
                )]

            company_name = arguments["company_name"]
            years = arguments.get("years", 3)

            logger.info(f"AI 分析 {company_name} 的研报...")
            data = research_crawler.crawl_all_research(company_name, years)

            if not data:
                return [TextContent(
                    type="text",
                    text=f"未能获取 {company_name} 的研报数据"
                )]

            all_reports = data.get('tonghuashun', []) + data.get('xueqiu', [])
            analysis = financial_agent.analyze_research_reports(company_name, all_reports)

            return [TextContent(type="text", text=analysis)]

        elif name == "compare_companies":
            if not financial_agent:
                return [TextContent(
                    type="text",
                    text="AI 分析功能不可用，请检查配置"
                )]

            company1 = arguments["company1"]
            company2 = arguments["company2"]
            years = arguments.get("years", 3)

            logger.info(f"对比分析 {company1} 和 {company2}...")

            data1 = financial_crawler.get_financial_summary(company1, years)
            data2 = financial_crawler.get_financial_summary(company2, years)

            if data1.empty or data2.empty:
                return [TextContent(
                    type="text",
                    text="数据不足，无法进行对比"
                )]

            comparison_data1 = {
                'company_name': company1,
                'financial_data': data1.to_dict('records')
            }
            comparison_data2 = {
                'company_name': company2,
                'financial_data': data2.to_dict('records')
            }

            analysis = financial_agent.compare_companies(comparison_data1, comparison_data2)

            return [TextContent(type="text", text=analysis)]

        elif name == "generate_investment_report":
            if not financial_agent:
                return [TextContent(
                    type="text",
                    text="AI 分析功能不可用，请检查配置"
                )]

            company_name = arguments["company_name"]
            years = arguments.get("years", 3)

            logger.info(f"生成 {company_name} 的投资报告...")

            financial_data = financial_crawler.get_financial_summary(company_name, years)
            research_data = research_crawler.crawl_all_research(company_name, years)

            all_data = {
                'company_name': company_name,
                'financial_data': financial_data.to_dict('records') if not financial_data.empty else [],
                'research_data': research_data
            }

            report = financial_agent.generate_investment_report(company_name, all_data)

            return [TextContent(type="text", text=report)]

        elif name == "answer_question":
            if not financial_agent:
                return [TextContent(
                    type="text",
                    text="AI 问答功能不可用，请检查配置"
                )]

            question = arguments["question"]
            company_name = arguments.get("company_name", "所有公司")

            logger.info(f"回答问题: {question}")

            # 收集相关公司的数据
            context = {}
            companies = SUPPORTED_COMPANIES if company_name == "所有公司" else [company_name]

            for company in companies:
                financial_data = financial_crawler.get_financial_summary(company, 3)
                research_data = research_crawler.crawl_all_research(company, 3)
                context[company] = {
                    'financial': financial_data.to_dict('records') if not financial_data.empty else [],
                    'research': research_data
                }

            answer = financial_agent.answer_question(question, context)

            return [TextContent(type="text", text=answer)]

        else:
            return [TextContent(
                type="text",
                text=f"未知的工具: {name}"
            )]

    except Exception as e:
        logger.error(f"工具调用出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return [TextContent(
            type="text",
            text=f"执行出错: {str(e)}"
        )]


async def main():
    """主函数"""
    logger.info("Starting Financial Analysis MCP Server...")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
