import os
import json
import shutil
from pathlib import Path
import argparse

def init_mock_data(regenerate=False):
    """初始化模拟数据"""
    print("初始化模拟数据...")
    
    # 获取当前脚本所在目录
    current_dir = Path(__file__).parent
    data_dir = current_dir / "data"
    storage_dir = current_dir / "storage"
    
    # 确保目录存在
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(storage_dir, exist_ok=True)
    
    # 清空存储目录
    for file in storage_dir.glob("*"):
        if file.is_file():
            os.remove(file)
    
    # 如果需要重新生成数据
    if regenerate:
        from generate_test_data import generate_all_test_data
        generate_all_test_data()
    
    print("模拟数据初始化完成")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="初始化模拟数据")
    parser.add_argument("--regenerate", action="store_true", help="重新生成模拟数据")
    args = parser.parse_args()
    
    init_mock_data(args.regenerate)
