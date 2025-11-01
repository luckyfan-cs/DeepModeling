# MathModeling → Bench Conversion Methodology

This guide outlines the process for turning tasks from the `mathmodeling` project into competitions that can be evaluated by `mathmodelingbench` and the Modeling framework.

## Workflow Overview
1. **Extract tasks** from the original dataset (e.g., `BWOR.json`).
2. **Generate registry metadata** under `mathmodelingbench/competitions/<competition-id>/` (`config.yaml`, `description.md`, `grade.py`, `prepare.py`, `leaderboard.csv`, `checksums.yaml`).
3. **Prepare runnable data assets** under `mathmodeling-bench/competitions/<competition-id>/` (raw JSON prompt, prepared public bundle, prepared private answers).
4. **Register the competitions** by appending their IDs to `config.yaml` (the `mathmodeling_competitions` section).
5. **Verify end-to-end** with `python main.py --workflow scientific --benchmark mathmodeling --data-dir <bench-data> --task <competition-id>`.

## Automation Script
The accompanying `convert_mathmodeling.py` script automates steps 1–3. It can parse JSON / JSONL datasets, normalise question text, create the full directory structure, and populate grading & preparation helpers with the appropriate submission tag.

### Key Features
- Supports custom competition prefixes so generated IDs remain readable (`mathmodeling-<index>-<slug>`).
- Automatically derives grade and prepare logic with tag-aware validation (e.g., `@profit[...]`, `@cost[...]`).
- Persists the raw prompt JSON alongside prepared public/private assets for reproducibility.
- Provides a dry-run option to inspect planned changes before writing to disk.

## Usage
```bash
python examples/mathmodleing-to-mlebech/convert_mathmodeling.py \
  --dataset-file /path/to/BWOR.json \
  --registry-root /home/aiops/liufan/projects/DeepModeling/mathmodelingbench/competitions \
  --data-root /home/aiops/liufan/projects/DeepModeling/mathmodeling-bench/competitions \
  --competition-prefix mathmodeling \
  --default-tag value \
  --start-index 2
```

### Optional Controls
- `--tag-map` allows overriding the submission tag (`profit`, `cost`, etc.) per task ID using a small JSON file.
- `--dry-run` prints the planned artefacts without touching the filesystem.
- `--leaderboard-score` adjusts the baseline leaderboard template when needed.

## Recommended Validation Checklist
1. Run the converter with `--dry-run` to verify naming and tag selection.
2. Execute the converter without `--dry-run` to materialise files.
3. Append the new IDs to `config.yaml` and update any helper scripts (e.g., `job_scripts/test.sh`).
4. Call the benchmark end-to-end to ensure the LLM submission format, grading and data paths line up.
5. Commit artefacts along with a short changelog summarising the added tasks.
