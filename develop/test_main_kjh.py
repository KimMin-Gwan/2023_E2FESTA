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

    def setButtonState(self, state):
        self.__buttonState = state

    def getButtonState(self):
        return self.__buttonState


def runButton(button):
    while True:
        button.buttonInput()

def runInfrasearch():
    duration = 2
    scan_delegate = ScanDelegate()
    scanner = Scanner().withDelegate(scan_delegate)
    master=beacon_master(scanner,duration)
    speaker=SpeakMaster()
    master.scan_beacon()
    master.process_beacon()
    speaker.set_txt(master.get_gtts_data())
    speaker.tts_read()


def main():
    info = information()
    button = Button(info)
    button_thread = threading.Thread(target=runButton, args=(button,))
    button_thread.start()
    while True:
        time.sleep(0.1)
        print(info.getButtonState())
        if info.getButtonState() == SCAN:
            runInfrasearch()
        elif info.getButtonState() == HANDCAM:
            break
    button_thread.join()

if __name__ == "__main__":
    main()
