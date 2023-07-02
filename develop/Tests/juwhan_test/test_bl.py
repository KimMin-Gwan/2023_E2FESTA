"""
* Project : 2023CDP Eddystone Receiver
* Program Purpose and Features :
* - receive broadcasting message and processing
* Author : JH KIM, JH SUN
* First Write Date : 2023.06.30
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		    Version		History
* JH SUN			2023.06.30      v1.00	    First Write
* JH KIM            2023.06.30      v1.01       scan func write
"""
from bluepy.btle import Scanner, DefaultDelegate


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


def scanData(scanner, duration):
    while True:
        devices = scanner.scan(duration)
        for dev in devices:
            #print(dev.rssi)
            for (adtype, desc, value) in dev.getScanData():
                #print(value)
                if  "aafe" in value:
                    beaconAdtype = adtype
                    beaconDesc = desc
                    beaconData = value[8:]
        print("beaconAdtype =", beaconAdtype)
        print("beaconDesc =", beaconDesc)
        print("beaconData =", beaconData)


def main():
    duration = 2
    scan_delegate = ScanDelegate()
    scanner = Scanner().withDelegate(scan_delegate)
    scanData(scanner, duration)


if __name__ == "__main__":
    main()
