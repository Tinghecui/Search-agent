# 📦 安装和配置指南

## 📋 系统要求

- Python 3.8 或更高版本
- pip 包管理器
- 4GB+ 可用内存
- 稳定的网络连接（用于获取实时数据）

## 🚀 快速安装

### 1. 克隆项目

```bash
git clone <repository-url>
cd Search-agent
```

### 2. 创建虚拟环境（推荐）

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

**重要提示**：`requirements.txt` 已包含 `akshare>=1.17.0`

### 4. 验证安装

```bash
python test_akshare_integration.py
```

## 🔧 AKShare 安装详解

### 标准安装

```bash
pip install akshare
```

### 如果遇到问题

#### 问题 1: jsonpath 依赖安装失败

**症状**：
```
ERROR: Failed building wheel for jsonpath
```

**解决方案**：
```bash
# 方案 A: 升级 pip 和 setuptools
pip install --upgrade pip setuptools wheel

# 方案 B: 使用预编译版本（Windows）
pip install --only-binary :all: akshare

# 方案 C: 跳过有问题的依赖
pip install akshare --no-deps
pip install pandas numpy requests beautifulsoup4
```

#### 问题 2: 网络超时

**解决方案**：
```bash
# 使用国内镜像源
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple akshare
```

#### 问题 3: 权限问题

**解决方案**：
```bash
# Windows: 以管理员身份运行 CMD
# Linux/Mac: 使用 --user 标志
pip install --user akshare
```

### 验证 AKShare 安装

```python
# 在 Python 中运行
import akshare as ak
print("AKShare 版本:", ak.__version__ if hasattr(ak, '__version__') else '已安装')

# 测试获取数据
try:
    df = ak.stock_zh_a_spot_em()
    print("✅ AKShare 工作正常!")
    print(f"获取到 {len(df)} 条股票数据")
except Exception as e:
    print(f"❌ 测试失败: {e}")
```

## 📊 数据获取模式

### 模式 1: AKShare 真实数据（推荐）

**优势**：
- ✅ 完全免费
- ✅ 真实数据
- ✅ 自动更新
- ✅ 无需 API Key

**要求**：
- 安装 AKShare: `pip install akshare`
- 稳定的网络连接

**使用方式**：
安装 AKShare 后，系统会自动使用真实数据。

### 模式 2: 差异化模拟数据（备用）

**优势**：
- ✅ 无需安装 AKShare
- ✅ 无网络要求
- ✅ 两个公司数据明显不同
- ✅ 即时可用

**限制**：
- ⚠️ 非真实数据
- ⚠️ 仅用于演示

**使用方式**：
如果 AKShare 未安装或获取失败，系统会自动降级到模拟数据。

## 🧪 运行测试

### 完整测试

```bash
python test_akshare_integration.py
```

测试内容：
1. ✅ AKShare 导入状态
2. ✅ 财务数据获取
3. ✅ 研报数据获取
4. ✅ 数据保存功能
5. ✅ 两公司数据差异性

### 预期输出

```
╔══════════════════════════════════════════════════════════╗
║               AKShare 集成测试                            ║
╚══════════════════════════════════════════════════════════╝

============================================================
测试 1: 检查 AKShare 导入状态
============================================================
✅ AKShare 已成功安装
   版本: 1.17.83

============================================================
测试 2: 获取财务数据
============================================================

📊 正在获取 大洋电机 的财务数据...
✅ 成功获取 大洋电机 数据
   数据条数: 12
   最新报告期: 2024-03-31
   营业收入: 48.5 亿元
   净利润: 5.2 亿元
   ROE: 10.1%

📊 正在获取 卧龙电机 的财务数据...
✅ 成功获取 卧龙电机 数据
   数据条数: 12
   最新报告期: 2024-03-31
   营业收入: 68.3 亿元
   净利润: 6.8 亿元
   ROE: 8.5%

------------------------------------------------------------
数据差异性检查:
------------------------------------------------------------
✅ 两个公司数据不同
   大洋电机营收: 48.5 亿元
   卧龙电机营收: 68.3 亿元

[...]
```

## 🎯 运行主应用

### 启动 Streamlit 应用

```bash
streamlit run app.py
```

### 访问应用

浏览器会自动打开：`http://localhost:8501`

如未自动打开，手动访问上述地址。

## 🐛 常见问题

### Q1: ImportError: No module named 'akshare'

**原因**：AKShare 未安装

**解决**：
```bash
pip install akshare
```

### Q2: 数据显示为空

**可能原因**：
1. 网络连接问题
2. AKShare API 暂时不可用
3. 股票代码错误

**解决**：
1. 检查网络连接
2. 查看日志输出
3. 系统会自动降级到模拟数据

### Q3: 两个公司数据相同

**原因**：正在使用模拟数据且未升级

**解决**：
1. 安装 AKShare 获取真实数据
2. 或确认已使用最新代码（模拟数据已差异化）

### Q4: Streamlit 无法启动

**解决**：
```bash
# 确保所有依赖都已安装
pip install -r requirements.txt

# 检查 Streamlit 版本
streamlit --version

# 重新安装 Streamlit
pip install --upgrade streamlit
```

## 📚 其他资源

- **AKShare 官方文档**: https://akshare.akfamily.xyz/
- **AKShare GitHub**: https://github.com/akfamily/akshare
- **Streamlit 文档**: https://docs.streamlit.io/
- **项目 README**: ./README.md

## 💡 提示

1. **首次运行**：第一次获取数据可能较慢，AKShare 需要初始化
2. **数据更新**：点击应用中的"刷新数据"按钮获取最新数据
3. **日志查看**：运行时会输出详细日志，有助于排查问题
4. **性能优化**：Streamlit 会缓存数据，避免重复请求

## 🎉 安装完成！

如果所有测试通过，你已成功配置项目！

运行 `streamlit run app.py` 开始使用 AI 财务分析助手。
