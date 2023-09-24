
import RPi.GPIO as GPIO
from Object_detect.constant import *
import time
import numpy as np

class Vibrater:
    def __init__(self):
        #GPIO.setmode(GPIO.BCM)
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
        while(True):
            # 최소거리에 바탕이된 진동 피드백 제공
            distance = self.__find_min_dist(distances=distances)
            # 현재 사물의 최소 거리를 바탕으로 진동사이클 지정
            if (self.__check_distance(distance)):
                GIPO.output(VIB_PIN, False)
                time.sleep(self.cycle)
                GIPO.output(VIB_PIN, True)
                time.sleep(self.cycle)
            else:
                self.cycle = VIB_CYCLE
     
            distances.clear()
            
    # 진동 사이클 지정
    def __check_distance(self, distance):
        if distance <= DIST_THRESHOLD and distance >= WARN_THRESHOLD:
            self.cycle = 2
        elif distance <= WARN_THRESHOLD and distance >= DANG_THRESHOLD:
            self.cycle = 1
        elif distance <= DANG_THRESHOLD and distance >= STOP_THRESHOLD:
            self.cycle = 0.5
        elif distance <= STOP_THRESHOLD:
            self.cycle = 0
        else:
            # 거리가 임계거리보다 크다면 False를 반환
            return False
        # 거리가 임계거리보다 작다면 True를 반환
        return True



