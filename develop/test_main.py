"""
* Project : 2023 CDP main
* Program Purpose and Features :
* - 2023 CDP main
* Author : JH KIM
* First Write Date : 2023.07.17
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		    Version		History
* JH KIM            2023.07.17		v1.00		First Write
* JH KIM            2023.07.26      v1.01       comment added
* JH KIM            2023.08.11      v1.02       Program optimized
"""
import sys

sys.path.append('/home/pi/2023_E2FESTA')

from develop.modules.button import *
from develop.modules.naviUtils import *
from develop.modules.Speaker import *
from develop.modules.InfraSearch import *



def runButton(button):  # run Button
    button.startButton()


def runInfrasearch(speaker, info):  # run InfraSearch(beacon scan)
    info.setSystemState(SYS_STATE_INFRA)
    master = beacon_master(speaker, info)
    state = master.runScanBeacon()
    info.setSystemState(SYS_STATE_DEFAULT)
    return


def main():
    # class object
    info = information()  # system information object
    button = Button(info)  # button object
    speaker = SpeakMaster(info)  # speaker object

    # Speaker Thread
    speaker_thread = threading.Thread(target=speaker.tts_read, args=("나비가 시작되었습니다.",))  # Welcome Sound Thread
    speaker_thread.start()  # Welcome Sound start

    # Button Thread
    button_thread = threading.Thread(target=runButton, args=(button,))  # Button Thread
    button_thread.start()  # Button start

    infrasearch_thread = None  # infrasearch Init

    while True:
        # print button state
        buttonState = info.getButtonState()
        # print(buttonState)

        # run func
        if buttonState == SCAN and (infrasearch_thread is None or not infrasearch_thread.is_alive()):
            info.setButtonState(DEFAULT)  # Button state reset
            infrasearch_thread = threading.Thread(target=runInfrasearch, args=(speaker, info))  # Infrasearch Thread
            infrasearch_thread.start()  # Thread start
        # elif buttonState == HANDCAM:        # 추후 작성예정
        time.sleep(0.01)
    return


if __name__ == "__main__":
    main()
