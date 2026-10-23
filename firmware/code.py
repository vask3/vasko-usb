import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

# Инициализация на клавиатурата (USB HID)
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

# Настройка на бутона на GP0 (който свързахме с нетлиста "BTN")
button = digitalio.DigitalInOut(board.GP0)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP  # Използваме вградения pull-up резистор

# Настройка на светодиода на GP1 (нетлиста "LED")
led = digitalio.DigitalInOut(board.GP1)
led.direction = digitalio.DigitalInOut.OUTPUT
led.value = False  # Изключен по подразбиране

print("USB Security Key is ready!")

while True:
    # Проверяваме дали бутонът е натиснат (при pull-up активното състояние е False/Low)
    if not button.value:
        # Светваме светодиода за индикация
        led.value = True
        
        # Малко закъснение против отскачане (debouncing)
        time.sleep(0.2)
        
        # --- ТВОЯТА СИГУРНА ПАРОЛА ИЛИ ТЕКСТ ТУК ---
        # Текстът ще бъде изписан автоматично все едно се пише от клавиатура
        layout.write("MySuperSecretPassword123!\n")
        
        # Изчакваме бутонът да бъде пуснат, за да не се повтаря безкрайно
        while not button.value:
            time.sleep(0.1)
            
        # Изгасваме светодиода
        led.value = False
        
    time.sleep(0.05)
