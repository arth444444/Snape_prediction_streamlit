import requests
from backend.laggeddata import *

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
laketown='ZWL001499'

locality_weather_data = get_locality_weather_data(kolkata)

hourly_demand['temperature'] = locality_weather_data['locality_weather_data']['temperature']
hourly_demand['rain_intensity'] = locality_weather_data['locality_weather_data']['rain_intensity']
hourly_demand['rain_accumulation'] = locality_weather_data['locality_weather_data']['rain_accumulation']


locality_weather_data= get_locality_weather_data(rabindrasadan)
hourly_demand_rabindrasadan['temperature'] = locality_weather_data['locality_weather_data']['temperature']
hourly_demand_rabindrasadan['rain_intensity'] = locality_weather_data['locality_weather_data']['rain_intensity']
hourly_demand_rabindrasadan['rain_accumulation'] = locality_weather_data['locality_weather_data']['rain_accumulation']

locality_weather_data= get_locality_weather_data(laketown)
hourly_demand_laketown['temperature'] = locality_weather_data['locality_weather_data']['temperature']
hourly_demand_laketown['rain_intensity'] = locality_weather_data['locality_weather_data']['rain_intensity']
hourly_demand_laketown['rain_accumulation'] = locality_weather_data['locality_weather_data']['rain_accumulation']

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


hourly_demand=hourly_demand[['y'	,'rain_intensity'	,'rain_accumulation'	,'temperature'	,'lag_1',	'lag_8',	'lag_12',	'lag_24']]
hourly_demand_airpot=hourly_demand_airpot[['y'	,'rain_intensity'	,'rain_accumulation'	,'temperature'	,'lag_1',	'lag_8',	'lag_12',	'lag_24']]
hourly_demand_laketown=hourly_demand_laketown[['y'	,'rain_intensity'	,'rain_accumulation'	,'temperature'	,'lag_1',	'lag_8',	'lag_12',	'lag_24']]
hourly_demand_howrah=hourly_demand_howrah[['y'	,'rain_intensity'	,'rain_accumulation'	,'temperature'	,'lag_1',	'lag_8',	'lag_12',	'lag_24']]
hourly_demand_rabindrasadan=hourly_demand_rabindrasadan[['y'	,'rain_intensity'	,'rain_accumulation'	,'temperature'	,'lag_1',	'lag_8',	'lag_12',	'lag_24']]
hourly_demand_sectorV=hourly_demand_sectorV[['y'	,'rain_intensity'	,'rain_accumulation'	,'temperature'	,'lag_1',	'lag_8',	'lag_12',	'lag_24']]


print("city",hourly_demand)
print("laketown",hourly_demand_laketown)
print("airpor",hourly_demand_airpot)
print('howrah',hourly_demand_howrah)
print('rabindrasadan',hourly_demand_rabindrasadan)
print('sector5',hourly_demand_sectorV)