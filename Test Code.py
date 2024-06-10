from microbit import *
import radio

radio.on()
radio.config(channel=55)
mxFrmSz = 8

cachInDat = ""

# Packet Vars
cData = []

# States
receivingData = False

def stateReset(fullReset):
    global cData

    if fullReset:
        reset()
    else:
        cData = []
    return

def finalFormat():
    formatMsg = ""

    return formatMsg

def getPacket(cPacket):

    return

while True:
    # Connection Control =====================================
    RMSG = radio.receive()

    if RMSG and RMSG.startswith("DAT:"):
        getPacket(RMSG)
        cachInDat += RMSG[8:]
        radio.send("ACK:")

    if RMSG and RMSG.startswith("TER:"):
        display.clear()
        receivingData = False
        radio.on()
        display.scroll(cachInDat, wait=True, delay=100)
        cachInDat = ""

    # Sets max size of data per packet from header packet ====
    if RMSG and RMSG.startswith("HED:"):
        mxFrmSz = int(RMSG[8:])
        receivingData = True

    # General Display ========================================
    if not receivingData:
        display.show(Image.ASLEEP)
    if button_a.is_pressed() and button_b.is_pressed():
        display.clear()
        display.scroll("Flushing Data", wait=False, delay=100)
        stateReset(fullReset=False)
    if receivingData:
        display.show(Image.ALL_CLOCKS[int((running_time() / 1000)) % 12])
        sleep(100)
