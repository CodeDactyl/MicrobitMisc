from microbit import *
import radio
import machine

# Radio Config
radio.on()
radio.config(channel=55)
deviceSelected = 0

# ARP IDs
deviceID = ""
knownDevices = ["None"]

# Input Controls
LButton = "None"

# Constants
splitChar = "#"
String1 = "Hello, Sir"
String2 = "GoodBye"


def initialiseID():
    global deviceID
    deviceID = str(machine.unique_id())
    return


def resetButton():
    global LButton
    LButton = "None"
    return


def chMod():
    return deviceSelected % len(knownDevices)


def echo():
    display.scroll("Echo", wait=False, delay=75)
    radio.send("ARP:" + deviceID)
    return


def resolveARP(ARP):
    global knownDevices

    if ARP[4:] not in knownDevices:
        knownDevices.append(ARP[4:])
        display.scroll("New Device Found", delay=75)
        echo()
    return


def changeChannel():
    global deviceSelected
    deviceSelected += 1
    display.scroll("Channel: " + str(chMod()), delay=75)
    return


def sendMsg(OutMSG):
    radio.send(knownDevices[chMod()] + splitChar + OutMSG)
    display.scroll("Sent To: " + str(chMod()), delay=75)
    return


def receiveMsg(InMSG):
    newMsg = ""
    temp = InMSG.split(splitChar)
    newMsg = str(temp[1])
    return newMsg


# StartUp Code
initialiseID()

while True:
    RMSG = radio.receive()

    if RMSG and RMSG.startswith("ARP:"):
        resolveARP(ARP=RMSG)
    if RMSG and RMSG.startswith(deviceID):
        display.scroll(str(receiveMsg(InMSG=RMSG)), delay=100)

    if button_a.was_pressed():
        if LButton == "None":
            LButton = "A"
            display.scroll("A", delay=75)
        elif LButton == "A":
            display.scroll("AA", delay=75)
            echo()
            resetButton()
        elif LButton == "B":
            display.scroll("BA", delay=75)
            sendMsg(String1)
            resetButton()

    if button_b.was_pressed():
        if LButton == "None":
            LButton = "B"
            display.scroll("B", delay=75)
        elif LButton == "B":
            display.scroll("BB", delay=75)
            changeChannel()
            resetButton()
        elif LButton == "A":
            display.scroll("AB", delay=75)
            sendMsg(String2)
            resetButton()
