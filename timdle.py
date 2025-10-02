#!/usr/bin/env python3
from modules.screen_manager import ScreenManager
from modules.time_display import TimeDisplay
from modules.weather_display import WeatherDisplay
from modules.weather_forecast_display import WeatherForecastDisplay
from modules.events_display import EventsDisplay
from modules.utils import TemperatureState
from modules.artwork_display import ArtworkDisplay
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import time
import datetime

ROWS = 32
COLS = 64

# ===== Settings =====
BRIGHTNESS = 60          # normal brightness (1–100)
QUIET_START_HOUR = 21    # 21 = 9:00 PM
QUIET_END_HOUR = 5       # 5 = 5:00 AM
QUIET_SLEEP_SEC = 30     # how often to wake/check time during quiet hours
DWELL_SEC = 5            # seconds per screen when rotating

def in_quiet_hours(now=None) -> bool:
    """Return True if current local time is within quiet hours [start..overnight..end)."""
    now = now or datetime.datetime.now()
    h = now.hour
    # Overnight range (e.g. 21 → 5)
    if QUIET_START_HOUR > QUIET_END_HOUR:
        return h >= QUIET_START_HOUR or h < QUIET_END_HOUR
    return QUIET_START_HOUR <= h < QUIET_END_HOUR

def main():
    # Configure and initialize the LED matrix
    options = RGBMatrixOptions()
    options.rows = ROWS
    options.cols = COLS
    options.chain_length = 1
    options.parallel = 1
    options.brightness = BRIGHTNESS
    # If you use Adafruit HAT on Pi 4 and see flicker, uncomment:
    # options.hardware_mapping = "adafruit-hat"
    # options.gpio_slowdown = 4

    matrix = RGBMatrix(options=options)

    # Shared temperature state
    temp_state = TemperatureState()

    # Initialize screens
    weather_screen = WeatherDisplay(matrix, temp_state)
    weather_screen.fetch_weather()

    time_screen = TimeDisplay(matrix, temp_state)
    events_screen = EventsDisplay(matrix, temp_state)
    forecast_screen = WeatherForecastDisplay(matrix, temp_state)
    artwork_screen = ArtworkDisplay(matrix)

    # Screen manager
    screen_manager = ScreenManager()
    screen_manager.add_screen("time", time_screen.display)
    screen_manager.add_screen("weather", weather_screen.display)
    screen_manager.add_screen("time", time_screen.display)
    screen_manager.add_screen("events", events_screen.display)
    screen_manager.add_screen("time", time_screen.display)
    screen_manager.add_screen("forecast", forecast_screen.display)
    screen_manager.add_screen("time", time_screen.display)
    screen_manager.add_screen("artwork", artwork_screen.display)

    dimmed = False

    try:
        while True:
            if in_quiet_hours():
                if not dimmed:
                    try:
                        matrix.SetBrightness(0)
                    except Exception:
                        pass
                    matrix.Clear()
                    dimmed = True
                time.sleep(QUIET_SLEEP_SEC)
                continue
            else:
                if dimmed:
                    try:
                        matrix.SetBrightness(BRIGHTNESS)
                    except Exception:
                        pass
                    dimmed = False

            # Normal rotation
            canvas = matrix.CreateFrameCanvas()
            screen_manager.show_next_screen(canvas)
            matrix.SwapOnVSync(canvas)
            time.sleep(DWELL_SEC)

    except KeyboardInterrupt:
        print("\nProgram exited gracefully.")
    finally:
        try:
            matrix.Clear()
        except Exception:
            pass

if __name__ == "__main__":
    main()
