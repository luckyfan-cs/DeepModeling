from pathlib import Path

from mathmodelingbench.competitions.dabench-0-mean-fare.prepare import prepare


if __name__ == "__main__":
    base_dir = Path(__file__).parent
    raw = base_dir / "raw"
    public = base_dir / "prepared" / "public"
    private = base_dir / "prepared" / "private"
    prepare(raw=raw, public=public, private=private)
