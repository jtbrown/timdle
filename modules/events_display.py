from rgbmatrix import graphics
from modules.utils import draw_border
from modules.icons import draw_birthday, draw_anniversary, draw_christmas, draw_fireworks, draw_torch, draw_turkey, draw_flag
import random
import json
from datetime import datetime, timedelta

class EventsDisplay:
    def __init__(self, matrix, temp_state):
        self.matrix = matrix
        self.temp_state = temp_state
        self.font_large = graphics.Font()
        self.font_large.LoadFont("../../../fonts/10x20.bdf")  # Large font for countdown
        self.font_small = graphics.Font()
        self.font_small.LoadFont("../../../fonts/4x6.bdf")  # Small font for event name
        self.text_color = graphics.Color(255, 255, 255)
        self.event_list = []
        self.event_index = 0

        # Load settings
        with open("modules/settings.json") as file:
            self.settings = json.load(file)
        self.load_events()

    def load_events(self):
        """Load all events (birthdays, anniversaries, holidays) into a list."""
        today = datetime.now()
        self.event_list = []

        # Process birthdays
        for birthday in self.settings["BROWNS"]["birthdays"]:
            event_date = datetime.strptime(birthday["date"], "%m/%d").replace(year=today.year)
            if event_date < today:
                event_date += timedelta(days=365)
            days_until = (event_date - today).days
            if days_until < 100:  # Only include events within 100 days
                self.event_list.append({
                    "days_until": days_until,
                    "name": birthday["name"],
                    "type": "birthday"
                })

        # Process anniversaries
        for anniversary in self.settings["BROWNS"]["anniversaries"]:
            event_date = datetime.strptime(anniversary["date"], "%m/%d").replace(year=today.year)
            if event_date < today:
                event_date += timedelta(days=365)
            days_until = (event_date - today).days
            if days_until < 100:  # Only include events within 100 days
                self.event_list.append({
                    "days_until": days_until,
                    "name": anniversary["name"],
                    "type": "anniversary"
                })

        # Process fixed holidays
        for holiday in self.settings["HOLIDAYS"]["fixed"]:
            event_date = datetime.strptime(holiday["date"], "%m/%d").replace(year=today.year)
            if event_date < today:
                event_date += timedelta(days=365)
            days_until = (event_date - today).days
            if days_until < 100:  # Only include events within 100 days
                icon_func = {
                    "Christmas": draw_christmas,
                    "Independence Day": draw_fireworks,
                    "MLK Day": draw_torch,
                    "Thanksgiving": draw_turkey,
                    "Memorial Day": draw_flag,
                }.get(holiday["name"], None)
                self.event_list.append({
                    "days_until": days_until,
                    "name": holiday["name"],
                    "type": "holiday",
                    "icon_func": icon_func
                })

        # Process floating holidays
        for holiday in self.settings["HOLIDAYS"]["floating"]:
            event_date = self.calculate_floating_holiday_date(holiday, today.year)
            if event_date < today:
                event_date = self.calculate_floating_holiday_date(holiday, today.year + 1)
            days_until = (event_date - today).days
            if days_until < 100:  # Only include events within 100 days
                icon_func = {
                    "MLK Day": draw_torch,
                    "Thanksgiving": draw_turkey,
                    "Memorial Day": draw_flag,
                }.get(holiday["name"], None)
                self.event_list.append({
                    "days_until": days_until,
                    "name": holiday["name"],
                    "type": "holiday",
                    "icon_func": icon_func
                })

        # Sort all events by days_until
        self.event_list.sort(key=lambda x: x["days_until"])
        print(f"[DEBUG] Events loaded: {self.event_list}")

    def calculate_floating_holiday_date(self, holiday, year):
        """Calculates the date of a floating holiday based on its rules."""
        month = holiday["month"]
        weekday = holiday["weekday"]
        occurrence = holiday["occurrence"]

        # Map weekday name to Python's weekday index
        weekday_map = {"Monday": 0, "Tuesday": 1, "Wednesday": 2,
                    "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
        target_weekday = weekday_map[weekday]

        # Get all dates in the month
        first_of_month = datetime(year, month, 1)
        days_in_month = (datetime(year, month + 1, 1) - timedelta(days=1)).day
        all_dates = [first_of_month + timedelta(days=i) for i in range(days_in_month)]

        # Filter dates to match the target weekday
        matching_dates = [date for date in all_dates if date.weekday() == target_weekday]

        # Get the specific occurrence
        if occurrence > 0:  # e.g., 3rd Monday
            return matching_dates[occurrence - 1]
        else:  # e.g., last Monday
            return matching_dates[occurrence]

    def display(self, canvas):
        """Displays the next event in the rotation."""
        canvas.Clear()
        draw_border(canvas, self.temp_state.color)  # Use shared temperature color

        # Check if there are events to display
        if not self.event_list:
            graphics.DrawText(canvas, self.font_small, 5, 15, self.text_color, "No Upcoming")
            graphics.DrawText(canvas, self.font_small, 5, 25, self.text_color, "Events")
            return

        # Get the current event to display
        event = self.event_list[self.event_index]
        days_until = event["days_until"]
        event_name = event["name"]

        # Display the countdown
        graphics.DrawText(canvas, self.font_large, 1, 15, self.text_color, f"{days_until}")
        graphics.DrawText(canvas, self.font_small, 23, 15, self.text_color, "days until")

        # Split event name if longer than 12 characters
        if len(event_name) > 12:
            graphics.DrawText(canvas, self.font_small, 12, 25, self.text_color, event_name[:12])
            graphics.DrawText(canvas, self.font_small, 8, 31, self.text_color, event_name[12:])
        else:
            graphics.DrawText(canvas, self.font_small, 12, 25, self.text_color, event_name)

        # Display icons for birthdays, anniversaries, and holidays
        if event["type"] == "birthday":
            draw_birthday(canvas, 1, 16)  # Adjust position as needed
        elif event["type"] == "anniversary":
            draw_anniversary(canvas, 1, 16)  # Adjust position as needed
        elif event["type"] == "holiday" and event.get("icon_func"):
            event["icon_func"](canvas, 1, 16)

        # Move to the next event for the next display cycle
        self.event_index = (self.event_index + 1) % len(self.event_list)
