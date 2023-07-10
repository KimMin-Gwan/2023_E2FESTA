#thread_bl.py
"""
* Project : 2023CDP Eddystone Receiver
* Program Purpose and Features :
* - receive broadcasting no thread
* Author : JH KIM, JH SUN
* First Write Date : 2023.06.30
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		    Version		History                                                                                 code to fix
* JH SUN			2023.06.30      v1.00	    thread 안쓰는 버전                                            
"""
from bluepy.btle import Scanner, DefaultDelegate
from queue import PriorityQueue

import threading
import time
from gtts import gTTS
import pygame


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
    


class beacon_master:
    def __init__(self,scanner,duration) -> None:
        self.receive=ReceiveSignal(scanner,duration)
        self.information={}

    def scan_beacon(self):
        self.receive.scanData()

    def get_scan_beacon(self):
        self.information=self.receive.get_scan_data()
        process=ProcessingData(self.information)   #ProcessingData클래스에 인자전달과 생성을 해준다
        process.process_beacon_data()



class ReceiveSignal:  #receive class
    def __init__(self,scanner,duration):
        self.scanner=scanner  #scanner
        self.duration=duration  #scan duration
        self.information_dict={}
    def scanData(self):   #scan thread func
        devices = self.scanner.scan(self.duration)
        print("scan end",end="\n ")
        print("=============================")
        for dev in devices:
            for (adtype, desc, value) in dev.getScanData():
                if  "aafe" in value:
                    rssi_power=abs(dev.rssi)   #if big rssi then less recive power
                    beaconData = value[8:]  #erase flag
                    print(rssi_power,beaconData)
                    key=self.Check_flag(beaconData)
                    self.information_dict[key]=beaconData

        
    def get_scan_data(self):
        return self.information_dict


    def Check_flag(self):
        if "545246" in self.data:
            return "Traffic"
        elif "535542" in self.data:  #SUB subway
            return "Subway"
        else:
            pass #추가 




class ProcessingData:  #data처리 클래스
    def __init__(self,info_dict):
        self.information_dict=info_dict

    def process_beacon_data(self):    #print thread func
            if self.information_dict.empty():
                print("주변에 비콘이 없습니다.")
            else:
                flag=input("위에서 scan받은 데이터중 원하는 데이터를 입력하세요")
                if flag=="Traffic":
                    self.Traffic_sign(flag)
                elif flag=="Subway":
                    self.Subway_sign(flag)

    def Traffic_sign(self,key):
        trafiic_number,color,Ten,One=self.information_dict[key][6:12],self.information_dict[key][12:14],self.information_dict[key][14:16],self.information_dict[key][16:18]  #tuple형태로 data 꺼내오기
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

    def Subway_sign(self,key):
        subway_number,way,Ten,One=self.information_dict[key][6:12],self.information_dict[key][12:14],self.information_dict[key][14:16],self.information_dict[key][16:18]
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
    master=beacon_master(scanner,duration)
    a=input("스캔을 원하시면 1을 입력하세요")
    if a==1:
        master.scan_beacon()
        master.get_scan_beacon()

    else:
        return 0
if __name__ == "__main__":
    main()

