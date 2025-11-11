#!/bin/bash

# AI 财务分析助手启动脚本

echo "========================================="
echo "  AI 财务分析助手 - Powered by Claude"
echo "========================================="
echo ""

# 检查 Python 版本
echo "检查 Python 版本..."
python3 --version

# 检查依赖
echo ""
echo "检查依赖..."
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo ""
echo "安装/更新依赖..."
pip install -r requirements.txt

# 创建必要的目录
echo ""
echo "创建数据目录..."
mkdir -p data/reports data/research data/cache

# 检查环境变量
echo ""
echo "检查配置..."
if [ ! -f ".env" ]; then
    echo "错误: 未找到 .env 文件"
    exit 1
fi

# 启动应用
echo ""
echo "========================================="
echo "启动 Streamlit 应用..."
echo "========================================="
echo ""
streamlit run app.py

# 清理
deactivate
