# infra_master.py
"""
* Project : 2023CDP Eddystone Receiver
* Program Purpose and Features :
* - infrastructure explore master class
* Author : JH KIM, JH SUN, MG KIM
* First Write Date : 2023.07.11
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		    Version		History                                                                                 code to fix
* MG KIM			2023.07.11      v0.10	    make from /juwhan_test/split_class.py
* JH SUN            2023.07.18      v1.00       write beacon master
* JH KIM            2023.07.20      v1.01       set_txt, read_tts merged
"""
import time

from modules.InfraSearch.processing import ProcessingData
from modules.InfraSearch.scannrecive import ScanDelegate, ReceiveSignal
from bluepy.btle import Scanner
from modules.InfraSearch.utils import *
from modules.InfraSearch.constant import *
import requests
import threading


class beacon_master:
    def __init__(self, Speaker, mainInfo) -> None:
        self.receive = ReceiveSignal(scanner, duration)
        self.process = 0
        self.information = {}
        self.key = ""
        self.flag = ""
        self.data = ""
        self.speaker = Speaker
        self.mainInfo = mainInfo

    def __call__(self):
        pass

    def scan_beacon(self):  # scan부분
        self.information = self.receive.scanData()  # scan을 한뒤 이러한 데이터가 있음을 알려주고 data를 전달받는다.
        if not self.information:  # 주변에 비콘이없다면
            self.data = "주변에 스캔된 비콘이 없습니다."
            #self.start_gtts()
            speaker_thread = threading.Thread(target=self.start_gtts)
            speaker_thread.start()
            return False
        else:
            self.scan_result_gtts()
            #self.start_gtts()

            for dict_key in self.information.keys():
                if dict_key == Subway:
                    self.data = "지하철"
                elif dict_key == Traffic:
                    self.data = "신호등"
                speaker_thread = threading.Thread(target=self.start_gtts)
                speaker_thread.start()
                #self.start_gtts()
                sTime = time.time()
                while True:
                    eTime = time.time()
                    if eTime - sTime > 3:
                        break
                    if self.mainInfo.getButtonState() == 2:
                        print("Here 2")
                        self.speaker.setSpeakerFlag(1)
                        time.sleep(0.01)
                        self.flag = dict_key
                        self.mainInfo.setButtonState(-1)
                        if speaker_thread.is_alive():
                            speaker_thread.join()
                        return True
            self.data = "버튼이 입력되지 않았습니다."
            speaker_thread = threading.Thread(target=self.start_gtts)
            speaker_thread.start()
            #self.start_gtts()
            return False

    def process_beacon(self):  # processes하는 부분이다.
        self.process = ProcessingData(self.information, self.flag)  # ProcessingData클래스에 인자전달과 생성을 해준다
        self.process.process_beacon_data()

    def get_gtts_data(self):
        self.data, self.flag, self.key = self.process.return_gtts_mssage()  # gtts 데이터를 return해준다.

    def send_server(self):
        url = 'http://43.201.213.223:8080/rcv?id=ID&id=' + self.flag + '&id=' + self.key  # server로 전달할 id이다.
        response = requests.get(url)
        self.data = response.text+self.data

        print("확인할 최종 data======================================", self.data)

    def start_gtts(self):
        self.speaker.tts_read(self.data)
        self.data = ""  # 항상 읽고 data는 초기화 시켜준다.

    def connect_data_base(self):
        self.get_gtts_data()
        self.send_server()
        self.start_gtts()

    def scan_result_gtts(self):
        result = []
        
        self.data = "주변에 "

        for i in self.information.keys():
            if i == Traffic:
                self.data += (trf_gtts+", ")

            elif i == Subway:
                self.data += (sub_gtts+", ")
        self.data = self.data[:-2]

        self.data += "이 있습니다. 원하시는 정보에 예 버튼을 눌러주세요"
        print(self.data)
        speaker_thread = threading.Thread(target=self.start_gtts(), args=())
        speaker_thread.start()
        self.mainInfo.setButtonState(-1)

    def runScanBeacon(self):
        self.mainInfo.setButtonState(-1)
        state = self.scan_beacon()
        if (state == True):  # 주변에 scan된 비콘이있을때
            self.process_beacon()
            self.connect_data_base()
            return
        else:
            return