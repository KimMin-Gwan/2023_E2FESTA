#scan n recive.py
"""
* Project : 2023CDP Eddystone Receiver
* Program Purpose and Features :
* - ScanDelegate Class
* Author : JH KIM, JH SUN, MG KIM
* First Write Date : 2023.07.11
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		    Version		History                                                                                 code to fix
* MG KIM			2023.07.11      v0.10	    make from /juwhan_test/split_class.py
* JH SUN            2023.07.24      v1.00       receiver writing complete
* JH KIM            2023.07.25      v1.01       dict value modified (power, data)
"""
from bluepy.btle import DefaultDelegate
from modules.InfraSearch.constant import *
import time
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
class ReceiveSignal:  #receive class
    
    def __init__(self,scanner,duration):
        self.scanner=scanner  #scanner
        self.duration=duration  #scan duration
        self.information_dict={}
        
    def scanData(self):   #scan thread func
        devices = self.scanner.scan(self.duration)
        receiveTime = time.time()
        print("scan end",end="\n ")
        print("=============================")
        for dev in devices:
            for (adtype, desc, value) in dev.getScanData():
                if KEY in value:
                    rssi_power=abs(dev.rssi)   #if big rssi then less recive power
                    beaconData = value[8:]  #erase flag
                    print(rssi_power,beaconData)
                    key=self.Check_flag(beaconData)
                    if key in self.information_dict:
                        if self.information_dict[key][0]< rssi_power:
                            self.information_dict[key] = (rssi_power, beaconData, receiveTime)       # (tx_power, data)
                        else:
                            continue
                    else :
                        self.information_dict[key]=(rssi_power, beaconData, receiveTime)
                    
        return self.information_dict  #scan하고 return하는 경우와
    
    def Check_flag(self,data):
        if TRAFFIC in data:
            return Traffic
        
        elif SUBWAY in data:  #SUB subway
            return Subway
    
        else: #이후 모듈추가될때 작성될 코드
            pass
