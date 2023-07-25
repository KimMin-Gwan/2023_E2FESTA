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
import threading
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
    speaker_thread = threading.Thread(target=speaker.tts_read, args=("나비가 시작되었습니다.",))
    button_thread = threading.Thread(target=runButton, args=(button,))
    infrasearch_thread = None
    button_thread.start()


    while True:
        infrasearch_cs = threading.Lock()
        time.sleep(0.1)
        info.cs.acquire()
        buttonState = info.getButtonState()
        print(info.getButtonState())
        info.cs.release()
        if buttonState == SCAN and (infrasearch_thread is None or not infrasearch_thread.is_alive()): # Linux는 or 뒤부터 확인
            info.setButtonState(-1)
            infrasearch_thread = threading.Thread(target=runInfrasearch, args=(speaker, info))
            infrasearch_thread.start()
        elif buttonState == HANDCAM:
            break
    button_thread.join()
    return


if __name__ == "__main__":
    main()
