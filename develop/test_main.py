"""
* Project : 2023 CDP main
* Program Purpose and Features :
* - 2023 CDP main
* Author : JH KIM
* First Write Date : 2023.07.17
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		Version		History
* JH KIM            2023.07.17		v1.00		First Write
* JH KIM            2023.07.26      v1.01       comment added
"""
import sys
import threading
import time

sys.path.append('/home/pi/2023_E2FESTA')
from develop.modules.button import *
from develop.modules.InfraSearch import *
from develop.modules.Speaker import *
from class_Information import *


def runButton(button):              # run Button
    button.startButton()


def runInfrasearch(speaker, info):  # run InfraSearch(beacon scan)
    master = beacon_master(speaker, info)
    state=master.runScanBeacon()
    return



def main():
    # class object
    info = information()
    button = Button(info)
    speaker = SpeakMaster(info)


    #speaker.tts_read("나비가 시작되었습니다.")
    speaker_thread = threading.Thread(target=speaker.tts_read, args=("나비가 시작되었습니다.",))   # welcome sound
    speaker_thread.start()


    button_thread = threading.Thread(target=runButton, args=(button,))      # button thread
    button_thread.start()                                                   # button start

    infrasearch_thread = None



    while True:
        # print button state
        info.cs.acquire()
        buttonState = info.getButtonState()
        print(info.getButtonState())
        info.cs.release()

        # run func
        if buttonState == SCAN and (infrasearch_thread is None or not infrasearch_thread.is_alive()):
            info.setButtonState(DEFAULT)
            infrasearch_thread = threading.Thread(target=runInfrasearch, args=(speaker, info))
            infrasearch_thread.start()

        #elif buttonState == HANDCAM:        # Handcam 미구성으로 Handcam버튼 입력시 프로그램 종료

        time.sleep(0.01)

    return


if __name__ == "__main__":
    main()
