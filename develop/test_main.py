
from modules.InfraSearch import *


def main():
    infrasearch()
    
def infrasearch():
    duration =3 
    scan_delegate = ScanDelegate()
    scanner = Scanner().withDelegate(scan_delegate)
    master=beacon_master(scanner,duration)
    
    while(True):
        a=input("스캔을 원하시면 1을 입력하세요")
        if a==1:
            master.scan_beacon()
            master.process_beacon()
        else:
            continue
    

if __name__=="__main__":
    main()
    