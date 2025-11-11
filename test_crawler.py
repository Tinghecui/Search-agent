"""
测试爬虫功能
"""

import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crawler.report_crawler import FinancialReportCrawler
from crawler.research_crawler import ResearchReportCrawler
import time


def test_financial_crawler():
    """测试财报爬虫"""
    print("="*60)
    print("测试财报爬虫")
    print("="*60)

    crawler = FinancialReportCrawler()

    companies = ['大洋电机', '卧龙电机']

    for company in companies:
        print(f"\n正在爬取 {company} 的数据...")

        # 测试财务摘要
        summary = crawler.get_financial_summary(company, years=3)
        print(f"\n{company} 财务摘要:")
        print(summary.head())

        # 保存数据
        if not summary.empty:
            summary.to_csv(f'data/reports/{company}_summary.csv', index=False, encoding='utf-8-sig')
            print(f"✓ 数据已保存到 data/reports/{company}_summary.csv")

        time.sleep(1)


def test_research_crawler():
    """测试研报爬虫"""
    print("\n" + "="*60)
    print("测试研报爬虫")
    print("="*60)

    crawler = ResearchReportCrawler()

    companies = ['大洋电机', '卧龙电机']

    for company in companies:
        print(f"\n正在爬取 {company} 的研报...")

        # 获取研报摘要
        summary = crawler.get_research_summary(company, years=3)

        print(f"\n{company} 研报统计:")
        print(f"  同花顺研报: {summary.get('tonghuashun_count', 0)} 条")
        print(f"  雪球文章: {summary.get('xueqiu_count', 0)} 条")
        print(f"  总计: {summary.get('total_reports', 0)} 条")

        if summary.get('latest_rating'):
            print(f"  最新评级: {summary['latest_rating']}")
            print(f"  最新日期: {summary['latest_report_date']}")

        # 保存数据
        crawler.save_to_file(summary, f'data/research/{company}_summary.json')
        print(f"✓ 数据已保存到 data/research/{company}_summary.json")

        time.sleep(1)


if __name__ == "__main__":
    print("\n" + "="*60)
    print("开始测试爬虫模块")
    print("="*60)

    # 创建数据目录
    os.makedirs('data/reports', exist_ok=True)
    os.makedirs('data/research', exist_ok=True)

    # 测试财报爬虫
    test_financial_crawler()

    # 测试研报爬虫
    test_research_crawler()

    print("\n" + "="*60)
    print("测试完成！")
    print("="*60)
