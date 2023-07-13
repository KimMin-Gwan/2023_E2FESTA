"""
* Project : 2023CDP Eddystone Broadcasting
* Program Purpose and Features :
* - send broadcasting message
* Author : JH KIM
* First Write Date : 2023.07.03
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		    Version		History
* JH KIM            2023.07.03      v1.00       First Write
* JH KIM            2023.07.03      v1.01       add init code
* JH KIM            2023.07.03      v1.02       creat class
* JH KIM            2023.07.04      v1.03       TRF code modified/start time change 60->30
"""
import os
import time


class trafficSignal:
    def __init__(self):
        os.system("sudo hciconfig hci0 up")
        os.system("sudo hciconfig hci0 leadv 3")
        self.signal = "R"
        self.leftTime = 30

    def setSignal(self, newSig):
        self.signal = newSig

    def getSignal(self):
        return self.signal

    def trafficBroadcasting(self):
        defaultStr = "sudo hcitool -i hci0 cmd 0x08 0x0008 17 02 01 06 03 03 aa fe 0f 16 aa fe 10 00 "
        TRF = "54 52 46 "
        if self.getSignal() == "G":
            signalStr = "47 "
        else:
            signalStr = "52 "

        Ten = str(self.leftTime // 10 + 30)
        One = str(self.leftTime % 10 + 30)
        sendStr = defaultStr + TRF + "30 30 31 "+ signalStr + Ten + " " + One
        os.system(sendStr)

    def changeTurn(self):
        if self.getSignal() == "R":
            self.setSignal("G")
        elif self.getSignal() == "G":
            self.setSignal("R")
        else:
            exit(1)
        self.leftTime = 60

    def afterOneSec(self):
        time.sleep(1)
        if self.leftTime > 0:
            self.leftTime -= 1
        else:
            self.changeTurn()


def main():
    trafficObj = trafficSignal()
    while True:
        # os.system("sudo hcitool -i hci0 cmd 0x08 0x0008 13 02 01 06 03 03 aa fe 0b 16 aa fe 10 00 74 72 66 52 36 30 00 00 00 00 00 00 00 00 00 00 00 00")
        trafficObj.trafficBroadcasting()
        trafficObj.afterOneSec()


if __name__ == "__main__":
    main()
