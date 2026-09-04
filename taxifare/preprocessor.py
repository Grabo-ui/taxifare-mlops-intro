"""Stateless preprocessing functions used inside the taxifare pipeline.

These live in a module (rather than in the notebook) so that a pipeline saved
with joblib can be loaded again from any process, including the API.
"""

import math

import numpy as np
import pandas as pd

LONLAT_FEATURES = [
    "pickup_latitude",
    "pickup_longitude",
    "dropoff_latitude",
    "dropoff_longitude",
]

TIMEDELTA_MIN = 0
TIMEDELTA_MAX = 2190


def manhattan_distance_vectorized(
    df: pd.DataFrame,
    start_lat: str,
    start_lon: str,
    end_lat: str,
    end_lon: str,
) -> pd.Series:
    """Compute the Manhattan (L1) distance in km between two points on earth.

    Args:
        df: DataFrame holding the coordinate columns.
        start_lat: Name of the pickup latitude column.
        start_lon: Name of the pickup longitude column.
        end_lat: Name of the dropoff latitude column.
        end_lon: Name of the dropoff longitude column.

    Returns:
        Distance in kilometers, one value per row.
    """
    earth_radius = 6371

    lat_1_rad, lon_1_rad = np.radians(df[start_lat]), np.radians(df[start_lon])
    lat_2_rad, lon_2_rad = np.radians(df[end_lat]), np.radians(df[end_lon])

    dlon_rad = lon_2_rad - lon_1_rad
    dlat_rad = lat_2_rad - lat_1_rad

    manhattan_rad = np.abs(dlon_rad) + np.abs(dlat_rad)

    return manhattan_rad * earth_radius


def scale_passenger(p):
    """Scale passenger count to roughly 0-1 using fixed bounds (0 to 8).

    Args:
        p: Passenger counts.

    Returns:
        Scaled passenger counts.
    """
    p_min = 0.0
    p_max = 8.0
    return (p - p_min) / (p_max - p_min)


def transform_time_features(X: pd.DataFrame) -> pd.DataFrame:
    """Turn pickup_datetime into cyclical and trend features.

    Args:
        X: DataFrame with a timezone-aware "pickup_datetime" column.

    Returns:
        DataFrame with hour_sin, hour_cos, day_of_week, month_sin, month_cos
        and timedelta (days since 2009-01-01).
    """
    timedelta = (
        X["pickup_datetime"] - pd.Timestamp("2009-01-01T00:00:00", tz="UTC")
    ) / pd.Timedelta(1, "D")

    pickup_dt = X["pickup_datetime"].dt.tz_convert("America/New_York").dt

    dow = pickup_dt.weekday
    hour = pickup_dt.hour
    month = pickup_dt.month

    hour_sin = np.sin(2 * math.pi / 24 * hour)
    hour_cos = np.cos(2 * math.pi / 24 * hour)

    month_sin = np.sin(2 * math.pi / 24 * month)
    month_cos = np.cos(2 * math.pi / 24 * month)

    return pd.DataFrame(
        {
            "hour_sin": hour_sin,
            "hour_cos": hour_cos,
            "day_of_week": dow,
            "month_sin": month_sin,
            "month_cos": month_cos,
            "timedelta": timedelta,
        }
    )


def scale_timedelta(timedelta):
    """Scale days-since-2009 to roughly 0-1 using fixed bounds.

    Args:
        timedelta: Days since 2009-01-01.

    Returns:
        Scaled values. May exceed 1.0 for dates beyond the training range.
    """
    return (timedelta - TIMEDELTA_MIN) / (TIMEDELTA_MAX - TIMEDELTA_MIN)


def manhattan_distance_for_pipe(df: pd.DataFrame) -> pd.DataFrame:
    """Wrap manhattan_distance_vectorized so it fits in a FunctionTransformer.

    Args:
        df: DataFrame with the four lon/lat columns.

    Returns:
        Single-column DataFrame named "distance".
    """
    distance = manhattan_distance_vectorized(df, *LONLAT_FEATURES)
    return pd.DataFrame({"distance": distance})


def scale_distance(dist):
    """Scale ride distance to roughly 0-1 using fixed bounds (0 to 100 km).

    Args:
        dist: Distances in kilometers.

    Returns:
        Scaled distances.
    """
    dist_min = 0
    dist_max = 100
    return (dist - dist_min) / (dist_max - dist_min)
