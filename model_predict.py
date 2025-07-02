from weatherunion_script import *
import joblib
from tensorflow.keras.models import load_model

# Function to predict demand for a given zone
def predict_demand_for_zone(zone, hourly_demand):
    # Load the LSTM model
    # model = load_model(f'/Users/arthparashar/Downloads/Snape/City Heatmap/model/Scales and Models/lstm_{zone}.h5')
    # scaler_X = joblib.load(f'/Users/arthparashar/Downloads/Snape/City Heatmap/model/Scales and Models/scaler_x_{zone}.pkl')
    # scaler_y = joblib.load(f'/Users/arthparashar/Downloads/Snape/City Heatmap/model/Scales and Models/scaler_y_{zone}.pkl')

    model = load_model(f'./models/lstm_{zone}.h5')

    scaler_X = joblib.load(f'./models/scaler_x_{zone}.pkl')
    scaler_y = joblib.load(f'./models/scaler_y_{zone}.pkl')



    # Extract hourly demand for the given zone
    hourly_demand_zone = hourly_demand[zone]

    new_sample = hourly_demand_zone.values
    new_sample = new_sample.reshape(1, -1)

    new_sample_scaled = scaler_X.transform(new_sample)

    new_sample_reshaped = new_sample_scaled.reshape((new_sample_scaled.shape[0], 1, new_sample_scaled.shape[1]))

    y_pred_scaled = model.predict(new_sample_reshaped)
    y_pred = scaler_y.inverse_transform(y_pred_scaled)

    predicted_value = y_pred.flatten()[0]  # Return the predicted value as a scalar
    return max(0, predicted_value)  # Return 0 if prediction is negative
    

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

# Predict demand for each zone and store in dictionary
for zone in zones:
    predicted_values[zone] = predict_demand_for_zone(zone, hourly_demand)

print("Predicted values:", predicted_values)

# Now you can pass `predicted_values` to another script or use it as needed.

'''from weatherunion_script import *
import joblib
from tensorflow.keras.models import load_model

model = load_model(f'/Users/arthparashar/Downloads/Snape/City Heatmap/modelScales and Models/lstm_kolkata_city.h5')
scaler_X = joblib.load(f'/Users/arthparashar/Downloads/Snape/City Heatmap/model/Scales and Models/scaler_x_kolkata_city.pkl')
scaler_y = joblib.load(f'/Users/arthparashar/Downloads/Snape/City Heatmap/model/Scales and Models/scaler_y_kolkata_city.pkl')
print("model loaded")

new_sample = hourly_demand.values
new_sample = new_sample.reshape(1, -1)

new_sample_scaled = scaler_X.transform(new_sample)

new_sample_reshaped = new_sample_scaled.reshape((new_sample_scaled.shape[0], 1, new_sample_scaled.shape[1]))

y_pred_scaled = model.predict(new_sample_reshaped)
y_pred = scaler_y.inverse_transform(y_pred_scaled)
print(f"Predicted value of y for city:", y_pred)


def predict_demand_for_zone(zone, hourly_demand):
    # Load the LSTM model
    model = load_model(f'/Users/arthparashar/Downloads/Snape/City Heatmap/model/Scales and Models/lstm_{zone}.h5')
    scaler_X = joblib.load(f'/Users/arthparashar/Downloads/Snape/City Heatmap/model/Scales and Models/scaler_x_{zone}.pkl')
    scaler_y = joblib.load(f'/Users/arthparashar/Downloads/Snape/City Heatmap/model/Scales and Models/scaler_y_{zone}.pkl')

    # Extract hourly demand for the given zone
    hourly_demand_zone = hourly_demand[zone]

    new_sample = hourly_demand_zone.values
    new_sample = new_sample.reshape(1, -1)

    new_sample_scaled = scaler_X.transform(new_sample)

    new_sample_reshaped = new_sample_scaled.reshape((new_sample_scaled.shape[0], 1, new_sample_scaled.shape[1]))

    y_pred_scaled = model.predict(new_sample_reshaped)
    y_pred = scaler_y.inverse_transform(y_pred_scaled)

    print(f"Predicted value of y for {zone}:", y_pred)

# Example usage:
zones = ['airport', 'laketown', 'sectorV', 'victoria', 'howrah','kolkata_city']

hourly_demand = {
    'airport': hourly_demand_airpot,
    'laketown': hourly_demand_laketown,
    'sectorV': hourly_demand_sectorV,
    'victoria': hourly_demand_laketown,
    'howrah': hourly_demand_howrah,
    'kolkata_city': hourly_demand
}

for zone in zones:
    predict_demand_for_zone(zone, hourly_demand)

'''