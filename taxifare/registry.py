from pathlib import Path

import joblib
from sklearn.pipeline import Pipeline

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "logreg_pipeline.joblib"


def load_model(path: Path = MODEL_PATH) -> Pipeline:
    """Load the trained pipeline from disk.

    Args:
        path: Location of the .joblib file. Defaults to models/logreg_pipeline.joblib
            in the repo root.

    Returns:
        The fitted scikit-learn Pipeline, ready to call .predict() on.

    Raises:
        FileNotFoundError: If no model file exists at the given path.
    """
    if not path.exists():
        raise FileNotFoundError(
            f"No model found at {path}. Train and save the pipeline first."
        )
    return joblib.load(path)
