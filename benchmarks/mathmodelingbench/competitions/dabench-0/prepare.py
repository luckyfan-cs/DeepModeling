from pathlib import Path

import pandas as pd


def prepare(raw: Path, public: Path, private: Path):
    """
    Prepare the DABench task 0 dataset for mathmodelingbench.
    """
    data_file = raw / "test_ave.csv"
    if not data_file.exists():
        raise FileNotFoundError(f"Data file not found: {data_file}")

    df = pd.read_csv(data_file)

    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)

    train_file = public / "train.csv"
    df.to_csv(train_file, index=False)

    sample_submission = pd.DataFrame({"id": [0], "answer": ["@mean_fare[0.00]"]})
    sample_submission.to_csv(public / "sample_submission.csv", index=False)

    answer = pd.DataFrame({"id": [0], "answer": ["@mean_fare[34.65]"]})
    answer.to_csv(private / "answer.csv", index=False)

    return train_file
