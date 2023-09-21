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
import RPi.GPIO as GPIO
import time

beaconScanButton = 8
yesNoButton = 10
handCamButton = 12
CaptureButton = 16


class Button:
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(beaconScanButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(yesNoButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(handCamButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(CaptureButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.__flag = 0
        self.__sTime = 0
        self.__eTime = 0
        self.__state = ""

    def getState(self):
        return self.__state

    def buttonInput(self):
        time.sleep(0.1)
        if GPIO.input(beaconScanButton) == GPIO.HIGH:
            print("1 Button Pushed")
            self.state = "SCAN"
            return None

        elif GPIO.input(handCamButton) == GPIO.HIGH:
            print("3 Button Pushed")
            self.state = "CAM"
            return None

        elif GPIO.input(CaptureButton) == GPIO.HIGH:
            print("4 Button Pushed")
            self.state = "CAM"
            return None

        elif self.__flag == 1 and GPIO.input(yesNoButton) == GPIO.LOW:
            self.eTime = time.time()
            elapsedTime = self.eTime - self.sTime
            if elapsedTime <= 0.5:
                print("Yes Button Pushed")
                self.state = "Yes"
            else:
                print("No Button Pushed")
                self.state = "No"
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