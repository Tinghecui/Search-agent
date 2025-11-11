"""
快速功能预览脚本
"""

print("="*80)
print("  🚀 AI 财务分析助手 - 功能预览")
print("="*80)

print("\n📍 应用访问地址:")
print("  Local:   http://localhost:8501")
print("  Network: http://21.0.0.22:8501")

print("\n" + "="*80)
print("  功能模块预览")
print("="*80)

modules = [
    {
        "icon": "📊",
        "name": "数据总览",
        "features": [
            "✓ 实时财务数据卡片",
            "✓ 营业收入、净利润、ROE 指标",
            "✓ 研报数量统计",
            "✓ 最新研报摘要"
        ]
    },
    {
        "icon": "🔍",
        "name": "财务分析",
        "features": [
            "✓ 营收/利润趋势折线图",
            "✓ ROE 变化趋势",
            "✓ 关键财务指标面板",
            "✓ AI 深度分析报告"
        ]
    },
    {
        "icon": "📑",
        "name": "研报分析",
        "features": [
            "✓ 同花顺券商研报",
            "✓ 雪球投资者文章",
            "✓ 机构评级统计",
            "✓ AI 研报综合解读"
        ]
    },
    {
        "icon": "⚖️",
        "name": "公司对比",
        "features": [
            "✓ 双公司指标柱状图",
            "✓ 营收趋势对比",
            "✓ 财务健康度对比",
            "✓ AI 对比分析报告"
        ]
    },
    {
        "icon": "💬",
        "name": "智能问答",
        "features": [
            "✓ 自然语言提问",
            "✓ AI 实时回答",
            "✓ 基于真实数据",
            "✓ 示例问题模板"
        ]
    },
    {
        "icon": "📄",
        "name": "投资报告",
        "features": [
            "✓ 完整投资分析报告",
            "✓ 包含6大分析维度",
            "✓ Markdown 格式",
            "✓ 一键下载功能"
        ]
    }
]

for i, module in enumerate(modules, 1):
    print(f"\n{module['icon']} {i}. {module['name']}")
    print("-" * 60)
    for feature in module['features']:
        print(f"    {feature}")

print("\n" + "="*80)
print("  🎯 使用建议")
print("="*80)

tips = [
    "1. 从「数据总览」开始，了解公司基本情况",
    "2. 切换到「财务分析」查看详细图表和趋势",
    "3. 在「研报分析」中了解市场观点",
    "4. 使用「公司对比」横向对比两家公司",
    "5. 在「智能问答」中提出你关心的问题",
    "6. 最后生成「投资报告」获取完整分析"
]

for tip in tips:
    print(f"\n  {tip}")

print("\n" + "="*80)
print("  💡 示例问题")
print("="*80)

questions = [
    "大洋电机和卧龙电机哪个更值得投资？",
    "大洋电机的营收增长率是多少？",
    "卧龙电机的财务风险高吗？",
    "两家公司的 ROE 对比如何？",
    "最新研报对大洋电机的评价是什么？"
]

for i, q in enumerate(questions, 1):
    print(f"\n  {i}. {q}")

print("\n" + "="*80)
print("  📊 数据说明")
print("="*80)

print("\n  目标公司: 大洋电机(002249)、卧龙电机(600580)")
print("  数据范围: 最近 3 年（12 个季度）")
print("  数据来源: 东方财富、巨潮资讯、同花顺、雪球")
print("  AI 模型: Claude Sonnet 4.5")

print("\n" + "="*80)
print("  ⚙️ 技术特性")
print("="*80)

features = [
    "✓ 实时数据加载",
    "✓ 智能缓存（1小时）",
    "✓ 交互式图表（Plotly）",
    "✓ 响应式布局",
    "✓ 一键刷新数据",
    "✓ 报告导出功能"
]

for feature in features:
    print(f"\n  {feature}")

print("\n" + "="*80)
print("  🎨 界面亮点")
print("="*80)

highlights = [
    "现代化 UI 设计",
    "直观的侧边栏导航",
    "丰富的数据可视化",
    "流畅的交互体验",
    "清晰的信息层次",
    "专业的配色方案"
]

for i, highlight in enumerate(highlights, 1):
    print(f"\n  {i}. {highlight}")

print("\n" + "="*80)
print("  ✨ 开始体验")
print("="*80)

print("\n  1. 在浏览器中打开: http://localhost:8501")
print("  2. 在左侧边栏选择公司")
print("  3. 选择分析模式")
print("  4. 点击「生成 AI 分析」体验智能功能")
print("  5. 尝试在「智能问答」中提问")

print("\n" + "="*80)
print("  📖 更多信息")
print("="*80)

print("\n  - 详细文档: README.md")
print("  - 使用指南: USAGE.md")
print("  - 运行测试: python test_agent.py")
print("  - Demo 演示: python demo.py")

print("\n" + "="*80)
print("  🎉 祝你使用愉快！")
print("="*80 + "\n")
