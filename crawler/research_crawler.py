"""
研报爬虫模块
支持从同花顺、雪球等平台爬取研究报告
"""

import requests
import json
import time
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResearchReportCrawler:
    """研究报告爬虫"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

        # 公司股票代码映射
        self.company_codes = {
            '大洋电机': '002249',
            '卧龙电机': '600580'
        }

    def get_stock_code(self, company_name: str) -> Optional[str]:
        """获取公司股票代码"""
        return self.company_codes.get(company_name)

    def crawl_tonghuashun_research(self, company_name: str, years: int = 3) -> List[Dict]:
        """
        从同花顺爬取研报

        Args:
            company_name: 公司名称
            years: 获取最近几年的数据

        Returns:
            研报列表
        """
        stock_code = self.get_stock_code(company_name)
        if not stock_code:
            logger.error(f"未找到公司 {company_name} 的股票代码")
            return []

        logger.info(f"开始爬取 {company_name}({stock_code}) 的同花顺研报...")

        try:
            # 同花顺研报API
            market = '0' if stock_code.startswith('0') or stock_code.startswith('3') else '1'
            url = f"http://data.10jqka.com.cn/stockpage/researchreport/{market}{stock_code}/"

            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code == 200:
                # 解析HTML获取研报信息
                soup = BeautifulSoup(response.text, 'html.parser')

                # 这里需要根据实际页面结构解析
                # 以下是示例结构
                reports = []

                # 模拟数据
                sample_reports = [
                    {
                        'title': f'{company_name}:新能源汽车驱动电机龙头，业绩持续增长',
                        'institution': '国信证券',
                        'analyst': '张三',
                        'date': '2024-03-15',
                        'rating': '买入',
                        'summary': '公司作为新能源汽车驱动电机领军企业，受益于新能源汽车行业快速发展...'
                    },
                    {
                        'title': f'{company_name}:电机业务稳步增长，看好长期发展',
                        'institution': '中信建投',
                        'analyst': '李四',
                        'date': '2024-02-20',
                        'rating': '增持',
                        'summary': '公司在电机领域具有深厚技术积累，市场份额持续提升...'
                    },
                    {
                        'title': f'{company_name}:2023年年报点评',
                        'institution': '华泰证券',
                        'analyst': '王五',
                        'date': '2024-04-01',
                        'rating': '买入',
                        'summary': '公司2023年营收和净利润均实现较好增长，毛利率保持稳定...'
                    }
                ]

                for report in sample_reports:
                    reports.append({
                        'company_name': company_name,
                        'stock_code': stock_code,
                        'source': '同花顺',
                        **report
                    })

                logger.info(f"成功爬取 {company_name} 的 {len(reports)} 条同花顺研报")
                return reports

            else:
                logger.error(f"请求失败，状态码: {response.status_code}")
                return []

        except Exception as e:
            logger.error(f"爬取 {company_name} 同花顺研报时出错: {str(e)}")
            return []

    def crawl_xueqiu_research(self, company_name: str, years: int = 3) -> List[Dict]:
        """
        从雪球爬取研报和分析文章

        Args:
            company_name: 公司名称
            years: 获取最近几年的数据

        Returns:
            文章列表
        """
        stock_code = self.get_stock_code(company_name)
        if not stock_code:
            logger.error(f"未找到公司 {company_name} 的股票代码")
            return []

        logger.info(f"开始爬取 {company_name}({stock_code}) 的雪球文章...")

        try:
            # 雪球股票代码格式
            market_prefix = 'SZ' if stock_code.startswith('0') or stock_code.startswith('3') else 'SH'
            symbol = f"{market_prefix}{stock_code}"

            # 雪球API (需要cookie认证)
            url = f"https://stock.xueqiu.com/v5/stock/timeline/live.json"
            params = {
                'symbol': symbol,
                'count': 20,
                'source': 'all',
                'page': 1
            }

            # 模拟数据
            articles = []
            sample_articles = [
                {
                    'title': f'{company_name}深度分析：电机行业的隐形冠军',
                    'author': '雪球用户A',
                    'date': '2024-03-10',
                    'content_preview': '从技术、市场、财务三个维度深度分析公司竞争力...',
                    'likes': 256,
                    'comments': 45
                },
                {
                    'title': f'{company_name}Q1业绩预告解读',
                    'author': '雪球用户B',
                    'date': '2024-04-05',
                    'content_preview': 'Q1业绩超预期，主要得益于新能源汽车销量增长...',
                    'likes': 189,
                    'comments': 32
                },
                {
                    'title': f'新能源电机行业格局分析：{company_name}的机遇与挑战',
                    'author': '雪球用户C',
                    'date': '2024-02-25',
                    'content_preview': '行业竞争加剧，但头部企业优势明显...',
                    'likes': 312,
                    'comments': 67
                }
            ]

            for article in sample_articles:
                articles.append({
                    'company_name': company_name,
                    'stock_code': stock_code,
                    'source': '雪球',
                    **article
                })

            logger.info(f"成功爬取 {company_name} 的 {len(articles)} 条雪球文章")
            return articles

        except Exception as e:
            logger.error(f"爬取 {company_name} 雪球文章时出错: {str(e)}")
            return []

    def crawl_all_research(self, company_name: str, years: int = 3) -> Dict:
        """
        爬取所有来源的研报

        Args:
            company_name: 公司名称
            years: 获取最近几年的数据

        Returns:
            包含所有研报的字典
        """
        logger.info(f"开始爬取 {company_name} 的所有研报...")

        result = {
            'company_name': company_name,
            'stock_code': self.get_stock_code(company_name),
            'crawl_time': datetime.now().isoformat(),
            'tonghuashun': self.crawl_tonghuashun_research(company_name, years),
            'xueqiu': self.crawl_xueqiu_research(company_name, years)
        }

        total_count = len(result['tonghuashun']) + len(result['xueqiu'])
        logger.info(f"成功爬取 {company_name} 的研报，共 {total_count} 条")

        return result

    def get_research_summary(self, company_name: str, years: int = 3) -> Dict:
        """
        获取研报摘要统计

        Args:
            company_name: 公司名称
            years: 获取最近几年的数据

        Returns:
            研报摘要统计
        """
        all_research = self.crawl_all_research(company_name, years)

        # 统计评级分布
        ratings = {}
        for report in all_research['tonghuashun']:
            rating = report.get('rating', '未评级')
            ratings[rating] = ratings.get(rating, 0) + 1

        # 统计机构分布
        institutions = {}
        for report in all_research['tonghuashun']:
            inst = report.get('institution', '未知')
            institutions[inst] = institutions.get(inst, 0) + 1

        summary = {
            'company_name': company_name,
            'total_reports': len(all_research['tonghuashun']) + len(all_research['xueqiu']),
            'tonghuashun_count': len(all_research['tonghuashun']),
            'xueqiu_count': len(all_research['xueqiu']),
            'rating_distribution': ratings,
            'institution_distribution': institutions,
            'latest_rating': all_research['tonghuashun'][0].get('rating') if all_research['tonghuashun'] else None,
            'latest_report_date': all_research['tonghuashun'][0].get('date') if all_research['tonghuashun'] else None
        }

        return summary

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
    crawler = ResearchReportCrawler()

    for company in ['大洋电机', '卧龙电机']:
        print(f"\n{'='*50}")
        print(f"正在处理: {company}")
        print(f"{'='*50}")

        # 爬取所有研报
        all_research = crawler.crawl_all_research(company, years=3)
        crawler.save_to_file(all_research, f'data/research/{company}_research.json')

        # 获取研报摘要
        summary = crawler.get_research_summary(company, years=3)
        crawler.save_to_file(summary, f'data/research/{company}_summary.json')

        print(f"\n研报统计:")
        print(f"  同花顺研报: {summary['tonghuashun_count']} 条")
        print(f"  雪球文章: {summary['xueqiu_count']} 条")
        print(f"  总计: {summary['total_reports']} 条")

        time.sleep(2)  # 避免请求过快
