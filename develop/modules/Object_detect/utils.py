import cv2
import numpy as np

class Bbox_maker:
    def __init__(self):
        pass
    
class Image_Manager:
    def __init__(self, tool):
        self.frame = None # 3차원 행렬
        self.tool = tool
        self.width = 0
        self.height = 0
        self.init_flag = False
        
    # 이번 루프에서 프레임 특징
    def recog_image(self, frame):
        self.frame = frame
        # 최초에 한번만 연산
        if not self.init_flag:
            height, width, _ = frame.shape
            self.height = height
            self.width = width
            
        return self.height, self.width
        
    # 해석기에 넣을 행렬 형태로 변환 (3차원 -> 4차원)
    def make_input_data(self):
        width, height = self.tool.get_tensor_size()
        rgb_image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        image_resized = cv2.resize(rgb_image, (width, height))
        input_data = np.expand_dims(image_resized, axis = 0) # 4차원 행렬로 재배치
        return input_data
        
        
    