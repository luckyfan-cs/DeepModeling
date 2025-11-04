from pathlib import Path
import importlib.util
import types


def _load_prepare_fn() -> types.ModuleType:
    repo_root = Path(__file__).resolve().parents[5]
    module_path = repo_root / "benchmarks" / "mathmodelingbench" / "competitions" / "dabench-0" / "prepare.py"
    spec = importlib.util.spec_from_file_location("dabench_0_prepare_module", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load prepare module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


prepare = _load_prepare_fn().prepare


if __name__ == "__main__":
    base_dir = Path(__file__).parent
    raw = base_dir / "raw"
    public = base_dir / "prepared" / "public"
    private = base_dir / "prepared" / "private"
    prepare(raw=raw, public=public, private=private)
