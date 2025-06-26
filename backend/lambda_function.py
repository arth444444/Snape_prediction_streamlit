import pandas as pd
from pymongo import MongoClient
from urllib.parse import quote_plus
from datetime import datetime, timedelta

username = 'bt22cse089'
password = 'aayush@123'
encoded_password = quote_plus(password)

connection_string = f'mongodb+srv://{username}:{encoded_password}@for-testing.ocsya6p.mongodb.net/?retryWrites=true&w=majority&appName=For-testing'

client = MongoClient(connection_string)
db = client['newdb']
collection = db['newAppCollection']

current_datetime = datetime.now()
current_datetime_utc = current_datetime - timedelta(hours=5, minutes=30)
prev_25_hours_utc= current_datetime_utc - timedelta(hours=25)

query = {
    'createdDate': {
        '$gte': prev_25_hours_utc,
        '$lte': current_datetime_utc
    }
}

# Projection to select specific fields
projection = {
    'bookingId': 1,
    'pickup.location.latitude': 1,
    'pickup.location.longitude': 1,
    'bookingDateDevice': 1,
    'createdBy.mobile': 1,
    'bookingDateDevice':1
}

# Retrieve documents and convert to a pandas DataFrame
cursor = collection.find(query, projection)
cursor_df = pd.DataFrame(list(cursor))

# daily demand by prophet. Y Hat at the particular hour to fetch the request, hour of the day with voting rights
dataset=cursor_df

