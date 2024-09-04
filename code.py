import time
import board
import usb_hid
import busio
import digitalio
import displayio
import terminalio
import adafruit_displayio_ssd1306
from adafruit_display_text import label
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

displayio.release_displays()

# Use for I2C
i2c = busio.I2C(scl=board.GP17, sda=board.GP16)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

WIDTH = 128
HEIGHT = 64
BORDER = 2

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

# Make the display context
def update(text):
        
    splash = displayio.Group()
    display.root_group = splash  # Updated to use root_group instead of show

    color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xFFFFFF  # White

    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

    # Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(WIDTH - BORDER * 2, HEIGHT - BORDER * 2, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = 0x000000  # Black
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER)
    splash.append(inner_sprite)

    # Draw a label
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=12, y=HEIGHT // 2 - 1)
    splash.append(text_area)
    display.refresh()

# Setup keyboard emulation 
kbd = Keyboard(usb_hid.devices)

# Setup consumer control for multimedia keys
cc = ConsumerControl(usb_hid.devices)

# Define button pins and configure them as inputs
buttons = [
    digitalio.DigitalInOut(board.GP0),  # Button 1
    digitalio.DigitalInOut(board.GP1),  # Button 2
    digitalio.DigitalInOut(board.GP2),  # Button 3
    digitalio.DigitalInOut(board.GP3),  # Button 4
    digitalio.DigitalInOut(board.GP4),  # Button 5
    digitalio.DigitalInOut(board.GP5)   # Mode switch button
]

# Set each button pin as input with an internal pull-up resistor
for button in buttons:
    button.direction = digitalio.Direction.INPUT

# Store the last state of each button
last_state = [True, True, True, True, True, True]

# Define modes
modes = ["Document Mode", "Multimedia Mode", "Website Mode"]
current_mode = 0  # Start with Document Mode

def handle_document_mode(button_index):
    if button_index == 0:
        update("Copy")
        kbd.send(Keycode.CONTROL, Keycode.C)  # Ctrl+C (Copy)
    elif button_index == 1:
        update("Paste")
        kbd.send(Keycode.CONTROL, Keycode.V)  # Ctrl+V (Paste)
    elif button_index == 2:
        update("Cut")
        kbd.send(Keycode.CONTROL, Keycode.X)  # Ctrl+X (Cut)
    elif button_index == 3:
        update("Undo")
        kbd.send(Keycode.CONTROL, Keycode.Z)  # Ctrl+Z (Undo)
    elif button_index == 4:
        update("Save")
        kbd.send(Keycode.CONTROL, Keycode.S)  # Ctrl+S (Save)

def handle_multimedia_mode(button_index):
    if button_index == 0:
        update("Play/Pause")
        kbd.send(Keycode.SPACEBAR)  # Play/Pause
    elif button_index == 1:
        update("Next Track")
        cc.send(ConsumerControlCode.SCAN_NEXT_TRACK)  # Next Track
    elif button_index == 2:
        update("Previous Track")
        cc.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK)  # Previous Track
    elif button_index == 3:
        update("Volume Up")
        cc.send(ConsumerControlCode.VOLUME_INCREMENT)  # Volume Up
    elif button_index == 4:
        update("Volume Down")
        cc.send(ConsumerControlCode.VOLUME_DECREMENT)  # Volume Down

def handle_website_mode(button_index):
    if button_index == 0:
        update("Open Google")
        kbd.send(Keycode.CONTROL, Keycode.ALT, Keycode.C)  # Open Run dialog
    elif button_index == 1:
        update("Open ChatGPT")
        kbd.send(Keycode.CONTROL, Keycode.ALT, Keycode.G)  # Open Run dialog
    elif button_index == 2:
        update("Open YouTube")
        kbd.send(Keycode.CONTROL, Keycode.ALT, Keycode.Y)  # Open Run dialog
    elif button_index == 3:
        update("Open Mail")
        kbd.send(Keycode.CONTROL, Keycode.ALT, Keycode.M)  # Open Run dialog
    elif button_index == 4:
        update("Open QuraanApp")
        kbd.send(Keycode.CONTROL, Keycode.ALT, Keycode.Q)  # Open Run dialog

# Function to debounce the button press
def debounce(last_state, current_state):
    if last_state and not current_state:  # Transition from high to low
        time.sleep(0.05)  # 50ms debounce time
        return not current_state  # If still pressed after delay, return True
    return False

while True:
    for i, button in enumerate(buttons):
        current_state = button.value
        if debounce(last_state[i], current_state):  # Button pressed with debounce
            if i == 5:  # Mode switch button
                current_mode = (current_mode + 1) % len(modes)
                update(f"-> {modes[current_mode]}")
            else:
                if modes[current_mode] == "Document Mode":
                    handle_document_mode(i)
                elif modes[current_mode] == "Multimedia Mode":
                    handle_multimedia_mode(i)
                elif modes[current_mode] == "Website Mode":
                    handle_website_mode(i)
             
        last_state[i] = current_state  # Update the last state
        
    time.sleep(0.05)  # Main loop delay (reduce for faster response)
