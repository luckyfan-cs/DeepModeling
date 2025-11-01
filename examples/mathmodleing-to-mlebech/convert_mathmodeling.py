#!/usr/bin/env python3
"""Convert mathmodeling dataset tasks into mathmodelingbench competitions."""
from __future__ import annotations

import argparse
import json
import re
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Dict, Any

DESCRIPTION_TEMPLATE = """# {title}\n\n{body}\n\n### Submission Format\n- Provide a single row with `id` and `answer` columns.\n- The answer must use the template `@{tag}[value]`, where `value` is the numeric solution rounded as appropriate.\n\n### Evaluation\n- Submissions are evaluated using an exact-match checker with a small tolerance (±1e-2) on the reported value.\n"""

CONFIG_TEMPLATE = """id: {competition_id}\nname: {name}\ncompetition_type: modeling\nawards_medals: false\nprizes: null\ndescription: {description_path}\n\ndataset:\n  answers: {dataset_name}/prepared/private/answer.csv\n  sample_submission: {dataset_name}/prepared/public/sample_submission.csv\n\ngrader:\n  name: generic_tag_{tag}\n  grade_fn: {module_path}.grade:grade\n\npreparer: {module_path}.prepare:prepare\n"""

GRADE_TEMPLATE = """import re\nimport pandas as pd\n\nTAG = {tag_literal}\nPATTERN = re.compile(rf"@{{TAG}}\\[(?P<value>-?\\d+(?:\\.\\d+)?)\\]", re.IGNORECASE)\n\n\ndef _extract_value(cell: str) -> float:\n    if not isinstance(cell, str):\n        return float("nan")\n    match = PATTERN.search(cell.strip())\n    if not match:\n        return float("nan")\n    return float(match.group("value"))\n\n\n\ndef grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:\n    try:\n        submitted = _extract_value(submission.iloc[0]["answer"])
    except Exception:
        submitted = float("nan")
    try:
        expected = _extract_value(answers.iloc[0]["answer"])
    except Exception:
        expected = float("nan")
    if pd.isna(submitted) or pd.isna(expected):
        return 0.0
    return 1.0 if abs(submitted - expected) <= 1e-2 else 0.0
"""

PREPARE_TEMPLATE = """import json\nfrom pathlib import Path\n\nimport pandas as pd\n\nTAG = {tag_literal}\nANSWER_LITERAL = {answer_literal}\n\n\ndef prepare(raw: Path, public: Path, private: Path):\n    problem_file = raw / "problem.json"\n    if not problem_file.exists():\n        raise FileNotFoundError(f"Problem specification not found: {{problem_file}}")\n\n    public.mkdir(parents=True, exist_ok=True)\n    private.mkdir(parents=True, exist_ok=True)\n\n    problem_data = problem_file.read_text(encoding="utf-8")\n    (public / "problem.json").write_text(problem_data, encoding="utf-8")\n\n    sample_submission = pd.DataFrame({{"id": [0], "answer": [f"@{{TAG}}[0.00]"]}})\n    sample_submission.to_csv(public / "sample_submission.csv", index=False)\n\n    answer = pd.DataFrame({{"id": [0], "answer": [f"@{{TAG}}[{{ANSWER_LITERAL}}]"]}})\n    answer.to_csv(private / "answer.csv", index=False)\n\n    return public / "problem.json"\n"""

LEADERBOARD_TEMPLATE = """scoreNullable,teamId,hasTeamName,submissionDate,score,hasScore\n{score},1,True,2024-01-01 00:00:00,{score},True\n0.0000,2,True,2024-01-01 00:00:00,0.0000,True\n"""

CHECKSUMS_TEMPLATE = """# Checksums for {competition_id} dataset\nzip: ""\n"""

RAW_TEMPLATE = """{{\n  "id": {id_literal},\n  "en_question": {en_question_literal},\n  "cn_question": {cn_question_literal},\n  "difficulty": {difficulty_literal},\n  "expected_answer": {answer_literal}\n}}\n"""


@dataclass
class TaskRecord:
    idx: int
    data: Dict[str, Any]

    @property
    def task_id(self) -> Any:
        return self.data.get("id", self.idx)

    @property
    def en_question(self) -> str:
        # Support multiple field names
        return self.data.get("en_question", self.data.get("Question", "")).strip()

    @property
    def cn_question(self) -> str:
        return self.data.get("cn_question", "").strip()

    @property
    def answer(self) -> str:
        # Support multiple field names
        return str(self.data.get("en_answer", self.data.get("Answer", ""))).strip()

    @property
    def difficulty(self) -> str:
        return str(self.data.get("difficulty", self.data.get("Type", "unknown")))

    def get_public_data(self) -> Dict[str, Any]:
        """Get sanitized data for public directory (without answer)."""
        public_data = self.data.copy()
        # Remove all answer-related fields to avoid leaking ground truth
        for key in ["en_answer", "Answer", "answer", "cn_answer"]:
            public_data.pop(key, None)
        return public_data


def parse_dataset(path: Path) -> List[TaskRecord]:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".jsonl":
        records = [json.loads(line) for line in text.splitlines() if line.strip()]
    else:
        records = []
        buffer = ""
        depth = 0
        for char in text:
            if char == "{":
                depth += 1
            if depth > 0:
                buffer += char
            if char == "}":
                depth -= 1
                if depth == 0 and buffer:
                    records.append(json.loads(buffer))
                    buffer = ""
        if buffer.strip():
            records.append(json.loads(buffer))
    return [TaskRecord(idx=i, data=data) for i, data in enumerate(records)]


