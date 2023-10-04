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
* JH KIM            2023.08.11      v1.10       System State added
"""
import time

from Speaker.utils import *
import threading


class SpeakMaster:
    # 생성자
    def __init__(self, info):
        pygame.init()
        self.cs = threading.Lock()
        self.info = info
        self.exitCode = 0

    def tts_read(self, str):  # Speaker Output
        self.cs.acquire()
        self.exitCode = 0
        print("SYSTEM ALARM::Speaker Output({})".format(str))
        self.tts = gTTS(text=str, lang='ko')
        self.tts.save('test3.mp3')
        pygame.mixer.music.load('test3.mp3')
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            if self.info.getSystemState() == 1 and self.info.getButtonState() == 1:
                self.exitCode = 1
                break
            elif self.info.getButtonState() == 2:
                self.exitCode = 2
                break
            elif self.info.getButtonState() == -2:
                self.exitCode = -2
                break
            time.sleep(0.01)
            #pygame.time.Clock().tick(60)
        pygame.mixer.music.stop()
        self.info.setButtonState(-1)
        self.cs.release()
        self.info.remove_system("speaker")
        self.info.terminate_thread("speaker")
        return self.exitCode



