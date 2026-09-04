import pandas as pd
from fastapi import FastAPI

from taxifare.registry import load_model
from taxifare.predict import predict as predict_fare

app = FastAPI()
model = load_model()


@app.get("/")
def root():
    return {"greeting": "Hello"}


@app.get("/predict")
def predict(
    pickup_datetime: str,
    pickup_longitude: float,
    pickup_latitude: float,
    dropoff_longitude: float,
    dropoff_latitude: float,
    passenger_count: int,
):
    X = pd.DataFrame([{
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count,
    }])
    X["pickup_datetime"] = pd.to_datetime(X["pickup_datetime"], utc=True)
    prediction = predict_fare(model, X)
    return {"fare": float(prediction[0])}
