#!/usr/bin/env python3
"""
批量准备 ScienceBench 数据

创建 public/ 和 private/ 数据目录
"""

import sys
import argparse
from pathlib import Path
import importlib.util


# 路径配置
COMPETITIONS_DIR = Path('/home/aiops/liufan/projects/DeepModeling/benchmarks/sciencebench/competitions')
DATA_BASE_DIR = Path('/home/aiops/liufan/projects/ScienceAgent-bench/competitions')
SCIENCEAGENT_DATASETS_DIR = Path('/home/aiops/liufan/projects/ScienceAgent-bench/benchmark/datasets')


def load_prepare_function(competition_dir: Path):
    """动态加载 prepare.py 中的 prepare 函数"""
    prepare_file = competition_dir / 'prepare.py'

    if not prepare_file.exists():
        print(f"❌ prepare.py not found in {competition_dir}")
        return None

    # 动态加载模块
    spec = importlib.util.spec_from_file_location("prepare_module", prepare_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, 'prepare'):
        print(f"❌ prepare() function not found in {prepare_file}")
        return None

    return module.prepare


def prepare_competition_data(comp_id: str, dataset_name: str = None) -> bool:
    """
    准备单个比赛的数据

    Args:
        comp_id: Competition ID (e.g., sciencebench-001-clintox-nn)
        dataset_name: Dataset directory name (auto-inferred if None)

    Returns:
        是否成功
    """
    print(f"\n{'='*60}")
    print(f"Preparing data for: {comp_id}")
    print(f"{'='*60}")

    # 获取比赛目录
    comp_dir = COMPETITIONS_DIR / comp_id
    if not comp_dir.exists():
        print(f"❌ Competition directory not found: {comp_dir}")
        return False

    # 推断数据集名称
    if dataset_name is None:
        # 从 comp_id 提取：sciencebench-001-clintox-nn -> clintox
        parts = comp_id.split('-')
        if len(parts) >= 3:
            dataset_name = '-'.join(parts[2:])  # clintox-nn
            # 尝试找到匹配的数据集
            possible_names = [
                dataset_name,
                dataset_name.replace('-', '_'),
                parts[2],  # 第一部分
            ]

            for name in possible_names:
                if (SCIENCEAGENT_DATASETS_DIR / name).exists():
                    dataset_name = name
                    break
                # 尝试 clintox (去掉后缀)
                if (SCIENCEAGENT_DATASETS_DIR / name.split('-')[0]).exists():
                    dataset_name = name.split('-')[0]
                    break
            else:
                print(f"⚠ Warning: Could not find dataset for {comp_id}")
                print(f"   Tried: {possible_names}")
                # 使用第一个作为默认值
                dataset_name = possible_names[0]

    # 加载 prepare 函数
    prepare_fn = load_prepare_function(comp_dir)
    if prepare_fn is None:
        return False

    source_dataset = prepare_fn.__globals__.get('SOURCE_DATASET')
    if source_dataset:
        dataset_name = source_dataset

    print(f"Dataset name: {dataset_name}")

    # 设置路径
    raw_dir = SCIENCEAGENT_DATASETS_DIR / dataset_name
    data_dir = DATA_BASE_DIR / comp_id
    public_dir = data_dir / 'prepared' / 'public'
    private_dir = data_dir / 'prepared' / 'private'

    print(f"Raw data: {raw_dir}")
    print(f"Data dir: {data_dir}")

    # 创建数据目录
    public_dir.mkdir(parents=True, exist_ok=True)
    private_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ Created data directories")

    # 运行 prepare
    try:
        print(f"\n📦 Running prepare function...")
        prepare_fn(raw_dir, public_dir, private_dir)
        print(f"✅ Data preparation completed!")

        # 验证生成的文件
        public_files = list(public_dir.glob('*'))
        private_files = list(private_dir.glob('*'))

        print(f"\n📊 Generated files:")
        print(f"  Public:  {len(public_files)} files")
        for f in public_files:
            print(f"    - {f.name}")
        print(f"  Private: {len(private_files)} files")
        for f in private_files:
            print(f"    - {f.name}")

        return True

    except Exception as e:
        print(f"❌ Error during data preparation: {e}")
        import traceback
        traceback.print_exc()
        return False


def list_competitions():
    """列出所有可用的比赛"""
    if not COMPETITIONS_DIR.exists():
        print(f"❌ Competitions directory not found: {COMPETITIONS_DIR}")
        return []

    competitions = sorted([d.name for d in COMPETITIONS_DIR.iterdir() if d.is_dir()])

    print(f"\n{'='*60}")
    print(f"Available Competitions ({len(competitions)})")
    print(f"{'='*60}\n")

    for comp_id in competitions:
        # 检查是否已准备数据
        data_dir = DATA_BASE_DIR / comp_id / 'prepared'
        status = "✅" if data_dir.exists() and any(data_dir.glob('*/*')) else "❌"
        print(f"{status} {comp_id}")

    print()
    return competitions


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Prepare data for ScienceBench competitions'
    )
    parser.add_argument(
        '--competitions',
        nargs='+',
        help='Competition IDs to prepare'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Prepare all competitions'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available competitions'
    )
    parser.add_argument(
        '--dataset-name',
        type=str,
        help='Override dataset name'
    )

    args = parser.parse_args()

    # 列出比赛
    if args.list:
        list_competitions()
        return

    # 确定要准备的比赛
    if args.competitions:
        comp_ids = args.competitions
    elif args.all:
        comp_ids = [d.name for d in COMPETITIONS_DIR.iterdir() if d.is_dir()]
    else:
        print("❌ Please specify --competitions, --all, or --list")
        parser.print_help()
        return

    print(f"\n🚀 Preparing data for {len(comp_ids)} competition(s)...\n")

    # 准备数据
    success_count = 0
    failed_comps = []

    for comp_id in comp_ids:
        success = prepare_competition_data(comp_id, args.dataset_name)

        if success:
            success_count += 1
        else:
            failed_comps.append(comp_id)

    # 总结
    print(f"\n{'='*60}")
    print(f"Data Preparation Summary")
    print(f"{'='*60}")
    print(f"✅ Success: {success_count}/{len(comp_ids)}")
    if failed_comps:
        print(f"❌ Failed: {len(failed_comps)}")
        print(f"   Competitions: {failed_comps}")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
