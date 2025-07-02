import requests
import pandas as pd
import streamlit as st
from laggeddata import *

# Get API key from secrets
try:
    API_KEY = st.secrets["WEATHER_API"]["OPENWEATHERMAP_API_KEY"]
    print("✅ Weather API key loaded from secrets")
except KeyError:
    API_KEY =  "19e278de393d960528df5972d5882d46" # Replace with your actual API key for testing
    print("⚠️ Weather API key not found in secrets, using fallback")

# OpenWeatherMap API Configuration
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Coordinates for each location (lat, lon)
locations = {
    'kolkata': {'lat': 22.5726, 'lon': 88.3639, 'name': 'Kolkata'},
    'howrah': {'lat': 22.5958, 'lon': 88.2636, 'name': 'Howrah'},
    'sectorV': {'lat': 22.5761, 'lon': 88.4355, 'name': 'Sector V'},
    'airport': {'lat': 22.6542, 'lon': 88.4467, 'name': 'Airport'},
    'rabindrasadan': {'lat': 22.5412, 'lon': 88.3476, 'name': 'Rabindra Sadan'},
    'laketown': {'lat': 22.6041, 'lon': 88.4037, 'name': 'Lake Town'}
}

def get_weather_data(lat, lon, location_name):
    """
    Get weather data from OpenWeatherMap API
    """
    try:
        params = {
            'lat': lat,
            'lon': lon,
            'appid': API_KEY,
            'units': 'metric'  # For Celsius temperature
        }
        
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extract relevant weather information
        weather_info = {
            'temperature': data['main']['temp'],
            'rain_intensity': 0.0,  # Default value
            'rain_accumulation': 0.0  # Default value
        }
        
        # Check for rain data
        if 'rain' in data:
            # Rain volume for last 1 hour in mm
            weather_info['rain_intensity'] = data['rain'].get('1h', 0.0)
            weather_info['rain_accumulation'] = data['rain'].get('1h', 0.0)
        
        print(f"✅ Weather data fetched for {location_name}: {weather_info}")
        return weather_info
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching weather data for {location_name}: {e}")
        return None
    except KeyError as e:
        print(f"❌ Unexpected API response format for {location_name}: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error for {location_name}: {e}")
        return None

def add_weather_data_to_dataframe(df, lat, lon, location_name):
    """
    Add weather data to a dataframe with fallback values
    """
    try:
        weather_data = get_weather_data(lat, lon, location_name)
        
        if weather_data:
            df['temperature'] = weather_data['temperature']
            df['rain_intensity'] = weather_data['rain_intensity']
            df['rain_accumulation'] = weather_data['rain_accumulation']
        else:
            # Fallback values if API fails
            df['temperature'] = 25.0
            df['rain_intensity'] = 0.0
            df['rain_accumulation'] = 0.0
            print(f"⚠️ Using fallback weather data for {location_name}")
            
    except Exception as e:
        print(f"❌ Error adding weather data to {location_name}: {e}")
        # Fallback values
        df['temperature'] = 25.0
        df['rain_intensity'] = 0.0
        df['rain_accumulation'] = 0.0

# Add weather data to all dataframes
print("🌤️ Fetching weather data for all locations...")

add_weather_data_to_dataframe(
    hourly_demand, 
    locations['kolkata']['lat'], 
    locations['kolkata']['lon'], 
    locations['kolkata']['name']
)

add_weather_data_to_dataframe(
    hourly_demand_rabindrasadan, 
    locations['rabindrasadan']['lat'], 
    locations['rabindrasadan']['lon'], 
    locations['rabindrasadan']['name']
)

add_weather_data_to_dataframe(
    hourly_demand_laketown, 
    locations['laketown']['lat'], 
    locations['laketown']['lon'], 
    locations['laketown']['name']
)

add_weather_data_to_dataframe(
    hourly_demand_airpot, 
    locations['airport']['lat'], 
    locations['airport']['lon'], 
    locations['airport']['name']
)

add_weather_data_to_dataframe(
    hourly_demand_howrah, 
    locations['howrah']['lat'], 
    locations['howrah']['lon'], 
    locations['howrah']['name']
)

add_weather_data_to_dataframe(
    hourly_demand_sectorV, 
    locations['sectorV']['lat'], 
    locations['sectorV']['lon'], 
    locations['sectorV']['name']
)

# Select relevant columns with error handling
def safe_column_selection(df, zone_name):
    try:
        required_cols = ['y', 'rain_intensity', 'rain_accumulation', 'temperature', 'lag_1', 'lag_8', 'lag_12', 'lag_24']
        available_cols = [col for col in required_cols if col in df.columns]
        
        if len(available_cols) < len(required_cols):
            missing_cols = set(required_cols) - set(available_cols)
            print(f"⚠️ Missing columns in {zone_name}: {missing_cols}")
        
        return df[available_cols]
    except Exception as e:
        print(f"❌ Error selecting columns for {zone_name}: {e}")
        return df

# Apply column selection to all dataframes
hourly_demand = safe_column_selection(hourly_demand, "city")
hourly_demand_airpot = safe_column_selection(hourly_demand_airpot, "airport")
hourly_demand_laketown = safe_column_selection(hourly_demand_laketown, "laketown")
hourly_demand_howrah = safe_column_selection(hourly_demand_howrah, "howrah")
hourly_demand_rabindrasadan = safe_column_selection(hourly_demand_rabindrasadan, "rabindrasadan")
hourly_demand_sectorV = safe_column_selection(hourly_demand_sectorV, "sectorV")

print("🌤️ Weather data processing completed!")
print("city", hourly_demand.shape)
print("laketown", hourly_demand_laketown.shape)
print("airport", hourly_demand_airpot.shape)
print('howrah', hourly_demand_howrah.shape)
print('rabindrasadan', hourly_demand_rabindrasadan.shape)
print('sector5', hourly_demand_sectorV.shape)