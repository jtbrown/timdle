from rgbmatrix import graphics

def draw_filled_circle(canvas, center_x, center_y, radius, color):
    """Draws a filled circle by setting pixels within a radius."""
    for x in range(center_x - radius, center_x + radius + 1):
        for y in range(center_y - radius, center_y + radius + 1):
            if (x - center_x) ** 2 + (y - center_y) ** 2 <= radius ** 2:
                canvas.SetPixel(x, y, color.red, color.green, color.blue)

def draw_filled_rectangle(canvas, x1, y1, x2, y2, color):
    """Draws a filled rectangle by setting pixels in a rectangular region."""
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            canvas.SetPixel(x, y, color.red, color.green, color.blue)

def draw_sun(canvas, reference_x=0, reference_y=0):
    """Draws a filled sun with orange rays around a yellow circle."""
    color_yellow = graphics.Color(255, 255, 0)
    color_orange = graphics.Color(255, 165, 0)
    # Orange rays around the sun
    for dx, dy in [(-5, 0), (5, 0), (0, -5), (0, 5), (-4, -4), (4, 4), (-4, 4), (4, -4)]:
        graphics.DrawLine(canvas, reference_x + 5, reference_y + 5, reference_x + 5 + dx, reference_y + 5 + dy, color_orange)
    draw_filled_circle(canvas, reference_x + 5, reference_y + 5, 3, color_yellow)  # Sun center

def draw_cloud(canvas, reference_x=0, reference_y=0):
    """Draws a new cloud shape with a rounded look, fitting within a 10x10 grid."""
    color_white = graphics.Color(255, 255, 255)
    
    # Center of the cloud
    draw_filled_circle(canvas, reference_x + 5, reference_y + 5, 3, color_white)  # Main body
    
    # Side puffs to give a fuller shape
    draw_filled_circle(canvas, reference_x + 3, reference_y + 6, 2, color_white)  # Left puff
    draw_filled_circle(canvas, reference_x + 7, reference_y + 6, 2, color_white)  # Right puff

def draw_rain(canvas, reference_x=0, reference_y=0):
    """Draws a cloud with three columns of rain below it."""
    draw_cloud(canvas, reference_x, reference_y)  # Cloud base
    color_blue = graphics.Color(0, 0, 255)
    # Raindrops in three columns below the cloud
    graphics.DrawLine(canvas, reference_x + 3, reference_y + 9, reference_x + 3, reference_y + 10, color_blue)
    graphics.DrawLine(canvas, reference_x + 5, reference_y + 9, reference_x + 5, reference_y + 10, color_blue)
    graphics.DrawLine(canvas, reference_x + 7, reference_y + 9, reference_x + 7, reference_y + 10, color_blue)

def draw_lightning(canvas, reference_x=0, reference_y=0):
    """Draws a cloud with a sharper lightning bolt below it."""
    draw_cloud(canvas, reference_x, reference_y)
    color_yellow = graphics.Color(255, 255, 0)
    # Sharper, more compact lightning bolt
    graphics.DrawLine(canvas, reference_x + 5, reference_y + 7, reference_x + 6, reference_y + 9, color_yellow)
    graphics.DrawLine(canvas, reference_x + 6, reference_y + 9, reference_x + 4, reference_y + 9, color_yellow)
    graphics.DrawLine(canvas, reference_x + 4, reference_y + 9, reference_x + 5, reference_y + 11, color_yellow)

def draw_snow(canvas, reference_x=0, reference_y=0):
    """Draws a more intricate snowflake with extra branching within a 10x10 grid."""
    color_white = graphics.Color(255, 255, 255)
    
    # Central cross shape (vertical and horizontal lines)
    graphics.DrawLine(canvas, reference_x + 5, reference_y + 2, reference_x + 5, reference_y + 8, color_white)  # Vertical
    graphics.DrawLine(canvas, reference_x + 2, reference_y + 5, reference_x + 8, reference_y + 5, color_white)  # Horizontal
    
    # Diagonal lines for main branches
    graphics.DrawLine(canvas, reference_x + 3, reference_y + 3, reference_x + 7, reference_y + 7, color_white)
    graphics.DrawLine(canvas, reference_x + 7, reference_y + 3, reference_x + 3, reference_y + 7, color_white)
    
def draw_fog(canvas, reference_x=0, reference_y=0):
    """Draws three white wavy lines for fog."""
    color_white = graphics.Color(255, 255, 255)
    graphics.DrawLine(canvas, reference_x + 2, reference_y + 4, reference_x + 8, reference_y + 5, color_white)
    graphics.DrawLine(canvas, reference_x + 2, reference_y + 6, reference_x + 8, reference_y + 7, color_white)
    graphics.DrawLine(canvas, reference_x + 2, reference_y + 8, reference_x + 8, reference_y + 9, color_white)

