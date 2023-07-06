"""
* Project : 2023CDP Eddystone Receiver
* Program Purpose and Features :
* - receive broadcasting message and processing
* Author : JH KIM, JH SUN
* First Write Date : 2023.06.30
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		    Version		History                                                                                 code to fix
* JH SUN			2023.06.30      v1.00	    First Write
* JH KIM            2023.06.30      v1.01       scan func write
* JH SUN            2023.07.02      V1.02       우선순위 큐 사용하여 다수의 eddystone이 들어왔을때 RSSI 가 가장 높은 비콘만 받아온다.             우선순위 큐의 사이즈 개선/시작할때 오류 발생(1회) 
* JH SUN            2023.07.02      V1.02       우선순위큐에서 데이터 추출후 원소 초기화 작업                                                    시작할때 오류 발생(1회) 
* JH SUN            2023 07.02      V1.10       멀티 스레드를 통해 scan과 출력을 각각의 스레드로 관리한다.                                       시작할때 오류 발생(1회)
"""
from bluepy.btle import Scanner, DefaultDelegate
from queue import PriorityQueue
import threading
import time
lock=threading.Lock()
que=PriorityQueue()
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        self.__scan_data__ = {}
        if (DefaultDelegate != None):
            DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        raw = dev.getScanData()
        mac = dev.addr.upper()
        rssi = dev.rssi
        data = {}
        data['raw'] = raw
        data['mac'] = mac
        data['rssi'] = rssi
        self.__scan_data__ = data

    def getScanData(self):
        return self.__scan_data__



def scanData(scanner, duration):   #scan thread func
    while True:
        devices = scanner.scan(duration)
        print("scan end now print",end="\n ")
        print("=============================")
        for dev in devices:
            #print(dev.rssi)
            for (adtype, desc, value) in dev.getScanData():
                #print(value)
                if  "aafe" in value:
                    rssi_power=abs(dev.rssi)   #if big rssi then less recive power 
                    #beaconAdtype = adtype
                    #beaconDesc = desc
                    beaconData = value[8:]  #erase flag
                    lock.acquire()
                    print(rssi_power,beaconData)
                    que.put((rssi_power,beaconData))
                    lock.release()
        
def print_scan_data(duration):    #print thread func
    while True:
        lock.acquire()
        if que.empty():
            time.sleep(duration)
        else:
            rssi_beacon,data=que.get()
            print("Nearest beacon_rssi : ",rssi_beacon,"beacon_data: ",data)
            while que.not_empty:
                que.get()
        lock.release()
        
def main():
    duration = 3
    scan_delegate = ScanDelegate()
    scanner = Scanner().withDelegate(scan_delegate)
    scan_thread=threading.Thread(target=scanData,args=(scanner,duration))
    print_thread=threading.Thread(target=print_scan_data,args=(duration))
    scan_thread.start()
    print_thread.start()
    
    scan_thread.join()
    print_thread.join()

if __name__ == "__main__":
    main()


