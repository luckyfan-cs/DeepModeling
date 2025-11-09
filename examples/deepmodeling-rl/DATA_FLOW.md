# 数据流程和 Prompt 生成说明

## 问题解答

### 1. Task Prompt 来自哪里？

**来源**: [src/data_utils.py:207-209](src/data_utils.py#L207-L209)

```python
def _format_engineering_prompt(description: str, public_dir: Path, sample_name: str) -> str:
    """Return the competition description (I/O instructions will be added by TaskHandler)."""
    return description.strip()
```

**说明**：
- `_format_engineering_prompt` **只返回原始的 competition description**
- **不再包含** "Additional instructions"，因为这些内容会由 TaskHandler → DataAnalyzer 动态生成
- `task["prompt"]` 只作为 `description` 传递给 ScienceTaskHandler

**生成时机**：在 `_load_engineering_tasks()` 函数中为每个任务生成 prompt

### 2. WorkspaceService 是 copy 还是 symlink？

**答案**: **优先使用软链接 (symlink)**，失败时回退到拷贝 (copy)

**代码位置**: [modeling/services/workspace.py:108-162](../../../modeling/services/workspace.py#L108-L162)

```python
def link_data_to_workspace(self, source_data_dir: Path):
    """Links or copies the CONTENTS of a source data directory into the run's sandbox_workdir."""

    for item in src.iterdir():
        destination_item = destination_dir / item.name

        try:
            # 1. 优先尝试创建软链接
            os.symlink(source_item, destination_item, target_is_directory=...)
            logger.debug(f"Linked {source_item.name} into sandbox.")

        except (OSError, NotImplementedError) as e:
            # 2. 软链接失败，回退到拷贝
            logger.warning(f"Symlink creation failed for {item.name} ({e}). Falling back to copying.")

            if source_item.is_dir():
                shutil.copytree(source_item, destination_item)
            else:
                shutil.copy2(source_item, destination_item)
```

**实际验证**：

```bash
$ ls -lah workspace_rl/modeling_run_industry_18_dc12600a/sandbox/

lrwxrwxrwx 1 liufan sailor  117 Nov  9 14:06 problem.json -> /home/aiops/liufan/projects/DeepModeling/data/engineering-bench/competitions/industry-18/prepared/public/problem.json
lrwxrwxrwx 1 liufan sailor  126 Nov  9 14:06 sample_submission.csv -> /home/aiops/liufan/projects/DeepModeling/data/engineering-bench/competitions/industry-18/prepared/public/sample_submission.csv
```

✅ **确认是软链接** (`lrwxrwxrwx` 和 `->` 符号)

### 3. DataAnalyzer 分析的是 sandbox 里的数据吗？

**答案**: **是的，但通过软链接指向原始数据**

## 完整数据流程

### Modeling Runner (main.py)

```
1. Benchmark 提供原始数据路径
   /home/aiops/liufan/projects/DeepModeling/data/engineering-bench/competitions/industry-3/prepared/public/
   ├── problem.json
   └── sample_submission.csv

2. WorkspaceService.link_data_to_workspace()
   ↓ 创建软链接

3. Workspace Sandbox
   /path/to/workspace/modeling_run_industry_3_xxx/sandbox/
   ├── problem.json -> /path/to/original/problem.json  (symlink)
   └── sample_submission.csv -> /path/to/original/...  (symlink)

4. DataAnalyzer.analyze_data(data_dir)
   ↓ data_dir = sandbox 目录
   ↓ 通过软链接读取原始数据
   生成数据报告（文件树、CSV 预览等）

5. TaskHandler.prepare_input()
   ↓ 拼接 description + data_report + Additional instructions
   生成完整 prompt

6. Workflow 执行
   ↓ 在 sandbox 目录中运行代码
   ↓ 读取数据（通过软链接）
   生成 submission.csv
```

### RL Agent (deepmodeling-rl)

流程相同，只是使用 `SimpleDeepModelingAgent` 而不是 `ModelingWorkflow`：

```
1. data_utils.py 生成 task dict
   {
     "data_dir": "/path/to/public/",
     "prompt": "description + Additional instructions"
   }

2. agent._prepare_task_io()
   ↓ 使用 ScienceTaskHandler
   ↓ 调用 DataAnalyzer
   生成 description, io_instructions

3. WorkspaceService 创建 sandbox
   ↓ link_data_to_workspace(data_dir)
   创建软链接

4. agent 在 sandbox 执行代码
   ↓ 读取数据（通过软链接）
   生成 submission.csv
```

## 关键概念

### 为什么使用软链接？

1. **节省磁盘空间** - 避免重复拷贝大数据文件
2. **提高速度** - 创建软链接比拷贝文件快得多
3. **保持一致性** - 多个 workspace 指向同一个数据源
4. **便于调试** - 可以直接看到数据来自哪里

### 软链接的限制

1. **平台依赖** - Windows 需要管理员权限或开发者模式
2. **移动性** - 移动 workspace 后软链接会失效
3. **权限** - 需要对原始数据有读权限

### DataAnalyzer 的作用

`DataAnalyzer` 分析 sandbox 中的数据（实际上是通过软链接读取原始数据），生成：

1. **文件树结构** - 列出所有文件
2. **CSV 数据预览** - 显示前几行
3. **数据类型信息** - 列类型、维度等
4. **I/O 指令** - 告诉模型如何读写文件

这些信息被拼接到 prompt 中，帮助 LLM 理解数据结构。

## Prompt 组成

完整的 LLM prompt 由以下部分组成：

```
┌─────────────────────────────────────────────────┐
│ 1. Task Description (from competition.description) │
│    - 问题描述                                    │
│    - 数据说明                                    │
│    - 评估指标                                    │
├─────────────────────────────────────────────────┤
│ 2. Data Report (from DataAnalyzer)              │
│    - 目录结构                                    │
│    - 文件列表                                    │
│    - CSV 预览                                   │
│    - 数据统计信息                                 │
├─────────────────────────────────────────────────┤
│ 3. I/O Instructions (from DataAnalyzer)         │
│    - 输入文件路径                                 │
│    - 输出文件要求                                 │
│    - Submission format                          │
│    - 文件位置说明                                 │
└─────────────────────────────────────────────────┘
```

**关键点**：
- `task["prompt"]` 只包含原始的 competition description
- **所有 I/O 相关的指令**都由 `ScienceTaskHandler` → `DataAnalyzer` 动态生成
- 这样确保指令与实际的 sandbox 环境完全一致

## 实际示例

### 路径对应关系

```
Original Data:
/home/aiops/liufan/projects/DeepModeling/data/engineering-bench/competitions/industry-3/prepared/public/
├── problem.json
└── sample_submission.csv

Workspace Sandbox:
/path/to/workspace/modeling_run_industry_3_xxx/sandbox/
├── problem.json -> (symlink to original)
├── sample_submission.csv -> (symlink to original)
└── submission.csv  (生成的输出，实际文件)
```

### Prompt 中的路径

```text
I/O Requirements (由 DataAnalyzer 生成):
- All input files are located in the **current working directory** (./).
  ↑ 这是 sandbox 的当前工作目录，通过软链接指向原始数据
- Save your final submission file to `./submission_industry-3_xxx.csv`
  ↑ 保存在 sandbox 中
- Available files: problem.json, sample_submission.csv
  ↑ DataAnalyzer 动态分析 sandbox 目录生成
```

## 总结

| 问题 | 答案 |
|------|------|
| Task prompt 来源 | `src/data_utils.py` 的 `_format_engineering_prompt()`，**只返回 description** |
| I/O instructions 来源 | `ScienceTaskHandler` → `DataAnalyzer` **动态生成** |
| 数据是 copy 还是 symlink | **软链接 (symlink)**，失败时才 copy |
| DataAnalyzer 分析什么数据 | **sandbox 中的数据**（通过软链接指向原始数据） |
| 代码在哪里执行 | **sandbox 目录** |
| 数据实际位置 | **原始数据目录**，通过软链接访问 |

**关键设计**：
- **数据隔离性**：每个 workspace 有独立的 sandbox
- **避免重复拷贝**：使用软链接节省磁盘空间和时间
- **动态生成指令**：I/O instructions 根据实际 sandbox 环境生成，确保准确性
