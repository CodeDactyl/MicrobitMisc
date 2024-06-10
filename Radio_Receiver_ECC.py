from microbit import *
import radio

radio.on()
radio.config(channel=55)
evenParity = True


def checkParity(Byte):
    errorFound = False
    bitCount = 0

    for x in range(len(Byte)):
        if Byte[x] == "1":
            bitCount += 1
    if evenParity:
        if bitCount % 2 == 1:
            errorFound = True
    if not evenParity:
        if bitCount % 2 == 0:
            errorFound = True
    return errorFound


while True:
    RMSG = radio.receive()

    if RMSG and RMSG.startswith("DAT:"):
        if checkParity(Byte=RMSG[4:0]):
            display.scroll("Error detected in message: " + RMSG)
        else:
            display.scroll("No errors:" + RMSG)
