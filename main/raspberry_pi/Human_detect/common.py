from typing import Any
import numpy as np
import cv2
from Human_detect.constant import *
#from tensorflow.lite.python.interpreter import Interpreter
import tflite_runtime.interpreter as tflite
import os
import re
from PIL import Image
import collections
from threading import Thread

Object = collections.namedtuple('Object', ['id', 'score', 'bbox']) #오브젝트 라는 튜플 서브 클래스

class BBox(collections.namedtuple('BBox', ['xmin', 'ymin', 'xmax', 'ymax'])):
    __slots__ = ()

class Tools:
    # 생성자
    def __init__(self):
        self.__load_model()
        pass

    def __load_model(self):
        self.__set_interpreter_tpu()
        self.__input_image_size()
        self.interpreter.allocate_tensors()
        self.labels = self.__load_labels()

    # 모델 세팅
    def __set_interpreter_tpu(self, model_file=PATH_TO_MODEL+TPU_MODEL):
        model_file, *device = model_file.split('@')
        self.interpreter = tflite.Interpreter(
            model_path=model_file,
            experimental_delegates=[
                tflite.load_delegate(EDGETPU_SHARED_LIB,
                                     {'device':device[0]} if device else {})
            ]
        )

    # 이미지 인풋
    def set_input(self, image, resample=Image.NEAREST):
        image = image.resize((self.width, self.height), resample)
        self.__input_tensor()[:,:] = image
        self.interpreter.invoke()
        #tensor_index = self.input_detail['index']
        #input = self.interpreter.tensor(tensor_index)()[0]
        #return input
    
    # 넘파이로 변환
    def __input_tensor(self):
        tensor_index = self.input_detail['index']
        return self.interpreter.tensor(tensor_index)()[0]

    # 텐서 인풋 세팅
    def __input_image_size(self):
        self.input_detail = self.interpreter.get_input_details()[0]
        self.height= self.input_detail['shape'][1]
        self.width = self.input_detail['shape'][2]
        self.channels = self.input_detail['shape'][3]

    # 연산결과  반환
    def output_tensor(self, i):
        """한번 양자화된 데이터라면 양자화를 해제한다."""
        output_details = self.interpreter.get_output_details()[i]
        output_data = np.squeeze(self.interpreter.tensor(output_details['index'])()) #실제로 사용중인 배열의 차원수를 줄여줌
        """만약 3차원 배열일때, 반드시 n차원일 필요가 없다면 명시적으로 분석하기 편한 n-x (x<n) 차원배열로 바꿀수 있다.
        ex) [[1,2,3]] => [1,2,3] (2차원배열이지만 굳이 2차원배열일 필요가 없기에 1차원 배열로 바꾸었다)
        """

        if 'quantization' not in output_details: #만약 세부정보가 양자화 되지 않았다면 바로 데이터를 반환
            return output_data

        scale, zero_point = output_details['quantization'] #양자화된 데이터의 scale(범위)와 zero_point(영점)을 받아온다.
        if scale == 0: #만약 범위가 양자화를 하나 마나 똑같다면 
            return output_data - zero_point #데이터를 영점에서 뺀 값을 돌려줌

        return scale * (output_data - zero_point) #위의 상황이 아니라면 범위와 영점을 이용하여 원래 값으로 양자화 해제한다.
    
    def __load_labels(self):
        p = re.compile(r'\s*(\d+)(.+)') #이거 대충 띄어쓰기 같은건데 정규식으로 반환된거 내용을 아래에서 match함수로 긁어올꺼라서 그럼
        with open(PATH_TO_LABEL, 'r', encoding='utf-8') as f:
            lines = (p.match(line).groups() for line in f.readlines()) #라벨 폴더에서 한줄씩 긁어옴
            return {int(num): text.strip() for num, text in lines} #한줄씩 긁어온 내용의 복사본을 반환(딕셔너리)
        
    def get_labels(self):
        return self.labels

    def get_output(self, top_k=TOP_K, image_scale=1.0):
        """Returns list of detected objects."""
        boxes = self.output_tensor(0)
        class_ids = self.output_tensor(1)
        scores = self.output_tensor(2)
        #count = int(self.output_tensor(self.interpreter, 3))
        #박스의 크기, 오브젝트의 아이디(사물의 이름), 얼마나 비슷한지, 몇개 인지


        def make(i): #박스의 크기 제단한 내용을 리턴할 것인데 아래의 make 함수를 재귀하여 사용
            #(재귀하기 때문에 지역변수 사용을 위해 get_output 함수 안에 작성)
            ymin, xmin, ymax, xmax = boxes[i]
            return Object(
                id=int(class_ids[i]),
                score=scores[i],
                bbox=BBox(xmin=np.maximum(0.0, xmin),
                        ymin=np.maximum(0.0, ymin),
                        xmax=np.minimum(1.0, xmax),
                        ymax=np.minimum(1.0, ymax)))

        return [make(i) for i in range(top_k) if scores[i] >= MIN_CONF_THRESHOLD] #재귀해서 리턴시킴
        

class Collision_Preventer:
    def __init__(self, info, camera, distance):
        self.camera = camera
        self.depth = np.array([0,0,0])
        self.flag = False
        self.info = info
        collision_thread= Thread(target=self.get_distance_all,
                                args=(distance,))
        collision_thread.start()
        self.info.add_system("distance_check")
        self.info.add_thread("distance_check")

    def check_object(self, objs, width, height, image_manager):
        min_depth = DIST_THRESHOLD + 1
        frame = image_manager.get_frame()
        for obj in objs:
            x0, y0, x1, y1 = list(obj.bbox)
            x0, y0, x1, y1 = int(x0*width), int(y0*height), int(x1*width), int(y1*height)
            
            # 거리에 대한 리스트 전체를 반환 nparray type
            depth = self.depth[y1:y0, x1:x0]
            # 최소값 검색
            min_depth = np.min(depth)
            frame = self.__draw_distance_object(frame, min_depth, x0, y0, x1, y1)
        # 작성된 프레임으로 재구성
        image_manager.set_frame(frame)

        # 바이브에 동시에 두번의 입력을 주지 않기 위한 대비책
        if min_depth < DIST_THRESHOLD:
            self.flag = True
        # 최소값보다 작으면 여기서 플레그 값을 수정
        else:
            self.flage = False
        return min_depth
    
    # 오브젝트에 대한 거리 작성
    def __draw_distance_object(self, frame, min_depth, x0, y0, x1, y1):
        frame = cv2.putText(frame, str(min_depth), (x0 + (x1-x0), y0 + (y1-y0)), FONT, 0.6, (255, 255, 0), 2)
        return frame
    

    # 상시 동작하는 디스턴스 확인 
    def get_distance_all(self, distance):
        while True:
            if self.info.get_terminate_flag():
                break

            # 만약 바이브가 동작하는 상황이면 하지말고
            if not self.flag:
                self.depth = self.camera.get_depth()
                # 전체 거리 프레임에서 일정 이상 가까운 오브젝트 탐색
                indices = np.where(self.depth < DIST_THRESHOLD)
                count = len(indices[0])
                # 가까운 오프젝트 프레임이 일정 수 이상이면 바이브레이터 동작
                if count > MIN_COUNT:
                        distance[0] = np.min(self.depth)

        self.info.remove_system("distance_check")
        self.info.terminate_thread("distance_check")
                






        
        
