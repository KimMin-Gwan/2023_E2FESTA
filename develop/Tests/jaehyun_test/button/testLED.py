"""
* Project : 2023CDP Eddystone Broadcasting
* Program Purpose and Features :
* - send broadcasting message
* Author : JH KIM
* First Write Date : 2023.07.10
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		Version		History
* JH KIM            2023.07.10		v1.00		First Write
* JH KIM            2023.07.11		v1.01		add button
"""
import RPi.GPIO as GPIO
import time

beaconScanButton = 8
yesNoButton = 10
handCamButton = 12


class Button:
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(beaconScanButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(yesNoButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(handCamButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.__flag = 0
        self.__sTime = 0
        self.__eTime = 0

    def flagUp(self):
        self.__flag = 1

    def flagDown(self):
        self.__flag = 0

    def buttonInput(self):
        if GPIO.input(beaconScanButton) == GPIO.HIGH:
            print("1 Button Pushed")
            return None
        elif GPIO.input(handCamButton) == GPIO.HIGH:
            print("3")
        elif self.__flag == 1 and GPIO.input(yesNoButton) == GPIO.LOW:
            self.eTime = time.time()
            elapsedTime = self.eTime - self.sTime
            if elapsedTime <= 1:
                print("Yes Button Pushed")
            else:
                print("No Button Pushed")
            self.__flag = 0
            return None
        elif self.__flag == 0 and GPIO.input(yesNoButton) == GPIO.HIGH:
            self.__flag = 1
            self.sTime = time.time()
            return None


def main():
    bu = Button()
    while True:
        bu.buttonInput()

if __name__ == "__main__":
    main()
