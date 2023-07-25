# speaker_master.py
"""
* Program Purpose and Features :
* - Speaker Master Class
* Author : MG KIM
* First Write Date : 2023.07.11
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		    Version		History                                                                                 code to fix
* MG KIM			2023.07.11      v0.10	    make file
* JH SUN            2023.07.18      v1.00       write SpeakerMaster
* JH KIM            2023.07.20      v1.01       set_txt, tts_read merged
* JH KIM            2023.07.25      v1.02       flag added
"""
import time

from modules.Speaker.utils import *
import threading


class SpeakMaster:
    # 생성자
    def __init__(self):
        pygame.init()
        self.flag = 0 # flag 0으로 초기화 1이면 종료 코드
        self.cs = threading.Lock()

    def setSpeakerFlag(self, state):
        self.flag = state

    def tts_read(self, str):  # speaker class로 들어갈 내용
        self.cs.acquire()
        self.tts = gTTS(text=str, lang='ko')
        self.tts.save('test3.mp3')
        pygame.mixer.music.load('test3.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() and self.flag == 0:
            time.sleep(0.01)
            #pygame.time.Clock().tick(60)
        self.cs.release()
        self.setSpeakerFlag(0)

