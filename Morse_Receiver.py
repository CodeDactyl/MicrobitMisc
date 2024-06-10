#Morse Receiver
from microbit import *
import music
import radio

Dot = Image("00000:00000:00900:00000:00000")
Dash = Image("00000:00000:99999:00000:00000")

radio.on()
while True:
  message = radio.receive()
  if message == 'dot':
    display.show(Dot)
    music.play("F5:1")
    display.clear()
    sleep(300)
  elif message == 'dash':
    display.show(Dash)
    music.play("F5:3")
    display.clear()
    sleep(300)
