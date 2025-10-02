from datetime import datetime
from rgbmatrix import graphics
from modules.utils import draw_border, get_temperature_color

class TimeDisplay:
    def __init__(self, matrix, temp_state):
        self.matrix = matrix
        self.temp_state = temp_state
        self.font_time = graphics.Font()
        self.font_time.LoadFont("../../../fonts/10x20.bdf")
        self.font_date = graphics.Font()
        self.font_date.LoadFont("../../../fonts/4x6.bdf")
    
    def display(self, canvas):
        canvas.Clear()

        # Draw the border using the utility function
        draw_border(canvas, self.temp_state.color)
        
        # Draw Date
        date_text = datetime.now().strftime("%a, %b %-d")  # Format example: "Mon, Jan 1"
        date_color = graphics.Color(255, 255, 255)
        graphics.DrawText(canvas, self.font_date, 10, 6, date_color, date_text)
        
        time_now = datetime.now().strftime('%I:%M%p').lstrip('0')  # Format example: "12:05PM" or "1:05PM"
        hour, minute_ampm = time_now.split(':', 1)  # Split into "hour" and "minuteAM/PM"

        if len(hour) == 2:  # Double-digit hour
            # Only display 'AM' or 'PM' with the first letter
            time_text = f"{hour}:{minute_ampm[:-2]}{minute_ampm[-2].lower()}"  # Example: "12:05 p"
        else:  # Single-digit hour
            # Display full time with "am/pm"
            time_text = f"{hour}:{minute_ampm.lower()}"  # Example: "1:05am"

        print(f"[DEBUG] Time: {time_text}")

        
        time_color = graphics.Color(255, 255, 255)
        graphics.DrawText(canvas, self.font_time, 2, 26, time_color, time_text)

        # Swap to display the updated canvas
        self.matrix.SwapOnVSync(canvas)
