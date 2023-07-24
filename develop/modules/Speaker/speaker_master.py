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
* JH SUN            2023.07.18      v0.11       write SpeakerMaster
* JH KIM            2023.07.20      v0.12       set_txt, tts_read merged
"""
from modules.Speaker.utils import *
import threading


class SpeakMaster:
    # 생성자
    def __init__(self):
        pygame.init()
        self.cs = threading.Lock()

    def tts_read(self, str):  # speaker class로 들어갈 내용
        
        self.cs.acquire()
        self.tts = gTTS(text=str, lang='ko')
        self.tts.save('test3.mp3')
        
        
        pygame.mixer.music.load('test3.mp3')
        pygame.mixer.music.play()
        #while pygame.mixer.music.get_busy():
        #    pygame.time.Clock().tick(10)
        self.cs.release()
