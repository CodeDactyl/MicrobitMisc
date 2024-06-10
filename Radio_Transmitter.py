from microbit import *
import radio

# Radio Config
radio.on()
radio.config(channel=55)
mxFrmSz = 8
clockPhase = 0

# Test Data
TESTSTRINGA = "THIS IS NOT TEST"
TESTSTRINGB = "I HATE PYTHON!"

# Packet Info
pcktLst = 0
pcktSnt = 0
pcktlssthrshld = 0.2

# Variables
sendingData = False
cachOutDat = ""
startTime = 0
timeout = 2000
frmNum = 0
waitAck = False
sendTerminate = False
temp = ""


def radSend(str):
    global cachOutDat
    global frmNum
    global sendingData
    global waitAck
    cachOutDat = str
    frmNum = 0
    sendingData = True
    waitAck = False
    return


def radSendFrame(str, int):
    global frmNum
    global mxFrmSz
    global cachOutDat
    global sendTerminate
    global startTime
    global waitAck
    global sendingData
    global pcktSnt
    global pcktLst
    global temp

    startTime = running_time()
    waitAck = True
    pcktSnt += 1

    if (mxFrmSz * frmNum) + mxFrmSz >= len(cachOutDat):
        radio.send("DAT:" + cachOutDat[mxFrmSz * frmNum :])
    else:
        radio.send("DAT:" + cachOutDat[frmNum * mxFrmSz : frmNum * mxFrmSz + mxFrmSz])
    if (mxFrmSz * frmNum) + mxFrmSz >= len(cachOutDat):
        radio.send("TER:")
        waitAck = False
        sendingData = False
        display.scroll("Complete", delay=100)
        cachOutDat = ""
    return


def packetReport():
    display.scroll("Packets Sent:" + str(pcktSnt), delay=100)
    display.scroll("Packets Lost:" + str(pcktLst), delay=100)
    return


while True:
    RMSG = radio.receive()
    if RMSG and RMSG.startswith("ACK:"):
        waitAck = False
        frmNum += 1
    if sendingData and waitAck is False:
        startTime = running_time()
        radSendFrame(str=cachOutDat, int=frmNum)
    if sendingData and waitAck:
        if (running_time() - startTime) >= timeout:
            pcktLst += 1
            radSendFrame(str=cachOutDat, int=frmNum)
    if sendingData is False:
        display.show(Image.ASLEEP)
    if pcktSnt > 0 and pcktLst / pcktSnt >= pcktlssthrshld:
        display.scroll("Unstable", delay=100)
    if button_a.was_pressed():
        radSend(str=TESTSTRINGA)
    if button_b.was_pressed():
        radSend(str=TESTSTRINGB)
    if button_a.is_pressed() and button_b.is_pressed():
        packetReport()
    if sendingData:
        display.scroll("Sending", wait=False, delay=100)
