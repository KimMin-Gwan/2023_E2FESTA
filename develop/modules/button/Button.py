"""
* Project : 2023CDP User Button
* Program Purpose and Features :
* - Recognize User Button input
* Author : JH KIM
* First Write Date : 2023.07.10
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		Version		History
* JH KIM            2023.07.10		v1.00		First Write
* JH KIM            2023.07.11		v1.01		add button
* JH KIM            2023.07.13      v1.01       add accessor
"""

from modules.button.constant import *
import RPi.GPIO as GPIO
import time

beaconScanButton = 8
yesNoButton = 10
handCamButton = 12


class Button:
    def __init__(self, info):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(beaconScanButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(yesNoButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(handCamButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.__flag = 0
        self.__sTime = 0
        self.__eTime = 0
        self.__state = ""
        self.info = info

    def getState(self):
        return self.__state

    def buttonInput(self):
        time.sleep(0.1)
        if GPIO.input(beaconScanButton) == GPIO.HIGH: 
            #print("1 Button Pushed")
            self.info.setButtonState(SCAN)
            return None

        elif GPIO.input(handCamButton) == GPIO.HIGH:
            #print("3 Button Pushed")
            self.info.setButtonState(3)
            return None

        elif self.__flag == 1 and GPIO.input(yesNoButton) == GPIO.LOW:    #senter
            self.eTime = time.time()
            elapsedTime = self.eTime - self.sTime
            if elapsedTime <= 0.5:
                #print("Yes Button Pushed")
                self.info.setButtonState(2)
            else:
                #print("No Button Pushed")
                self.info.setButtonState(-2)
            self.__flag = 0
            return None

        elif self.__flag == 0 and GPIO.input(yesNoButton) == GPIO.HIGH:
            self.__flag = 1
            self.sTime = time.time()
            return None


#def main():
#    bu = Button()
#    while True:
#        bu.buttonInput()
#
#if __name__ == "__main__":
#    main()
