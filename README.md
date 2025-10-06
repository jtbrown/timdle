# Timdle

Timdle is a Python app for displaying time, weather, events, and artwork on an RGB LED matrix (using hzeller’s `rpi-rgb-led-matrix`).

## Run
```bash
python3 timdle.py

# 🕰️ Timdle

**Timdle** is a modular, Raspberry Pi-powered family dashboard that turns your LED matrix into a dynamic smart display. It shows the time, weather, upcoming calendar events, birthdays, anniversaries, holidays, and even rotating artwork—all with seasonal and contextual flair.

Built with:
- Python 3
- [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix)
- PIL (Python Imaging Library)

---

## 🧠 Features

- ⏰ **Time + Date** with animated or seasonal borders
- 🌤️ **Current Weather** and forecasts
- 📅 **Calendar Events** from a JSON feed or other source
- 🎉 **Birthdays & Anniversaries** from a config file
- 🎨 **Rotating Artwork** from your own image library
- 🌎 **Holiday Messages** (fixed and floating holidays supported)
- 💤 **Auto-Sleep/Wake**: Turns off the display from 9pm–5am (configurable)

---

## 📷 Demo

<p align="center">
  <img src="docs/demo.gif" alt="Timdle display demo" width="500"/>
</p>

---

## 📁 Project Structure

```
timdle/
├── timdle.py                  # Main runner script
├── modules/
│   ├── artwork_display.py     # Displays random artwork
│   ├── display_all_icons.py   # Debug screen to show all icons
│   ├── events_display.py      # Pulls and shows calendar events
│   ├── icons.py               # Icon drawing helpers
│   ├── screen_manager.py      # Rotates through screen types
│   ├── time_display.py        # Time + date rendering
│   ├── utils.py               # Shared utilities (e.g. temp thresholds)
│   ├── weather_display.py     # Current weather rendering
│   └── weather_forecast_display.py  # Forecasts and icons
├── display_config.json        # Display layout and font sizes
├── settings.json              # Birthdays, holidays, seasonal data
├── artwork_data.json          # Image paths and metadata for artwork
├── README.md                  # This file
```

---

## 🔧 Installation

### Hardware Requirements

- Raspberry Pi (4 or 5 recommended)
- HUB75-compatible RGB LED Matrix (64x64 suggested)
- Adafruit RGB Matrix HAT/Bonnet
- Power supply for matrix (5V/4A)
- Optional: RTC, buttons, enclosures, etc.

### Software Setup

1. **Clone the repo**  
   ```bash
   git clone https://github.com/YOUR_USERNAME/timdle.git
   cd timdle
   ```

2. **Set up dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip
   pip3 install -r requirements.txt
   ```

3. **Install the RGB Matrix library**  
   Follow [these instructions](https://github.com/hzeller/rpi-rgb-led-matrix#installation) to install and test your matrix.

4. **Run the display**  
   ```bash
   sudo python3 timdle.py
   ```

5. (Optional) **Create a systemd service** to start at boot:
   - See [`docs/timdle.service`](docs/timdle.service) example

---

## ⚙️ Configuration

### `settings.json`

Customize:
- Birthdays and anniversaries
- Holiday greetings (fixed and floating)
- Seasons (used for border colors or messages)

Example:
```jsonc
{
  "BROWNS": {
    "birthdays": [
      {
        "date": "02/07",           // MM/DD format
        "name": "Jeff's Bday",      // Display name
        "message": "Happy Birthday, Jeff!" // Message to show
      }
    ],
    "anniversaries": [
      {
        "date": "01/19",
        "name": "Jeff & Sarah Anniversary",
        "message": "Happy Anniversary!"
      }
    ]
  }
}
```


### `display_config.json`

Control:
- Font sizes
- X/Y display positions
- Custom static messages

Example:
```jsonc
{
  "time": {
    "position": [5, 5],      // X, Y coordinates on matrix
    "font_size": 12          // Font size for time text
  },
  "weather": {
    "position": [5, 15],
    "font_size": 10,
    "message": "Sunny, 75°F" // Optional static message override
  }
}
```

### 🌤️ Local Weather Setup

To customize the local weather display, edit the `weather_display.py` (or `weather_forecast_display.py`) file with your location and API key.

```python
API_KEY = "your_openweathermap_api_key"   # Get one at https://openweathermap.org/api
LOCATION = "Rockville,US"                 # Format: City,CountryCode
UNITS = "imperial"                        # Use "metric" for Celsius
LANG = "en"                               # Language for weather descriptions
```

> You can also override the display with static text in `display_config.json`, like:

```jsonc
"weather": {
  "position": [5, 15],
  "font_size": 10,
  "message": "Sunny, 75°F"  // Optional; remove to use live data
}
```

---

## 🔁 Auto Sleep/Wake

Display automatically turns **off at 9:00 PM** and **back on at 5:00 AM**.

To change this, modify the logic in `screen_manager.py` or use a config flag (feature coming soon).

---

## ✍️ Customizing the Display

- Add new screen types via `screen_manager.py`
- Add weather providers or icon sets via `weather_display.py`
- Use your own fonts, colors, layouts with `display_config.json`

Want pixel art? Flash messages? News tickers? You can build your own screens or expand the manager!

---

## 🧪 Development Notes

- Keep functions modular (`display()` returns a PIL Image)
- Images are drawn using `graphics.DrawText` or `ImageDraw`
- Matrix updates via `.SetImage(image.convert("RGB"))`
- Use `time.sleep()` between screen cycles (default: 10s)

---

## 📬 Contributing

Pull requests welcome! Especially for:
- More weather icons
- New screen modules
- Config file support
- Better animations

---

## 🧊 Example Enhancements

- 🧠 Add OpenAI-generated daily quotes
- 📰 Add RSS headlines
- 🎶 Show Spotify “Now Playing”
- 🔔 Integrate Google Calendar or iCloud feeds

---

## 📄 License

MIT — free to use, modify, and build upon.