import pandas as pd
dataset['date_column'] = pd.to_datetime(dataset['bookingDateDevice'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
dataset['date_column'] = dataset['date_column'].fillna(pd.to_datetime(dataset['bookingDateDevice'], format='%m/%d/%Y %H:%M', errors='coerce'))
dataset['10min_window'] = dataset['date_column'].dt.floor('10min')
deduped_data = dataset.sort_values(['user_id', 'date_column']).drop_duplicates(['user_id', '10min_window'], keep='first')

dataset=deduped_data
from haversine import haversine, Unit
# Pickup lat long extraction
dataset['pickup_latitude'] = dataset['pickup_latitude'].astype(float)
dataset['pickup_longitude'] = dataset['pickup_longitude'].astype(float)

dakshindari= (22.604061, 88.403715)
sector_5=(22.576222, 88.435053)
rabindrasadan_metro=(22.541297, 88.347389)
howrah=(22.583474, 88.342969)
airport=(22.642434, 88.439351)

def calculate_distance(coords,lat, lon):
    point_coords = (lat, lon)
    return haversine(coords, point_coords, unit=Unit.KILOMETERS)

dataset['aerial_dist_dakshindari'] = dataset.apply(
    lambda row: calculate_distance(dakshindari,row['pickup_latitude'], row['pickup_longitude']), axis=1
)
dataset['aerial_dist_sector_V'] = dataset.apply(
    lambda row: calculate_distance(sector_5,row['pickup_latitude'], row['pickup_longitude']), axis=1
)
dataset['aerial_dist_rabindrasadan_metro'] = dataset.apply(
    lambda row: calculate_distance(rabindrasadan_metro,row['pickup_latitude'], row['pickup_longitude']), axis=1
)
dataset['aerial_dist_howrah'] = dataset.apply(
    lambda row: calculate_distance(howrah,row['pickup_latitude'], row['pickup_longitude']), axis=1
)
dataset['aerial_dist_airport'] = dataset.apply(
    lambda row: calculate_distance(airport,row['pickup_latitude'], row['pickup_longitude']), axis=1
)


dataset_rabindrasadan=dataset[dataset['aerial_dist_rabindrasadan_metro']<2]
dataset_airport=dataset[dataset['aerial_dist_airport']<2]
dataset_dakshindari=dataset[dataset['aerial_dist_dakshindari']<2]
dataset_howrah=dataset[dataset['aerial_dist_howrah']<2]
dataset_sectorV=dataset[dataset['aerial_dist_sector_V']<2]

from datetime import datetime, timedelta
import pandas as pd

########## Overall############
dataset['date'] = dataset['date_column'].dt.date
dataset['hour'] = dataset['date_column'].dt.hour
hourly_demand = dataset.groupby(['date', 'hour']).size().reset_index(name='y')
hourly_demand['ds'] = hourly_demand.apply(lambda row: datetime.combine(row['date'], datetime.min.time()) + timedelta(hours=row['hour']), axis=1)
hourly_demand = hourly_demand.drop(columns=['date', 'hour'])
hourly_demand['ds'] = pd.to_datetime(hourly_demand['ds'])

all_hours = pd.date_range(start=hourly_demand['ds'].min(), end=hourly_demand['ds'].max(), freq='H')
hourly_demand = hourly_demand.set_index('ds').reindex(all_hours, fill_value=0).reset_index()
hourly_demand = hourly_demand.rename(columns={'index': 'ds'})
hourly_demand = hourly_demand.set_index('ds')


############ Airport #########
dataset_airport['date'] = dataset_airport['date_column'].dt.date
dataset_airport['hour'] = dataset_airport['date_column'].dt.hour
hourly_demand_airpot = dataset_airport.groupby(['date', 'hour']).size().reset_index(name='y')
hourly_demand_airpot['ds'] = hourly_demand_airpot.apply(lambda row: datetime.combine(row['date'], datetime.min.time()) + timedelta(hours=row['hour']), axis=1)
hourly_demand_airpot = hourly_demand_airpot.drop(columns=['date', 'hour'])
hourly_demand_airpot['ds'] = pd.to_datetime(hourly_demand_airpot['ds'])

all_hours = pd.date_range(start=hourly_demand_airpot['ds'].min(), end=hourly_demand_airpot['ds'].max(), freq='H')
hourly_demand_airpot = hourly_demand_airpot.set_index('ds').reindex(all_hours, fill_value=0).reset_index()
hourly_demand_airpot = hourly_demand_airpot.rename(columns={'index': 'ds'})
hourly_demand_airpot= hourly_demand_airpot.set_index('ds')

########### Rabindrasadan ##########
dataset_rabindrasadan['date'] = dataset_rabindrasadan['date_column'].dt.date
dataset_rabindrasadan['hour'] = dataset_rabindrasadan['date_column'].dt.hour
hourly_demand_rabindrasadan = dataset_rabindrasadan.groupby(['date', 'hour']).size().reset_index(name='y')
hourly_demand_rabindrasadan['ds'] = hourly_demand_rabindrasadan.apply(lambda row: datetime.combine(row['date'], datetime.min.time()) + timedelta(hours=row['hour']), axis=1)
hourly_demand_rabindrasadan = hourly_demand_rabindrasadan.drop(columns=['date', 'hour'])
hourly_demand_rabindrasadan['ds'] = pd.to_datetime(hourly_demand_rabindrasadan['ds'])

all_hours = pd.date_range(start=hourly_demand_rabindrasadan['ds'].min(), end=hourly_demand_rabindrasadan['ds'].max(), freq='H')
hourly_demand_rabindrasadan = hourly_demand_rabindrasadan.set_index('ds').reindex(all_hours, fill_value=0).reset_index()
hourly_demand_rabindrasadan = hourly_demand_rabindrasadan.rename(columns={'index': 'ds'})
hourly_demand_rabindrasadan = hourly_demand_rabindrasadan.set_index('ds')

############## Howrah #########
dataset_howrah['date'] = dataset_howrah['date_column'].dt.date
dataset_howrah['hour'] = dataset_howrah['date_column'].dt.hour
hourly_demand_howrah = dataset_howrah.groupby(['date', 'hour']).size().reset_index(name='y')
hourly_demand_howrah['ds'] = hourly_demand_howrah.apply(lambda row: datetime.combine(row['date'], datetime.min.time()) + timedelta(hours=row['hour']), axis=1)
hourly_demand_howrah = hourly_demand_howrah.drop(columns=['date', 'hour'])
hourly_demand_howrah['ds'] = pd.to_datetime(hourly_demand_howrah['ds'])

all_hours = pd.date_range(start=hourly_demand_howrah['ds'].min(), end=hourly_demand_howrah['ds'].max(), freq='H')
hourly_demand_howrah = hourly_demand_howrah.set_index('ds').reindex(all_hours, fill_value=0).reset_index()
hourly_demand_howrah = hourly_demand_howrah.rename(columns={'index': 'ds'})
hourly_demand_howrah = hourly_demand_howrah.set_index('ds')


########## DakshinDari ###########
dataset_dakshindari['date'] = dataset_dakshindari['date_column'].dt.date
dataset_dakshindari['hour'] = dataset_dakshindari['date_column'].dt.hour
hourly_demand_dakshinDari = dataset_dakshindari.groupby(['date', 'hour']).size().reset_index(name='y')
hourly_demand_dakshinDari['ds'] = hourly_demand_dakshinDari.apply(lambda row: datetime.combine(row['date'], datetime.min.time()) + timedelta(hours=row['hour']), axis=1)
hourly_demand_dakshinDari = hourly_demand_dakshinDari.drop(columns=['date', 'hour'])
hourly_demand_dakshinDari['ds'] = pd.to_datetime(hourly_demand_dakshinDari['ds'])

all_hours = pd.date_range(start=hourly_demand_dakshinDari['ds'].min(), end=hourly_demand_dakshinDari['ds'].max(), freq='H')
hourly_demand_dakshinDari = hourly_demand_dakshinDari.set_index('ds').reindex(all_hours, fill_value=0).reset_index()
hourly_demand_dakshinDari = hourly_demand_dakshinDari.rename(columns={'index': 'ds'})
hourly_demand_dakshinDari = hourly_demand_dakshinDari.set_index('ds')


########### Sector V ###########
dataset_sectorV['date'] = dataset_sectorV['date_column'].dt.date
dataset_sectorV['hour'] = dataset_sectorV['date_column'].dt.hour
hourly_demand_sectorV = dataset_sectorV.groupby(['date', 'hour']).size().reset_index(name='y')
hourly_demand_sectorV['ds'] = hourly_demand_sectorV.apply(lambda row: datetime.combine(row['date'], datetime.min.time()) + timedelta(hours=row['hour']), axis=1)
hourly_demand_sectorV = hourly_demand_sectorV.drop(columns=['date', 'hour'])
hourly_demand_sectorV['ds'] = pd.to_datetime(hourly_demand_sectorV['ds'])

all_hours = pd.date_range(start=hourly_demand_sectorV['ds'].min(), end=hourly_demand_sectorV['ds'].max(), freq='H')
hourly_demand_sectorV = hourly_demand_sectorV.set_index('ds').reindex(all_hours, fill_value=0).reset_index()
hourly_demand_sectorV = hourly_demand_sectorV.rename(columns={'index': 'ds'})
hourly_demand_sectorV = hourly_demand_sectorV.set_index('ds')


for lag in [1, 8, 12, 24]:
    hourly_demand[f'lag_{lag}'] = hourly_demand['y'].shift(lag)

for lag in [1, 8, 12, 24]:
    hourly_demand_airpot[f'lag_{lag}'] = hourly_demand_airpot['y'].shift(lag)

for lag in [1, 8, 12, 24]:
    hourly_demand_dakshinDari[f'lag_{lag}'] = hourly_demand_dakshinDari['y'].shift(lag)

for lag in [1, 8, 12, 24]:
    hourly_demand_howrah[f'lag_{lag}'] = hourly_demand_howrah['y'].shift(lag)

for lag in [1, 8, 12, 24]:
    hourly_demand_rabindrasadan[f'lag_{lag}'] = hourly_demand_rabindrasadan['y'].shift(lag)

for lag in [1, 8, 12, 24]:
    hourly_demand_sectorV[f'lag_{lag}'] = hourly_demand_sectorV['y'].shift(lag)

hourly_demand= hourly_demand.tail(1)
hourly_demand_airpot= hourly_demand_airpot.tail(1)
hourly_demand_dakshinDari= hourly_demand_dakshinDari.tail(1)
hourly_demand_howrah= hourly_demand_howrah.tail(1)
hourly_demand_rabindrasadan= hourly_demand_rabindrasadan.tail(1)
hourly_demand_sectorV= hourly_demand_sectorV.tail(1)

import requests

API_KEY = "24b3227970223a36294433a167dc358b"
BASE_URL = "https://www.weatherunion.com/gw/weather/external/v0"

def get_locality_weather_data(locality_id):
    url = f"{BASE_URL}/get_locality_weather_data"
    headers = {
        "Content-Type": "application/json",
        "x-zomato-api-key": API_KEY
    }
    params = {
        "locality_id": locality_id
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data

kolkata='ZWL005429'
howrah='ZWL002488'
sectorV='ZWL002931'
airport='ZWL005435'
rabindrasadan='ZWL005244'
dakshindari='ZWL001499'

locality_weather_data = get_locality_weather_data(kolkata)

hourly_demand['temperature'] = locality_weather_data['locality_weather_data']['temperature']
hourly_demand['rain_intensity'] = locality_weather_data['locality_weather_data']['rain_intensity']
hourly_demand['rain_accumulation'] = locality_weather_data['locality_weather_data']['rain_accumulation']


locality_weather_data= get_locality_weather_data(rabindrasadan)
hourly_demand_rabindrasadan['temperature'] = locality_weather_data['locality_weather_data']['temperature']
hourly_demand_rabindrasadan['rain_intensity'] = locality_weather_data['locality_weather_data']['rain_intensity']
hourly_demand_rabindrasadan['rain_accumulation'] = locality_weather_data['locality_weather_data']['rain_accumulation']

locality_weather_data= get_locality_weather_data(dakshindari)
hourly_demand_dakshinDari['temperature'] = locality_weather_data['locality_weather_data']['temperature']
hourly_demand_dakshinDari['rain_intensity'] = locality_weather_data['locality_weather_data']['rain_intensity']
hourly_demand_dakshinDari['rain_accumulation'] = locality_weather_data['locality_weather_data']['rain_accumulation']

locality_weather_data= get_locality_weather_data(airport)
hourly_demand_airpot['temperature'] = locality_weather_data['locality_weather_data']['temperature']
hourly_demand_airpot['rain_intensity'] = locality_weather_data['locality_weather_data']['rain_intensity']
hourly_demand_airpot['rain_accumulation'] = locality_weather_data['locality_weather_data']['rain_accumulation']

locality_weather_data= get_locality_weather_data(howrah)
hourly_demand_howrah['temperature'] = locality_weather_data['locality_weather_data']['temperature']
hourly_demand_howrah['rain_intensity'] = locality_weather_data['locality_weather_data']['rain_intensity']
hourly_demand_howrah['rain_accumulation'] = locality_weather_data['locality_weather_data']['rain_accumulation']

locality_weather_data= get_locality_weather_data(sectorV)
hourly_demand_sectorV['temperature'] = locality_weather_data['locality_weather_data']['temperature']
hourly_demand_sectorV['rain_intensity'] = locality_weather_data['locality_weather_data']['rain_intensity']
hourly_demand_sectorV['rain_accumulation'] = locality_weather_data['locality_weather_data']['rain_accumulation']


import joblib
from tensorflow.keras.models import load_model
'''
def predict_demand_for_zone(zone, hourly_demand):
    # Load the LSTM model
    model = load_model(f'/Scales and Models/lstm_{zone}.h5')
    scaler_X = joblib.load(f'/Scales and Models/scaler_x_{zone}.pkl')
    scaler_y = joblib.load(f'/Scales and Models/scaler_y_{zone}.pkl')

    new_sample = hourly_demand.values
    new_sample = new_sample.reshape(1, -1)

    new_sample_scaled = scaler_X.transform(new_sample)

    new_sample_reshaped = new_sample_scaled.reshape((new_sample_scaled.shape[0], 1, new_sample_scaled.shape[1]))

    y_pred_scaled = model.predict(new_sample_reshaped)
    y_pred = scaler_y.inverse_transform(y_pred_scaled)

    print(f"Predicted value of y for {zone}:", y_pred)

# Example usage:
zones = ['airport', 'dakshindari', 'sectorV', 'victoria', 'howrah','kolkata_city']
for zone in zones:
    predict_demand_for_zone(zone, hourly_demand)
    
def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
'''
import json

def predict_demand_for_zone(zone, hourly_demand):
    # Load the LSTM model
    model = load_model(f'/Scales and Models/lstm_{zone}.h5')
    scaler_X = joblib.load(f'/Scales and Models/scaler_x_{zone}.pkl')
    scaler_y = joblib.load(f'/Scales and Models/scaler_y_{zone}.pkl')

    new_sample = hourly_demand.values
    new_sample = new_sample.reshape(1, -1)

    new_sample_scaled = scaler_X.transform(new_sample)

    new_sample_reshaped = new_sample_scaled.reshape((new_sample_scaled.shape[0], 1, new_sample_scaled.shape[1]))

    y_pred_scaled = model.predict(new_sample_reshaped)
    y_pred = scaler_y.inverse_transform(y_pred_scaled)

    return {zone: y_pred.tolist()}  # Convert NumPy array to list for JSON serialization

def lambda_handler(event, context):
    predictions = {}
    zones = ['airport', 'dakshindari', 'sectorV', 'victoria', 'howrah', 'kolkata_city']
    for zone in zones:
        predictions.update(predict_demand_for_zone(zone, hourly_demand))
    
    return {
        'statusCode': 200,
        'body': json.dumps(predictions)
    }
