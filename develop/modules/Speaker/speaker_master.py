#speaker_master.py
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
"""
from modules.Speaker.utils import *

class SpeakMaster:
    #생성자
    def __init__(self):
        self.text=""
        
    def __call__(self):
        
        pass
    def set_txt(self,txt):
        self.text=txt
    def tts_read(self):  #speaker class로 들어갈 내용
        self.tts=gTTS(text=self.text,lang='ko')
        self.tts.save('test3.mp3')
        
        pygame.init()
        pygame.mixer.music.load('test3.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(15)