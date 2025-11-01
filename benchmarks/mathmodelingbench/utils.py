import importlib
import importlib.util
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, List, Optional

import pandas as pd
import yaml

LOGGER_NAME = "mathmodelingbench"


def _ensure_logger_configured() -> None:
    root = logging.getLogger(LOGGER_NAME)
    if root.handlers:
        return
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    root.addHandler(handler)
    root.setLevel(logging.INFO)


def get_logger(name: str) -> logging.Logger:
    _ensure_logger_configured()
    return logging.getLogger(name)


def purple(text: str) -> str:
    return f"\033[1;35m{text}\033[0m"


def get_timestamp() -> str:
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S")


def get_module_dir() -> Path:
    path = Path(__file__).parent.resolve()
    assert path.name == "mathmodelingbench", (
        f"Expected module directory named 'mathmodelingbench', got '{path.name}'"
    )
    return path


def get_repo_dir() -> Path:
    return get_module_dir().parent


def load_yaml(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def import_fn(path: str) -> Callable:
    if ":" not in path:
        raise ValueError(f"Expected 'module.submodule:function', got '{path}'")
    module_name, fn_name = path.split(":", maxsplit=1)

    # Try standard import first
    try:
        module = importlib.import_module(module_name)
    except (ImportError, ModuleNotFoundError) as e:
        # If module name contains hyphens, try loading via file path
        if "-" in module_name and module_name.startswith("mathmodelingbench.competitions."):
            # Extract competition name: mathmodelingbench.competitions.xxx-yyy.zzz -> xxx-yyy
            parts = module_name.split(".")
            if len(parts) >= 4:
                competition_dir = parts[2]
                file_name = parts[3] if len(parts) > 3 else fn_name

                # Build file path
                module_dir = get_module_dir()
                file_path = module_dir / "competitions" / competition_dir / f"{file_name}.py"

                if file_path.exists():
                    # Load module from file path
                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        sys.modules[module_name] = module
                        spec.loader.exec_module(module)
                    else:
                        raise ImportError(f"Failed to load module from {file_path}")
                else:
                    raise ImportError(f"Module file not found: {file_path}") from e
            else:
                raise e
        else:
            raise e

    if not hasattr(module, fn_name):
        raise AttributeError(f"Module '{module_name}' has no attribute '{fn_name}'")
    fn = getattr(module, fn_name)
    if not callable(fn):
        raise TypeError(f"Imported object '{fn_name}' from '{module_name}' is not callable")
    return fn


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def read_jsonl(path: Path, skip_commented_out_lines: bool = False) -> List[dict]:
    records: List[dict] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if skip_commented_out_lines and line.startswith(("#", "//")):
                continue
            records.append(json.loads(line))
    return records


def load_answers(path_to_answers: Path) -> Any:
    if path_to_answers.suffix == ".csv":
        return read_csv(path_to_answers)
    if path_to_answers.suffix == ".jsonl":
        return read_jsonl(path_to_answers)
    raise ValueError(f"Unsupported answers format for {path_to_answers}")


def is_empty(directory: Path) -> bool:
    return not any(directory.iterdir())


def get_diff(actual: dict, expected: dict) -> str:
    import difflib

    actual_lines = json.dumps(actual, indent=2, sort_keys=True).splitlines()
    expected_lines = json.dumps(expected, indent=2, sort_keys=True).splitlines()
    diff = difflib.unified_diff(
        actual_lines,
        expected_lines,
        fromfile="actual",
        tofile="expected",
        lineterm="",
    )
    return "\n".join(diff)


def get_path_to_callable(fn: Callable) -> str:
    module = fn.__module__
    qualname = getattr(fn, "__qualname__", fn.__name__)
    return f"{module}:{qualname}"
