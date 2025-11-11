"""
Demo 演示脚本
快速演示项目的主要功能
"""

import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crawler.report_crawler import FinancialReportCrawler
from crawler.research_crawler import ResearchReportCrawler
from agent.financial_agent import FinancialAgent
from agent.tools import FinancialTools
import time


def print_banner(text):
    """打印横幅"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)


def demo_crawlers():
    """演示爬虫功能"""
    print_banner("📡 Demo 1: 数据采集功能")

    print("\n正在初始化爬虫...")
    financial_crawler = FinancialReportCrawler()
    research_crawler = ResearchReportCrawler()

    company = "大洋电机"
    print(f"\n目标公司: {company}")

    # 演示财报爬取
    print(f"\n[1/2] 爬取 {company} 财务数据...")
    financial_data = financial_crawler.get_financial_summary(company, years=3)

    if not financial_data.empty:
        print(f"✓ 成功获取 {len(financial_data)} 条财务记录")
        print(f"\n最新数据:")
        latest = financial_data.iloc[-1]
        print(f"  - 营业收入: {latest['营业收入(亿元)']} 亿元")
        print(f"  - 净利润: {latest['净利润(亿元)']} 亿元")
        print(f"  - ROE: {latest['净资产收益率(%)']}%")
        print(f"  - 资产负债率: {latest['资产负债率(%)']}%")

    # 演示研报爬取
    print(f"\n[2/2] 爬取 {company} 研报数据...")
    research_summary = research_crawler.get_research_summary(company, years=3)

    if research_summary:
        print(f"✓ 成功获取研报数据")
        print(f"  - 同花顺研报: {research_summary.get('tonghuashun_count', 0)} 条")
        print(f"  - 雪球文章: {research_summary.get('xueqiu_count', 0)} 条")
        print(f"  - 最新评级: {research_summary.get('latest_rating', 'N/A')}")

    print("\n✓ 数据采集演示完成")


def demo_agent():
    """演示 Agent 分析功能"""
    print_banner("🤖 Demo 2: AI 智能分析")

    print("\n正在初始化 Claude Agent...")
    try:
        agent = FinancialAgent()
        print("✓ Agent 初始化成功")
        print(f"  - 模型: {agent.model}")

        # 测试数据
        test_data = {
            'company_name': '大洋电机',
            'financial_metrics': {
                '营业收入': '150亿元',
                '净利润': '12亿元',
                '净资产收益率': '15%',
                '资产负债率': '45%'
            }
        }

        print(f"\n[1/3] 生成财务分析报告...")
        print("提示: 这将调用 Claude API，可能需要 10-20 秒...")

        analysis = agent.analyze_financial_data('大洋电机', test_data)

        print("\n" + "-"*70)
        print("AI 分析结果 (前 500 字符):")
        print("-"*70)
        print(analysis[:500] + "..." if len(analysis) > 500 else analysis)
        print("-"*70)

        print("\n✓ AI 分析演示完成")

    except Exception as e:
        print(f"\n✗ Agent 初始化失败: {str(e)}")
        print("  请检查 .env 文件中的 API 配置")


def demo_tools():
    """演示工具函数"""
    print_banner("🔧 Demo 3: 财务分析工具")

    tools = FinancialTools()

    print("\n[1/5] 增长率计算")
    current, previous = 120, 100
    growth = tools.calculate_growth_rate(current, previous)
    print(f"  当前值: {current}, 上期值: {previous}")
    print(f"  增长率: {growth:.2f}%")

    print("\n[2/5] 复合年均增长率 (CAGR)")
    start, end, years = 100, 150, 3
    cagr = tools.calculate_cagr(start, end, years)
    print(f"  起始值: {start}, 结束值: {end}, 期数: {years}年")
    print(f"  CAGR: {cagr:.2f}%")

    print("\n[3/5] 净资产收益率 (ROE)")
    net_profit, net_assets = 10, 100
    roe = tools.calculate_roe(net_profit, net_assets)
    print(f"  净利润: {net_profit}亿, 净资产: {net_assets}亿")
    print(f"  ROE: {roe:.2f}%")

    print("\n[4/5] 资产负债率")
    liabilities, assets = 45, 100
    debt_ratio = tools.calculate_debt_ratio(liabilities, assets)
    print(f"  总负债: {liabilities}亿, 总资产: {assets}亿")
    print(f"  资产负债率: {debt_ratio:.2f}%")

    print("\n[5/5] 流动比率")
    current_assets, current_liabilities = 80, 40
    current_ratio = tools.calculate_current_ratio(current_assets, current_liabilities)
    print(f"  流动资产: {current_assets}亿, 流动负债: {current_liabilities}亿")
    print(f"  流动比率: {current_ratio:.2f}")

    print("\n✓ 工具函数演示完成")


def demo_summary():
    """项目功能总结"""
    print_banner("📊 项目功能总结")

    features = [
        ("数据采集", [
            "支持东方财富、巨潮资讯财报数据",
            "支持同花顺、雪球研报数据",
            "自动化数据爬取和存储",
            "智能缓存机制"
        ]),
        ("AI 分析", [
            "基于 Claude Sonnet 4.5",
            "财务数据深度分析",
            "研报智能解读",
            "公司对比分析",
            "投资价值评估"
        ]),
        ("可视化", [
            "Streamlit 交互式界面",
            "Plotly 动态图表",
            "多维度数据展示",
            "一键生成投资报告"
        ]),
        ("分析工具", [
            "盈利能力分析",
            "偿债能力分析",
            "运营能力分析",
            "成长能力分析",
            "30+ 财务指标计算"
        ])
    ]

    for category, items in features:
        print(f"\n{category}:")
        for item in items:
            print(f"  ✓ {item}")

    print("\n" + "="*70)
    print("  目标公司: 大洋电机、卧龙电机")
    print("  数据范围: 最近 3 年")
    print("  技术栈: Python + Claude + Streamlit")
    print("="*70)


def main():
    """主函数"""
    print("\n" + "="*70)
    print("  🚀 AI 财务分析助手 - Demo 演示")
    print("  Powered by Anthropic Claude")
    print("="*70)

    demos = [
        ("1", "数据采集演示", demo_crawlers),
        ("2", "AI 分析演示", demo_agent),
        ("3", "工具函数演示", demo_tools),
        ("4", "项目总结", demo_summary),
        ("5", "全部演示", None)
    ]

    print("\n请选择要演示的内容:")
    for num, name, _ in demos:
        print(f"  {num}. {name}")

    choice = input("\n请输入选项 (1-5): ").strip()

    if choice == "1":
        demo_crawlers()
    elif choice == "2":
        demo_agent()
    elif choice == "3":
        demo_tools()
    elif choice == "4":
        demo_summary()
    elif choice == "5":
        print("\n开始全部演示...\n")
        demo_crawlers()
        time.sleep(2)
        demo_agent()
        time.sleep(2)
        demo_tools()
        time.sleep(2)
        demo_summary()
    else:
        print("\n无效选项！")
        return

    print("\n" + "="*70)
    print("  ✓ 演示完成！")
    print("\n  运行 Streamlit 应用查看完整功能:")
    print("    streamlit run app.py")
    print("\n  或使用启动脚本:")
    print("    ./run.sh (Linux/Mac)")
    print("    run.bat (Windows)")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
