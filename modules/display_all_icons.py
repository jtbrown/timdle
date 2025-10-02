import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from icons import draw_sun, draw_cloud, draw_rain, draw_lightning, draw_snow, draw_fog, draw_birthday, draw_anniversary

# Matrix setup
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
matrix = RGBMatrix(options=options)

# List of icons to display (function references)
icons = [
    ("Sun", draw_sun),
    ("Cloud", draw_cloud),
    ("Rain", draw_rain),
    ("Lightning", draw_lightning),
    ("Snow", draw_snow),
    ("Fog", draw_fog),
    ("Birthday", draw_birthday),
    ("Anniversary", draw_anniversary)
]

# Display each icon for 3 seconds
while True:
    for icon_name, icon_func in icons:
        print(f"[DEBUG] Displaying icon: {icon_name}")
        canvas = matrix.CreateFrameCanvas()

        # Clear the screen and draw the icon at a central position
        canvas.Clear()
        icon_func(canvas, reference_x=10, reference_y=5)  # Adjust positions as necessary
        matrix.SwapOnVSync(canvas)

        time.sleep(3)  # Display each icon for 3 seconds

# Clear the display after showing all icons
matrix.Clear()
print("[DEBUG] All icons displayed.")
