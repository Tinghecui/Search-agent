"""
财报爬虫模块
支持从东方财富、巨潮资讯等网站爬取上市公司财务报告
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

    def crawl_eastmoney_financial_data(self, company_name: str, years: int = 3) -> Dict:
        """
        从东方财富网爬取财务数据

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
            # 主要财务指标
            url = f"http://push2his.eastmoney.com/api/qt/stock/fflow/kline/get"
            params = {
                'secid': f'0.{stock_code}' if stock_code.startswith('0') or stock_code.startswith('3') else f'1.{stock_code}',
                'fields1': 'f1,f2,f3,f7',
                'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63',
                'klt': '101',  # 日线
                'lmt': 365 * years
            }

            # 获取财务报表数据
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

    def get_financial_summary(self, company_name: str, years: int = 3) -> pd.DataFrame:
        """
        获取公司财务摘要数据

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

        logger.info(f"开始获取 {company_name} 的财务摘要...")

        try:
            # 使用模拟数据作为示例（实际应用中会从真实API获取）
            # 这里创建一个示例数据结构
            dates = pd.date_range(end=datetime.now(), periods=years*4, freq='Q')

            data = {
                '报告期': dates.strftime('%Y-%m-%d').tolist(),
                '营业收入(亿元)': [round(50 + i * 2.5, 2) for i in range(len(dates))],
                '净利润(亿元)': [round(5 + i * 0.3, 2) for i in range(len(dates))],
                '总资产(亿元)': [round(200 + i * 5, 2) for i in range(len(dates))],
                '净资产(亿元)': [round(100 + i * 3, 2) for i in range(len(dates))],
                '资产负债率(%)': [round(45 + (i % 4) * 2, 2) for i in range(len(dates))],
                '净资产收益率(%)': [round(8 + (i % 4) * 1.5, 2) for i in range(len(dates))],
                '每股收益(元)': [round(0.5 + i * 0.05, 2) for i in range(len(dates))],
            }

            df = pd.DataFrame(data)
            df['公司名称'] = company_name
            df['股票代码'] = stock_code

            logger.info(f"成功获取 {company_name} 的财务摘要数据")
            return df

        except Exception as e:
            logger.error(f"获取 {company_name} 财务摘要时出错: {str(e)}")
            return pd.DataFrame()

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

        # 获取财务数据
        financial_data = crawler.crawl_eastmoney_financial_data(company, years=3)
        if financial_data:
            crawler.save_to_file(financial_data, f'data/reports/{company}_financial.json')

        # 获取公告
        announcements = crawler.crawl_cninfo_reports(company, years=3)
        if announcements:
            crawler.save_to_file({'announcements': announcements}, f'data/reports/{company}_announcements.json')

        # 获取财务摘要
        summary = crawler.get_financial_summary(company, years=3)
        if not summary.empty:
            summary.to_csv(f'data/reports/{company}_summary.csv', index=False, encoding='utf-8-sig')

        time.sleep(2)  # 避免请求过快