def draw_birthday(canvas, reference_x=0, reference_y=0):
    """Draws a birthday cake with a taller base and two centered candles."""
    color_cake = graphics.Color(139, 69, 19)
    color_candle = graphics.Color(255, 255, 255)
    color_flame = graphics.Color(255, 69, 0)
    
    # Taller cake base
    draw_filled_rectangle(canvas, reference_x + 3, reference_y + 6, reference_x + 7, reference_y + 8, color_cake)
    
    # Two centered candles with flames
    for candle_x in [reference_x + 4, reference_x + 6]:
        graphics.DrawLine(canvas, candle_x, reference_y + 5, candle_x, reference_y + 6, color_candle)  # Candle
        canvas.SetPixel(candle_x, reference_y + 4, color_flame.red, color_flame.green, color_flame.blue)  # Flame

def draw_anniversary(canvas, reference_x=0, reference_y=0):
    """Draws a smaller ring outline for an anniversary."""
    color_gold = graphics.Color(255, 215, 0)
    # Smaller ring outline
    graphics.DrawCircle(canvas, reference_x + 5, reference_y + 5, 3, color_gold)

def draw_filled_circle(canvas, center_x, center_y, radius, color):
    for x in range(center_x - radius, center_x + radius + 1):
        for y in range(center_y - radius, center_y + radius + 1):
            if (x - center_x) ** 2 + (y - center_y) ** 2 <= radius ** 2:
                canvas.SetPixel(x, y, color.red, color.green, color.blue)

def draw_christmas(canvas, reference_x=0, reference_y=0):
    """Draws a Christmas tree."""
    color_green = graphics.Color(0, 255, 0)
    color_brown = graphics.Color(139, 69, 19)
    color_yellow = graphics.Color(255, 255, 0)
    # Tree layers
    graphics.DrawLine(canvas, reference_x + 5, reference_y, reference_x + 2, reference_y + 3, color_green)
    graphics.DrawLine(canvas, reference_x + 5, reference_y, reference_x + 8, reference_y + 3, color_green)
    graphics.DrawLine(canvas, reference_x + 5, reference_y + 3, reference_x + 3, reference_y + 6, color_green)
    graphics.DrawLine(canvas, reference_x + 5, reference_y + 3, reference_x + 7, reference_y + 6, color_green)
    # Trunk
    graphics.DrawLine(canvas, reference_x + 4, reference_y + 7, reference_x + 5, reference_y + 7, color_brown)
    # Star
    canvas.SetPixel(reference_x + 5, reference_y - 1, color_yellow.red, color_yellow.green, color_yellow.blue)

def draw_fireworks(canvas, reference_x=0, reference_y=0):
    """Draws a firework burst."""
    color_red = graphics.Color(255, 0, 0)
    color_blue = graphics.Color(0, 0, 255)
    # Center point
    canvas.SetPixel(reference_x + 5, reference_y + 5, color_red.red, color_red.green, color_red.blue)
    # Radiating lines
    for dx, dy in [(-2, -2), (2, 2), (-2, 2), (2, -2), (0, -3), (0, 3), (-3, 0), (3, 0)]:
        graphics.DrawLine(canvas, reference_x + 5, reference_y + 5, reference_x + 5 + dx, reference_y + 5 + dy, color_blue)

def draw_torch(canvas, reference_x=0, reference_y=0):
    """Draws a torch."""
    color_flame = graphics.Color(255, 69, 0)
    color_handle = graphics.Color(139, 69, 19)
    # Flame
    graphics.DrawLine(canvas, reference_x + 4, reference_y + 2, reference_x + 5, reference_y + 0, color_flame)
    graphics.DrawLine(canvas, reference_x + 5, reference_y + 0, reference_x + 6, reference_y + 2, color_flame)
    # Handle
    graphics.DrawLine(canvas, reference_x + 4, reference_y + 3, reference_x + 5, reference_y + 8, color_handle)
    graphics.DrawLine(canvas, reference_x + 5, reference_y + 3, reference_x + 6, reference_y + 8, color_handle)

def draw_turkey(canvas, reference_x=0, reference_y=0):
    """Draws a turkey."""
    color_body = graphics.Color(165, 42, 42)
    color_tail = graphics.Color(255, 165, 0)
    # Tail feathers
    graphics.DrawLine(canvas, reference_x + 3, reference_y + 3, reference_x + 7, reference_y + 3, color_tail)
    graphics.DrawLine(canvas, reference_x + 2, reference_y + 4, reference_x + 8, reference_y + 4, color_tail)
    # Body
    draw_filled_circle(canvas, reference_x + 5, reference_y + 6, 2, color_body)

def draw_flag(canvas, reference_x=0, reference_y=0):
    """Draws a flag."""
    color_pole = graphics.Color(139, 69, 19)
    color_flag = graphics.Color(255, 0, 0)
    color_star = graphics.Color(255, 255, 255)
    # Pole
    graphics.DrawLine(canvas, reference_x + 2, reference_y, reference_x + 2, reference_y + 8, color_pole)
    # Flag rectangle
    for x in range(reference_x + 3, reference_x + 7):
        for y in range(reference_y + 1, reference_y + 4):
            canvas.SetPixel(x, y, color_flag.red, color_flag.green, color_flag.blue)
    # Star
    canvas.SetPixel(reference_x + 4, reference_y + 2, color_star.red, color_star.green, color_star.blue)
