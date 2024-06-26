# Keylogger GUI Application

This application allows users to log keystrokes using a graphical user interface. Additionally, it features a light/dark mode toggle.

## Features
- Start and stop keylogging
- Toggle between light and dark modes

## Requirements
- Python 3.x
- `customtkinter`
- `pynput`
- `Pillow`

## Installation and Running the Code

### For Developers:

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/aisaac498/PRODIGY_CS_03.git
    ```

2. **Create and Activate a Virtual Environment**:
    ```sh
    python -m venv kylg
    source kylg/bin/activate  # On Windows, use `kylg\Scripts\activate`
    ```

3. **Install the Required Packages**:
    ```sh
    pip install customtkinter pynput Pillow
    ```

4. **Run the Application**:
    ```sh
    python key_logger.py
    ```

### For Prodigy Reviewers:

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/aisaac498/PRODIGY_CS_03.git
    ```

2. **Create and Activate a Virtual Environment**:
    ```sh
    python -m venv kylg
    source kylg/bin/activate  # On Windows, use `kylg\Scripts\activate`
    ```

3. **Install the Required Packages**:
    ```sh
    pip install customtkinter pynput Pillow
    ```

4. **Run the Application**:
    ```sh
    python key_logger.py
    ```

## Usage
- Click "Start" to begin logging keystrokes.
- Click "Stop" to end the logging session.
- Use the moon/sun icon at the top right to switch between light and dark modes.

## Developer Notes
- This keylogger was developed for Windows machines. Please run it on a Windows machine, preferably Windows 11.
- The `fn` key may not be detectable via `pynput`, as it's often handled by the operating system at a lower level.
- The keylogger may not be capturing `ctrl + {any key}` combinations due to the way the `pynput` library handles keyboard events. When a modifier key like `ctrl` is held down and another key is pressed, it might be that only the `ctrl` key press is captured, and the subsequent key press isn't recognized as a separate event or is processed differently.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
