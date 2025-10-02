import requests
from rgbmatrix import graphics
from modules.icons import draw_sun, draw_cloud, draw_rain, draw_lightning, draw_snow, draw_fog
from modules.utils import draw_border, get_temperature_color
from datetime import datetime

# API setup
API_KEY = '3652cde54a500def6ef61246eb8826d2'
CITY = 'Clarksburg,MD,US'
URL = f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&units=imperial&appid={API_KEY}'

# Map OpenWeatherMap icon codes to drawing functions
WEATHER_ICON_MAPPING = {
    "01d": draw_sun,       # Clear sky (day)
    "01n": draw_sun,       # Clear sky (night)
    "02d": draw_cloud,     # Few clouds (day)
    "02n": draw_cloud,     # Few clouds (night)
    "03d": draw_cloud,     # Scattered clouds (day)
    "03n": draw_cloud,     # Scattered clouds (night)
    "04d": draw_cloud,     # Broken clouds (day)
    "04n": draw_cloud,     # Broken clouds (night)
    "09d": draw_rain,      # Shower rain (day)
    "09n": draw_rain,      # Shower rain (night)
    "10d": draw_rain,      # Rain (day)
    "10n": draw_rain,      # Rain (night)
    "11d": draw_lightning, # Thunderstorm (day)
    "11n": draw_lightning, # Thunderstorm (night)
    "13d": draw_snow,      # Snow (day)
    "13n": draw_snow,      # Snow (night)
    "50d": draw_fog,       # Fog (day)
    "50n": draw_fog        # Fog (night)
}

class WeatherDisplay:
    def __init__(self, matrix, temp_state):
        self.matrix = matrix
        self.temp_state = temp_state  # Reference to shared temperature state
        self.font = graphics.Font()
        self.font.LoadFont("../../../fonts/6x12.bdf")
        self.font2 = graphics.Font()
        self.font2.LoadFont("../../../fonts/10x20.bdf")

    def fetch_weather(self):
        """Fetches weather data from the OpenWeatherMap API."""
        response = requests.get(URL)
        data = response.json()

        if data.get('cod') == 200:
            current_temp = round(data['main']['temp'])
            high_temp = round(data['main']['temp_max'])
            low_temp = round(data['main']['temp_min'])
            icon_code = data['weather'][0]['icon']

            # Update the shared temperature color
            self.temp_state.update_color(current_temp)

            # Debugging output for selected icon
            icon_func = WEATHER_ICON_MAPPING.get(icon_code)
            print(f"[DEBUG] Weather Icon Code: {icon_code}, Function: {icon_func.__name__ if icon_func else 'None'}")

            return {
                "current_temp": current_temp,
                "high_temp": high_temp,
                "low_temp": low_temp,
                "icon_func": icon_func,
            }
        return None

    def fetch_forecast(self):
        """Fetches 5-day weather forecast data from OpenWeatherMap."""
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&units=imperial&appid={API_KEY}"
        response = requests.get(forecast_url)
        data = response.json()

        if data.get('cod') == "200":
            forecast = []
            daily_temps = {}
            
            # Group forecast data by day
            for item in data["list"]:
                timestamp = datetime.fromtimestamp(item["dt"])
                day = timestamp.strftime("%a")  # Abbreviated weekday (e.g., "Mon")
                if day not in daily_temps:
                    daily_temps[day] = {"temps": [], "icons": []}
                daily_temps[day]["temps"].append(item["main"]["temp"])
                daily_temps[day]["icons"].append(item["weather"][0]["icon"])

            # Process each day's data
            for day, values in daily_temps.items():
                avg_temp = round(sum(values["temps"]) / len(values["temps"]))
                common_icon = max(set(values["icons"]), key=values["icons"].count)  # Most common icon
                forecast.append({
                    "day": day,
                    "avg_temp": avg_temp,
                    "icon": common_icon
                })

            return forecast[:5]  # Return the next 5 days
        return None

    def display(self, canvas):
        weather_data = self.fetch_weather()
        if not weather_data:
            print("[DEBUG] No weather data available.")
            return

        canvas.Clear()
        draw_border(canvas, self.temp_state.color)  # Use shared temperature color

        # Display temperatures
        current_temp_text = f"{weather_data['current_temp']}°F"
        graphics.DrawText(canvas, self.font2, 20, 15, self.temp_state.color, current_temp_text)

        high_low_text = f"{weather_data['high_temp']}°-{weather_data['low_temp']}°"
        graphics.DrawText(canvas, self.font, 12, 28, self.temp_state.color, high_low_text)

        # Display weather icon
        icon_func = weather_data["icon_func"]
        if icon_func:
            icon_func(canvas, 4, 2)
