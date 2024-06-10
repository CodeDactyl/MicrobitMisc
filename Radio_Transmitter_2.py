from microbit import *
import radio
import math

# Radio Config
radio.on()
radio.config(channel=55)
mxPcktSz = 8
clockPhase = 0

# Test Data
TESTSTRINGA = "Why is debugging so painful?"
TESTSTRINGB = "The answer is 42"

# Packet Wizard CONSTANTS
pcktLst = 0
pcktSnt = 0
pcktlssthrshld = 0.5
timeout = 1500

# Com Variables
startTime = 0
cachOutDat = ""
slicedPacket = []
cPacket = 0

# State
sendingData = False
waitAck = False


def stateReset(fullReset):
    global sendingData
    global waitAck
    global cPacket
    global slicedPacket

    if fullReset:
        reset()
    else:
        sendingData = False
        waitAck = False
        cPacket = 0
        slicedPacket = []
    return


def nextPacket():
    global waitAck
    global pcktSnt

    radio.send(slicedPacket[cPacket])
    pcktSnt += 1
    waitAck = True
    if cPacket >= len(slicedPacket) - 1:
        stateReset(fullReset=False)
    return


# 4 digit Num formatter
def numFormat(inInt):
    formedInt = ""
    for x in range(4 - len(str(inInt))):
        formedInt += "0"
    formedInt += str(inInt)
    return formedInt


# Formats the packets to be sent
def dataFormat(rawDat):
    global slicedPacket
    pcktCnt = math.ceil(len(rawDat) / mxPcktSz)

    slicedPacket.append("HED:" + str(pcktCnt))
    for x in range(pcktCnt):
        frmLow = mxPcktSz * x
        frmHigh = mxPcktSz * x + mxPcktSz
        slicedPacket.append("DAT:" + numFormat(x + 1) + rawDat[frmLow:frmHigh])
    slicedPacket.append("TER:" + str(pcktCnt))
    return


def startConnection(data):
    global sendingData
    sendingData = True
    dataFormat(rawDat=data)
    return


def packetReport():
    display.scroll("Packets Sent:" + str(pcktSnt), delay=100)
    display.scroll("Packets Lost:" + str(pcktLst), delay=100)
    return


while True:
    # Signal Reception
    RMSG = radio.receive()
    if RMSG and RMSG.startswith("ACK:"):
        cPacket += 1
        waitAck = False
    if RMSG and RMSG.startswith("REQ:"):
        frmNum = int(RMSG[4:])
        waitAck = False
    if RMSG and RMSG.startswith("TER:"):
        stateReset(fullReset=False)
    # Packet Sender
    if sendingData and waitAck is False:
        startTime = running_time()
        nextPacket()
    if sendingData and waitAck:
        if (running_time() - startTime) >= timeout:
            pcktLst += 1
            nextPacket()
    # Network Verification
    if pcktSnt > 0:
        if pcktLst / pcktSnt > pcktlssthrshld:
            display.scroll("Link Dropped:", delay=100)
            packetReport()
            stateReset(fullReset=True)
    # I/O Code
    if button_a.was_pressed():
        startConnection(data=TESTSTRINGA)
    if button_b.was_pressed():
        startConnection(data=TESTSTRINGB)
    if button_a.is_pressed() and button_b.is_pressed():
        display.scroll("LPacket: " + str(cPacket))
    if sendingData:
        display.show(Image.ALL_CLOCKS[int((running_time() / 1000)) % 12])
    else:
        display.show(Image.ASLEEP)
