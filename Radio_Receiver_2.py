from microbit import *
import radio

radio.on()
radio.config(channel=55)
mxFrmSz = 8

# Packet Vars
lastPacket = 0
cData = []

# States
receivingData = False


def stateReset(fullReset):
    global cData
    global lastPacket
    global receivingData

    if fullReset:
        reset()
    else:
        cData = []
        lastPacket = 0
        receivingData = False
    return


def finalFormat():
    global cData

    formatMsg = ""
    for x in range(len(cData)):
        formatMsg = formatMsg + cData[x]
    return formatMsg


def requestPacket(packetNum):
    radio.send("REQ:" + str(packetNum))
    return


def getPacket(cPacket):
    global cData
    global lastPacket

    if lastPacket == int(cPacket[4:8]):
        cData.append(cPacket[8:])
        radio.send("ACK:" + cPacket[4:8])
        lastPacket += 1
    else:
        requestPacket(packetNum=lastPacket)
    return


def startTransmission():
    global receivingData
    global lastPacket
    global mxFrmSz

    mxFrmSz = int(RMSG[4:])
    lastPacket += 1
    receivingData = True

    radio.send("ACK:")
    return


def devDebug():
    display.scroll("RData: " + str(receivingData))
    display.scroll("lPacket: " + str(lastPacket))
    return


while True:
    # Connection Control =====================================
    RMSG = radio.receive()
    # Data packet management =================================
    if RMSG and RMSG.startswith("DAT:"):
        getPacket(cPacket=RMSG)
    if RMSG and RMSG.startswith("TER:"):
        display.clear()
        radio.send("TER:")
        display.scroll(finalFormat(), delay=100)
        stateReset(fullReset=False)
    # Sets max size of data per packet from header packet ====
    if RMSG and RMSG.startswith("HED:"):
        startTransmission()
    # General Display ========================================
    if not receivingData:
        display.show(Image.ASLEEP)
    if button_a.is_pressed() and button_b.is_pressed():
        devDebug()
        display.clear()
        display.scroll("Flushing Data", wait=False, delay=100)
        stateReset(fullReset=True)
    if receivingData:
        display.show(Image.ALL_CLOCKS[int((running_time() / 1000)) % 12])
        sleep(100)
