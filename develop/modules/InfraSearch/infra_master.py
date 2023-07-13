
#infra_master.py
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
"""

from modules.InfraSearch.processing import ProcessingData
from modules.InfraSearch.scannrecive import ScanDelegate, ReceiveSignal
from bluepy.btle import Scanner
import threading


class beacon_master:
    def __init__(self,scanner,duration) -> None:
        self.receive=ReceiveSignal(scanner,duration)
        self.process=0
        self.information={}
        
    def __call__(self):
        pass
    
    def scan_beacon(self):  #scan부분
        self.information=self.receive.scanData()   #scan을 한뒤 이러한 데이터가 있음을 알려주고 data를 전달받는다.
    
    def process_beacon(self): #processes하는 부분이다.
        self.process=ProcessingData(self.information)   #ProcessingData클래스에 인자전달과 생성을 해준다
        self.process.process_beacon_data()

    def get_gtts_data(self):
        return self.process.return_gtts_mssage()  #gtts 데이터를 return해준다.        







