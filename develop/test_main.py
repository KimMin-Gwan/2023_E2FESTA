
from modules.InfraSearch import *
import threading
import time
que=PriorityQueue()


def print_a():
    while True:
        print("a")
        time.sleep(0.1)
def main():
    infrasearch()
    
def infrasearch():
    duration =3 
    scan_delegate = ScanDelegate()
    scanner = Scanner().withDelegate(scan_delegate)
    master=beacon_master(scanner,duration)
    
    while(True):
        a=input("스캔을 원하시면 1을 입력하세요")
        if a=="1":
            master.scan_beacon()
            master.process_beacon()
        else:
            continue
        time.sleep(0.1)

if __name__=="__main__":
    main()
    

    scan_thread=threading.Thread(target=infrasearch)  #scan스레드
    print_thread=threading.Thread(target=print_a)  #scan후 처리할 스레드 시작

    scan_thread.start()
    print_thread.start()

    scan_thread.join()
    print_thread.join()
    