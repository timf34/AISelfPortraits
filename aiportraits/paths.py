from pathlib import Path

RESULTS_ROOT = Path(__file__).resolve().parent.parent / "results"
SEEDS_ROOT = Path(__file__).resolve().parent.parent / "seeds"


def safe_model_name(slug: str) -> str:
    return slug.replace("/", "__")


def experiment_dir(model: str, prompt: str, language: str, run: int, root: Path = RESULTS_ROOT) -> Path:
    return root / safe_model_name(model) / prompt / language / f"run{run}"
