from typing import Any
import numpy as np
from Object_detect import PATH_TO_MODEL, PATH_TO_LABEL, INPUT_MEAN, INPUT_STD
from tensorflow.lite.python.interpreter import Interpreter

class Tools:
    # 생성자
    def __init__(self):
        self.labels = []
        
    # lable 체크
    def __call__(self):
        print('labels : ', self.labels)
    
    # 해석기 생성
    def set_interpreter(self, model_path = PATH_TO_MODEL):
        self.interpreter = Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.__make_details()
    
    # 라벨 가지고 오기
    def set_labels(self, label_path = PATH_TO_LABEL):
        with open(label_path, 'r') as f:
            labels = [line.strip() for line in f.readlines()]
        self.labels = labels
    
    def get_tensor_size(self):
        return self.width, self.height
    
    #텐서 생성
    def __make_details(self):
        self.input_details = self.interpreter.get_input_details()
        self.output_dtails = self.interpreter.get_output_details()
        self.float_input = (self.input_details[0]['dtype'] == np.float32)
        self.height = self.input_details[0]['shape'][1]
        self.width = self.input_details[0]['shape'][2]

    

        
    
        
        