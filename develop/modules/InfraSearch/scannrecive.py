# scan n recive.py
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
* JH KIM            2023.08.11      v1.02       source code optimized
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


class ReceiveSignal:  # receive class
    def __init__(self, scanner, duration):
        self.scanner = scanner  # scanner
        self.duration = duration  # scan duration
        self.information_dict = {}

    def scanData(self):  # scan thread func
        devices = self.scanner.scan(self.duration)  # scan beacon for duration
        receiveTime = time.time()       # time check
        print("SYSTEM ALARM::Scanned Data")
        for dev in devices:
            for (adtype, desc, value) in dev.getScanData():
                if KEY in value:    # Verify if the scanned data is NAVI data
                    rssi_power = abs(dev.rssi)  # if big rssi then less recive power
                    beaconData = value[8:]  # erase flag
                    print(rssi_power, beaconData)
                    key = self.Check_flag(beaconData)
                    if key in self.information_dict:
                        if self.information_dict[key][0] < rssi_power:  # 같은 종류의 beacon이 여러개 scan된 경우, rssi power가 가장 큰 비콘 사용
                            self.information_dict[key] = [rssi_power, beaconData,
                                                          receiveTime]  # (tx_power, data, receiveTime)
                        else:
                            continue
                    else:
                        self.information_dict[key] = [rssi_power, beaconData, receiveTime]

        return self.information_dict

    def Check_flag(self, data):
        if TRAFFIC in data:  # Traffic Sign
            return Traffic
        elif SUBWAY in data:  # Subway
            return Subway
        else:  # beacon 종류가 추가 되면 작성
            pass
