# DeepModeling RL - 项目结构

## 目录结构

```
deepmodeling-rl/
├── README.md                    # 项目说明文档
├── USAGE.md                     # 使用指南
├── PROJECT_STRUCTURE.md         # 项目结构说明（本文件）
├── requirements_dsrl.txt        # Python 依赖列表
├── .gitignore                   # Git 忽略规则
│
├── src/                         # 源代码目录
│   ├── __init__.py             # 包初始化文件
│   ├── agent.py                # DeepModeling RL Agent 实现
│   ├── config.py               # 训练配置
│   ├── data_utils.py           # 数据加载工具
│   ├── reward_function.py      # 奖励函数
│   ├── utils.py                # 工具函数（benchmark grading 等）
│   └── train.py                # 训练脚本
│
├── scripts/                     # Shell 脚本目录
│   ├── quickstart.sh           # 快速启动脚本
│   ├── monitor_training.sh     # 训练监控脚本
│   ├── watch_logs.sh           # 日志监控脚本
│   └── run.sh                  # 简单启动脚本
│
├── logs/                        # 日志文件（.gitignore）
│   ├── agentops.log
│   ├── training.log
│   └── ...
│
├── backup/                      # 备份文件（.gitignore）
│   └── *.bak
│
└── workspace/                   # RL 训练工作空间（.gitignore）
    ├── rl_industry_0_*/
    ├── rl_industry_1_*/
    └── ...
```

## 源代码模块说明

### src/agent.py
- **SimpleDeepModelingAgent**: 核心 RL agent 实现
  - 使用科学方法流程（Phenomenon → Hypothesis → Model → Experiment → Observation → Inference → Conclusion）
  - 支持多轮对话和代码执行
  - 集成 SandboxService 和 WorkspaceService
- **LitDeepModelingAgent**: Agent-Lightning 包装器
  - 用于 VERL PPO 训练

### src/utils.py
- **BenchmarkGrader**: 统一的 benchmark grading 接口
  - 支持 4 个 benchmark: engineering, mathmodeling, mle, science
  - 自动选择正确的 grading 函数和 registry
  - 分数标准化（统一为 higher-is-better）
- **工具函数**:
  - `normalize_score()`: 分数标准化
  - `format_conversation()`: 格式化对话历史
  - `build_episode_metadata()`: 构建 episode 元数据

### src/reward_function.py
- **RewardCalculator**: 奖励计算器
- **calculate_reward()**: 计算总奖励
- **calculate_detailed_reward()**: 计算详细奖励分解
  - execution: 执行奖励
  - quality: 质量分数
  - thoroughness: 完整性分数
  - achievement: 达标奖励

### src/config.py
- **resolve_config()**: 解析训练配置（fast/standard/advanced）
- 配置 GPU、批次大小、训练参数等

### src/data_utils.py
- **load_benchmark_tasks()**: 从 benchmark 加载任务
- **load_predefined_split()**: 加载预定义的训练/验证划分
- **PREDEFINED_SPLITS**: 预定义的数据集划分（如 engineering_mini）

### src/train.py
- **main()**: 训练主函数
- 集成 Agent-Lightning 和 VERL
- 支持多 GPU 训练

## 使用方式

### 方式 1: 使用快速启动脚本（推荐）

```bash
cd scripts
./quickstart.sh <benchmark> <mode> <gpu_count>

# 示例
./quickstart.sh engineering fast 1
```

### 方式 2: 直接运行训练脚本

```bash
# 从项目根目录运行
python -m src.train fast --benchmark engineering --split engineering_mini

# 或使用 conda 环境
conda run -n dm-env python -m src.train fast --benchmark engineering --split engineering_mini
```

### 方式 3: 作为 Python 模块导入

```python
from src import SimpleDeepModelingAgent, LitDeepModelingAgent, get_grader

# 创建 agent
agent = SimpleDeepModelingAgent(
    llm_endpoint="http://localhost:8000",
    model_name="deepseek-v3",
    max_turns=10
)

# 运行 episode
result = agent.run_episode(task)

# 获取 grader
grader = get_grader()
score = grader.grade_submission(task, submission_path)
```

## 监控训练

```bash
# 实时监控训练日志
cd scripts
./watch_logs.sh

# 监控训练进度（另一个终端）
./monitor_training.sh
```

## 清理

```bash
# 清理工作空间
rm -rf workspace/*

# 清理日志
rm -rf logs/*

# 清理 Python 缓存
find . -type d -name __pycache__ -exec rm -rf {} +
```

## 开发指南

### 添加新的 benchmark

1. 在 `src/utils.py` 的 `BenchmarkGrader._load_grading_modules()` 中添加导入
2. 在 `src/data_utils.py` 中添加数据加载逻辑
3. 在 `DEFAULT_DATA_ROOTS` 中添加数据路径

### 修改奖励函数

编辑 `src/reward_function.py` 中的 `RewardCalculator` 类。

### 调整训练配置

编辑 `src/config.py` 中的配置预设。

## 依赖安装

```bash
pip install -r requirements_dsrl.txt
```

## 版本历史

- **v0.1.0** (2025-11-09): 项目重组，模块化设计
  - 创建 src/ 源代码目录
  - 创建 scripts/ 脚本目录
  - 分离日志和备份文件
  - 统一 benchmark grading 接口
  - 简化导入和使用方式
