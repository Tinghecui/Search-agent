"""
测试 Claude Agent 功能
"""

import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.financial_agent import FinancialAgent
from agent.tools import FinancialTools
import pandas as pd


def test_agent():
    """测试 Agent 基本功能"""
    print("="*60)
    print("测试 Claude Financial Agent")
    print("="*60)

    try:
        # 初始化 Agent
        print("\n初始化 Agent...")
        agent = FinancialAgent()
        print("✓ Agent 初始化成功")

        # 测试数据
        test_financial_data = {
            'company_name': '大洋电机',
            'stock_code': '002249',
            'financial_metrics': {
                '营业收入': '150亿元',
                '净利润': '12亿元',
                '总资产': '300亿元',
                '净资产': '200亿元',
                '资产负债率': '45%',
                '净资产收益率': '15%',
                '每股收益': '1.2元'
            },
            'growth_data': {
                '营收增长率': '18%',
                '利润增长率': '22%'
            }
        }

        # 测试财务分析
        print("\n" + "="*60)
        print("测试财务数据分析")
        print("="*60)

        result = agent.analyze_financial_data('大洋电机', test_financial_data)
        print(result[:500] + "..." if len(result) > 500 else result)
        print("\n✓ 财务分析测试完成")

        # 测试研报分析
        print("\n" + "="*60)
        print("测试研报分析")
        print("="*60)

        test_reports = [
            {
                'title': '大洋电机：新能源汽车驱动电机领军企业',
                'institution': '国信证券',
                'date': '2024-03-15',
                'rating': '买入',
                'summary': '公司在新能源汽车驱动电机领域具有领先地位'
            }
        ]

        result = agent.analyze_research_reports('大洋电机', test_reports)
        print(result[:500] + "..." if len(result) > 500 else result)
        print("\n✓ 研报分析测试完成")

        # 测试问答
        print("\n" + "="*60)
        print("测试智能问答")
        print("="*60)

        question = "大洋电机的盈利能力如何？"
        context = {
            '大洋电机': test_financial_data
        }

        answer = agent.answer_question(question, context)
        print(f"问题: {question}")
        print(f"回答: {answer[:300]}..." if len(answer) > 300 else f"回答: {answer}")
        print("\n✓ 问答测试完成")

    except Exception as e:
        print(f"\n✗ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()


def test_tools():
    """测试工具函数"""
    print("\n" + "="*60)
    print("测试财务分析工具")
    print("="*60)

    tools = FinancialTools()

    # 测试增长率计算
    growth = tools.calculate_growth_rate(120, 100)
    print(f"\n增长率计算: 120/100 = {growth:.2f}%")
    assert growth == 20.0, "增长率计算错误"
    print("✓ 增长率计算正确")

    # 测试 CAGR
    cagr = tools.calculate_cagr(100, 150, 3)
    print(f"\nCAGR 计算: 100->150 (3年) = {cagr:.2f}%")
    print("✓ CAGR 计算正确")

    # 测试 ROE
    roe = tools.calculate_roe(10, 100)
    print(f"\nROE 计算: 10/100 = {roe:.2f}%")
    assert roe == 10.0, "ROE 计算错误"
    print("✓ ROE 计算正确")

    # 测试资产负债率
    debt_ratio = tools.calculate_debt_ratio(45, 100)
    print(f"\n资产负债率: 45/100 = {debt_ratio:.2f}%")
    assert debt_ratio == 45.0, "资产负债率计算错误"
    print("✓ 资产负债率计算正确")

    print("\n✓ 所有工具函数测试通过")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("开始测试 Agent 模块")
    print("="*60)

    # 测试工具函数
    test_tools()

    # 测试 Agent
    test_agent()

    print("\n" + "="*60)
    print("所有测试完成！")
    print("="*60)
