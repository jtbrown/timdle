import time
import json
import random
from PIL import Image
from rgbmatrix import graphics

class ArtworkDisplay:
    def __init__(self, matrix, data_file="modules/artwork_data.json"):
        self.matrix = matrix
        self.artwork_data = self.load_artwork_data(data_file)
        self.artwork_keys = list(self.artwork_data.keys())
        self.current_image_index = 0
        random.shuffle(self.artwork_keys)  # Randomize the display order

    def load_artwork_data(self, data_file):
        """Loads artwork data from the specified JSON file."""
        print(f"[DEBUG] Attempting to load artwork data from: {data_file}")
        try:
            with open(data_file, "r") as file:
                artwork_data = json.load(file)
                print(f"[DEBUG] Loaded {len(artwork_data)} artworks from {data_file}")
                return artwork_data
        except FileNotFoundError:
            print(f"[ERROR] File {data_file} not found.")
            return {}
        except json.JSONDecodeError:
            print(f"[ERROR] Failed to decode JSON from {data_file}.")
            return {}

    def process_image(self, image_path):
        """Loads and processes the image to fit the 32x64 matrix."""
        if not image_path or not isinstance(image_path, str):
            print(f"[ERROR] Invalid image path: {image_path}")
            return None

        try:
            img = Image.open(image_path)
            img = img.convert("RGB")  # Ensure the image is in RGB format

            # Resize or crop to fit the 32x64 matrix
            width, height = img.size
            aspect_ratio = width / height

            if aspect_ratio > (64 / 32):  # Wider than matrix
                new_height = 32
                new_width = int(aspect_ratio * new_height)
            else:  # Taller or square
                new_width = 64
                new_height = int(new_width / aspect_ratio)

            img = img.resize((new_width, new_height), Image.ANTIALIAS)

            # Center the image on the 32x64 matrix
            left = (new_width - 64) // 2 if new_width > 64 else 0
            top = (new_height - 32) // 2 if new_height > 32 else 0
            right = left + 64
            bottom = top + 32

            img = img.crop((left, top, right, bottom))
            return img
        except FileNotFoundError:
            print(f"[ERROR] Image file not found: {image_path}")
            return None
        except Exception as e:
            print(f"[ERROR] Failed to process image {image_path}: {e}")
            return None

    def display(self, canvas):
        """Displays a preprocessed pixel data."""
        canvas.Clear()

        if not self.artwork_data:
            print("[DEBUG] No artwork data to display.")
            graphics.DrawText(
                canvas,
                graphics.Font().LoadFont("../../../fonts/4x6.bdf"),
                5, 15,
                graphics.Color(255, 255, 255),
                "No Artwork"
            )
            return

        # Get the current artwork
        current_key = self.artwork_keys[self.current_image_index]
        pixel_data = self.artwork_data.get(current_key)

        print(f"[DEBUG] Displaying preprocessed pixel data for: {current_key}")

        if not pixel_data or not isinstance(pixel_data, list):
            print(f"[ERROR] Invalid pixel data for key: {current_key}")
            return

        # Render pixel data
        for pixel in pixel_data:
            try:
                x, y = pixel['x'], pixel['y']
                r, g, b = map(int, pixel['color'][4:-1].split(','))
                canvas.SetPixel(x, y, r, g, b)
            except Exception as e:
                print(f"[ERROR] Failed to render pixel: {pixel} - {e}")

        # Swap and display the canvas
        self.matrix.SwapOnVSync(canvas)
        time.sleep(5)

        # Move to the next artwork
        self.current_image_index = (self.current_image_index + 1) % len(self.artwork_keys)
