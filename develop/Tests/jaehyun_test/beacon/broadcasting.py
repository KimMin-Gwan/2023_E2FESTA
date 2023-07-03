"""
* Project : 2023CDP Eddystone Broadcasting
* Program Purpose and Features :
* - send broadcasting message
* Author : JH KIM, JH SUN
* First Write Date : 2023.07.03
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		    Version		History
* JH KIM            2023.07.03      v1.01       First Write
* JH KIM            2023.07.03      v1.01       add init code
* JH KIM            2023.07.03      v1.02       creat class
* JH KIM            2023.07.03      v1.03       add identifyCode
"""
import os
import time

identifyCode = "30 30 31 "

class trafficSignal:
    def __init__(self):
        os.system("sudo hciconfig hci0 up")
        os.system("sudo hciconfig hcio leadv 3")
        self.signal = "R"
        self.leftTime = 60

    def setSignal(self, newSig):
        self.signal = newSig

    def getSignal(self):
        return self.signal

    def trafficBroadcasting(self):
        defaultStr = "sudo hcitool -i hci0 cmd 0x08 0x0008 15 02 01 06 03 03 aa fe 0d 16 aa fe 10 00 "
        trf = "74 72 66 "
        if self.getSignal() == "G":
            signalStr = "42 "
        else:
            signalStr = "52 "

        Ten = str(self.leftTime // 10 + 30)
        One = str(self.leftTime % 10 + 30)
        sendStr = defaultStr + trf + identifyCode + signalStr + Ten + " " + One
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
        if self.leftTime > 0:
            self.leftTime -= 1
        else:
            self.changeTurn()


def main():
    trafficObj = trafficSignal()
    while True:
        # os.system("sudo hcitool -i hci0 cmd 0x08 0x0008 13 02 01 06 03 03 aa fe 0b 16 aa fe 10 00 74 72 66 52 36 30 00 00 00 00 00 00 00 00 00 00 00 00")
        trafficObj.trafficBroadcasting()
        time.sleep(1)
        trafficObj.afterOneSec()


if __name__ == "__main__":
    main()
