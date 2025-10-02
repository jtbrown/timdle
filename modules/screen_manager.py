class ScreenManager:
    def __init__(self):
        self.screens = []
        self.current_index = 0

    def add_screen(self, name, display_function):
        """Adds a screen to the rotation."""
        self.screens.append((name, display_function))

    def show_next_screen(self, canvas):
        """Displays the next screen in the rotation."""
        if not self.screens:
            return
        # Get the next screen in the list
        screen_name, display_function = self.screens[self.current_index]
        print(f"Displaying screen: {screen_name}")
        # Call the screen's display function, passing the canvas
        display_function(canvas)
        # Move to the next screen in the rotation
        self.current_index = (self.current_index + 1) % len(self.screens)
