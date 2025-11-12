"""
财报爬虫模块
使用 AKShare 获取上市公司财务数据
"""

import requests
import pandas as pd
import json
import time
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    import akshare as ak
    AKSHARE_AVAILABLE = True
    logger.info("AKShare 已成功导入")
except ImportError:
    AKSHARE_AVAILABLE = False
    logger.warning("AKShare 未安装，将使用模拟数据。请运行: pip install akshare")


class FinancialReportCrawler:
    """财务报告爬虫"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # 公司股票代码映射
        self.company_codes = {
            '大洋电机': '002249',
            '卧龙电机': '600580'
        }

    def get_stock_code(self, company_name: str) -> Optional[str]:
        """获取公司股票代码"""
        return self.company_codes.get(company_name)

    def get_financial_summary(self, company_name: str, years: int = 3) -> pd.DataFrame:
        """
        获取公司财务摘要数据（使用 AKShare）

        Args:
            company_name: 公司名称
            years: 获取最近几年的数据

        Returns:
            财务数据DataFrame
        """
        stock_code = self.get_stock_code(company_name)
        if not stock_code:
            logger.error(f"未找到公司 {company_name} 的股票代码")
            return pd.DataFrame()

        logger.info(f"开始获取 {company_name} ({stock_code}) 的财务数据...")

        if AKSHARE_AVAILABLE:
            try:
                return self._get_real_financial_data(company_name, stock_code, years)
            except Exception as e:
                logger.error(f"获取真实数据失败: {str(e)}，使用模拟数据")
                return self._get_mock_financial_data(company_name, stock_code, years)
        else:
            logger.warning(f"AKShare 未安装，使用模拟数据")
            return self._get_mock_financial_data(company_name, stock_code, years)

    def _get_real_financial_data(self, company_name: str, stock_code: str, years: int = 3) -> pd.DataFrame:
        """
        使用 AKShare 获取真实财务数据

        Args:
            company_name: 公司名称
            stock_code: 股票代码
            years: 获取最近几年的数据

        Returns:
            财务数据DataFrame
        """
        logger.info(f"正在从 AKShare 获取 {company_name} 的真实财务数据...")

        # 获取主要财务指标
        # AKShare 函数: stock_financial_abstract_ths
        try:
            # 获取财务摘要数据
            financial_data = ak.stock_financial_analysis_indicator(symbol=stock_code)

            if financial_data.empty:
                logger.warning(f"{company_name} 财务数据为空，尝试其他接口")
                # 尝试备用接口
                financial_data = ak.stock_zh_a_hist_min_em(symbol=stock_code, period='1', adjust='qfq')

            # 只保留最近几年的数据
            if '日期' in financial_data.columns:
                financial_data['日期'] = pd.to_datetime(financial_data['日期'])
                cutoff_date = datetime.now() - timedelta(days=365 * years)
                financial_data = financial_data[financial_data['日期'] >= cutoff_date]

            # 重命名列以匹配应用需求
            column_mapping = {
                '日期': '报告期',
                '营业收入': '营业收入(亿元)',
                '净利润': '净利润(亿元)',
                '总资产': '总资产(亿元)',
                '净资产': '净资产(亿元)',
                '资产负债率': '资产负债率(%)',
                '净资产收益率': '净资产收益率(%)',
                '每股收益': '每股收益(元)',
            }

            # 只重命名存在的列
            existing_columns = {k: v for k, v in column_mapping.items() if k in financial_data.columns}
            financial_data = financial_data.rename(columns=existing_columns)

            # 添加公司信息
            financial_data['公司名称'] = company_name
            financial_data['股票代码'] = stock_code

            # 转换单位（假设原始数据是元，转换为亿元）
            for col in ['营业收入(亿元)', '净利润(亿元)', '总资产(亿元)', '净资产(亿元)']:
                if col in financial_data.columns:
                    financial_data[col] = financial_data[col] / 100000000

            logger.info(f"成功获取 {company_name} 的真实财务数据，共 {len(financial_data)} 条记录")
            return financial_data

        except Exception as e:
            logger.error(f"AKShare 获取数据出错: {str(e)}")
            raise

    def _get_mock_financial_data(self, company_name: str, stock_code: str, years: int = 3) -> pd.DataFrame:
        """
        生成模拟财务数据（差异化版本）

        Args:
            company_name: 公司名称
            stock_code: 股票代码
            years: 生成最近几年的数据

        Returns:
            模拟财务数据DataFrame
        """
        logger.info(f"生成 {company_name} 的差异化模拟数据...")

        dates = pd.date_range(end=datetime.now(), periods=years*4, freq='Q')

        # 根据公司生成不同的基准数据
        if company_name == '大洋电机':
            # 大洋电机：中等规模，增长较快
            base_revenue = 45
            revenue_growth = 3.2
            base_profit = 4.5
            profit_growth = 0.35
            base_assets = 180
            base_equity = 95
            base_debt_ratio = 42
            base_roe = 9.5
            base_eps = 0.45
        elif company_name == '卧龙电机':
            # 卧龙电机：规模较大，增长稳定
            base_revenue = 65
            revenue_growth = 2.8
            base_profit = 6.2
            profit_growth = 0.28
            base_assets = 250
            base_equity = 130
            base_debt_ratio = 48
            base_roe = 8.2
            base_eps = 0.52
        else:
            # 默认值
            base_revenue = 50
            revenue_growth = 2.5
            base_profit = 5
            profit_growth = 0.3
            base_assets = 200
            base_equity = 100
            base_debt_ratio = 45
            base_roe = 8
            base_eps = 0.5

        data = {
            '报告期': dates.strftime('%Y-%m-%d').tolist(),
            '营业收入(亿元)': [
                round(base_revenue + i * revenue_growth + (i % 4) * 1.5, 2)
                for i in range(len(dates))
            ],
            '净利润(亿元)': [
                round(base_profit + i * profit_growth + (i % 4) * 0.2, 2)
                for i in range(len(dates))
            ],
            '总资产(亿元)': [
                round(base_assets + i * 5 + (i % 4) * 3, 2)
                for i in range(len(dates))
            ],
            '净资产(亿元)': [
                round(base_equity + i * 3 + (i % 4) * 2, 2)
                for i in range(len(dates))
            ],
            '资产负债率(%)': [
                round(base_debt_ratio + (i % 4) * 1.5, 2)
                for i in range(len(dates))
            ],
            '净资产收益率(%)': [
                round(base_roe + (i % 4) * 1.2 - i * 0.1, 2)
                for i in range(len(dates))
            ],
            '每股收益(元)': [
                round(base_eps + i * 0.04 + (i % 4) * 0.02, 2)
                for i in range(len(dates))
            ],
        }

        df = pd.DataFrame(data)
        df['公司名称'] = company_name
        df['股票代码'] = stock_code

        logger.info(f"成功生成 {company_name} 的差异化模拟数据")
        return df

    def crawl_eastmoney_financial_data(self, company_name: str, years: int = 3) -> Dict:
        """
        从东方财富网爬取财务数据（保留原有接口）

        Args:
            company_name: 公司名称
            years: 获取最近几年的数据

        Returns:
            包含财务数据的字典
        """
        stock_code = self.get_stock_code(company_name)
        if not stock_code:
            logger.error(f"未找到公司 {company_name} 的股票代码")
            return {}

        logger.info(f"开始爬取 {company_name}({stock_code}) 的财务数据...")

        try:
            # 东方财富网财务数据API
            financial_url = "https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/ZYZBAjaxNew"
            financial_params = {
                'companyType': '4',
                'reportDateType': '0',
                'reportType': '1',
                'dates': self._get_report_dates(years),
                'code': stock_code
            }

            response = requests.get(financial_url, params=financial_params, headers=self.headers, timeout=10)

            if response.status_code == 200:
                data = response.json()

                result = {
                    'company_name': company_name,
                    'stock_code': stock_code,
                    'crawl_time': datetime.now().isoformat(),
                    'source': '东方财富网',
                    'data': data
                }

                logger.info(f"成功爬取 {company_name} 的财务数据")
                return result
            else:
                logger.error(f"请求失败，状态码: {response.status_code}")
                return {}

        except Exception as e:
            logger.error(f"爬取 {company_name} 财务数据时出错: {str(e)}")
            return {}

    def crawl_cninfo_reports(self, company_name: str, years: int = 3) -> List[Dict]:
        """
        从巨潮资讯网爬取公司公告

        Args:
            company_name: 公司名称
            years: 获取最近几年的数据

        Returns:
            公告列表
        """
        stock_code = self.get_stock_code(company_name)
        if not stock_code:
            logger.error(f"未找到公司 {company_name} 的股票代码")
            return []

        logger.info(f"开始爬取 {company_name}({stock_code}) 的公告...")

        try:
            # 巨潮资讯网API
            url = "http://www.cninfo.com.cn/new/hisAnnouncement/query"

            end_date = datetime.now()
            start_date = end_date - timedelta(days=365 * years)

            data = {
                'pageNum': 1,
                'pageSize': 30,
                'tabName': 'fulltext',
                'column': 'szse',
                'stock': stock_code,
                'searchkey': '',
                'secid': '',
                'plate': '',
                'category': 'category_ndbg_szsh;',  # 年度报告
                'trade': '',
                'seDate': f'{start_date.strftime("%Y-%m-%d")}~{end_date.strftime("%Y-%m-%d")}'
            }

            response = requests.post(url, data=data, headers=self.headers, timeout=10)

            if response.status_code == 200:
                result = response.json()
                announcements = result.get('announcements', [])

                logger.info(f"成功爬取 {company_name} 的 {len(announcements)} 条公告")

                return [{
                    'company_name': company_name,
                    'stock_code': stock_code,
                    'title': item.get('announcementTitle'),
                    'date': item.get('announcementTime'),
                    'url': f"http://www.cninfo.com.cn/{item.get('adjunctUrl')}",
                    'type': item.get('announcementType'),
                    'source': '巨潮资讯网'
                } for item in announcements]
            else:
                logger.error(f"请求失败，状态码: {response.status_code}")
                return []

        except Exception as e:
            logger.error(f"爬取 {company_name} 公告时出错: {str(e)}")
            return []

    def _get_report_dates(self, years: int) -> str:
        """生成报告期日期字符串"""
        dates = []
        current_year = datetime.now().year

        for year in range(current_year - years, current_year + 1):
            for quarter in ['03-31', '06-30', '09-30', '12-31']:
                dates.append(f'{year}-{quarter}')

        return ','.join(dates[-12:])  # 返回最近12个季度

    def save_to_file(self, data: Dict, filename: str):
        """保存数据到文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"数据已保存到 {filename}")
        except Exception as e:
            logger.error(f"保存数据时出错: {str(e)}")


if __name__ == "__main__":
    # 测试代码
    crawler = FinancialReportCrawler()

    for company in ['大洋电机', '卧龙电机']:
        print(f"\n{'='*50}")
        print(f"正在处理: {company}")
        print(f"{'='*50}")

        # 获取财务摘要
        summary = crawler.get_financial_summary(company, years=3)
        if not summary.empty:
            print(f"\n{company} 财务数据预览:")
            print(summary.head())
            print(f"\n最新数据:")
            print(summary.iloc[-1])
            summary.to_csv(f'data/reports/{company}_summary.csv', index=False, encoding='utf-8-sig')

        time.sleep(2)  # 避免请求过快