def slugify(text: str, default: str = "task") -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", text.lower())
    cleaned = cleaned.strip("-")
    return cleaned or default


def select_tag(record: TaskRecord, default_tag: str, tag_map: Dict[str, str]) -> str:
    key = str(record.task_id)
    if key in tag_map:
        return tag_map[key]
    question = f"{record.en_question} {record.cn_question}".lower()
    if "profit" in question:
        return "profit"
    if "cost" in question or "expense" in question or "minimize" in question:
        return "cost"
    return default_tag


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def write_file(path: Path, content: str, dry_run: bool):
    if dry_run:
        print(f"[DRY-RUN] Would write {path}")
        return
    path.write_text(content, encoding="utf-8")


def convert_task(record: TaskRecord, args: argparse.Namespace, index_offset: int, dry_run: bool):
    tag = select_tag(record, args.default_tag, args.tag_map)
    base_slug = slugify(record.en_question.split(".")[0], f"task-{record.idx}")
    competition_id = f"{args.competition_prefix}-{index_offset + record.idx}-{base_slug}"[:80]

    # Use hyphens consistently for both registry and data directories
    registry_dir = Path(args.registry_root) / competition_id
    data_dir = Path(args.data_root) / competition_id

    description_path = f"benchmarks/mathmodelingbench/competitions/{competition_id}/description.md"
    module_path = f"benchmarks.mathmodelingbench.competitions.{competition_id}"

    if not dry_run:
        ensure_dir(registry_dir)
        ensure_dir(data_dir / "raw")
        ensure_dir(data_dir / "prepared" / "public")
        ensure_dir(data_dir / "prepared" / "private")
        init_file = registry_dir / "__init__.py"
        if not init_file.exists():
            init_file.write_text("", encoding="utf-8")

    title = f"{competition_id.replace('-', ' ').title()}"
    body = textwrap.dedent(record.en_question or record.cn_question or "Math modeling task.").strip()
    description = DESCRIPTION_TEMPLATE.format(title=title, body=body, tag=tag)

    config = CONFIG_TEMPLATE.format(
        competition_id=competition_id,
        name=title,
        description_path=description_path,
        dataset_name=competition_id,
        module_path=module_path,
        tag=tag,
    )

    grade = GRADE_TEMPLATE.format(tag_literal=repr(tag))
    prepare = PREPARE_TEMPLATE.format(tag_literal=repr(tag), answer_literal=record.answer or "0.0")
    leaderboard = LEADERBOARD_TEMPLATE.format(score="1.0000")
    checksums = CHECKSUMS_TEMPLATE.format(competition_id=competition_id)
    raw = RAW_TEMPLATE.format(
        id_literal=json.dumps(competition_id),
        en_question_literal=json.dumps(record.en_question),
        cn_question_literal=json.dumps(record.cn_question),
        difficulty_literal=json.dumps(record.difficulty),
        answer_literal=json.dumps(record.answer),
    )

    dataset_problem_path = data_dir / "raw" / "problem.json"

    # Generate public problem.json without answer (to avoid leaking ground truth to LLM)
    public_problem_data = record.get_public_data()
    public_problem_json = json.dumps(public_problem_data, indent=2, ensure_ascii=False)

    write_file(registry_dir / "description.md", description, dry_run)
    write_file(registry_dir / "config.yaml", config, dry_run)
    write_file(registry_dir / "grade.py", grade, dry_run)
    write_file(registry_dir / "prepare.py", prepare, dry_run)
    write_file(registry_dir / "leaderboard.csv", leaderboard, dry_run)
    write_file(registry_dir / "checksums.yaml", checksums, dry_run)

    # Write raw data with answer (for reference)
    write_file(dataset_problem_path, raw, dry_run)
    # Write public data WITHOUT answer (for LLM)
    write_file(data_dir / "prepared" / "public" / "problem.json", public_problem_json, dry_run)
    write_file(data_dir / "prepared" / "public" / "sample_submission.csv", f"id,answer\n0,@{tag}[0.00]\n", dry_run)
    write_file(data_dir / "prepared" / "private" / "answer.csv", f"id,answer\n0,@{tag}[{record.answer}]\n", dry_run)

    print(f"Generated competition {competition_id} with tag @{tag} and answer {record.answer}")


def parse_tag_map(path: str | None) -> Dict[str, str]:
    if not path:
        return {}
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return {str(k): str(v) for k, v in data.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-file", required=True, help="Path to the mathmodeling dataset (JSON / JSONL).")
    parser.add_argument("--registry-root", required=True, help="Destination for competition metadata (mathmodelingbench/competitions).")
    parser.add_argument("--data-root", required=True, help="Destination for prepared data (mathmodeling-bench/competitions).")
    parser.add_argument("--competition-prefix", default="mathmodeling", help="Prefix for generated competition IDs.")
    parser.add_argument("--default-tag", default="value", help="Default submission tag when heuristics do not match.")
    parser.add_argument("--tag-map", help="Optional JSON mapping of dataset task_id to submission tag.")
    parser.add_argument("--start-index", type=int, default=0, help="Offset added to dataset indices when forming IDs.")
    parser.add_argument("--dry-run", action="store_true", help="Preview generated files without writing to disk.")

    args = parser.parse_args()
    args.dataset_file = Path(args.dataset_file)
    args.registry_root = Path(args.registry_root)
    args.data_root = Path(args.data_root)
    args.tag_map = parse_tag_map(args.tag_map)

    records = parse_dataset(args.dataset_file)
    if not records:
        raise SystemExit("No records found in dataset")

    for record in records:
        convert_task(record, args, args.start_index, args.dry_run)


if __name__ == "__main__":
    main()
