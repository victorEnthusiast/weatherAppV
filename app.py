import tkinter as tk
from tkinter import messagebox
import datetime as dt
import requests

def fetch_weather():
    cities = city_var.get().split(",")  # Split the input into a list of cities
    with open('api_key', 'r') as file:
        api_key = file.read().strip()

    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

    weather_info = ""
    city_entry=""
    for city in cities:
        url = f"{BASE_URL}q={city}&appid={api_key}"
        try:
            response = requests.get(url)
            data = response.json()
            
            temp_kelvin = data['main']['temp']
            temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
            
            feels_like_kelvin = data['main']['feels_like']
            feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)
            
            wind_speed = data['wind']['speed']
            humidity = data['main']['humidity']
            description = data['weather'][0]['description']
            
            sunrise_time = dt.datetime.utcfromtimestamp(data['sys']['sunrise']) + dt.timedelta(seconds=data['timezone'])
            sunset_time = dt.datetime.utcfromtimestamp(data['sys']['sunset']) + dt.timedelta(seconds=data['timezone'])

            result_text = (
                f"Temperature in {city}: {temp_celsius:.2f}°C or {temp_fahrenheit:.2f}°F\n"
                f"Temperature in {city} feels like: {feels_like_celsius:.2f}°C or {feels_like_fahrenheit:.2f}°F\n"
                f"Humidity in {city}: {humidity}%\n"
                f"Wind speed in {city}: {wind_speed} m/s\n"
                f"General weather in {city}: {description}\n"
                f"Sun rises in {city}: at {sunrise_time} local time\n"
                f"Sun sets in {city}: at {sunset_time} local time\n\n"
            )
            
            weather_info += result_text
            
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching weather data for {city}: {e}")
       
        try:
         val = int( city_entry)
        except ValueError:
         print("That's an int!")
    # Show all weather information in a single message box
    if weather_info:
        messagebox.showinfo("Weather Information", weather_info)

def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * 9/5 + 32
    return celsius, fahrenheit

# Create the main window
root = tk.Tk()
root.title("Weather App")

# Create and place widgets
tk.Label(root, text="Enter Cities (separated by commas):").grid(row=0, column=0, sticky="w")

# Create a variable to store the selected cities
city_var = tk.StringVar(root)
city_entry = tk.Entry(root, textvariable=city_var)
city_entry.grid(row=0, column=1)

fetch_button = tk.Button(root, text="Fetch Weather", command=fetch_weather)
fetch_button.grid(row=2, column=0, columnspan=2)

# Run the main event loop
root.mainloop()