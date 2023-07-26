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


class Button:
    def __init__(self, info):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(BEACONSCANBUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(YESNOBUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(HANDCAMBUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.__flag = 0
        self.__sTime = 0
        self.__eTime = 0
        self.__lastInput = 0
        self.__state = ""
        self.info = info
        self.__buttonExitFlag = False

    def getState(self):
        self.__lastInput = time.time()
        return self.__state

    def buttonInput(self):
        time.sleep(0.1)
        if time.time() - self.__lastInput < 0.5:
            return None
        if GPIO.input(BEACONSCANBUTTON) == GPIO.HIGH:
            # print("1 Button Pushed")
            self.info.setButtonState(SCAN)
            return None

        elif GPIO.input(HANDCAMBUTTON) == GPIO.HIGH:
            # print("3 Button Pushed")
            self.info.setButtonState(HANDCAM)
            return None

        elif self.__flag == 1 and GPIO.input(YESNOBUTTON) == GPIO.LOW:  # senter
            self.eTime = time.time()
            elapsedTime = self.eTime - self.sTime
            if elapsedTime <= 0.5:
                # print("Yes Button Pushed")
                self.info.setButtonState(YES)
            else:
                # print("No Button Pushed")
                self.info.setButtonState(NO)
            self.__flag = 0
            return None

        elif self.__flag == 0 and GPIO.input(YESNOBUTTON) == GPIO.HIGH:
            self.__flag = 1
            self.sTime = time.time()
            return None

    def setbuttonExitFlag(self, state):
        self.__buttonExitFlag = state

    def getbuttonExitFlag(self, state):
        return self.__buttonExitFlag

    def startButton(self):
        while True:
            if self.getbuttonExitFlag() == True:
                break
            self.buttonInput()
