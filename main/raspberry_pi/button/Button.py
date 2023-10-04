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
* MG KIM            2023.08.23      v1.20       add HCAM Capture Button
"""


from button.constant import *
import RPi.GPIO as GPIO
import time
from bluetooth import *
import bluetooth
from PIL import Image
from io import BytesIO
import cv2
import io
import numpy as np
from PIL import ImageFile

class Button:
    def __init__(self, info = None):
        print("SYSTEM ALARM::Button Configure initiating")
        GPIO.setwarnings(False)
        #GPIO.setmode(GPIO.BOARD)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BEACONSCANBUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(YESNOBUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(HANDCAMBUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(HANDCAMCAPTUREBUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.__flag = 0
        self.__sTime = 0
        self.__eTime = 0
        self.__lastInput = 0
        self.__state = ""
        self.info = info
        self.__buttonExitFlag = False
        print("______________BUTTON SET_________________")
        print(f"Button GPIO | infra_search : {BEACONSCANBUTTON}")
        print(f"Button GPIO | yes_button : {YESNOBUTTON}")
        print(f"Button GPIO | text_recognition : {HANDCAMBUTTON}")
        print(f"Button GPIO | camera pick : {HANDCAMCAPTUREBUTTON}")
        print("SYSTEM ALARM::Button Configure initiating Complete")
        self.socket=None

    def _receive_data(self):
        image_data=b''
        self.socket.settimeout(9)
        while True:
            try:
                data=self.socket.recv(1024)
                if not data:
                    break
                image_data+=data
            except bluetooth.btcommon.BluetoothError as e:
                print(e)
                if "timed out" in  str(e):
                    break
                else:
                    print("error somting")
                    break
        try:
            image=Image.open(io.BytesIO(image_data))
            self.info.set_capture_data(image)
            #self.camera=io.BytesIO(image_data)
            image.save("/home/pi/FORK_2023_E2FESTA/main/test.jpg")
        except:
            print("end")
            return
        
    def setLastInputTime(self):
        self.__lastInput = time.time()

    def getLastInputTime(self):
        return self.__lastInput

    # def buttonInput(self):
    #     # print(time.time() - self.getLastInputTime())
    #     if time.time() - self.getLastInputTime() < 0.3:
    #         return None

    #     if GPIO.input(BEACONSCANBUTTON) == GPIO.HIGH:  # Button 1, Beacon Search Input
    #         # print("1 Button Pushed")
    #         self.info.setButtonState(SCAN)
    #         self.setLastInputTime()
    #         return None

    #     elif GPIO.input(HANDCAMBUTTON) == GPIO.HIGH:  # Button 3, Handcam Search Input
    #         # print("3 Button Pushed")
    #         self.info.setButtonState(HAND_CAM)
    #         self.setLastInputTime()
    #         return None

    #     # Yes/No Button의 동작 원리
    #     # 1. self.__flag는 초기 0으로 설정
    #     # 2. Yes/No 버튼이 입력되면 __flag 1로 설정
    #     # 3. __flag상태가 1일 때, Yes/No Button state가 Low인 경우 버튼 입력이 종료 되었다고 판단
    #     # 4. 버튼 입력 종료까지의 시간이 0.5초 이하면 Yes, 0.5초 초과이면 No 버튼으로 판단.

    #     elif self.__flag == 1 and GPIO.input(YESNOBUTTON) == GPIO.LOW:  # Button 2, Yes Button Input
    #         self.eTime = time.time()
    #         elapsedTime = self.eTime - self.sTime
    #         if elapsedTime <= 0.5:
    #             # print("Yes Button Pushed")
    #             self.info.setButtonState(YES)
    #             self.setLastInputTime()
    #         else:  # Button 2, No Button Input
    #             # print("No Button Pushed")
    #             self.info.setButtonState(NO)
    #             self.setLastInputTime()
    #         self.__flag = 0
    #         return None

    #     elif self.__flag == 0 and GPIO.input(YESNOBUTTON) == GPIO.HIGH:
    #         self.__flag = 1
    #         self.sTime = time.time()
    #         return None

    #     elif GPIO.input(HANDCAMCAPTUREBUTTON) == GPIO.HIGH:  # Button 4, HandCam Capture Button Input
    #         self.info.setButtonState(HCAMCAPTURE)
    #         self.setLastInputTime()
    #         return None
    def buttonInput(self):
        # print(time.time() - self.getLastInputTime())

        if self.data == b'1':  # Button 1, Beacon Search Input
            # print("1 Button Pushed")
            self.info.setButtonState(SCAN)
            return None

        elif self.data == b'3':  # Button 3, Handcam Search Input
            self.info.setButtonState(HAND_CAM)
            self._receive_data() 
            self.info.set_return_capture_end_flag(1)  #return capture flag return
            return None

        # Yes/No Button의 동작 원리
        # 1. self.__flag는 초기 0으로 설정
        # 2. Yes/No 버튼이 입력되면 __flag 1로 설정
        # 3. __flag상태가 1일 때, Yes/No Button state가 Low인 경우 버튼 입력이 종료 되었다고 판단
        # 4. 버튼 입력 종료까지의 시간이 0.5초 이하면 Yes, 0.5초 초과이면 No 버튼으로 판단.

        elif self.data == b'2':  # Button 2, Yes Button Input
            self.info.setButtonState(YES)
            return None

        elif self.data == b'-2':
            self.info.setButtonState(NO)
            return None

        elif self.data == b'4':  # Button 4, HandCam Capture Button Input
            self.info.setButtonState(HCAMCAPTURE)
            return None   

    def startButton(self):
        self.socket=BluetoothSocket(RFCOMM)       
        self.socket.connect(('24:DC:C3:C3:33:C6',1))
        while True:
            if self.info.get_terminate_flag():
               break
            try:
                self.data=self.socket.recv(1024)
                print("input button num is",self.data)
                self.buttonInput()
                time.sleep(0.01)
            except bluetooth.btcommon.BluetoothError as e:
                if "timed out" in str(e):
                    continue
            
        self.info.remove_system('button')
        self.info.terminate_thread('button')
