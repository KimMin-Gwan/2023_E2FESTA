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
* JH KIM            2023.08.09      v1.10       source code optimization
"""
import time

from InfraSearch.processing import ProcessingData
from InfraSearch.scannrecive import ScanDelegate, ReceiveSignal
from bluepy.btle import Scanner
from InfraSearch.utils import *
from InfraSearch.constant import *
import requests


class Beacon_Master:
    def __init__(self, speaker, mainInfo) -> None:
        self.receive = ReceiveSignal(scanner, duration)
        self.process = 0
        self.information = {}
        self.key = ""
        self.flag = ""
        self.data = ""
        self.speaker = speaker
        self.mainInfo = mainInfo

    def scanDataConvertToText(self):
        self.data = "주변에 "
        for i in self.information.keys():
            if i == Traffic:  # 신호등
                self.data += (trf_gtts + ", ")
            elif i == Subway:  # 지하철
                self.data += (sub_gtts + ", ")
        self.data = self.data[:-2]
        self.data += "이 있습니다. 원하시는 정보에 예 버튼을 눌러주세요"

    def scan_beacon(self):
        self.information = self.receive.scanData()  # Beacon Scan
        if not self.information:  # Beacons not scanned
            self.data = "주변에 스캔된 비콘이 없습니다."
            self.start_gtts()  # Speaker Output
            return False
        else:
            self.scanDataConvertToText()  # 스캔된 데이터를 Speaker Output을 위해 변환
            exitCode = self.start_gtts()
            if exitCode == 1:  # Infrasearch exit button input
                return -1

            for dict_key in self.information.keys():
                if dict_key == Subway:
                    self.data = "지하철"
                elif dict_key == Traffic:
                    self.data = "신호등"

                exitCode = self.start_gtts()
                if exitCode == 1:  # Infrasearch exit button input
                    return -1
                sTime = time.time()
                while True:
                    eTime = time.time()
                    if eTime - sTime > 1.5:   # waiting Button Input
                        break
                    if self.mainInfo.getButtonState() == 2 or exitCode == 2:    # Yes Button Input
                        self.mainInfo.setButtonState(-1)
                        self.flag = dict_key
                        return True
            self.data = "버튼이 입력되지 않았습니다."
            self.start_gtts()
            return False

    def start_gtts(self):
        exitCode = self.speaker.tts_read(self.data)  # Speaker Output
        self.data = ""  # data reset
        return exitCode

    def connect_data_base(self):
        url = 'http://'+self.mainInfo.get_IP()+':'+self.mainInfo.get_PORT()+'/rcv?id=ID&id=' + self.flag + '&id=' + self.key  # server로 전달할 id이다.
        response = requests.get(url)
        self.data = response.text + self.data

    def process_beacon(self):  # processes하는 부분이다.
        self.process = ProcessingData(self.information, self.flag)  # ProcessingData Object
        self.process.process_beacon_data()
        # self.connect_data_base()                                  # data_base에 연결하는 경우 주석 해제
        self.data, self.flag, self.key = self.process.return_gtts_mssage()  # prcessing된 message return

    def runScanBeacon(self):
        state = self.scan_beacon()  # beacon scan
        if (state == True):  # beacon scan success
            self.process_beacon()  # beacon data processing
            self.start_gtts()  # speaker output
        
        self.mainInfo.remove_system("infra")
        self.mainInfo.terminate_thread("infra")

        return
