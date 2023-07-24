import threading
import time
import os
def a():
    while(True):
        print("T1 Thread id",threading.get_ident())
        time.sleep(1)


def b():
    print("여기는 b야 들어오면 안돼",threading.get_ident())
    time.sleep(3)
        
        
        
        
if __name__ == "__main__":
    t1 = threading.Thread(target=a)
    t1.start()
    t2 = None  # t2 변수를 미리 선언해줍니다.

    while True:
        a = int(input("input number"))
        if a == 1 and  t2 is None or not t2.is_alive():
            t2 = threading.Thread(target=b)  # t2 스레드를 매번 새로 생성합니다.
            t2.start()
        else:
            print("retry")
        time.sleep(1)

        