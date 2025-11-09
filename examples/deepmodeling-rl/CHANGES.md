# RL Agent 修改说明 - 与 Modeling Runner 保持一致

## 修改目标

使 RL agent 的文件保存方式、命名规范和评估流程与 `modeling/runner.py` 保持完全一致，确保与各个 benchmark 的兼容性。

## 参考命令

```bash
python main.py --workflow scientific \
    --benchmark mathmodeling \
    --data-dir "/path/to/data/mathmodeling-bench/competitions" \
    --llm-model openai/deepseek-ai/DeepSeek-V3.1-Terminus \
    --task mathmodeling-0
```

## 文件结构对比

### Modeling Runner 的结构 (`runs/`)

```
runs/
└── modeling_run_bwor_0_731b5760/          # run_name: modeling_run_{task_id}_{uuid}
    ├── sandbox/                            # sandbox_workdir
    │   ├── submission_bwor-0_546f36.csv   # 在这里生成文件
    │   ├── train.csv                       # 数据文件（symlink）
    │   └── test.csv
    ├── artifacts/                          # 元数据和 telemetry
    │   └── telemetry/
    │       ├── conversation.jsonl
    │       └── run_metadata.json
    ├── logs/                              # 日志
    └── state/                             # 状态文件
```

### RL Agent 的结构（修改后，`workspace/`）

```
workspace/
└── modeling_run_industry_0_a1b2c3d4/      # run_name: modeling_run_{task_id}_{uuid}
    ├── sandbox/                            # sandbox_workdir（相同）
    │   ├── submission_industry-0_e5f6a7.csv  # 在这里生成文件（相同）
    │   ├── train.csv                       # 数据文件（symlink，相同）
    │   └── test.csv
    ├── artifacts/                          # 元数据和 telemetry（相同）
    │   └── telemetry/
    │       ├── conversation.jsonl
    │       └── run_metadata.json
    ├── logs/                              # 日志
    └── state/                             # 状态文件
```

**Grading 文件位置**: `{workspace_base}/submission_{task_id}_{uuid}.csv`

## 主要修改

### 1. Run Name 格式统一 (`src/agent.py:222`)

```python
# 之前
run_name = f"rl_{safe_task_id}_{unique_suffix}"

# 现在 (与 runner.py 一致)
run_name = f"modeling_run_{safe_task_id}_{unique_suffix}"
```

### 2. Submission 文件命名 (`src/agent.py:224-228`)

```python
# 创建 output submission path (与 benchmark 一致)
submission_unique_id = uuid.uuid4().hex[:6]
output_filename = f"submission_{task_id}_{submission_unique_id}.csv"
output_submission_path = str((Path(self.workspace_base) / output_filename).absolute())
```

格式: `submission_{competition_id}_{uuid}.csv`

### 3. TaskHandler 输入路径 (`src/agent.py:86-120`)

```python
def _prepare_task_io(
    self,
    task: Dict[str, Any],
    output_submission_path: str  # 新增参数：完整的输出路径
) -> tuple[str, str, Path, Path]:
    """Prepare task I/O using ScienceTaskHandler from modeling."""

    task_def = TaskDefinition(
        task_id=task["task_id"],
        task_type="science",
        payload={
            "description": task["prompt"],
            "public_data_dir": task["data_dir"],
            "output_submission_path": output_submission_path,  # 使用完整路径
            ...
        }
    )
```

### 4. 文件复制流程（已存在，保持不变）

在每次执行后，从 sandbox 复制到 grading 路径：

```python
# src/agent.py:333-342
sandbox_workdir = workspace.get_path("sandbox_workdir")
generated_file = sandbox_workdir / output_path.name
if generated_file.exists():
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if generated_file.resolve() != output_path.resolve():
        shutil.copy(generated_file, output_path)
        logger.info(f"[TURN] Copied output to: {output_path}")
    success = True
```

## 工作流程

### Modeling Runner (main.py)

1. 创建 run_name: `modeling_run_{task_id}_{uuid}`
2. Benchmark 创建 output_submission_path: `{log_path}/submission_{competition_id}_{uuid}.csv`
3. WorkspaceService 创建目录结构（包括 `sandbox/`）
4. TaskHandler.prepare_input() 处理路径
5. Workflow 在 sandbox_workdir 执行代码
6. Runner 从 `sandbox/submission.csv` 复制到 `output_submission_path`
7. Benchmark 使用 `grade_csv(output_submission_path, competition)` 评分

### RL Agent (修改后)

1. 创建 run_name: `modeling_run_{task_id}_{uuid}` ✓
2. Agent 创建 output_submission_path: `{workspace_base}/submission_{task_id}_{uuid}.csv` ✓
3. WorkspaceService 创建目录结构（包括 `sandbox/`）✓
4. TaskHandler.prepare_input() 处理路径 ✓
5. Agent 在 sandbox_workdir 执行代码 ✓
6. Agent 从 `sandbox/submission.csv` 复制到 `output_submission_path` ✓
7. Grader 使用 `grade_csv(output_submission_path, competition)` 评分 ✓

## Benchmark 兼容性

### Engineering Benchmark
- ✓ 文件格式: `submission_{competition_id}_{uuid}.csv`
- ✓ 路径结构: 与 runner.py 一致
- ✓ Grading: 使用 `engineeringbench.grade_csv()`

### Math Modeling Benchmark
- ✓ 文件格式: `submission_{competition_id}_{uuid}.csv`
- ✓ 路径结构: 与 runner.py 一致
- ✓ Grading: 使用 `mathmodelingbench.grade_csv()`

### MLE Benchmark
- ✓ 文件格式: `submission_{competition_id}_{uuid}.csv`
- ✓ 路径结构: 与 runner.py 一致
- ✓ Grading: 使用 `mlebench.grade_csv()`

### Science Benchmark
- ✓ 文件格式: `submission_{competition_id}_{uuid}.csv`
- ✓ 路径结构: 与 runner.py 一致
- ✓ Grading: 使用 `sciencebench.grade_csv()`

## 验证

```bash
# 测试 agent 创建
cd /home/aiops/liufan/projects/DeepModeling/examples/deepmodeling-rl
python3 -c "from src.agent import SimpleDeepModelingAgent; agent = SimpleDeepModelingAgent('http://localhost:8000', 'test'); print('✓ Agent created')"

# 运行训练
python -m src.train fast --benchmark engineering --split engineering_mini
```

## 关键改进

1. **统一命名**: run_name 使用 `modeling_run_` 前缀而不是 `rl_`
2. **完整路径**: output_submission_path 使用完整的绝对路径
3. **结构一致**: workspace 目录结构与 modeling runner 完全一致
4. **兼容所有 benchmark**: 支持 engineering、mathmodeling、mle、science

## 注意事项

- 所有文件都在 `sandbox/` 目录下执行
- submission 文件会被复制到 workspace_base 根目录用于 grading
- UUID 确保每次运行的文件名唯一，避免冲突
- 保持与 modeling/runner.py 的行为一致性
