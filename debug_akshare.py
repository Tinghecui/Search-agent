"""
调试脚本：查看 AKShare 返回的实际数据结构
"""

import akshare as ak
import pandas as pd

def check_akshare_data():
    """检查 AKShare 各个接口返回的数据结构"""

    print("=" * 80)
    print("AKShare 数据结构调试")
    print("=" * 80)

    stock_codes = ['002249', '600580']  # 大洋电机、卧龙电机

    for stock_code in stock_codes:
        print(f"\n{'='*80}")
        print(f"股票代码: {stock_code}")
        print(f"{'='*80}")

        # 测试 1: 财务分析指标
        print("\n[1] stock_financial_analysis_indicator")
        try:
            df = ak.stock_financial_analysis_indicator(symbol=stock_code)
            print(f"✅ 成功获取数据")
            print(f"数据形状: {df.shape}")
            print(f"列名: {list(df.columns)}")
            print(f"\n前3行数据:")
            print(df.head(3))
        except Exception as e:
            print(f"❌ 错误: {e}")

        # 测试 2: A股历史数据
        print(f"\n[2] stock_zh_a_hist (日线数据)")
        try:
            df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", adjust="qfq")
            print(f"✅ 成功获取数据")
            print(f"数据形状: {df.shape}")
            print(f"列名: {list(df.columns)}")
            print(f"\n最近3天数据:")
            print(df.tail(3))
        except Exception as e:
            print(f"❌ 错误: {e}")

        # 测试 3: 个股信息查询
        print(f"\n[3] stock_individual_info_em (个股信息)")
        try:
            df = ak.stock_individual_info_em(symbol=stock_code)
            print(f"✅ 成功获取数据")
            print(f"数据形状: {df.shape}")
            print(f"列名: {list(df.columns)}")
            print(f"\n数据预览:")
            print(df)
        except Exception as e:
            print(f"❌ 错误: {e}")

        # 测试 4: 财务指标
        print(f"\n[4] stock_financial_abstract (财务摘要)")
        try:
            df = ak.stock_financial_abstract(symbol=stock_code)
            print(f"✅ 成功获取数据")
            print(f"数据形状: {df.shape}")
            print(f"列名: {list(df.columns)}")
            print(f"\n数据预览:")
            print(df.head(3))
        except Exception as e:
            print(f"❌ 错误: {e}")

        # 测试 5: 股票新闻
        print(f"\n[5] stock_news_em (股票新闻)")
        try:
            df = ak.stock_news_em(symbol=stock_code)
            print(f"✅ 成功获取数据")
            print(f"数据形状: {df.shape}")
            print(f"列名: {list(df.columns)}")
            print(f"\n最新3条新闻:")
            print(df.head(3))
        except Exception as e:
            print(f"❌ 错误: {e}")

        print(f"\n{'='*80}\n")

if __name__ == "__main__":
    check_akshare_data()
