from weatherunion_script import *
import joblib
import os
from tensorflow.keras.models import load_model

# Function to predict demand for a given zone
def predict_demand_for_zone(zone, hourly_demand):
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct paths to model files using relative paths
    model_path = os.path.join(script_dir, 'models', f'lstm_{zone}.h5')
    scaler_x_path = os.path.join(script_dir, 'models', f'scaler_x_{zone}.pkl')
    scaler_y_path = os.path.join(script_dir, 'models', f'scaler_y_{zone}.pkl')
    
    # Check if files exist
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    if not os.path.exists(scaler_x_path):
        raise FileNotFoundError(f"Scaler X file not found: {scaler_x_path}")
    if not os.path.exists(scaler_y_path):
        raise FileNotFoundError(f"Scaler Y file not found: {scaler_y_path}")
    
    # Load the LSTM model and scalers
    try:
        model = load_model(model_path, compile=False)
        scaler_X = joblib.load(scaler_x_path)
        scaler_y = joblib.load(scaler_y_path)
        print(f"Successfully loaded model and scalers for {zone}")
    except Exception as e:
        print(f"Error loading model or scalers for zone {zone}: {e}")
        raise
    
    # Extract hourly demand for the given zone
    hourly_demand_zone = hourly_demand[zone]
    print(f"Hourly demand for {zone}: {hourly_demand_zone}")
    print(f"Hourly demand shape: {hourly_demand_zone.shape}")
    print(f"Hourly demand values: {hourly_demand_zone.values}")
    
    new_sample = hourly_demand_zone.values
    new_sample = new_sample.reshape(1, -1)
    print(f"New sample shape after reshape: {new_sample.shape}")
    print(f"New sample values: {new_sample}")
    
    new_sample_scaled = scaler_X.transform(new_sample)
    print(f"Scaled sample: {new_sample_scaled}")
    print(f"Scaled sample shape: {new_sample_scaled.shape}")
    
    new_sample_reshaped = new_sample_scaled.reshape((new_sample_scaled.shape[0], 1, new_sample_scaled.shape[1]))
    print(f"Reshaped sample for LSTM: {new_sample_reshaped.shape}")
    
    y_pred_scaled = model.predict(new_sample_reshaped)
    print(f"Raw prediction (scaled): {y_pred_scaled}")
    
    y_pred = scaler_y.inverse_transform(y_pred_scaled)
    print(f"Prediction after inverse transform: {y_pred}")
    
    predicted_value = y_pred.flatten()[0]
    print(f"Final predicted value for {zone}: {predicted_value}")
    
    # REMOVE the max(0, predicted_value) to see actual predictions
    return predicted_value  # Return actual value, not max(0, value)


# Example usage:
zones = ['airport', 'laketown', 'sectorV', 'victoria', 'howrah', 'kolkata_city']

hourly_demand = {
    'airport': hourly_demand_airpot,
    'laketown': hourly_demand_laketown,
    'sectorV': hourly_demand_sectorV,
    'victoria': hourly_demand_rabindrasadan,
    'howrah': hourly_demand_howrah,
    'kolkata_city': hourly_demand
}

# Dictionary to store results
predicted_values = {}

# Test with just one zone first
test_zone = 'airport'  # Start with one zone
try:
    print(f"\n=== Testing zone: {test_zone} ===")
    predicted_values[test_zone] = predict_demand_for_zone(test_zone, hourly_demand)
    print(f"Successfully predicted for {test_zone}: {predicted_values[test_zone]}")
except Exception as e:
    print(f"Error predicting for zone {test_zone}: {e}")
    import traceback
    traceback.print_exc()

# Once the above works, uncomment the loop below:
"""
# Predict demand for each zone and store in dictionary
for zone in zones:
    try:
        print(f"\n=== Processing zone: {zone} ===")
        predicted_values[zone] = predict_demand_for_zone(zone, hourly_demand)
        print(f"Successfully predicted for {zone}: {predicted_values[zone]}")
    except Exception as e:
        print(f"Error predicting for zone {zone}: {e}")
        predicted_values[zone] = 0  # Default value

print("Final predicted values:", predicted_values)
"""