#from Object_detect import MIN_CONF_THRESHOLD
from Object_detect.common import *
from Object_detect.constant import *
from Object_detect.utils import *
import cv2
import numpy as np
from threading import Thread


class Object_detector():
    def __init__(self, camera, info = None):
        self.info = info  # 현재 상탱 확인
        self.camera = camera # 카메라 정보 
        self.status = 0 # 0 : 정지, 1 : 동작, 2 : 일시정지
        self.pause_flag = False

        self.cp = Collision_Preventer()
        self.tool = Tools()
        self.tool.set_labels()
        self.image_manager = Image_Manager(self.tool, self.tool.get_labels())
        #self.camera = camera.main_cam() # 카메라 클래스에서 넘겨올 것
    
    def __object_detection(self):
        # 해석기 세팅
        self.tool.set_interpreter()
        # 라벨 세팅

        #반복되는 핵심 와일문
        while True:
            now_camera_set = self.camera.get_status()
            # 일시정지 상태
            #if now_camera_set != 'web':
            #    continue
            if self.pause_flag:
                continue

            frame = self.camera.get_webcam_frame()

            width, height = self.image_manager.recog_image(frame)
            input_data = self.image_manager.make_input_data()
            boxes, classes, scores = self.tool.get_tensor(input_data)

            for i in range(len(scores)):
                bbox = self.tool.recog_tensor(boxes[i], scores[i], width, height)
                if bbox['ymin'] == 0 and bbox['ymax'] == 0:
                   continue
                x, y = self.cp.check_object(bbox)
                depth = self.camera.get_depth(x, y)
                self.image_manager.make_bbox(scores[i], bbox, classes[i])
                self.image_manager.depth_draw(x, y, depth)

            # 테스트용 윈도우 보여주는 창
            #self.image_manager.show_test_window()
            bboxed_frame = self.image_manager.get_bboxed_frame()
            self.camera.set_object_frame(bboxed_frame)

        
    # 실행기
    def run_system(self):
        now_camera_set = self.camera.get_status()
        # 카메라 점검 있어야함
        if now_camera_set == 'hand':
            self.camera.swap_camera()

        self.status = 1  
        object_detector_thread = Thread(target=self.__object_detection)
        object_detector_thread.start()
        #self.__object_detection()

    def pause_system(self):
        # 동작중인 시스템을 일시정지
        if self.status == 1:
            self.pause_flag = True
            self.status = 2
        elif self.status == 2:
            self.pause_flag = False
            self.status = 1  
        else:
            print("Error : System does not work")

        return






            
        
        
        
