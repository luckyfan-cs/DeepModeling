# 立即开始使用 DeepModeling-Infer

## 30 秒快速开始

```bash
# 1. 进入目录
cd /home/aiops/liufan/projects/DeepModeling/examples/deepmodeling-infer

# 2. 一键测试（自动部署 + 推理）
./deploy_and_test.sh --model /path/to/your/model --task industry-0

# 完成！查看结果
cat results/summary_*.json | jq .
```

---

## 或使用您熟悉的接口

```bash
# 1. 先部署模型
python -m vllm.entrypoints.openai.api_server \
    --model /path/to/your/model --port 8000 &

# 2. 运行推理（您熟悉的命令格式）
python main.py --workflow scientific --benchmark engineering \
    --llm-api http://localhost:8000 --task industry-0

# 3. 查看结果
cat results/summary_*.json | jq .
```

---

## 完整示例

### Engineering Benchmark
```bash
python main.py --workflow scientific --benchmark engineering \
    --llm-api http://localhost:8000 --task industry-0
```

### MathModeling Benchmark
```bash
python main.py --workflow scientific --benchmark mathmodeling \
    --data-dir "/home/aiops/liufan/projects/DeepModeling/data/mathmodeling-bench/competitions" \
    --llm-api http://localhost:8000 --task mathmodeling-0
```

### 批量测试
```bash
python main.py --workflow scientific --benchmark engineering \
    --llm-api http://localhost:8000 --task-limit 10
```

---

## 5 种使用方式

1. **一键脚本** `./deploy_and_test.sh` - 最简单
2. **main.py** - 兼容您的接口（推荐）
3. **src.infer** - 高级控制
4. **quickstart.sh** - 快速测试
5. **Python API** - 代码集成

---

## 文档目录

| 文档 | 用途 |
|------|------|
| **GET_STARTED.md** | 👈 本文档，立即开始 |
| [README.md](README.md) | 完整功能文档 |
| [QUICKSTART.md](QUICKSTART.md) | 10 个快速示例 |
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | 详细部署指南 |
| [USAGE_SUMMARY.md](USAGE_SUMMARY.md) | 5 种使用方式 |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | 项目总结 |

---

## 需要帮助？

```bash
# 查看帮助
python main.py --help
./deploy_and_test.sh --help

# 查看示例
cat example_usage.py
```

---

## 核心优势

✅ **完全兼容您的命令行接口**  
✅ **无需训练依赖（不需要 Agent-Lightning/VERL）**  
✅ **支持 API 和本地模型**  
✅ **自动评分（基准原生）**  
✅ **详细日志和结果**  

---

**立即开始**:
```bash
./deploy_and_test.sh --model /path/to/model --task industry-0
```

🚀 就是这么简单！
