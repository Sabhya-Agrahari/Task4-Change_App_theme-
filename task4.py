import tkinter as tk
from datetime import datetime
from geopy.geocoders import Nominatim
import pytz
import requests

# Function to get current time in IST
def get_current_time():
    tz = pytz.timezone('Asia/Kolkata')  # IST timezone
    return datetime.now(tz)

# Function to get current city and state using IP address
def get_current_city_state():
    try:
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode('')
        if location:
            address_components = location.address.split(', ')
            if len(address_components) >= 3:
                city_state = address_components[-3:-1]  # Assuming this returns city, state
                return city_state
            else:
                return ["Unnao", "Uttar Pradesh"]  # Default to Unnao, Uttar Pradesh
        else:
            return ["Unnao", "Uttar Pradesh"]  # Default to Unnao, Uttar Pradesh
    except Exception as e:
        print(f"Error fetching city/state: {e}")
        return ["Unnao", "Uttar Pradesh"]  # Default to Unnao, Uttar Pradesh

# Function to get weather data from OpenWeatherMap API
def get_weather(lat, lon):
    api_key = 'be592c0049dfe6c1c6b7239aa6dff774'  # Replace with your actual API key
    base_url = f'https://api.openweathermap.org/data/2.5/weather?'
    url = f'{base_url}lat={lat}&lon={lon}&appid={api_key}&units=metric'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404, 500)

        data = response.json()

        temperature = data['main']['temp']
        country = data['sys']['country']
        city = data['name'] 

        return temperature, country, city

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None, None, None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None, None, None

# Function to change app theme based on daytime
def change_theme(is_daytime, app):
    if is_daytime:
        app.config(bg='white')  # Light theme
    else:
        app.config(bg='black')  # Dark theme




# Create the main Tkinter application window
app = tk.Tk()
app.title("Weather App")
app.geometry('400x300')

canvas = tk.Canvas(app, width=400, height=300)

canvas.pack()




current_address_label = tk.Label(app, text="Current Address: ", padx=10, pady=10)
canvas.create_window(200, 50, window=current_address_label)



delivery_address_label = tk.Label(app, text="Delivery Address: ", padx=10, pady=10)
canvas.create_window(200, 80, window=delivery_address_label)



# Labels for displaying weather information
temperature_label = tk.Label(app, text="Temperature", padx=10, pady=10)
canvas.create_window(200, 110, window=temperature_label)

city_label = tk.Label(app, text="City", padx=10, pady=10)
canvas.create_window(200, 140, window=city_label)

country_label = tk.Label(app, text="Country", padx=10, pady=10)
canvas.create_window(200, 170, window=country_label)



# Example of integrating with fetched data
current_time = get_current_time()
if current_time.hour >= 6 and current_time.hour < 12:
    city_state = get_current_city_state()
    if city_state:
        city, state = city_state
        print(f"Current city: {city}, State: {state}")
        tk.Label(app, text=f"City: {city}, State: {state}", padx=10, pady=10).pack()  # Display city and state
        current_address_label.config(text=f"Current Address: {city}")
        delivery_address_label.config(text=f"Delivery Address: {city}")
        change_theme(True, app)  # Light theme
    else:
        city = "Unnao"  # Default city setting
        print("Failed to fetch current city. Using default city settings.")
else:
    lat, lon = 26.5673264, 80.61981926788883  # Replace with actual logic to fetch coordinates based on time
    temperature, country, city = get_weather(lat, lon)
    if temperature is not None and country is not None and city is not None:
        print(f"Temperature: {temperature}°C, Country: {country}, City: {city}")
        tk.Label(app, text=f"Temperature: {temperature}°C, Country: {country}, City: {city}", padx=10, pady=10).pack() 
        # Display weather info
        temperature_label.config(text=f"Temperature: {temperature}")
        country_label.config(text=f"Country: {country}")
        city_label.config(text=f"City: {city}")
        

        current_address_label.config(text=f"Current Address: {city}")
        delivery_address_label.config(text=f"Delivery Address: {city}")
        change_theme(False, app)  # Dark theme
    else:
        print("Failed to fetch weather data. Using default city settings.")

app.mainloop()
