# DeepModeling RL 快速开始指南

## 最简单的使用方式

### 直接运行（使用所有默认值）

```bash
bash /home/aiops/liufan/projects/DeepModeling/examples/deepmodeling-rl/scripts/quickstart.sh
```

默认配置：
- Benchmark: `engineering`
- Mode: `fast`
- GPU 数量: `1`

### 指定参数运行

```bash
bash /home/aiops/liufan/projects/DeepModeling/examples/deepmodeling-rl/scripts/quickstart.sh [benchmark] [mode] [num_gpus]
```

参数说明：
1. **benchmark**: 数据集类型（默认: `engineering`）
   - `engineering` - 工程问题
   - `mathmodeling` - 数学建模
   - `mle` - Kaggle 竞赛
   - `science` - 科学问题

2. **mode**: 训练模式（默认: `fast`）
   - `fast` - 快速测试（1 epoch）
   - `standard` - 标准训练（2 epochs）
   - `advanced` - 高级训练（4 epochs）

3. **num_gpus**: GPU 数量（默认: `1`）
   - `1` - 单 GPU
   - `2`, `4`, `8` - 多 GPU

## 使用示例

### 示例 1: 默认配置（最简单）
```bash
cd /home/aiops/liufan/projects/DeepModeling/examples/deepmodeling-rl
bash scripts/quickstart.sh
```

### 示例 2: 使用 2 个 GPU
```bash
bash scripts/quickstart.sh engineering fast 2
```

### 示例 3: 数学建模 benchmark
```bash
bash scripts/quickstart.sh mathmodeling fast 1
```

### 示例 4: 标准模式训练
```bash
bash scripts/quickstart.sh engineering standard 1
```

## 从任何位置运行

无论你在哪个目录，都可以使用完整路径运行：

```bash
# 从任何位置运行
bash /home/aiops/liufan/projects/DeepModeling/examples/deepmodeling-rl/scripts/quickstart.sh

# 或者设置别名（添加到 ~/.bashrc）
alias dm-rl-train='bash /home/aiops/liufan/projects/DeepModeling/examples/deepmodeling-rl/scripts/quickstart.sh'

# 然后就可以简单地运行
dm-rl-train
dm-rl-train mathmodeling
dm-rl-train engineering fast 2
```

## 环境变量配置（可选）

你也可以通过环境变量覆盖默认值：

```bash
# 指定 GPU 数量
export DM_NUM_GPUS=2
bash scripts/quickstart.sh

# 指定 workspace 目录
export WORKSPACE_DIR=/path/to/custom/workspace
bash scripts/quickstart.sh

# 指定数据目录
export DATA_ROOT=/path/to/data
bash scripts/quickstart.sh
```

## 训练配置说明

### Fast Mode（快速测试）
- 适用于: 调试、快速验证
- 训练轮数: 1 epoch
- 耗时: 约 10-30 分钟

### Standard Mode（标准训练）
- 适用于: 日常训练
- 训练轮数: 2 epochs
- 耗时: 约 30-60 分钟

### Advanced Mode（高级训练）
- 适用于: 完整训练、性能优化
- 训练轮数: 4 epochs
- 耗时: 约 1-2 小时

## 监控训练

在另一个终端中，你可以监控训练进度：

```bash
# 实时查看日志
bash /home/aiops/liufan/projects/DeepModeling/examples/deepmodeling-rl/scripts/watch_logs.sh

# 监控训练指标
bash /home/aiops/liufan/projects/DeepModeling/examples/deepmodeling-rl/scripts/monitor_training.sh
```

## 查看结果

训练完成后，结果保存在：

```
/home/aiops/liufan/projects/DeepModeling/examples/deepmodeling-rl/workspace/
└── modeling_run_{task_id}_{uuid}/
    ├── sandbox/
    │   └── submission_{task_id}_{uuid}.csv  # 提交文件
    ├── artifacts/
    │   └── telemetry/
    │       ├── conversation.jsonl           # 对话历史
    │       └── run_metadata.json            # 运行元数据
    └── logs/                                # 日志文件
```

## 常见问题

### Q: 脚本报错 "Permission denied"
```bash
# 添加执行权限
chmod +x /home/aiops/liufan/projects/DeepModeling/examples/deepmodeling-rl/scripts/quickstart.sh
```

### Q: 显示 "conda: command not found"
```bash
# 确保 conda 已激活
source ~/miniconda3/etc/profile.d/conda.sh
conda activate dm-env
```

### Q: GPU out of memory
```bash
# 使用更少的 GPU 或修改配置
bash scripts/quickstart.sh engineering fast 1
```

### Q: 如何停止训练
```bash
# 按 Ctrl+C 停止
# 或在另一个终端
pkill -f "train.py"
```

## 进阶使用

### 直接调用 Python 模块

如果你需要更多控制，可以直接调用 Python：

```bash
cd /home/aiops/liufan/projects/DeepModeling/examples/deepmodeling-rl

# 使用 conda 环境
conda run -n dm-env python -m src.train fast \
    --benchmark engineering \
    --split engineering_mini \
    --max-turns 2 \
    --n-runners 1

# 或激活环境后运行
conda activate dm-env
python -m src.train fast --benchmark engineering --split engineering_mini
```

### 自定义配置

修改 [src/config.py](src/config.py) 以自定义训练参数。

## 相关文档

- [项目结构说明](PROJECT_STRUCTURE.md)
- [对话历史说明](CONVERSATION_HISTORY.md)
- [修改日志](CHANGES.md)
- [完整使用指南](USAGE.md)
