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

class ProcessingData:  #data처리 클래스
    def __init__(self,info_dict):
        self.information_dict=info_dict
        self.text=""
        self.key=""
        self.flag=""
        
        
    def process_beacon_data(self):    #print thread func
            if not self.information_dict:
                
                print("주변에 비콘이 없습니다.")
            else:
                flag=input("위에서 scan받은 데이터중 원하는 데이터를 입력하세요")
                if flag==Traffic:   #TRF
                    self.flag=Traffic
                    self.Traffic_sign(flag)
                elif flag==Subway:
                    self.flag=Subway  #SUB
                    self.Subway_sign(flag)


    def Traffic_sign(self,key):
        trafiic_number,color,Ten,One=self.information_dict[key][6:12],self.information_dict[key][12:14],self.information_dict[key][14:16],self.information_dict[key][16:18]  #tuple형태로 data 꺼내오기
        if color==GREEN: 
            color=Green
            
        elif color==RED:
            color=Red

        trafiic_number_thrid,trafiic_number_second,trafiic_number_first=trafiic_number[0:2],trafiic_number[2:4],trafiic_number[4:6]
        trafiic_number= str(int(str(int(trafiic_number_thrid)-30)+str(int(trafiic_number_second)-30)+str(int(trafiic_number_first)-30)))
        
        if int(Ten)-30==0:
            my_str=Traffic_info+color+" 입니다. "+Left_time+str(int(One)-30)+Second
        else:
            my_str=Traffic_info+color+" 입니다. "+Left_time+str(int(Ten)-30)+"십"+str(int(One)-30)+Second


        print("This is Traffic  traffic_number is : " , trafiic_number,"color : ",color,"left time is ",int(Ten)-30,int(One)-30,"sec")  #콘솔 출력창 확인 위함 나중에 지워질 코드
        self.text=my_str
        self.key=trafiic_number

    def Subway_sign(self,key):
        subway_number,way,Ten,One=self.information_dict[key][6:12],self.information_dict[key][12:14],self.information_dict[key][14:16],self.information_dict[key][16:18]
        if way==UP_LINE:
            way=Up_line
        elif way==DOWN_LINE:
            way=Down_line


        subway_number_third,subway_number_second,subway_number_first=subway_number[0:2],subway_number[2:4],subway_number[4:6]
        subway_number=  str(int(str(int(subway_number_third)-30)+str(int(subway_number_second)-30)+str(int(subway_number_first)-30)))
    
        
        
        if int(Ten)-30==0:
            my_str=Subway_info+Left_time+str(int(One)-30)+Minutes
        else:
            my_str=Subway_info+Left_time+str(int(Ten)-30)+"십"+str(int(One)-30)+Minutes
        print(my_str)
        self.text=my_str
        self.key=subway_number
        
    def return_gtts_mssage(self):
        
        return self.text, self.flag ,self.key
        