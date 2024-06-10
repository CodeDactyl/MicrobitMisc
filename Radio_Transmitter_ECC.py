from microbit import *
import radio

# Radio Config
radio.on()
radio.config(channel=55)

# Test Data
TESTSTRINGA = "11110011"
TESTSTRINGB = "00110010"

while True:
    if button_a.was_pressed():
        radio.send("DAT:" + TESTSTRINGA)
    if button_b.was_pressed():
        radio.send("DAT:" + TESTSTRINGB)
    if button_a.is_pressed() and button_b.is_pressed():
        display.clear()

