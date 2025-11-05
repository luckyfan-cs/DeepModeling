#!/usr/bin/env python3
"""
数据准备脚本 - DABench Task 0: Calculate Mean Fare

功能：
1. 调用框架的 prepare.py 生成 prepared/ 目录
2. 处理原始数据并生成答案文件

使用：
    cd /home/aiops/liufan/projects/DSFlow/data/competitions/dabench-0-mean-fare
    python prepare.py
"""
import sys
from pathlib import Path

# 添加框架路径
sys.path.insert(0, '/home/aiops/liufan/projects/data_science_agent_toolkit')

# 导入框架的 prepare 函数
# Use importlib.util to load module from file path directly
import importlib.util

prepare_file = Path('/home/aiops/liufan/projects/data_science_agent_toolkit/mlebench/competitions/dabench-0-mean-fare/prepare.py')
spec = importlib.util.spec_from_file_location("prepare_module", prepare_file)
prepare_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prepare_module)
prepare_fn = prepare_module.prepare

# 定义路径（相对于当前脚本）
current_dir = Path(__file__).parent
raw_dir = current_dir / 'raw'
public_dir = current_dir / 'prepared' / 'public'
private_dir = current_dir / 'prepared' / 'private'

# 创建目录
public_dir.mkdir(parents=True, exist_ok=True)
private_dir.mkdir(parents=True, exist_ok=True)

if __name__ == '__main__':
    print("=" * 60)
    print("Preparing DABench Task 0 - Calculate Mean Fare...")
    print("=" * 60)
    print(f"  Raw:     {raw_dir}")
    print(f"  Public:  {public_dir}")
    print(f"  Private: {private_dir}")
    print()

    # 调用框架的 prepare 函数
    prepare_fn(raw_dir, public_dir, private_dir)

    print()
    print("=" * 60)
    print("✓ Dataset prepared successfully!")
    print("=" * 60)

    # 验证生成的文件
    print("\nGenerated files:")
    print("  Public:")
    for file in sorted(public_dir.glob("*")):
        size = file.stat().st_size / 1024  # KB
        print(f"    - {file.name} ({size:.2f} KB)")

    print("  Private:")
    for file in sorted(private_dir.glob("*")):
        size = file.stat().st_size / 1024  # KB
        print(f"    - {file.name} ({size:.2f} KB)")
