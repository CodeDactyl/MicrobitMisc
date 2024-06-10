from microbit import *
import radio

radio.on()
radio.config(channel=55)
mxFrmSz = 8

clockPhase = 0
receivingData = False
cachInDat = ""

while True:
    RMSG = radio.receive()

    if RMSG and RMSG.startswith("DAT:"):
        clockPhase += 1
        receivingData = True
        cachInDat = cachInDat + RMSG[4:]
        radio.send("ACK:")

    if RMSG and RMSG.startswith("TER:"):
        display.clear()
        receivingData = False
        radio.on()
        display.scroll(cachInDat, wait=True, delay=100)
        cachInDat = ""

    if button_a.is_pressed() and button_b.is_pressed():
        display.clear()
        display.scroll("Flushing Data", wait=False, delay=100)
        cachInDat = ""

    if not receivingData:
        display.show(Image.ASLEEP)

    if receivingData:
        display.show(Image.ALL_CLOCKS[int(clockPhase % 12)])
        sleep(100)
