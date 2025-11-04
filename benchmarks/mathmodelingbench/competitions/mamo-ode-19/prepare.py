import json
from pathlib import Path

import pandas as pd

TAG = 'value'
ANSWER_LITERAL = 18.867


def prepare(raw: Path, public: Path, private: Path):
    problem_file = raw / "problem.json"
    if not problem_file.exists():
        raise FileNotFoundError(f"Problem specification not found: {problem_file}")

    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)

    problem_data = problem_file.read_text(encoding="utf-8")
    (public / "problem.json").write_text(problem_data, encoding="utf-8")

    sample_submission = pd.DataFrame({"id": [0], "answer": [f"@{TAG}[0.00]"]})
    sample_submission.to_csv(public / "sample_submission.csv", index=False)

    answer = pd.DataFrame({"id": [0], "answer": [f"@{TAG}[{ANSWER_LITERAL}]"]})
    answer.to_csv(private / "answer.csv", index=False)

    return public / "problem.json"
