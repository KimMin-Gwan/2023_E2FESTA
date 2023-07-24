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


def runInfrasearch(speaker, info):
    master = beacon_master(speaker, info)
    state=master.runScanBeacon()
    return



def main():
    info = information()
    button = Button(info)
    speaker = SpeakMaster()
    speaker.tts_read("나비가 시작되었습니다.")
    button_thread = threading.Thread(target=runButton, args=(button,))
    button_thread.start()

    infrasearch_thread = threading.Thread(target=runInfrasearch, args=(speaker, info))
    while True:
        infrasearch_cs = threading.Lock()
        time.sleep(0.1)
        info.cs.acquire()
        buttonState = info.getButtonState()
        print(info.getButtonState())
        info.cs.release()
        if buttonState == SCAN and not infrasearch_thread.is_alive():
            info.setButtonState(-1)
            infrasearch_thread.start()

            infrasearch_thread.join()
        elif buttonState == HANDCAM:
            break
    button_thread.join()
    return


if __name__ == "__main__":
    main()
