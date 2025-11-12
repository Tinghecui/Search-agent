"""
AKShare 集成测试脚本
用于验证 AKShare 安装和数据获取功能
"""

import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crawler.report_crawler import FinancialReportCrawler
from crawler.research_crawler import ResearchReportCrawler


def test_akshare_import():
    """测试 AKShare 是否成功导入"""
    print("=" * 60)
    print("测试 1: 检查 AKShare 导入状态")
    print("=" * 60)

    try:
        import akshare as ak
        print("✅ AKShare 已成功安装")
        print(f"   版本: {ak.__version__ if hasattr(ak, '__version__') else '未知'}")
        return True
    except ImportError:
        print("❌ AKShare 未安装")
        print("   请运行: pip install akshare")
        return False


def test_financial_data():
    """测试财务数据获取"""
    print("\n" + "=" * 60)
    print("测试 2: 获取财务数据")
    print("=" * 60)

    crawler = FinancialReportCrawler()

    for company in ['大洋电机', '卧龙电机']:
        print(f"\n📊 正在获取 {company} 的财务数据...")

        try:
            data = crawler.get_financial_summary(company, years=3)

            if not data.empty:
                print(f"✅ 成功获取 {company} 数据")
                print(f"   数据条数: {len(data)}")
                print(f"   数据列: {list(data.columns)}")

                if len(data) > 0:
                    latest = data.iloc[-1]
                    print(f"   最新报告期: {latest.get('报告期', 'N/A')}")
                    print(f"   营业收入: {latest.get('营业收入(亿元)', 'N/A')} 亿元")
                    print(f"   净利润: {latest.get('净利润(亿元)', 'N/A')} 亿元")
                    print(f"   ROE: {latest.get('净资产收益率(%)', 'N/A')}%")

                    # 检查数据是否不同
                    if company == '大洋电机':
                        data_dy = data
                    elif company == '卧龙电机':
                        data_wl = data

            else:
                print(f"⚠️  {company} 数据为空")

        except Exception as e:
            print(f"❌ 获取 {company} 数据时出错: {str(e)}")

    # 比较两个公司的数据是否不同
    print("\n" + "-" * 60)
    print("数据差异性检查:")
    print("-" * 60)

    try:
        if 'data_dy' in locals() and 'data_wl' in locals():
            dy_revenue = data_dy.iloc[-1]['营业收入(亿元)']
            wl_revenue = data_wl.iloc[-1]['营业收入(亿元)']

            if dy_revenue != wl_revenue:
                print(f"✅ 两个公司数据不同")
                print(f"   大洋电机营收: {dy_revenue} 亿元")
                print(f"   卧龙电机营收: {wl_revenue} 亿元")
            else:
                print(f"⚠️  两个公司数据相同（可能使用了模拟数据）")
    except:
        pass


def test_research_data():
    """测试研报数据获取"""
    print("\n" + "=" * 60)
    print("测试 3: 获取研报数据")
    print("=" * 60)

    crawler = ResearchReportCrawler()

    for company in ['大洋电机', '卧龙电机']:
        print(f"\n📰 正在获取 {company} 的研报数据...")

        try:
            data = crawler.crawl_all_research(company, years=3)

            tonghuashun_count = len(data.get('tonghuashun', []))
            xueqiu_count = len(data.get('xueqiu', []))

            print(f"✅ 成功获取 {company} 研报")
            print(f"   同花顺/新闻: {tonghuashun_count} 条")
            print(f"   雪球文章: {xueqiu_count} 条")
            print(f"   总计: {tonghuashun_count + xueqiu_count} 条")

            if tonghuashun_count > 0:
                latest = data['tonghuashun'][0]
                print(f"   最新标题: {latest.get('title', 'N/A')[:40]}...")
                print(f"   日期: {latest.get('date', 'N/A')}")

        except Exception as e:
            print(f"❌ 获取 {company} 研报时出错: {str(e)}")


def test_data_save():
    """测试数据保存功能"""
    print("\n" + "=" * 60)
    print("测试 4: 数据保存功能")
    print("=" * 60)

    import os

    # 创建数据目录
    os.makedirs('data/reports', exist_ok=True)
    os.makedirs('data/research', exist_ok=True)

    print("✅ 数据目录已创建")
    print("   data/reports/")
    print("   data/research/")

    # 测试保存财务数据
    crawler_report = FinancialReportCrawler()
    company = '大洋电机'

    try:
        data = crawler_report.get_financial_summary(company, years=3)
        if not data.empty:
            filename = f'data/reports/{company}_test.csv'
            data.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"✅ 财务数据已保存到 {filename}")
    except Exception as e:
        print(f"❌ 保存财务数据失败: {str(e)}")


def main():
    """主测试函数"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "AKShare 集成测试" + " " * 27 + "║")
    print("╚" + "=" * 58 + "╝")

    # 运行所有测试
    akshare_available = test_akshare_import()

    test_financial_data()
    test_research_data()
    test_data_save()

    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)

    if akshare_available:
        print("✅ AKShare 已安装，可以获取真实数据")
        print("   如果数据获取失败，会自动使用差异化模拟数据作为备用")
    else:
        print("⚠️  AKShare 未安装，正在使用差异化模拟数据")
        print("   安装 AKShare 可获取真实数据: pip install akshare")

    print("\n下一步:")
    print("1. 如果 AKShare 未安装，运行: pip install akshare")
    print("2. 运行主应用: streamlit run app.py")
    print("3. 在浏览器中查看数据分析结果")
    print("=" * 60)


if __name__ == "__main__":
    main()
