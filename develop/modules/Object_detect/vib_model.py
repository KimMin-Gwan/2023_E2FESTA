
import RPi.GPIO as GPIO
import time

"""
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)

while(True):
    GPIO.output(17,False)
    time.sleep(2)
    GPIO.output(17,True)
    time.sleep(2)
"""

class vib:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.OUT)

        self.cycle = 2
    
    def give_vib_feedback(self, distance):
        
        while(distance < DIST_THRESHOLD):
            GIPO.output(17, False)
            time.sleep(self.cycle)
            GIPO.output(17, True)
            time.sleep(self.cycle)
            self.__check_distance(distance)
        
        self.cycle = 2

    def __check_distance(self, distance):
        if distance <= DIST_THRESHOLD and distance >= WARN:
            self.cycle = 2
        elif distance <= WARN and distance >= DANG:
            self.cycle = 1
        elif distance <= DANG and distance >= STOP:
            self.cycle = 0.5
        elif distance <= STOP:
            self.cycle = 0



