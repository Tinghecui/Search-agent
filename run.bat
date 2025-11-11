@echo off
REM AI 财务分析助手启动脚本 (Windows)

echo =========================================
echo   AI 财务分析助手 - Powered by Claude
echo =========================================
echo.

REM 检查 Python 版本
echo 检查 Python 版本...
python --version

REM 检查虚拟环境
echo.
echo 检查虚拟环境...
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖
echo.
echo 安装/更新依赖...
pip install -r requirements.txt

REM 创建必要的目录
echo.
echo 创建数据目录...
if not exist "data\reports" mkdir data\reports
if not exist "data\research" mkdir data\research
if not exist "data\cache" mkdir data\cache

REM 检查环境变量
echo.
echo 检查配置...
if not exist ".env" (
    echo 错误: 未找到 .env 文件
    exit /b 1
)

REM 启动应用
echo.
echo =========================================
echo 启动 Streamlit 应用...
echo =========================================
echo.
streamlit run app.py

REM 清理
call venv\Scripts\deactivate.bat
