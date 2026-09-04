import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline


def predict(model: Pipeline, X: pd.DataFrame) -> np.ndarray:
    """Predict taxi fares for one or more rides.

    Args:
        model: A fitted pipeline, as returned by load_model().
        X: Raw ride features with the same columns the model was trained on
            (pickup_datetime, pickup_longitude, pickup_latitude,
            dropoff_longitude, dropoff_latitude, passenger_count).

    Returns:
        Predicted fares in USD, one per row of X.
    """
    return model.predict(X)
