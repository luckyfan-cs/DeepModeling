#!/usr/bin/env python3
"""
测试 DABench Task 0 的评分功能
"""
import sys
from pathlib import Path
import pandas as pd
import importlib.util

# 添加框架路径
sys.path.insert(0, '/home/aiops/liufan/projects/data_science_agent_toolkit')

# 加载 grade 模块
grade_file = Path('/home/aiops/liufan/projects/data_science_agent_toolkit/mlebench/competitions/dabench-0-mean-fare/grade.py')
spec = importlib.util.spec_from_file_location("grade_module", grade_file)
grade_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grade_module)
grade_fn = grade_module.grade

# 数据路径
data_dir = Path(__file__).parent
answer_file = data_dir / 'prepared' / 'private' / 'answer.csv'

# 加载答案
answers = pd.read_csv(answer_file)
print("Ground truth answer:")
print(answers)
print()

# 测试 1: 正确答案
print("=" * 60)
print("Test 1: Perfect submission (correct answer)")
print("=" * 60)
perfect_submission = pd.DataFrame({
    'id': [0],
    'answer': ['@mean_fare[34.65]']
})
score = grade_fn(perfect_submission, answers)
print(f"Score: {score}")
print(f"Expected: 1.0")
print(f"✓ PASS" if score == 1.0 else f"✗ FAIL")
print()

# 测试 2: 错误答案
print("=" * 60)
print("Test 2: Wrong answer")
print("=" * 60)
wrong_submission = pd.DataFrame({
    'id': [0],
    'answer': ['@mean_fare[50.00]']
})
score = grade_fn(wrong_submission, answers)
print(f"Score: {score}")
print(f"Expected: 0.0")
print(f"✓ PASS" if score == 0.0 else f"✗ FAIL")
print()

# 测试 3: 非常接近的答案（应该通过，因为我们使用 0.01 的容差）
print("=" * 60)
print("Test 3: Very close answer (34.64 vs 34.65)")
print("=" * 60)
close_submission = pd.DataFrame({
    'id': [0],
    'answer': ['@mean_fare[34.64]']
})
score = grade_fn(close_submission, answers)
print(f"Score: {score}")
print(f"Expected: 1.0 (within tolerance)")
print(f"✓ PASS" if score == 1.0 else f"✗ FAIL")
print()

# 测试 4: 格式错误
print("=" * 60)
print("Test 4: Format error")
print("=" * 60)
format_error_submission = pd.DataFrame({
    'id': [0],
    'answer': ['mean_fare=34.65']
})
score = grade_fn(format_error_submission, answers)
print(f"Score: {score}")
print(f"Expected: 0.0")
print(f"✓ PASS" if score == 0.0 else f"✗ FAIL")
print()

# 验证实际计算
print("=" * 60)
print("Verification: Calculate actual mean fare from data")
print("=" * 60)
train_file = data_dir / 'prepared' / 'public' / 'train.csv'
df = pd.read_csv(train_file)
mean_fare = df['Fare'].mean()
print(f"Calculated mean fare: {mean_fare:.2f}")
print(f"Expected answer: 34.65")
print()

print("=" * 60)
print("All tests completed!")
print("=" * 60)
