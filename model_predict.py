import joblib
import os
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from weatherunion_script import *

# Folder where models are stored (relative path)
MODEL_DIR = "models"

def predict_demand_for_zone(zone, hourly_demand):
    # Construct paths to model and scalers
    model_path = os.path.join(MODEL_DIR, f"lstm_{zone}.h5")
    scaler_x_path = os.path.join(MODEL_DIR, f"scaler_x_{zone}.pkl")
    scaler_y_path = os.path.join(MODEL_DIR, f"scaler_y_{zone}.pkl")

    # Load model and scalers
    model = load_model(model_path)
    scaler_X = joblib.load(scaler_x_path)
    scaler_y = joblib.load(scaler_y_path)

    # Prepare input
    hourly_demand_zone = hourly_demand[zone]
    new_sample = hourly_demand_zone.values.reshape(1, -1)
    new_sample_scaled = scaler_X.transform(new_sample)
    new_sample_reshaped = new_sample_scaled.reshape((new_sample_scaled.shape[0], 1, new_sample_scaled.shape[1]))

    # Predict
    y_pred_scaled = model.predict(new_sample_reshaped)
    y_pred = scaler_y.inverse_transform(y_pred_scaled)

    return max(0, y_pred.flatten()[0])

# Sample zones
zones = ['airport', 'laketown', 'sectorV', 'victoria', 'howrah', 'kolkata_city']

# Make sure these are defined earlier in your pipeline
hourly_demand = {
    'airport': hourly_demand_airpot,
    'laketown': hourly_demand_laketown,
    'sectorV': hourly_demand_sectorV,
    'victoria': hourly_demand_rabindrasadan,
    'howrah': hourly_demand_howrah,
    'kolkata_city': hourly_demand  # the city-wide value
}

# Prediction dictionary
predicted_values = {zone: predict_demand_for_zone(zone, hourly_demand) for zone in zones}
