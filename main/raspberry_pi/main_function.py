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
        self.monitor = Monitoring.Monitor()
        self.button = button.Button(self.info)
        self.camera = Camera.Camera_Master(self.info, self.monitor)
        self.speaker = Speaker.SpeakMaster(self.info)
        self.infra = InfraSearch.Beacon_Master(self.speaker, self.info)
        self.object_detect = Object_detect.Object_detector(self.info, self.camera)
        self.txt_recog = TextRecognition.TxtRecognizer(self.info, self.camera, self.speaker)
        print("SYSTEM ALARM::Initializing Successfully Finishied")

        self.infra_search_thread = None
        self.object_detection_thread = None
        self.text_recognition_thread = None

    def start_System(self):
        # Speaker Thread
        speaker_thread = Thread(target=self.speaker.tts_read, args=("나비가 시작되었습니다.",))  # Welcome Sound Thread
        speaker_thread.start()  # Welcome Sound start

        # Button Thread
        button_thread = Thread(target=self.button.startButton , args=(button,))  # Button Thread
        button_thread.start()  # Button start

        print("SYSTEM ALARM::Object_Detection System Start")
        self.object_detection_thread = Thread(target=self.object_detect.run_system)
        self.object_detection_thread.start()

    def _infra_Search(self):
        print("SYSTEM ALARM::Infra_Search System Start")
        self.infra_search_thread = Thread(target=self.infra.runScanBeacon)
        self.infra_search_thread.start()

    def _text_recognition(self):
        print("SYSTEM ALARM::Text_Recognition System Start")
        self.text_recognition_thread = Thread(target=self.txt_recog.RunRecognition())
        self.object_detection_thread.start()

    def main_loop(self):
        while True:
            buttonState = self.info.getButtonState()

            if buttonState == SCAN and (self.infra_search_thread is None or not self.infra_search_thread.is_alive()):
                self.info.setButtonState(DEFAULT)  # Button state reset
                self._infra_Search()

            if buttonState == HAND_CAM and (self.text_recognition_thread is None or not self.text_recognition_thread.is_alive()):
                self.info.setButtonState(DEFAULT)  # Button state reset
                self._text_recognition()




        

    


