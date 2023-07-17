"""
* Project : 2023CDP main
* Program Purpose and Features :
* - Recognize User Button input
* Author : JH KIM
* First Write Date : 2023.07.17
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		Version		History
* JH KIM            2023.07.17		v1.00		First Write
"""
import sys
import time
import threading

sys.path.append('/home/pi/2023_E2FESTA')
from develop.modules.button import *
from develop.modules.InfraSearch import *
from modules.Speaker import *


class information:
    def __init__(self):
        self.__buttonState = -1
        self.cs = threading.Lock()

    def setButtonState(self, state):
        self.cs.acquire()
        self.__buttonState = state
        self.cs.release()

    def getButtonState(self):
        return self.__buttonState


def runButton(button):
    while True:
        button.buttonInput()


def runInfrasearch():
    master = beacon_master()
    speaker = SpeakMaster()
    master.scan_beacon() #주변에서 비콘 스캔
    master.process_beacon()  #스캔 받은 비콘 데이터 처리
    speaker.set_txt(master.get_gtts_data())  #  전달 받은 data를 speak한다.
    speaker.tts_read() 


def main():
    info = information()
    button = Button(info)
    button_thread = threading.Thread(target=runButton, args=(button,))
    button_thread.start()
    while True:
        time.sleep(0.1)
        info.cs.acquire()
        buttonState = info.getButtonState()
        info.cs.release()
        print(info.getButtonState())
        if buttonState == SCAN:
            info.setButtonState(-1)
            runInfrasearch()
        elif buttonState == HANDCAM:
            break
    button_thread.join()
    return


if __name__ == "__main__":
    main()
