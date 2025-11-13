#!/usr/bin/env python3
"""
展示 AKShare API 返回的所有字段信息
"""

import akshare as ak
import pandas as pd
from datetime import datetime

def show_stock_news_fields():
    """展示股票新闻 API 返回的所有字段"""
    print("\n" + "="*80)
    print("1. 股票新闻 API - ak.stock_news_em()")
    print("="*80)

    # 获取大洋电机的新闻
    stock_code = "002249"
    print(f"\n测试股票：大洋电机 ({stock_code})")

    try:
        # 获取新闻数据
        news_df = ak.stock_news_em(symbol=stock_code)

        print(f"\n返回数据类型：pandas.DataFrame")
        print(f"数据行数：{len(news_df)} 条")
        print(f"\n所有字段列表：")
        print("-" * 40)

        # 显示所有列名
        for i, col in enumerate(news_df.columns, 1):
            print(f"{i:2}. {col}")

        # 显示第一条数据的详细内容
        if not news_df.empty:
            print("\n第一条新闻数据示例：")
            print("-" * 40)
            first_row = news_df.iloc[0]
            for col in news_df.columns:
                value = first_row[col]
                # 截断过长的内容
                if isinstance(value, str) and len(value) > 100:
                    value = value[:100] + "..."
                print(f"{col}: {value}")

        # 显示数据类型
        print("\n字段数据类型：")
        print("-" * 40)
        print(news_df.dtypes)

    except Exception as e:
        print(f"获取新闻数据失败：{str(e)}")

def show_financial_data_fields():
    """展示财务数据 API 返回的所有字段"""
    print("\n" + "="*80)
    print("2. 财务数据 API - ak.stock_financial_abstract_ths()")
    print("="*80)

    # 获取大洋电机的财务数据
    stock_code = "002249"
    print(f"\n测试股票：大洋电机 ({stock_code})")

    try:
        # 获取财务数据（按报告期）
        financial_df = ak.stock_financial_abstract_ths(symbol=stock_code, indicator='按报告期')

        print(f"\n返回数据类型：pandas.DataFrame")
        print(f"数据行数：{len(financial_df)} 条")
        print(f"\n所有字段列表：")
        print("-" * 40)

        # 显示所有列名
        for i, col in enumerate(financial_df.columns, 1):
            print(f"{i:2}. {col}")

        # 显示最新一条数据的详细内容
        if not financial_df.empty:
            print("\n最新财务数据示例（最近一期）：")
            print("-" * 40)
            latest_row = financial_df.iloc[-1]
            for col in financial_df.columns:
                value = latest_row[col]
                print(f"{col}: {value}")

        # 显示数据类型
        print("\n字段数据类型：")
        print("-" * 40)
        print(financial_df.dtypes)

    except Exception as e:
        print(f"获取财务数据失败：{str(e)}")

def show_financial_data_fields_by_year():
    """展示财务数据 API 按年度返回的字段"""
    print("\n" + "="*80)
    print("3. 财务数据 API - ak.stock_financial_abstract_ths() [按年度]")
    print("="*80)

    stock_code = "002249"
    print(f"\n测试股票：大洋电机 ({stock_code})")

    try:
        # 获取财务数据（按年度）
        financial_df = ak.stock_financial_abstract_ths(symbol=stock_code, indicator='按年度')

        print(f"\n返回数据类型：pandas.DataFrame")
        print(f"数据行数：{len(financial_df)} 条")
        print(f"\n所有字段列表（按年度）：")
        print("-" * 40)

        # 显示所有列名
        for i, col in enumerate(financial_df.columns, 1):
            print(f"{i:2}. {col}")

    except Exception as e:
        print(f"获取年度财务数据失败：{str(e)}")

def show_other_useful_apis():
    """展示其他有用的 AKShare API"""
    print("\n" + "="*80)
    print("4. 其他有用的 AKShare API")
    print("="*80)

    stock_code = "002249"

    # 1. 个股资金流向
    print("\n4.1 个股资金流向 - ak.stock_individual_fund_flow()")
    print("-" * 40)
    try:
        fund_flow = ak.stock_individual_fund_flow(stock=stock_code, market="深圳")
        print(f"字段列表：{list(fund_flow.columns)}")
    except Exception as e:
        print(f"获取失败：{str(e)}")

    # 2. 股票基本信息
    print("\n4.2 股票基本信息 - ak.stock_individual_info_em()")
    print("-" * 40)
    try:
        stock_info = ak.stock_individual_info_em(symbol=stock_code)
        print(f"字段列表：{list(stock_info.columns) if hasattr(stock_info, 'columns') else '返回字典格式'}")
        if isinstance(stock_info, pd.DataFrame):
            print("\n基本信息内容：")
            for _, row in stock_info.iterrows():
                print(f"  {row['item']}: {row['value']}")
    except Exception as e:
        print(f"获取失败：{str(e)}")

    # 3. 财务指标
    print("\n4.3 主要财务指标 - ak.stock_financial_analysis_indicator()")
    print("-" * 40)
    try:
        indicators = ak.stock_financial_analysis_indicator(symbol=stock_code)
        print(f"字段列表：{list(indicators.columns)}")
    except Exception as e:
        print(f"获取失败：{str(e)}")

def create_field_documentation():
    """创建字段说明文档"""
    print("\n" + "="*80)
    print("字段说明文档")
    print("="*80)

    print("""
1. 股票新闻字段说明 (ak.stock_news_em)：
   - 新闻标题：新闻的标题
   - 发布时间：新闻发布的时间戳
   - 新闻内容：新闻的详细内容
   - 新闻链接：新闻的原始链接

2. 财务数据字段说明 (ak.stock_financial_abstract_ths)：
   主要财务指标：
   - 报告期：财报的报告期（季度/年度）
   - 净利润：公司净利润（单位：亿元）
   - 净利润同比增长率：与去年同期相比的增长率
   - 扣非净利润：扣除非经常性损益后的净利润
   - 营业总收入：公司总营业收入
   - 营业总收入同比增长率：营收同比增长率
   - 基本每股收益：每股收益（EPS）
   - 每股净资产：每股净资产
   - 净资产收益率：ROE
   - 销售毛利率：毛利率
   - 资产负债率：负债占总资产的比例

   资产负债表指标：
   - 流动比率：流动资产/流动负债
   - 速动比率：（流动资产-存货）/流动负债
   - 产权比率：负债总额/股东权益

   现金流量表指标：
   - 每股经营现金流：经营活动产生的现金流量净额/总股本

   营运能力指标：
   - 存货周转率：销售成本/平均存货
   - 存货周转天数：365/存货周转率
   - 应收账款周转天数：应收账款周转期
   - 营业周期：存货周转天数+应收账款周转天数
    """)

def main():
    """主函数"""
    print("\n" + "="*80)
    print("AKShare API 字段信息完整展示")
    print("="*80)
    print(f"运行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 展示各个API的字段
    show_stock_news_fields()
    show_financial_data_fields()
    show_financial_data_fields_by_year()
    show_other_useful_apis()
    create_field_documentation()

    print("\n" + "="*80)
    print("字段信息展示完成")
    print("="*80)

if __name__ == "__main__":
    main()