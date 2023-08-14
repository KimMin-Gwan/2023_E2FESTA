"""
* Project : 2023CDP User Button
* Program Purpose and Features :
* - Recognize User Button input
* Author : JH KIM
* First Write Date : 2023.07.10
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		    Version		History
* JH KIM            2023.07.10		v1.00		First Write
* JH KIM            2023.07.11		v1.01		add button
* JH KIM            2023.07.13      v1.01       add accessor
* JH KIM            2023.08.14      v1.10       add HCAM Capture Button
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

    def setLastInputTime(self):
        self.__lastInput = time.time()

    def getLastInputTime(self):
        return self.__lastInput

    def buttonInput(self):
        # print(time.time() - self.getLastInputTime())
        if time.time() - self.getLastInputTime() < 0.3:
            return None

        if GPIO.input(BEACONSCANBUTTON) == GPIO.HIGH:  # Button 1, Beacon Search Input
            # print("1 Button Pushed")
            self.info.setButtonState(SCAN)
            self.setLastInputTime()
            return None

        elif GPIO.input(HANDCAMBUTTON) == GPIO.HIGH:  # Button 3, Handcam Search Input
            # print("3 Button Pushed")
            self.info.setButtonState(HANDCAM)
            self.setLastInputTime()
            return None
        """
        Yes/No Button의 동작 원리
        1. self.__flag는 초기 0으로 설정
        2. Yes/No 버튼이 입력되면 __flag 1로 설정
        3. __flag상태가 1일 때, Yes/No Button state가 Low인 경우 버튼 입력이 종료 되었다고 판단
        4. 버튼 입력 종료까지의 시간이 0.5초 이하면 Yes, 0.5초 초과이면 No 버튼으로 판단.
        """
        elif self.__flag == 1 and GPIO.input(YESNOBUTTON) == GPIO.LOW:  # Button 2, Yes Button Input
            self.eTime = time.time()
            elapsedTime = self.eTime - self.sTime
            if elapsedTime <= 0.5:
                # print("Yes Button Pushed")
                self.info.setButtonState(YES)
                self.setLastInputTime()
            else:  # Button 2, No Button Input
                # print("No Button Pushed")
                self.info.setButtonState(NO)
                self.setLastInputTime()
            self.__flag = 0
            return None

        elif self.__flag == 0 and GPIO.input(YESNOBUTTON) == GPIO.HIGH:
            self.__flag = 1
            self.sTime = time.time()
            return None

        elif GPIO.input(HCAMCAPTUREBUTTON) == GPIO.HIGH:  # Button 4, HandCam Capture Button Input
            self.info.setButtonState(HCAMCAPTURE)
            self.setLastInputTime()
            return None

    def startButton(self):
        while True:
            self.buttonInput()
            time.sleep(0.01)
