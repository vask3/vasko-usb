# 🔑 USB Security Key (RP2040-Zero)

A compact, easy-to-build hardware token and automated credential provider built around the **RP2040-Zero** microcontroller module.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-CircuitPython%20%2F%20Arduino-green.svg)
![EDA](https://img.shields.io/badge/designed%20with-EasyEDA-red.svg)

---

## 📌 Overview

This project is an open-source USB security key designed using **EasyEDA** and optimized for simple SMT manufacturing (e.g., via JLCPCB or PCBWay). When plugged into a computer, it identifies itself as a standard USB HID keyboard and executes custom macros, scripts, or secure credential typing upon a physical button press.

## 🛠️ Hardware Architecture

* **Microcontroller (`U2`):** Waveshare RP2040-Zero module (RP2040 dual-core ARM Cortex-M0+, USB-C, castellated pads).
* **Tactile Button (`SW1`):** `TS-1187A-C-D-B` SMD push button for physical confirmation (`GP0`).
* **Indicator LED (`LED1`):** 0805 SMD LED for status indication (`GP1`).
* **Current-Limiting Resistor (`R1`):** 330Ω 0603 SMD resistor.
* **Decoupling Capacitor (`C1`):** 100nF 0603 SMD capacitor across `3V3` and `GND`.

---

## 🔌 Circuit Net Connections

| Net Label | Connection Point | Description |
| :--- | :--- | :--- |
| `3V3` | RP2040-Zero 3V3 rail | Power supply for circuit & decoupling capacitor |
| `GND` | Common Ground | Ground line for button, LED, and capacitor |
| `BTN` | `GP0` $\rightarrow$ Button Pin 1 | Triggers action when pulled to `GND` |
| `LED` | `GP1` $\rightarrow$ Resistor `R1` | Controls the indicator LED |

---

## 💻 Firmware (CircuitPython)

The device runs **CircuitPython** and uses the `adafruit_hid` library to emulate a USB keyboard.

### 🚀 Setup Instructions

1. Put the **RP2040-Zero** into bootloader mode (hold `BOOT` while connecting USB) and flash the latest CircuitPython `.uf2` image.
2. Copy the `adafruit_hid` library folder into the `lib/` directory on the `CIRCUITPY` drive.
3. Save the following code as `code.py`:

```python
import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# Initialize USB HID Keyboard
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

# Configure Button (GP0) with internal Pull-Up
button = digitalio.DigitalInOut(board.GP0)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# Configure Status LED (GP1)
led = digitalio.DigitalInOut(board.GP1)
led.direction = digitalio.Direction.OUTPUT
led.value = False

while True:
    # Button press drops GP0 to GND (Active LOW)
    if not button.value:
        led.value = True
        time.sleep(0.2)  # Debounce delay
        
        # --- TYPE CREDENTIALS OR MACRO HERE ---
        layout.write("MySuperSecretPassword123!\n")
        
        # Wait until button is released
        while not button.value:
            time.sleep(0.1)
            
        led.value = False
        
    time.sleep(0.05)
