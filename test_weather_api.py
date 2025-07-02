import requests

# Replace with your actual API key
API_KEY = "19e278de393d960528df5972d5882d46"
lat, lon = 22.5726, 88.3639  # Kolkata

url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

response = requests.get(url)
print(response.json())