
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

from InfraSearch.processing import ProcessingData
from InfraSearch.scannrecive import ScanDelegate, ReceiveSignal
from bluepy.btle import Scanner
import threading

class InfraMaster:
    # 생성자
    def __init__(self):
        self.scan_delegate = ScanDelegate() # 스캐너
        self.scanner = Scanner().withDelegate(self.scan_delegate)
        self.receive_signal = ReceiveSignal() # 수신기 
        self.processer = ProcessingData() # 데이터 처리 

    # 호출자
    def __call__(self):
        pass

    # 실행부
    def run_process(self):
        scan_thread=threading.Thread(target=self.receive_signal.scanData)  #scan스레드
        print_thread=threading.Thread(target=self.processer.process_beacon_data)  #scan후 처리할 스레드 시작

        scan_thread.start()
        print_thread.start()

        scan_thread.join()
        print_thread.join()










