from Object_detect import MIN_CONF_THRESHOLD
from Object_detect import Tools, Bbox_maker, Image_Manager
import cv2
import numpy as np



class Object_detector():
    def __init__(self, info, camera):
        self.info = info  # 현재 상탱 확인
        self.tool = Tools()
        self.image_manager = Image_Manager(self.tool)
        self.bbox_maker = Bbox_maker()
        self.camera = camera
        #self.camera = camera.main_cam() # 카메라 클래스에서 넘겨올 것
        
    def run_system(self, running_type):
        self.__object_detection()
        pass
    
    
    def __object_detection(self):
        self.tool.set_interpreter()
        self.tool.set_labels()
        
        #반복되는 핵심 와일문
        while True:
            ret, frame = self.camera.read() # ret : 정상작동 플레그
            if ret:
                self.image_manager.recog_image(frame)
                input_data = self.image_manager.make_input_data()
                self.tool.init_tensor(input_data)
            
                self.bbox_maker.making_bbox(frame)
            
        
        
        
