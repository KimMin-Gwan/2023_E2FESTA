#from Object_detect import MIN_CONF_THRESHOLD
from Socket_maker.Object_detect.common import *
from Socket_maker.Object_detect.constant import *
from Socket_maker.Object_detect.utils import *
import cv2
import numpy as np
from threading import Thread
import time


class Object_detector():
    def __init__(self):
        self.status = 0 # 0 : 정지, 1 : 동작, 2 : 일시정지
        self.pause_flag = False

        #self.cp = Collision_Preventer(speaker)
        self.tool = Tools()
        self.tool.set_labels()
        self.image_manager = Image_Manager(self.tool, self.tool.get_labels())
        self.fps = 1
        #vib_thread = Thread(target=self.vib.give_vib_feedback)
        #vib_thread.start()
        #self.camera = camera.main_cam() # 카메라 클래스에서 넘겨올 것
    
    def object_detection(self, frame):
        # 해석기 세팅
        if EDGETPU == True:
            return
        else:
            self.tool.set_interpreter()  # normal


        # 라벨 세팅
        start_time = time.time()
        # 일시정지 상태
        # if server connected, using server resorce

        width, height = self.image_manager.recog_image(frame)
        input_data = self.image_manager.make_input_data()
        boxes, classes, scores = self.tool.get_tensor(input_data)

        self.fps = round(1.0/(time.time() - start_time), 1)
        text = 'FPS : {}'.format(self.fps)
        return (boxes, scores, classes, width, height)


    def pause_system(self):
        # 동작중인 시스템을 일시정지
        if self.status == 1:
            self.pause_flag = True
            self.status = 2
        elif self.status == 2:
            self.pause_flag = False
            self.status = 1  
        else:
            print("ERROR::System does not work")

        return






            
        
        
        
