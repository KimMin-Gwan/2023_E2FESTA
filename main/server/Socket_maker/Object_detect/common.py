from typing import Any
import numpy as np
from Object_detect.constant import *
from tensorflow.lite.python.interpreter import Interpreter
import tflite_runtime.interpreter as tflite
import os

class Tools:
    # 생성자
    def __init__(self):
        self.labels = []
        
    # lable 체크
    def __call__(self):
        print('labels : ', self.labels)
    
    # 해석기 생성
    def set_interpreter(self, model_path = PATH_TO_MODEL, model = MODEL):
        self.interpreter = Interpreter(model_path=model_path+model)
        self.interpreter.allocate_tensors()
        self.__make_details()
        return
    
    def set_interpreter_tpu(self, model_path = PATH_TO_MODEL, model = TPU_MODEL):
        model_path=os.path.join(model_path, model)
        model_path, *device = model_path.split('@')
        self.interpreter = tflite.Interpreter(model_path=model_path,
                                experimental_delegates=[
                                    tflite.load_delegate(EDGETPU_SHARED_LIB
                                    ) #edeTPU 데이터 디바이스에서 받아옴
        ])
        #{'device': device[0]} if device else {}
        self.interpreter.allocate_tensors()
        self.__make_details()
        return
    
    # 라벨 가지고 오기
    def set_labels(self, label_path = PATH_TO_LABEL):
        with open(label_path, 'r') as f:
            labels = [line.strip() for line in f.readlines()]
        self.labels = labels
        return
    
    def get_tensor_size(self):
        return self.width, self.height
    
    def get_labels(self):
        return self.labels
    
    #텐서 생성
    def __make_details(self):
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.float_input = (self.input_details[0]['dtype'] == np.float32)
        self.height = self.input_details[0]['shape'][1]
        self.width = self.input_details[0]['shape'][2]
        return

    # 해석 준비 및 세팅
    def get_tensor(self, input_data):
        self.__init_tensor(input_data)
        boxes, classes, scores = self.__get_tensor_data()

        return boxes, classes, scores
    
    # 텐서 해석 세팅
    def __init_tensor(self, input_data):
        if self.float_input:
            input_data = (np.float32(input_data) - INPUT_MEAN) / INPUT_STD

        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke() # 현재 작업과 분리 시켜서 대기
        return 

    # 해석기로 부터 텐서 데이터 해석
    def __get_tensor_data(self):
        boxes = self.interpreter.get_tensor(self.output_details[1]['index'])[0] # boxes == bbox
        classes = self.interpreter.get_tensor(self.output_details[3]['index'])[0] # classes == 4
        scores = self.interpreter.get_tensor(self.output_details[0]['index'])[0] # output late
        return boxes, classes, scores
            

    # 각 텐서의 bbox 분석 및 사용가능하게 준비
    def recog_tensor(self, boxes, scores, img_width, img_height):
        ymin = 0
        xmin = 0
        ymax = 0
        xmax = 0
        if ((scores > MIN_CONF_THRESHOLD) and (scores <= 1.0)):
            ymin = int(max(1, (boxes[0] * img_height)))
            xmin = int(max(1, (boxes[1] * img_width)))
            ymax = int(min(img_height, (boxes[2] * img_height)))
            xmax = int(min(img_width, (boxes[3] * img_width)))
        bbox= {"ymin":ymin, "xmin":xmin, "ymax":ymax, "xmax":xmax}
        return bbox


class Collision_Preventer:
    def __init__(self, speaker):
        self.speaker = speaker
        pass

    def check_object(self, bbox):
        y = bbox['ymin'] + (bbox['ymax'] - bbox['ymin'])
        x = bbox['xmin'] + (bbox['xmax'] - bbox['xmin'])
        return x, y

    def check_depth(self, depth, classes):
        if depth < 100:
            self.warning_vib()
        return


    def warning_vib(self):
        return

        











    

        
    
        
        