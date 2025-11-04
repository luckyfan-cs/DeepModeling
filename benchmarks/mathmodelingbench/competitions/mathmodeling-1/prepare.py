import json
from pathlib import Path

import pandas as pd


def _sanitize_problem_content(problem_data: str) -> str:
    payload = json.loads(problem_data)
    sanitized = dict(payload)
    for key in list(sanitized.keys()):
        if key.startswith("expected_"):
            sanitized.pop(key)
    return json.dumps(sanitized, indent=2, ensure_ascii=False)


def prepare(raw: Path, public: Path, private: Path):
    problem_file = raw / "problem.json"
    if not problem_file.exists():
        raise FileNotFoundError(f"Problem specification not found: {problem_file}")

    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)

    problem_data = problem_file.read_text(encoding="utf-8")
    sanitized_problem = _sanitize_problem_content(problem_data)
    (public / "problem.json").write_text(sanitized_problem, encoding="utf-8")

    sample_submission = pd.DataFrame({"id": [0], "answer": ["@cost[0.00]"]})
    sample_submission.to_csv(public / "sample_submission.csv", index=False)

    answer = pd.DataFrame({"id": [0], "answer": ["@cost[32.43]"]})
    answer.to_csv(private / "answer.csv", index=False)

    return public / "problem.json"
