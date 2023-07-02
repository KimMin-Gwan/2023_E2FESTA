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
"""
from bluepy.btle import Scanner, DefaultDelegate
from queue import PriorityQueue
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



def scanData(scanner, duration,que):
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
                    print(rssi_power,beaconData)
                    que.put((rssi_power,beaconData))
        if que.empty():
            print("que is empty()")
            pass
        else:
            rssi_be,data=que.get()  #get data near becon
            print("Nearest becon is ","beacon_rssi: ",rssi_be,"beacon data: ",data)    #get()[0]=rssi ,[1]= data
            while que.not_empty:
                que.get()     #그외의 eddystone의 정보는 다 지운다.

def main():
    que=PriorityQueue()
    duration = 3
    scan_delegate = ScanDelegate()
    scanner = Scanner().withDelegate(scan_delegate)
    scanData(scanner, duration,que)


if __name__ == "__main__":
    main()



