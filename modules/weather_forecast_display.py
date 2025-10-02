from rgbmatrix import graphics
from modules.utils import draw_border
from modules.icons import draw_sun, draw_cloud, draw_rain, draw_lightning, draw_snow, draw_fog
from modules.weather_display import WeatherDisplay, WEATHER_ICON_MAPPING, get_temperature_color
from datetime import datetime

class WeatherForecastDisplay:
    def __init__(self, matrix, temp_state):
        self.matrix = matrix
        self.temp_state = temp_state
        self.font_small = graphics.Font()
        self.font_small.LoadFont("../../../fonts/4x6.bdf")  # Small font for text
        self.font_large = graphics.Font()
        self.font_large.LoadFont("../../../fonts/5x8.bdf")  # Medium font for temperatures
        self.forecast = []

    def update_forecast(self):
        """Updates the 5-day forecast data."""
        weather_display = WeatherDisplay(self.matrix, self.temp_state)
        self.forecast = weather_display.fetch_forecast()

    def draw_column_separator(self, canvas, x, color):
        """Draws a partial vertical line separator."""
        for y in range(5, 29):  # Vertical line from y=5 to y=28
            canvas.SetPixel(x, y, color.red, color.green, color.blue)

    def display(self, canvas):
        """Displays the 5-day weather forecast."""
        canvas.Clear()
        draw_border(canvas, self.temp_state.color)  # Use shared temperature color

        if not self.forecast:
            self.update_forecast()

        if not self.forecast:
            graphics.DrawText(canvas, self.font_small, 5, 15, graphics.Color(255, 255, 255), "No Forecast")
            return

        column_width = 12
        padding = 2
        start_x = padding

        today = datetime.now().strftime("%a")  # Today's abbreviation

        for i, day_data in enumerate(self.forecast):
            x_offset = start_x + (i * column_width)

            # Draw a partial vertical line on the right side of each column (except the last one)
            if i < len(self.forecast) - 1:
                self.draw_column_separator(canvas, x_offset + column_width - 1, graphics.Color(255, 255, 255))

            # Day name or arrow for today
            if i == 0:
                graphics.DrawText(canvas, self.font_small, x_offset + 4, 6, graphics.Color(255, 255, 255), "↓")  # Centered arrow
            else:
                graphics.DrawText(canvas, self.font_small, x_offset + 4, 6, graphics.Color(255, 255, 255), day_data["day"][:1])

            # Average temperature
            avg_temp = day_data["avg_temp"]
            temp_color = get_temperature_color(avg_temp)  # Use color map for temperature
            temp_text = f"{avg_temp}"
            graphics.DrawText(canvas, self.font_large, x_offset + 1, 16, temp_color, temp_text)

            # Weather icon
            icon_func = WEATHER_ICON_MAPPING.get(day_data["icon"], None)
            if icon_func:
                icon_func(canvas, x_offset, 18)  # Adjust icon position as needed
