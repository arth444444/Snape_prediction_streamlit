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

        new_sample = hourly_demand_zone.values
        new_sample = new_sample.reshape(1, -1)

        new_sample_scaled = scaler_X.transform(new_sample)
        new_sample_reshaped = new_sample_scaled.reshape((new_sample_scaled.shape[0], 1, new_sample_scaled.shape[1]))

        y_pred_scaled = model.predict(new_sample_reshaped, verbose=0)
        y_pred = scaler_y.inverse_transform(y_pred_scaled)

        predicted_value = y_pred.flatten()[0]
        final_value = max(0, predicted_value)
        
        print(f"  ✅ {zone}: {final_value:.1f} rides (raw)")
        return final_value
        
    except Exception as e:
        print(f"  ❌ Error predicting {zone}: {e}")
        return 0

def correct_zone_predictions(raw_predictions):
    """
    Correct zone predictions to ensure they don't exceed city total
    """
    print("\n🔧 APPLYING LOGIC CORRECTION...")
    
    # Separate city total from zones
    city_total = raw_predictions.get('kolkata_city', 0)
    zone_predictions = {k: v for k, v in raw_predictions.items() if k != 'kolkata_city'}
    
    # Calculate current zone sum
    zone_sum = sum(zone_predictions.values())
    
    print(f"City Total: {city_total:.1f}")
    print(f"Zone Sum (raw): {zone_sum:.1f}")
    
    if zone_sum > city_total:
        # Apply proportional scaling to zones
        scaling_factor = (city_total * 0.8) / zone_sum  # Use 80% of city total for zones
        print(f"Scaling factor: {scaling_factor:.3f}")
        
        corrected_predictions = {}
        for zone, prediction in zone_predictions.items():
            corrected_value = prediction * scaling_factor
            corrected_predictions[zone] = corrected_value
            print(f"  {zone}: {prediction:.1f} → {corrected_value:.1f}")
        
        # Keep city total as is
        corrected_predictions['kolkata_city'] = city_total
        
        # Verify correction
        new_zone_sum = sum([v for k, v in corrected_predictions.items() if k != 'kolkata_city'])
        print(f"New zone sum: {new_zone_sum:.1f}")
        print(f"Remaining for other areas: {city_total - new_zone_sum:.1f}")
        
        return corrected_predictions
    else:
        print("✅ No correction needed - zones sum is reasonable")
        return raw_predictions

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

# Get raw predictions
raw_predicted_values = {}
for zone in zones:
    raw_predicted_values[zone] = predict_demand_for_zone(zone, hourly_demand)

print("\n📊 RAW PREDICTIONS:")
print("="*50)
for zone, prediction in raw_predicted_values.items():
    print(f"{zone:15s}: {prediction:6.1f} rides")

# Apply logic correction
predicted_values = correct_zone_predictions(raw_predicted_values)

print("\n✅ CORRECTED PREDICTIONS:")
print("="*50)
for zone, prediction in predicted_values.items():
    print(f"{zone:15s}: {prediction:6.1f} rides")

# Final logic check
print("\n🔍 FINAL VALIDATION:")
zone_predictions = {k: v for k, v in predicted_values.items() if k != 'kolkata_city'}
total_zone_demand = sum(zone_predictions.values())
city_demand = predicted_values.get('kolkata_city', 0)

print(f"Sum of 5 zones: {total_zone_demand:.1f}")
print(f"Total city:     {city_demand:.1f}")
print(f"Difference:     {city_demand - total_zone_demand:.1f} (other areas)")

if total_zone_demand <= city_demand:
    print("✅ Logic check passed!")
else:
    print("⚠️  Still have issues - manual adjustment needed")

print(f"\nFinal predicted_values: {predicted_values}")