# Shortcut Keyboard with Pico Multi-Controller and OLED Display

A customizable shortcut keyboard built using the Raspberry Pi Pico with an OLED display for quick access to various functions with a single click.

## Features

- **Multiple Modes**:
  - **Document Mode**: Quick shortcuts for text editing and formatting.
  - **Multimedia Mode**: Controls for media playback, volume, and more.
  - **Website Mode**: Open frequently used websites or perform web-based actions.
  
- **Customizable Shortcuts**: Easily customize shortcuts for each mode to suit your needs.

- **Plug-and-Play**: Compatible with any device that supports USB keyboards. Simply plug it in, and it's ready to use.

## Technology Stack

- **Hardware**: Raspberry Pi Pico with OLED Display
- **Libraries**: `HID` and `Adafruit-Keyboard` Libraries
- **Programming Language**: CircuitPython

## Installation

1. Install CircuitPython on your Raspberry Pi Pico.
2. Copy the required libraries (`HID`, `Adafruit-Keyboard`, etc.) to the Pico's `lib` folder.
3. Upload the provided CircuitPython code to the Pico.

## Usage

1. Plug the Pico into your device via USB.
2. Use the OLED display and buttons to switch between modes.
3. Enjoy quick access to your favorite shortcuts and functions!

## Customization

- Edit the `code.py` file to modify or add new shortcuts for different modes.
- Use the OLED display to visually confirm the selected mode and shortcut.

## Future Improvements

- Adding more modes for specific applications (e.g., gaming mode).
- Enhancing the OLED display to show dynamic shortcut information.

## License

This project is open-source and available under the MIT License.
