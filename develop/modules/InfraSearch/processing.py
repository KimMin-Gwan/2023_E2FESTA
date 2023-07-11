#processing.py
"""
* Program Purpose and Features :
* - data processer class
* Author : JH KIM, JH SUN, MG KIM
* First Write Date : 2023.07.11
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		    Version		History                                                                                 code to fix
* MG KIM			2023.07.11      v0.10	    make from /juwhan_test/split_class.py 
* MG KIM			2023.07.11      v0.10	    하드코딩 지양바람 - constnat.py에 기록 
"""


import time
from modules.InfraSearch.constant import *
from gtts import gTTS
import pygame

# class ProcessingData:  #data처리 클래스
#     def __init__(self):
#         self.data=""  #비콘 data 초기화
        
        
        
#     def process_beacon_data(self):    #print thread func
#         while True:

#             lock.acquire()
#             if que.empty():
#                 lock.release()
#                 time.sleep(2)
#             else:

#                 rssi_beacon,data=que.get()
#                 self.data=data
#                 flag=self.Check_flag()   #chk flag
    
#                 if flag=="Traffic":
                    
#                     self.Traffic_sign()

#                 elif flag=="Subway":
#                     self.Subway_sign()
                    
                
#                 self.Erase_que()  #erase que 
#                 lock.release() #mutex unlock
#                 time.sleep(1)
                
                
                
                
#     def Erase_que(self):    #priortyqueue use not que.empty()  erase all value 
#         while not que.empty():
#             que.get()


#     def Check_flag(self):
#         if "545246" in self.data:
#             return "Traffic"
#         elif "535542" in self.data:  #SUB subway
#             return "Subway"
#         else:
#             pass #추가 

#     def Traffic_sign(self):
#         trafiic_number,color,Ten,One=self.data[6:12],self.data[12:14],self.data[14:16],self.data[16:18]  #tuple형태로 data 꺼내오기
#         if color=="47": 
#             color="초록색"
#         elif color=="52":
#             color="빨간색"

#         trafiic_number_thrid,trafiic_number_second,trafiic_number_first=trafiic_number[0:2],trafiic_number[2:4],trafiic_number[4:6]
#         trafiic_number=str(int(trafiic_number_thrid)-30)+str(int(trafiic_number_second)-30)+str(int(trafiic_number_first)-30)
#         if int(Ten)-30==0:
#             my_str="신호등 입니다. "+"현재 색깔은"+color+"이고 남은 시간은"+str(int(One)-30)+"초 입니다."
#         else:
#             my_str="신호등 입니다. "+"현재 색깔은"+color+"이고 남은 시간은"+str(int(Ten)-30)+"십"+str(int(One)-30)+"초 입니다."

#         print("This is Traffic  traffic_number is : " , trafiic_number,"color : ",color,"left time is ",int(Ten)-30,int(One)-30,"sec")
#         self.tts_read(my_str)

#     def Subway_sign(self):
#         subway_number,way,Ten,One=self.data[6:12],self.data[12:14],self.data[14:16],self.data[16:18]
#         if way=="55":
#             way="상행선"
#         elif way=="44":
#             way="하행선"
        
#         subway_number_third,subway_number_second,subway_number_first=subway_number[0:2],subway_number[2:4],subway_number[4:6]
#         subway_number=str(int(subway_number_third)-30)+str(int(subway_number_second)-30)+str(int(subway_number_first)-30)
#         if int(Ten)-30==0:
#             my_str=my_str="지하철 입니다. "+"현재"+way+"이고 남은 시간은"+str(int(One)-30)+"분 입니다."
#         else:
#             my_str=my_str="지하철 입니다. "+"현재"+way+"이고 남은 시간은"+str(int(Ten)-30)+"십"+str(int(One)-30)+"분 입니다."
#         print("This is Subway subway_number is : ",subway_number,"Way is ",way,"left time is ",int(Ten)-30,int(One)-30,"min")
        
        
#         self.tts_read(my_str)

#     # 아래 함수 스피커 패키지로 이동바람
#     def tts_read(self,mytext):
#         self.tts=gTTS(text=mytext,lang='ko')

#         self.tts.save('test2.mp3')
#         pygame.init()
#         pygame.mixer.music.load('test2.mp3')
#         pygame.mixer.music.play()

#         while pygame.mixer.music.get_busy():
#             pygame.time.Clock().tick(10)


class ProcessingData:  #data처리 클래스
    def __init__(self,info_dict):
        self.information_dict=info_dict

    def process_beacon_data(self):    #print thread func
            if not self.information_dict:
                print("주변에 비콘이 없습니다.")
            else:
                flag=input("위에서 scan받은 데이터중 원하는 데이터를 입력하세요")
                if flag==Traffic:
                    self.Traffic_sign(flag)
                elif flag==Subway:
                    self.Subway_sign(flag)

    def Traffic_sign(self,key):
        trafiic_number,color,Ten,One=self.information_dict[key][6:12],self.information_dict[key][12:14],self.information_dict[key][14:16],self.information_dict[key][16:18]  #tuple형태로 data 꺼내오기
        if color==GREEN: 
            color=Green
            
        elif color==RED:
            color=Red

        trafiic_number_thrid,trafiic_number_second,trafiic_number_first=trafiic_number[0:2],trafiic_number[2:4],trafiic_number[4:6]
        trafiic_number=str(int(trafiic_number_thrid)-30)+str(int(trafiic_number_second)-30)+str(int(trafiic_number_first)-30)
        
        if int(Ten)-30==0:
            my_str=Traffic_info+color+Left_time+str(int(One)-30)+Second
        else:
            my_str=Traffic_info+color+Left_time+str(int(Ten)-30)+"십"+str(int(One)-30)+Minutes

        print("This is Traffic  traffic_number is : " , trafiic_number,"color : ",color,"left time is ",int(Ten)-30,int(One)-30,"sec")  #콘솔 출력창 확인 위함 나중에 지워질 코드
        

        self.tts_read(my_str)




    def Subway_sign(self,key):
        subway_number,way,Ten,One=self.information_dict[key][6:12],self.information_dict[key][12:14],self.information_dict[key][14:16],self.information_dict[key][16:18]
        if way==UP_LINE:
            way=Up_line
        elif way==DOWN_LINE:
            way=Down_line
        
        
        subway_number_third,subway_number_second,subway_number_first=subway_number[0:2],subway_number[2:4],subway_number[4:6]
        subway_number=str(int(subway_number_third)-30)+str(int(subway_number_second)-30)+str(int(subway_number_first)-30)
        
        
        
        
        
        if int(Ten)-30==0:
            my_str=my_str=Subway_info+way+Left_time+str(int(One)-30)+Minutes
        else:
            my_str=my_str=Subway_info+way+Left_time+str(int(Ten)-30)+"십"+str(int(One)-30)+Minutes
            



        print("This is Subway subway_number is : ",subway_number,"Way is ",way,"left time is ",int(Ten)-30,int(One)-30,"min")
        self.tts_read(my_str)
        
        
        
    def tts_read(self,mytext):  #speaker class로 들어갈 내용
        self.tts=gTTS(text=mytext,lang='ko')

        self.tts.save('test2.mp3')
        pygame.init()
        pygame.mixer.music.load('test2.mp3')
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)