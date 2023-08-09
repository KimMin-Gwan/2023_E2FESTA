#thread_bl.py
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
* JH SUN            2023 07.02      V1.11       dead_lock 발생 해결 priorty_queue에서는 que.notempty()가아닌 not que.empty()사용   멀티스레드 정상 작동                                                      시작할때 오류 발생(1회)
* JH SUN            2023 07.03      V1.20       ReceiveSignal 클래스 생성       
* JH SUN            2023 07.04      V1.21       flag 에 따른 각각 함수 생성          
* JH SUN            2023 07 04      V1.22       SUBWAY 추가 각각의 eddystone 번호 string화 완료   
* JH SUN            2023 07 04      V1.23       Receive 와 Processign 클래스 분리                                               
"""
from bluepy.btle import Scanner, DefaultDelegate
from queue import PriorityQueue

import threading
lock=threading.Lock()
import time
from gtts import gTTS
import pygame
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
    

class ReceiveSignal:  #receive class
    def __init__(self,scanner,duration):
        self.scanner=scanner  #scanner
        self.duration=duration  #scan duration

    def scanData(self):   #scan thread func
        while True:
            devices = self.scanner.scan(self.duration)
            print("scan end",end="\n ")
            print("=============================")
            for dev in devices:
                for (adtype, desc, value) in dev.getScanData():
                    if  "aafe" in value:
                        rssi_power=abs(dev.rssi)   #if big rssi then less recive power
                        beaconData = value[8:]  #erase flag
                        print(rssi_power,beaconData)
                        lock.acquire()
                        que.put((rssi_power,beaconData))
                        lock.release()
            time.sleep(1)



class ProcessingData:  #data처리 클래스
    def __init__(self):
        self.data=""  #비콘 data 초기화
    def process_beacon_data(self):    #print thread func
        while True:

            lock.acquire()
            if que.empty():
                lock.release()
                time.sleep(2)
            else:

                rssi_beacon,data=que.get()
                self.data=data
                flag=self.Check_flag()   #chk flag
                
                if flag=="Traffic":
                    self.Traffic_sign()

                elif flag=="Subway":
                    self.Subway_sign()
                    
                self.Erase_que()  #erase que 
                lock.release() #mutex unlock
                time.sleep(1)
                
    def Erase_que(self):    #priortyqueue use not que.empty()  erase all value 
        while not que.empty():
            que.get()


    def Check_flag(self):
        if "545246" in self.data:
            return "Traffic"
        elif "535542" in self.data:  #SUB subway
            return "Subway"
        else:
            pass #추가 

    def Traffic_sign(self):
        trafiic_number,color,Ten,One=self.data[6:12],self.data[12:14],self.data[14:16],self.data[16:18]  #tuple형태로 data 꺼내오기
        if color=="47": 
            color="초록색"
        elif color=="52":
            color="빨간색"

        trafiic_number_thrid,trafiic_number_second,trafiic_number_first=trafiic_number[0:2],trafiic_number[2:4],trafiic_number[4:6]
        trafiic_number=str(int(trafiic_number_thrid)-30)+str(int(trafiic_number_second)-30)+str(int(trafiic_number_first)-30)
        if int(Ten)-30==0:
            my_str="신호등 입니다. "+"현재 색깔은"+color+"이고 남은 시간은"+str(int(One)-30)+"초 입니다."
        else:
            my_str="신호등 입니다. "+"현재 색깔은"+color+"이고 남은 시간은"+str(int(Ten)-30)+"십"+str(int(One)-30)+"초 입니다."

        print("This is Traffic  traffic_number is : " , trafiic_number,"color : ",color,"left time is ",int(Ten)-30,int(One)-30,"sec")
        self.tts_read(my_str)

    def Subway_sign(self):
        subway_number,way,Ten,One=self.data[6:12],self.data[12:14],self.data[14:16],self.data[16:18]
        if way=="55":
            way="상행선"
        elif way=="44":
            way="하행선"
        
        subway_number_third,subway_number_second,subway_number_first=subway_number[0:2],subway_number[2:4],subway_number[4:6]
        subway_number=str(int(subway_number_third)-30)+str(int(subway_number_second)-30)+str(int(subway_number_first)-30)
        if int(Ten)-30==0:
            my_str=my_str="지하철 입니다. "+"현재"+way+"이고 남은 시간은"+str(int(One)-30)+"분 입니다."
        else:
            my_str=my_str="지하철 입니다. "+"현재"+way+"이고 남은 시간은"+str(int(Ten)-30)+"십"+str(int(One)-30)+"분 입니다."
        print("This is Subway subway_number is : ",subway_number,"Way is ",way,"left time is ",int(Ten)-30,int(One)-30,"min")
        
        
        self.tts_read(my_str)
    def tts_read(self,mytext):
        self.tts=gTTS(text=mytext,lang='ko')

        self.tts.save('test2.mp3')
        pygame.init()
        pygame.mixer.music.load('test2.mp3')
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)


def main():


    duration =3 
    scan_delegate = ScanDelegate()
    scanner = Scanner().withDelegate(scan_delegate)
    receive_signal=ReceiveSignal(scanner,duration)
    processing_signal=ProcessingData()

    scan_thread=threading.Thread(target=receive_signal.scanData)  #scan스레드
    print_thread=threading.Thread(target=processing_signal.process_beacon_data)  #scan후 처리할 스레드 시작

    scan_thread.start()
    print_thread.start()

    scan_thread.join()
    print_thread.join()

if __name__ == "__main__":
    main()

