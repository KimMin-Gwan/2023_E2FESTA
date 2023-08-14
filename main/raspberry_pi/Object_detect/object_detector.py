#from Object_detect import MIN_CONF_THRESHOLD
from Object_detect import *
import cv2
import numpy as np

MIN_CONF_THRESHOLD = 0.5


class Object_detector():
    def __init__(self, info, camera):
        self.info = info  # 현재 상탱 확인
        self.camera = camera # 카메라 정보 
        self.status = 0 # 0 : 정지, 1 : 동작, 2 : 일시정지
        self.pause_flag = False

        self.cp = Object_detector.Collision_Preventer()
        self.tool = Object_detector.Tools()
        self.tool.set_labels()
        self.image_manager = Object_detector.Image_Manager(self.tool, self.tool.get_labels())
        #self.camera = camera.main_cam() # 카메라 클래스에서 넘겨올 것
    
    def __object_detection(self):
        # 해석기 세팅
        self.tool.set_interpreter()
        # 라벨 세팅

        #반복되는 핵심 와일문
        while True:
            # 일시정지 상태
            if self.pause_flag:
                continue

            ret, frame = self.camera.get_frame()

            if ret:
                width, height = self.image_manager.recog_image(frame)
                input_data = self.image_manager.make_input_data()
                boxes, classes, scores = self.tool.get_object(input_data)

                for i in range(len(scores)):
                    bbox = self.recog_tensor(boxes[i], scores[i], width, height)
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
        self.__object_detection()

    def pause_system(self):
        # 동작중인 시스템을 일시정지
        if self.status == 1:
            self.pause_flag = True
        elif self.status == 2:
            self.pause_flag = False
        else:
            print("Error : System does not work")

        return






            
        
        
        
