"""
* Project : 2023 CDP main
* Program Purpose and Features :
* - main
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

sys.path.append('/home/pi/2023_E2FESTA')
from develop.modules.button import *
from develop.modules.InfraSearch import *
from develop.modules.Speaker import *
from class_Information import *


def runButton(button):
    while True:
        button.buttonInput()


def runInfrasearch():
    duration = 2
    scan_delegate = ScanDelegate()
    scanner = Scanner().withDelegate(scan_delegate)
    master = beacon_master(scanner, duration)
    speaker = SpeakMaster()
    master.scan_beacon()
    master.process_beacon()
    speaker.set_txt(master.get_gtts_data())
    speaker.tts_read()


def main():
    info = information()
    button = Button(info)
    speaker = SpeakMaster()
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
            runInfrasearch(speaker)
        elif buttonState == HANDCAM:
            break
    button_thread.join()
    return


if __name__ == "__main__":
    main()
