"""
* Project : 2023CDP Eddystone Broadcasting Subway ver
* Program Purpose and Features :
* - send broadcasting message
* Author : JH KIM, JH SUN
* First Write Date : 2023.07.04
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		    Version		History
* JH KIM            2023.07.04      v1.00       First Write
"""
import os
import time


class trafficSignal:
    def __init__(self):
        os.system("sudo hciconfig hci0 up")
        os.system("sudo hciconfig hci0 leadv 3")
        self.signal = "U"
        self.leftTime = 6

    def setSignal(self, newSig):
        self.signal = newSig

    def getSignal(self):
        return self.signal

    def trafficBroadcasting(self):
        defaultStr = "sudo hcitool -i hci0 cmd 0x08 0x0008 17 02 01 06 03 03 aa fe 0f 16 aa fe 10 00 "
        SUB = "53 55 42 "
        if self.getSignal() == "U":
            signalStr = "55 "
        else:
            signalStr = "44 "

        Ten = str(self.leftTime // 10 + 30)
        One = str(self.leftTime % 10 + 30)
        sendStr = defaultStr + SUB + "30 30 31 "+ signalStr + Ten + " " + One
        os.system(sendStr)

    def changeTurn(self):
        if self.getSignal() == "U":
            self.setSignal("D")
        elif self.getSignal() == "D":
            self.setSignal("U")
        else:
            exit(1)
        self.leftTime = 12

    def afterOneMin(self):
        time.sleep(60)
        if self.leftTime > 0:
            self.leftTime -= 1
        else:
            self.changeTurn()


def main():
    trafficObj = trafficSignal()
    while True:
        # os.system("sudo hcitool -i hci0 cmd 0x08 0x0008 13 02 01 06 03 03 aa fe 0b 16 aa fe 10 00 74 72 66 52 36 30 00 00 00 00 00 00 00 00 00 00 00 00")
        trafficObj.trafficBroadcasting()
        trafficObj.afterOneMin()


if __name__ == "__main__":
    main()
