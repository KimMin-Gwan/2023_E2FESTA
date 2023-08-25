import button
import Camera
import InfraSearch
import Monitoring
import naviUtils
import Object_detect
import Speaker
import TextRecognition
from threading import Thread
from button.constant import *


class Main_Function():
    def __init__(self):
        print("SYSTEM ALARM::Initiating Navi")
        self.info = naviUtils.Information()
        self.monitor = Monitoring.Monitor(info=self.info) # 모니터
        self.button = button.Button(info=self.info)  # 버튼
        self.camera = Camera.Camera_Master(info=self.info) # 카메라
        self.speaker = Speaker.SpeakMaster(info=self.info) # 스피커
        self.infra = InfraSearch.Beacon_Master(speaker=self.speaker, info=self.info)  # 인프라 서치
        self.object_detect = Object_detect.Object_detector(info=self.info, camera=self.camera, speaker=self.speaker) # 객체 탐지
        self.txt_recog = TextRecognition.TxtRecognizer(info=self.info, camera=self.camera, speaker=self.speaker) # OCR
        print("SYSTEM ALARM::Initializing Successfully Finishied")


    def start_System(self):
        # Speaker Thread
        print("SYSTEM ALARM::System Start")
        self.info.add_system("speaker")
        self.info.add_thread("speaker")
        speaker_thread = Thread(target=self.speaker.tts_read, args=("나비가 시작되었습니다.",))  # Welcome Sound Thread
        speaker_thread.start()  # Welcome Sound start

        # Button Thread
        print("SYSTEM ALARM::Button System Start")
        self.info.add_system("button")
        self.info.add_thread("button")
        button_thread = Thread(target=self.button.startButton)  # Button Thread
        button_thread.start()  # Button start

        # Camera Start
        print("SYSTEM ALARM::Button System Start")
        self.camera.RunCamera()

        # Object Detection System Start
        print("SYSTEM ALARM::Object_Detection System Start")
        self.object_detect.run_system()

        # main_loop Start
        self.info.add_system("main_loop")
        self.info.add_thread("main_loop")
        loop_thread = Thread(target=self.main_loop)
        loop_thread.start()

        # Monitoring System Start (main_thread)
        self.monitor.start_monitor(self.camera)

    # infra seartch system start
    def _infra_Search(self):
        print("SYSTEM ALARM::Infra_Search System Start")
        self.info.add_system("infra")
        self.info.add_thread("infra")
        self.infra_search_thread = Thread(target=self.infra.runScanBeacon)
        self.infra_search_thread.start()

    # txt recognition system start
    def _text_recognition(self):
        print("SYSTEM ALARM::Text_Recognition System Start")
        self.txt_recog.runRecognition()

    # System Main Loop
    def main_loop(self):
        print("SYSTEM ALARM::Main Loop Starting")
        while True:
            if self.info.get_terminate_flag():
                break

            # check button State
            buttonState = self.info.getButtonState()

            # if alive already, do not start this system again
            # only start since default state
            if buttonState == SCAN and ("infra" not in self.info.get_now_system() and "textRecognizer" not in self.info.get_now_system()):
                self.info.setButtonState(DEFAULT)  # Button state reset
                self._infra_Search()

            # need to check now system alive
            if buttonState == HAND_CAM and ("infra" not in self.info.get_now_system() and "textRecognizer" not in self.info.get_now_system()):
                self.info.setButtonState(DEFAULT)  # Button state reset
                self._text_recognition()

        self.info.remove_system("main_loop")
        self.info.terminate_thread("main_loop")



        

    


