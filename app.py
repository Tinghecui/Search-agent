"""
Financial Analysis Agent Demo
基于 Streamlit 的金融数据分析和可视化应用
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os
import sys

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crawler.report_crawler import FinancialReportCrawler
from crawler.research_crawler import ResearchReportCrawler
from agent.financial_agent import FinancialAgent
from agent.tools import FinancialTools

# 页面配置
st.set_page_config(
    page_title="AI 财务分析助手",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def init_agent():
    """初始化 Agent"""
    try:
        return FinancialAgent()
    except Exception as e:
        st.error(f"初始化 Agent 失败: {str(e)}")
        return None


@st.cache_data(ttl=3600)
def load_financial_data(company_name):
    """加载财务数据"""
    crawler = FinancialReportCrawler()
    return crawler.get_financial_summary(company_name, years=3)


@st.cache_data(ttl=3600)
def load_research_data(company_name):
    """加载研报数据"""
    crawler = ResearchReportCrawler()
    return crawler.crawl_all_research(company_name, years=3)


def main():
    """主函数"""

    # 标题
    st.markdown('<p class="main-header">🤖 AI 财务分析助手</p>', unsafe_allow_html=True)
    st.markdown("---")

    # 侧边栏
    with st.sidebar:
        st.image("https://www.anthropic.com/images/icons/apple-touch-icon.png", width=100)
        st.title("设置")

        # 公司选择
        st.subheader("选择公司")
        companies = ["大洋电机", "卧龙电机"]
        selected_companies = st.multiselect(
            "分析目标",
            companies,
            default=companies
        )

        # 分析功能选择
        st.subheader("分析功能")
        analysis_mode = st.radio(
            "选择分析模式",
            ["📊 数据总览", "🔍 财务分析", "📑 研报分析", "⚖️ 公司对比", "💬 智能问答", "📄 投资报告"]
        )

        # 数据更新
        st.subheader("数据管理")
        if st.button("🔄 刷新数据"):
            st.cache_data.clear()
            st.success("数据已刷新！")

        # 关于
        st.markdown("---")
        st.markdown("""
        ### 关于
        - **模型**: Claude Sonnet 4.5
        - **数据源**: 东方财富、同花顺、雪球
        - **版本**: 1.0.0
        """)

    # 主内容区
    if not selected_companies:
        st.warning("请在侧边栏选择至少一家公司进行分析")
        return

    # 初始化 Agent
    agent = init_agent()
    if not agent:
        st.error("Agent 初始化失败，请检查配置")
        return

    # 根据选择的模式显示内容
    if analysis_mode == "📊 数据总览":
        show_data_overview(selected_companies)

    elif analysis_mode == "🔍 财务分析":
        show_financial_analysis(selected_companies, agent)

    elif analysis_mode == "📑 研报分析":
        show_research_analysis(selected_companies, agent)

    elif analysis_mode == "⚖️ 公司对比":
        if len(selected_companies) >= 2:
            show_company_comparison(selected_companies[:2], agent)
        else:
            st.warning("公司对比需要选择至少两家公司")

    elif analysis_mode == "💬 智能问答":
        show_qa_interface(selected_companies, agent)

    elif analysis_mode == "📄 投资报告":
        show_investment_report(selected_companies, agent)


def show_data_overview(companies):
    """显示数据总览"""
    st.markdown('<p class="sub-header">📊 数据总览</p>', unsafe_allow_html=True)

    for company in companies:
        with st.expander(f"📈 {company}", expanded=True):
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("财务数据")
                with st.spinner(f"加载 {company} 财务数据..."):
                    financial_data = load_financial_data(company)

                if not financial_data.empty:
                    # 显示最新数据
                    latest = financial_data.iloc[-1]
                    metrics_col1, metrics_col2, metrics_col3 = st.columns(3)

                    with metrics_col1:
                        revenue = latest.get('营业收入(亿元)', 0)
                        prev_revenue = financial_data.iloc[-2].get('营业收入(亿元)', 0) if len(financial_data) > 1 else 0
                        st.metric(
                            "营业收入",
                            f"{revenue:.2f} 亿",
                            delta=f"{prev_revenue:.2f}"
                        )

                    with metrics_col2:
                        profit = latest.get('净利润(亿元)', 0)
                        prev_profit = financial_data.iloc[-2].get('净利润(亿元)', 0) if len(financial_data) > 1 else 0
                        st.metric(
                            "净利润",
                            f"{profit:.2f} 亿",
                            delta=f"{prev_profit:.2f}"
                        )

                    with metrics_col3:
                        roe = latest.get('净资产收益率(%)', 0)
                        st.metric(
                            "ROE",
                            f"{roe:.2f}%"
                        )

                    # 显示数据表
                    st.dataframe(financial_data.tail(10), use_container_width=True)
                else:
                    st.info("暂无财务数据")

            with col2:
                st.subheader("研报数据")
                with st.spinner(f"加载 {company} 研报数据..."):
                    research_data = load_research_data(company)

                if research_data:
                    total_reports = research_data.get('tonghuashun', []) + research_data.get('xueqiu', [])
                    st.metric("研报总数", len(total_reports))

                    # 显示最新研报
                    if research_data.get('tonghuashun'):
                        st.write("**最新研报:**")
                        for report in research_data['tonghuashun'][:3]:
                            st.markdown(f"- **{report['title']}**")
                            st.markdown(f"  *{report['institution']} | {report['date']} | {report['rating']}*")
                else:
                    st.info("暂无研报数据")


def show_financial_analysis(companies, agent):
    """显示财务分析"""
    st.markdown('<p class="sub-header">🔍 财务分析</p>', unsafe_allow_html=True)

    for company in companies:
        st.subheader(f"📊 {company} 财务分析")

        financial_data = load_financial_data(company)

        if not financial_data.empty:
            # 创建标签页
            tab1, tab2, tab3 = st.tabs(["📈 趋势图表", "📊 财务指标", "🤖 AI 分析"])

            with tab1:
                # 营收和利润趋势
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=financial_data['报告期'],
                    y=financial_data['营业收入(亿元)'],
                    name='营业收入',
                    mode='lines+markers'
                ))
                fig.add_trace(go.Scatter(
                    x=financial_data['报告期'],
                    y=financial_data['净利润(亿元)'],
                    name='净利润',
                    mode='lines+markers',
                    yaxis='y2'
                ))
                fig.update_layout(
                    title='营业收入和净利润趋势',
                    yaxis=dict(title='营业收入(亿元)'),
                    yaxis2=dict(title='净利润(亿元)', overlaying='y', side='right'),
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)

                # ROE 趋势
                fig2 = px.line(
                    financial_data,
                    x='报告期',
                    y='净资产收益率(%)',
                    title='净资产收益率(ROE)趋势',
                    markers=True
                )
                st.plotly_chart(fig2, use_container_width=True)

            with tab2:
                # 财务指标
                tools = FinancialTools()
                metrics = tools.extract_key_metrics(financial_data)

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("营业收入", f"{metrics.get('latest_revenue', 0):.2f} 亿")
                    st.metric("净利润", f"{metrics.get('latest_profit', 0):.2f} 亿")

                with col2:
                    st.metric("总资产", f"{metrics.get('latest_assets', 0):.2f} 亿")
                    st.metric("净资产", f"{metrics.get('latest_equity', 0):.2f} 亿")

                with col3:
                    st.metric("资产负债率", f"{metrics.get('latest_debt_ratio', 0):.2f}%")
                    st.metric("ROE", f"{metrics.get('latest_roe', 0):.2f}%")

                with col4:
                    st.metric("EPS", f"{metrics.get('latest_eps', 0):.2f} 元")
                    if 'revenue_growth' in metrics:
                        st.metric("营收增长", f"{metrics.get('revenue_growth', 0):.2f}%")

            with tab3:
                # AI 分析
                if st.button(f"生成 {company} AI 财务分析", key=f"analyze_{company}"):
                    with st.spinner("AI 分析中..."):
                        analysis = agent.analyze_financial_data(
                            company,
                            financial_data.to_dict('records')
                        )
                        st.markdown(analysis)

        else:
            st.warning(f"暂无 {company} 的财务数据")

        st.markdown("---")


def show_research_analysis(companies, agent):
    """显示研报分析"""
    st.markdown('<p class="sub-header">📑 研报分析</p>', unsafe_allow_html=True)

    for company in companies:
        st.subheader(f"📰 {company} 研报分析")

        research_data = load_research_data(company)

        if research_data:
            # 统计信息
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("同花顺研报", len(research_data.get('tonghuashun', [])))
            with col2:
                st.metric("雪球文章", len(research_data.get('xueqiu', [])))
            with col3:
                total = len(research_data.get('tonghuashun', [])) + len(research_data.get('xueqiu', []))
                st.metric("总计", total)

            # 研报列表
            tab1, tab2, tab3 = st.tabs(["同花顺研报", "雪球文章", "🤖 AI 分析"])

            with tab1:
                for report in research_data.get('tonghuashun', []):
                    with st.container():
                        st.markdown(f"### {report['title']}")
                        st.markdown(f"**机构**: {report['institution']} | **分析师**: {report['analyst']} | **日期**: {report['date']}")
                        st.markdown(f"**评级**: `{report['rating']}`")
                        st.markdown(f"{report['summary']}")
                        st.markdown("---")

            with tab2:
                for article in research_data.get('xueqiu', []):
                    with st.container():
                        st.markdown(f"### {article['title']}")
                        st.markdown(f"**作者**: {article['author']} | **日期**: {article['date']}")
                        st.markdown(f"👍 {article['likes']} | 💬 {article['comments']}")
                        st.markdown(f"{article['content_preview']}")
                        st.markdown("---")

            with tab3:
                if st.button(f"生成 {company} AI 研报分析", key=f"research_{company}"):
                    with st.spinner("AI 分析中..."):
                        all_reports = research_data.get('tonghuashun', []) + research_data.get('xueqiu', [])
                        analysis = agent.analyze_research_reports(company, all_reports)
                        st.markdown(analysis)

        else:
            st.warning(f"暂无 {company} 的研报数据")

        st.markdown("---")


def show_company_comparison(companies, agent):
    """显示公司对比"""
    st.markdown('<p class="sub-header">⚖️ 公司对比</p>', unsafe_allow_html=True)

    company1, company2 = companies[0], companies[1]

    st.markdown(f"### {company1} vs {company2}")

    # 加载数据
    data1 = load_financial_data(company1)
    data2 = load_financial_data(company2)

    if not data1.empty and not data2.empty:
        # 对比图表
        tab1, tab2 = st.tabs(["📊 指标对比", "🤖 AI 对比分析"])

        with tab1:
            # 营收对比
            fig = go.Figure()
            fig.add_trace(go.Bar(name=company1, x=['营业收入', '净利润', 'ROE'],
                                 y=[data1.iloc[-1]['营业收入(亿元)'],
                                    data1.iloc[-1]['净利润(亿元)'],
                                    data1.iloc[-1]['净资产收益率(%)']]))
            fig.add_trace(go.Bar(name=company2, x=['营业收入', '净利润', 'ROE'],
                                 y=[data2.iloc[-1]['营业收入(亿元)'],
                                    data2.iloc[-1]['净利润(亿元)'],
                                    data2.iloc[-1]['净资产收益率(%)']]))
            fig.update_layout(title='关键指标对比', barmode='group')
            st.plotly_chart(fig, use_container_width=True)

            # 趋势对比
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=data1['报告期'], y=data1['营业收入(亿元)'],
                                      name=f'{company1} 营收', mode='lines+markers'))
            fig2.add_trace(go.Scatter(x=data2['报告期'], y=data2['营业收入(亿元)'],
                                      name=f'{company2} 营收', mode='lines+markers'))
            fig2.update_layout(title='营业收入趋势对比')
            st.plotly_chart(fig2, use_container_width=True)

        with tab2:
            if st.button("生成 AI 对比分析"):
                with st.spinner("AI 分析中..."):
                    comparison_data = {
                        company1: {
                            'company_name': company1,
                            'financial_data': data1.to_dict('records')
                        },
                        company2: {
                            'company_name': company2,
                            'financial_data': data2.to_dict('records')
                        }
                    }
                    analysis = agent.compare_companies(
                        comparison_data[company1],
                        comparison_data[company2]
                    )
                    st.markdown(analysis)
    else:
        st.warning("数据不足，无法进行对比")


def show_qa_interface(companies, agent):
    """显示智能问答界面"""
    st.markdown('<p class="sub-header">💬 智能问答</p>', unsafe_allow_html=True)

    st.info("向 AI 助手提问关于公司财务、研报的任何问题")

    # 问题输入
    question = st.text_input("请输入你的问题:", placeholder="例如: 大洋电机的盈利能力如何?")

    if st.button("🚀 提问") and question:
        with st.spinner("AI 思考中..."):
            # 准备上下文数据
            context = {}
            for company in companies:
                financial_data = load_financial_data(company)
                research_data = load_research_data(company)
                context[company] = {
                    'financial': financial_data.to_dict('records') if not financial_data.empty else [],
                    'research': research_data
                }

            # 获取答案
            answer = agent.answer_question(question, context)
            st.markdown("### 📝 AI 回答:")
            st.markdown(answer)

    # 示例问题
    st.markdown("### 💡 示例问题:")
    example_questions = [
        "大洋电机和卧龙电机哪个更值得投资?",
        "大洋电机的营收增长趋势如何?",
        "卧龙电机的资产负债率健康吗?",
        "最新的研报对这两家公司的评级是什么?",
        "这两家公司的ROE对比如何?"
    ]

    for i, q in enumerate(example_questions):
        if st.button(q, key=f"example_{i}"):
            st.session_state['question'] = q


def show_investment_report(companies, agent):
    """显示投资报告"""
    st.markdown('<p class="sub-header">📄 投资报告</p>', unsafe_allow_html=True)

    selected_company = st.selectbox("选择公司生成投资报告:", companies)

    if st.button(f"📊 生成 {selected_company} 投资报告"):
        with st.spinner("正在生成完整投资报告..."):
            # 收集所有数据
            financial_data = load_financial_data(selected_company)
            research_data = load_research_data(selected_company)

            all_data = {
                'company_name': selected_company,
                'financial_data': financial_data.to_dict('records') if not financial_data.empty else [],
                'research_data': research_data
            }

            # 生成报告
            report = agent.generate_investment_report(selected_company, all_data)

            # 显示报告
            st.markdown(report)

            # 下载按钮
            st.download_button(
                label="💾 下载报告",
                data=report,
                file_name=f"{selected_company}_投资报告_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown"
            )


if __name__ == "__main__":
    main()
