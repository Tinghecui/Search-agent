"""
工具函数和帮助方法
"""

import json
import os
from typing import Any, Dict
from datetime import datetime


def save_json(data: Dict, filepath: str):
    """
    保存数据到JSON文件

    Args:
        data: 要保存的数据
        filepath: 文件路径
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(filepath: str) -> Dict:
    """
    从JSON文件加载数据

    Args:
        filepath: 文件路径

    Returns:
        加载的数据
    """
    if not os.path.exists(filepath):
        return {}

    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def format_currency(amount: float, unit: str = '亿元') -> str:
    """
    格式化货币金额

    Args:
        amount: 金额
        unit: 单位

    Returns:
        格式化后的字符串
    """
    return f"{amount:.2f} {unit}"


def format_percentage(value: float) -> str:
    """
    格式化百分比

    Args:
        value: 数值

    Returns:
        格式化后的百分比字符串
    """
    return f"{value:.2f}%"


def get_timestamp() -> str:
    """
    获取当前时间戳字符串

    Returns:
        时间戳字符串
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def safe_divide(numerator: float, denominator: float, default: float = 0) -> float:
    """
    安全除法，避免除零错误

    Args:
        numerator: 分子
        denominator: 分母
        default: 默认值

    Returns:
        除法结果
    """
    if denominator == 0:
        return default
    return numerator / denominator


def create_directory_structure():
    """创建项目目录结构"""
    directories = [
        'data/reports',
        'data/research',
        'data/cache',
        'logs'
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)


if __name__ == "__main__":
    # 测试
    create_directory_structure()
    print("目录结构创建成功")
