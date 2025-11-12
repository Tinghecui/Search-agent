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
            财务数据DataFrame（标准化列名）
        """
        logger.info(f"正在从 AKShare 获取 {company_name} 的真实财务数据...")

        try:
            # 使用东方财富的业绩报表接口获取财务数据
            # 这个接口返回：报告期、营业收入、净利润等关键财务指标
            logger.info(f"尝试获取 {stock_code} 的业绩报表数据...")
            financial_data = ak.stock_yjbb_em(symbol=stock_code)

            if financial_data.empty:
                logger.warning(f"{company_name} 业绩报表为空，尝试财务分析指标接口")
                financial_data = ak.stock_financial_analysis_indicator(symbol=stock_code)

            if financial_data.empty:
                logger.warning(f"{company_name} 财务分析指标也为空，尝试个股信息接口")
                # 最后尝试获取个股基本信息
                financial_data = ak.stock_individual_info_em(symbol=stock_code)

            logger.info(f"原始数据列名: {list(financial_data.columns)}")
            logger.info(f"原始数据形状: {financial_data.shape}")

            # 打印前几行以调试
            if not financial_data.empty:
                logger.info(f"数据预览:\n{financial_data.head(3)}")

            # 标准化列名映射（根据 AKShare 实际返回的列名）
            # 这里需要处理多种可能的列名格式
            column_mapping = self._build_column_mapping(financial_data.columns)

            # 重命名列
            financial_data = financial_data.rename(columns=column_mapping)

            # 确保必需的列存在，如果不存在则创建默认值
            required_columns = {
                '报告期': datetime.now().strftime('%Y-%m-%d'),
                '营业收入(亿元)': 0.0,
                '净利润(亿元)': 0.0,
                '总资产(亿元)': 0.0,
                '净资产(亿元)': 0.0,
                '资产负债率(%)': 0.0,
                '净资产收益率(%)': 0.0,
                '每股收益(元)': 0.0,
            }

            for col, default_val in required_columns.items():
                if col not in financial_data.columns:
                    logger.warning(f"列 '{col}' 不存在，使用默认值")
                    financial_data[col] = default_val

            # 处理日期列
            if '报告期' in financial_data.columns:
                financial_data['报告期'] = pd.to_datetime(financial_data['报告期'], errors='coerce')
                # 过滤最近几年的数据
                cutoff_date = datetime.now() - timedelta(days=365 * years)
                financial_data = financial_data[financial_data['报告期'] >= cutoff_date]
                # 转换回字符串格式
                financial_data['报告期'] = financial_data['报告期'].dt.strftime('%Y-%m-%d')

            # 添加公司信息
            financial_data['公司名称'] = company_name
            financial_data['股票代码'] = stock_code

            # 数据单位转换（根据实际数据判断是否需要转换）
            self._normalize_units(financial_data)

            # 只保留需要的列
            final_columns = ['报告期', '营业收入(亿元)', '净利润(亿元)', '总资产(亿元)',
                           '净资产(亿元)', '资产负债率(%)', '净资产收益率(%)',
                           '每股收益(元)', '公司名称', '股票代码']

            financial_data = financial_data[final_columns]

            logger.info(f"成功获取 {company_name} 的真实财务数据，共 {len(financial_data)} 条记录")
            logger.info(f"最终列名: {list(financial_data.columns)}")

            return financial_data

        except Exception as e:
            logger.error(f"AKShare 获取数据出错: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            raise

    def _build_column_mapping(self, columns: pd.Index) -> dict:
        """
        构建列名映射字典
        处理 AKShare 可能返回的各种列名格式
        """
        mapping = {}

        # 日期相关
        for col in columns:
            col_str = str(col)
            col_lower = col_str.lower()

            # 报告期/日期
            if any(x in col_lower for x in ['日期', 'date', '报告期', '截止日期', '公告日期']):
                mapping[col] = '报告期'

            # 营业收入（多种可能的列名）
            elif any(x in col_lower for x in ['营业收入', '营收', 'revenue', '主营业务收入', '营业总收入']):
                mapping[col] = '营业收入(亿元)'

            # 净利润（归属母公司股东的净利润）
            elif any(x in col_lower for x in ['净利润', 'net_profit', '归属', '扣非净利润']):
                if '扣非' not in col_lower:  # 优先使用归母净利润
                    mapping[col] = '净利润(亿元)'

            # 总资产
            elif any(x in col_lower for x in ['总资产', 'total_asset', '资产总计']):
                mapping[col] = '总资产(亿元)'

            # 净资产/股东权益
            elif any(x in col_lower for x in ['净资产', 'net_asset', '股东权益', '所有者权益', '归属母公司']):
                if '负债' not in col_lower:  # 排除包含"负债"的列
                    mapping[col] = '净资产(亿元)'

            # 资产负债率
            elif any(x in col_lower for x in ['资产负债率', 'debt_ratio', '负债率']):
                mapping[col] = '资产负债率(%)'

            # 净资产收益率 ROE
            elif any(x in col_lower for x in ['净资产收益率', 'roe', '加权平均']):
                mapping[col] = '净资产收益率(%)'

            # 每股收益 EPS
            elif any(x in col_lower for x in ['每股收益', 'eps', '基本每股']):
                mapping[col] = '每股收益(元)'

        logger.info(f"列名映射: {mapping}")
        return mapping

    def _normalize_units(self, df: pd.DataFrame):
        """
        标准化数据单位
        将所有金额转换为亿元，百分比保持不变
        """
        # 需要转换为亿元的列
        money_columns = ['营业收入(亿元)', '净利润(亿元)', '总资产(亿元)', '净资产(亿元)']

        for col in money_columns:
            if col in df.columns:
                # 检查数值范围，判断当前单位
                try:
                    sample_val = df[col].dropna().iloc[0] if not df[col].dropna().empty else 0

                    # 如果数值很大（>1000），可能是元为单位，需要转换为亿元
                    if abs(sample_val) > 1000:
                        logger.info(f"转换 {col} 从元到亿元")
                        df[col] = df[col] / 100000000
                    # 如果数值适中（10-1000），可能是万元，转换为亿元
                    elif abs(sample_val) > 10:
                        logger.info(f"转换 {col} 从万元到亿元")
                        df[col] = df[col] / 10000
                    # 否则可能已经是亿元
                    else:
                        logger.info(f"{col} 已经是亿元单位")

                except Exception as e:
                    logger.warning(f"单位转换出错: {e}")
                    pass

        # 确保百分比列的值在合理范围内（0-100）
        percent_columns = ['资产负债率(%)', '净资产收益率(%)']
        for col in percent_columns:
            if col in df.columns:
                try:
                    sample_val = df[col].dropna().iloc[0] if not df[col].dropna().empty else 0
                    # 如果值很小（<1），可能是小数形式，需要乘以100
                    if 0 < abs(sample_val) < 1:
                        logger.info(f"转换 {col} 从小数到百分比")
                        df[col] = df[col] * 100
                except Exception as e:
                    logger.warning(f"百分比转换出错: {e}")
                    pass

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
