
import RPi.GPIO as GPIO
from Human_detect.constant import *
import time
import numpy as np

class Vibrater:
    def __init__(self, info):
        #GPIO.setmode(GPIO.BCM)
        self.info = info
        GPIO.setup(VIB_PIN, GPIO.OUT)
        # 진동 사이클
        self.cycle = VIB_CYCLE #초

    # 제공된 거리들중 가장 작은 값을 확인
    def __find_min_dist(self, distances=[DIST_THRESHOLD+1]):
        if len(distances) <= 0:
            distances.append(DIST_THRESHOLD+1)
        distances = np.array(distances)
        dist = np.min(distances)
        return dist
    
    # 진동 사이클 제공
    def give_vib_feedback(self, distances = [DIST_THRESHOLD+1]):
        end_time=0
        while True:
            if self.info.get_terminate_flag():
                break

            if len(distances)==0:
                distances.append(DIST_THRESHOLD+1)
            distance=distances[0]
            if(self.__check_distance(distance)):
                now_time=time.time()
                if(now_time-end_time>self.cycle):
                    GPIO.output(VIB_PIN,True)
                    time.sleep(0.5) 
                    end_time=time.time()
                    GPIO.output(VIB_PIN,False)
                                    
        self.info.remove_system("vib_thread")
        self.info.terminate_thread("vib_thread")
            
            
    # 진동 사이클 지정
    def __check_distance(self, distance):
        if distance <= DIST_THRESHOLD and distance >= WARN_THRESHOLD:
            self.cycle = 2
        elif distance <= WARN_THRESHOLD and distance >= DANG_THRESHOLD:
            self.cycle = 1
        elif distance <= DANG_THRESHOLD and distance >= STOP_THRESHOLD:
            self.cycle = 0.3
        elif distance <= STOP_THRESHOLD:
            self.cycle = 0
        else:
            # 거리가 임계거리보다 크다면 False를 반환
            return False
        # 거리가 임계거리보다 작다면 True를 반환
        return True



