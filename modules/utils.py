from rgbmatrix import graphics

def draw_border(canvas, color, rows=32, cols=64):
    """Draws a border around the perimeter of the matrix display."""
    # Top and Bottom borders
    for x in range(cols):  # Full width
        canvas.SetPixel(x, 0, color.red, color.green, color.blue)    # Top border
        canvas.SetPixel(x, rows - 1, color.red, color.green, color.blue)  # Bottom border
    # Left and Right borders
    for y in range(rows):  # Full height
        canvas.SetPixel(0, y, color.red, color.green, color.blue)    # Left border
        canvas.SetPixel(cols - 1, y, color.red, color.green, color.blue)  # Right border

from rgbmatrix import graphics

class TemperatureState:
    """Manages the shared state for the temperature color."""
    def __init__(self):
        self.color = graphics.Color(255, 255, 255)  # Default white color

    def update_color(self, temp):
        """Updates the temperature color based on the given temperature."""
        if temp <= 32:
            self.color = graphics.Color(0, 0, 139)  # Dark Blue
        elif temp <= 50:
            self.color = graphics.Color(70, 130, 180)  # Light Blue
        elif temp <= 70:
            self.color = graphics.Color(144, 238, 144)  # Light Green
        elif temp <= 85:
            self.color = graphics.Color(255, 165, 0)  # Orange
        else:
            self.color = graphics.Color(255, 0, 0)  # Red
        print(f"[DEBUG] Temperature color updated to: {self.color.red}, {self.color.green}, {self.color.blue}")

def get_temperature_color(temp):
    """Returns an RGB color based on temperature ranges."""
    if temp <= 32:
        return graphics.Color(0, 0, 139)  # Dark Blue
    elif temp <= 50:
        return graphics.Color(70, 130, 180)  # Light Blue
    elif temp <= 70:
        return graphics.Color(144, 238, 144)  # Light Green
    elif temp <= 85:
        return graphics.Color(255, 165, 0)  # Orange
    else:
        return graphics.Color(255, 0, 0)  # Red
