"""
Agent 工具函数
提供各种财务分析和数据处理工具
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FinancialTools:
    """财务分析工具集"""

    @staticmethod
    def calculate_growth_rate(current: float, previous: float) -> float:
        """
        计算增长率

        Args:
            current: 当前值
            previous: 上期值

        Returns:
            增长率（百分比）
        """
        if previous == 0:
            return 0
        return ((current - previous) / previous) * 100

    @staticmethod
    def calculate_cagr(start_value: float, end_value: float, periods: int) -> float:
        """
        计算复合年均增长率 (CAGR)

        Args:
            start_value: 起始值
            end_value: 结束值
            periods: 期数

        Returns:
            复合年均增长率（百分比）
        """
        if start_value == 0 or periods == 0:
            return 0
        return (pow(end_value / start_value, 1 / periods) - 1) * 100

    @staticmethod
    def calculate_roe(net_profit: float, net_assets: float) -> float:
        """
        计算净资产收益率 (ROE)

        Args:
            net_profit: 净利润
            net_assets: 净资产

        Returns:
            ROE（百分比）
        """
        if net_assets == 0:
            return 0
        return (net_profit / net_assets) * 100

    @staticmethod
    def calculate_roa(net_profit: float, total_assets: float) -> float:
        """
        计算总资产收益率 (ROA)

        Args:
            net_profit: 净利润
            total_assets: 总资产

        Returns:
            ROA（百分比）
        """
        if total_assets == 0:
            return 0
        return (net_profit / total_assets) * 100

    @staticmethod
    def calculate_debt_ratio(total_liabilities: float, total_assets: float) -> float:
        """
        计算资产负债率

        Args:
            total_liabilities: 总负债
            total_assets: 总资产

        Returns:
            资产负债率（百分比）
        """
        if total_assets == 0:
            return 0
        return (total_liabilities / total_assets) * 100

    @staticmethod
    def calculate_current_ratio(current_assets: float, current_liabilities: float) -> float:
        """
        计算流动比率

        Args:
            current_assets: 流动资产
            current_liabilities: 流动负债

        Returns:
            流动比率
        """
        if current_liabilities == 0:
            return 0
        return current_assets / current_liabilities

    @staticmethod
    def calculate_gross_margin(revenue: float, cost: float) -> float:
        """
        计算毛利率

        Args:
            revenue: 营业收入
            cost: 营业成本

        Returns:
            毛利率（百分比）
        """
        if revenue == 0:
            return 0
        return ((revenue - cost) / revenue) * 100

    @staticmethod
    def calculate_net_margin(net_profit: float, revenue: float) -> float:
        """
        计算净利率

        Args:
            net_profit: 净利润
            revenue: 营业收入

        Returns:
            净利率（百分比）
        """
        if revenue == 0:
            return 0
        return (net_profit / revenue) * 100

    @staticmethod
    def analyze_profitability(financial_data: pd.DataFrame) -> Dict:
        """
        盈利能力分析

        Args:
            financial_data: 财务数据DataFrame

        Returns:
            盈利能力分析结果
        """
        try:
            analysis = {
                'revenue_trend': [],
                'profit_trend': [],
                'margin_trend': [],
                'roe_trend': []
            }

            if '营业收入(亿元)' in financial_data.columns:
                revenue = financial_data['营业收入(亿元)'].tolist()
                analysis['revenue_trend'] = revenue
                analysis['revenue_growth'] = [
                    FinancialTools.calculate_growth_rate(revenue[i], revenue[i-1])
                    for i in range(1, len(revenue))
                ]

            if '净利润(亿元)' in financial_data.columns:
                profit = financial_data['净利润(亿元)'].tolist()
                analysis['profit_trend'] = profit
                analysis['profit_growth'] = [
                    FinancialTools.calculate_growth_rate(profit[i], profit[i-1])
                    for i in range(1, len(profit))
                ]

            if '净资产收益率(%)' in financial_data.columns:
                analysis['roe_trend'] = financial_data['净资产收益率(%)'].tolist()

            return analysis

        except Exception as e:
            logger.error(f"盈利能力分析出错: {str(e)}")
            return {}

    @staticmethod
    def analyze_solvency(financial_data: pd.DataFrame) -> Dict:
        """
        偿债能力分析

        Args:
            financial_data: 财务数据DataFrame

        Returns:
            偿债能力分析结果
        """
        try:
            analysis = {
                'debt_ratio_trend': [],
                'solvency_rating': ''
            }

            if '资产负债率(%)' in financial_data.columns:
                debt_ratio = financial_data['资产负债率(%)'].tolist()
                analysis['debt_ratio_trend'] = debt_ratio

                # 评级
                avg_debt_ratio = sum(debt_ratio) / len(debt_ratio)
                if avg_debt_ratio < 40:
                    analysis['solvency_rating'] = '优秀'
                elif avg_debt_ratio < 60:
                    analysis['solvency_rating'] = '良好'
                elif avg_debt_ratio < 70:
                    analysis['solvency_rating'] = '一般'
                else:
                    analysis['solvency_rating'] = '较差'

            return analysis

        except Exception as e:
            logger.error(f"偿债能力分析出错: {str(e)}")
            return {}

    @staticmethod
    def compare_metrics(company1_data: pd.DataFrame, company2_data: pd.DataFrame) -> Dict:
        """
        对比两家公司的关键指标

        Args:
            company1_data: 公司1数据
            company2_data: 公司2数据

        Returns:
            对比结果
        """
        try:
            comparison = {
                'revenue_comparison': {},
                'profit_comparison': {},
                'roe_comparison': {},
                'growth_comparison': {}
            }

            # 营收对比
            if '营业收入(亿元)' in company1_data.columns and '营业收入(亿元)' in company2_data.columns:
                rev1 = company1_data['营业收入(亿元)'].iloc[-1]
                rev2 = company2_data['营业收入(亿元)'].iloc[-1]
                comparison['revenue_comparison'] = {
                    'company1_latest': rev1,
                    'company2_latest': rev2,
                    'ratio': rev1 / rev2 if rev2 != 0 else 0
                }

            # 利润对比
            if '净利润(亿元)' in company1_data.columns and '净利润(亿元)' in company2_data.columns:
                profit1 = company1_data['净利润(亿元)'].iloc[-1]
                profit2 = company2_data['净利润(亿元)'].iloc[-1]
                comparison['profit_comparison'] = {
                    'company1_latest': profit1,
                    'company2_latest': profit2,
                    'ratio': profit1 / profit2 if profit2 != 0 else 0
                }

            # ROE对比
            if '净资产收益率(%)' in company1_data.columns and '净资产收益率(%)' in company2_data.columns:
                roe1 = company1_data['净资产收益率(%)'].iloc[-1]
                roe2 = company2_data['净资产收益率(%)'].iloc[-1]
                comparison['roe_comparison'] = {
                    'company1_latest': roe1,
                    'company2_latest': roe2,
                    'difference': roe1 - roe2
                }

            return comparison

        except Exception as e:
            logger.error(f"指标对比出错: {str(e)}")
            return {}

    @staticmethod
    def extract_key_metrics(financial_data: pd.DataFrame) -> Dict:
        """
        提取关键财务指标

        Args:
            financial_data: 财务数据DataFrame

        Returns:
            关键指标字典
        """
        try:
            metrics = {}

            if not financial_data.empty:
                latest = financial_data.iloc[-1]

                metrics['latest_revenue'] = latest.get('营业收入(亿元)', 0)
                metrics['latest_profit'] = latest.get('净利润(亿元)', 0)
                metrics['latest_assets'] = latest.get('总资产(亿元)', 0)
                metrics['latest_equity'] = latest.get('净资产(亿元)', 0)
                metrics['latest_debt_ratio'] = latest.get('资产负债率(%)', 0)
                metrics['latest_roe'] = latest.get('净资产收益率(%)', 0)
                metrics['latest_eps'] = latest.get('每股收益(元)', 0)

                # 计算增长率
                if len(financial_data) >= 2:
                    prev = financial_data.iloc[-2]
                    if '营业收入(亿元)' in financial_data.columns:
                        metrics['revenue_growth'] = FinancialTools.calculate_growth_rate(
                            latest.get('营业收入(亿元)', 0),
                            prev.get('营业收入(亿元)', 0)
                        )
                    if '净利润(亿元)' in financial_data.columns:
                        metrics['profit_growth'] = FinancialTools.calculate_growth_rate(
                            latest.get('净利润(亿元)', 0),
                            prev.get('净利润(亿元)', 0)
                        )

            return metrics

        except Exception as e:
            logger.error(f"提取关键指标出错: {str(e)}")
            return {}

    @staticmethod
    def generate_summary_stats(financial_data: pd.DataFrame) -> Dict:
        """
        生成汇总统计

        Args:
            financial_data: 财务数据DataFrame

        Returns:
            汇总统计
        """
        try:
            stats = {}

            numeric_columns = financial_data.select_dtypes(include=[np.number]).columns

            for col in numeric_columns:
                stats[col] = {
                    'mean': financial_data[col].mean(),
                    'median': financial_data[col].median(),
                    'std': financial_data[col].std(),
                    'min': financial_data[col].min(),
                    'max': financial_data[col].max()
                }

            return stats

        except Exception as e:
            logger.error(f"生成汇总统计出错: {str(e)}")
            return {}


if __name__ == "__main__":
    # 测试工具函数
    tools = FinancialTools()

    # 测试增长率计算
    growth = tools.calculate_growth_rate(120, 100)
    print(f"增长率: {growth}%")

    # 测试 CAGR
    cagr = tools.calculate_cagr(100, 150, 3)
    print(f"复合年均增长率: {cagr:.2f}%")

    # 测试 ROE
    roe = tools.calculate_roe(10, 100)
    print(f"ROE: {roe}%")
