from weatherunion_script import *
import joblib
from tensorflow.keras.models import load_model
import warnings

# Suppress the sklearn version warning
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')

def predict_demand_for_zone(zone, hourly_demand):
    try:
        print(f"🔄 Predicting for {zone}...")
        
        # Load the LSTM model (keeping your original paths)
        model = load_model(f'./models/lstm_{zone}.h5')
        scaler_X = joblib.load(f'./models/scaler_x_{zone}.pkl')
        scaler_y = joblib.load(f'./models/scaler_y_{zone}.pkl')

        # Extract hourly demand for the given zone
        hourly_demand_zone = hourly_demand[zone]
        
        # Debug: Print input data
        print(f"  Input data shape: {hourly_demand_zone.shape}")
        print(f"  Input values: {hourly_demand_zone.values.flatten()}")

        new_sample = hourly_demand_zone.values
        new_sample = new_sample.reshape(1, -1)

        new_sample_scaled = scaler_X.transform(new_sample)
        new_sample_reshaped = new_sample_scaled.reshape((new_sample_scaled.shape[0], 1, new_sample_scaled.shape[1]))

        y_pred_scaled = model.predict(new_sample_reshaped, verbose=0)
        y_pred = scaler_y.inverse_transform(y_pred_scaled)

        predicted_value = y_pred.flatten()[0]
        final_value = max(0, predicted_value)
        
        print(f"  ✅ {zone}: {final_value:.1f} rides")
        return final_value
        
    except Exception as e:
        print(f"  ❌ Error predicting {zone}: {e}")
        return 0

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

print("🚖 Starting Kolkata Demand Predictions...")
print("="*50)

# Dictionary to store results
predicted_values = {}

# Predict demand for each zone and store in dictionary
for zone in zones:
    predicted_values[zone] = predict_demand_for_zone(zone, hourly_demand)

print("\n📊 FINAL PREDICTIONS:")
print("="*50)
for zone, prediction in predicted_values.items():
    print(f"{zone:15s}: {prediction:6.1f} rides")

# Logic check
print("\n🔍 LOGIC VALIDATION:")
zone_predictions = {k: v for k, v in predicted_values.items() if k != 'kolkata_city'}
total_zone_demand = sum(zone_predictions.values())
city_demand = predicted_values.get('kolkata_city', 0)

print(f"Sum of 5 zones: {total_zone_demand:.1f}")
print(f"Total city:     {city_demand:.1f}")
print(f"Difference:     {total_zone_demand - city_demand:.1f}")

if total_zone_demand > city_demand:
    print("⚠️  WARNING: Zone sum exceeds city total!")
    print("   This suggests different scaling factors between models")
else:
    print("✅ Logic check passed!")

print("\nPredicted values:", predicted_values)