#from Object_detect import MIN_CONF_THRESHOLD
from Human_detect.common import *
from Human_detect.constant import *
from Human_detect.utils import *
from Human_detect.vib_model import *
import cv2
import numpy as np
from threading import Thread
import time


class Human_detector():
    def __init__(self, camera, info = None, speaker = None):
        self.info = info  # 현재 상탱 확인
        self.camera = camera # 카메라 정보 
        self.status = 0 # 0 : 정지, 1 : 동작, 2 : 일시정지
        self.pause_flag = False
        #self.tcp_connector = TCP_connector(info=info)
        #self.udp_connector = UDP_connector(info=info)
        self.tool = Tools() # 로드 모델, 로드 라벨, 텐서 세팅
        self.vib = Vibrater(info=info)
        self.image_manager = Image_Manager()
        self.distance=[DIST_THRESHOLD+1]
        self.cp = Collision_Preventer(info, camera, self.distance) # 검색 시작
        vib_thread = Thread(target=self.vib.give_vib_feedback,args=(self.distance,))
        vib_thread.start()
        self.info.add_system("vib_thread")
        self.info.add_thread("vib_thread")

    def __human_detection(self):
        # 라벨 세팅
        #distance = []
        fps = 1
        #반복되는 핵심 와일문
        while True:
            # 일시정지 상태
            if self.camera.get_status() == 'hand':
                continue

            if self.info.get_terminate_flag():
                break



            # if server connected, using server resorce
            frame = self.camera.get_webcam_frame()
            
            self.camera.set_object_frame(frame)

            continue
            #cv2.imshow("test", frame)
            start_time = time.time()
            width, height, pil_im = self.image_manager.recog_image(frame)

            # 연산 부분
            self.tool.set_input(pil_im)
            objs = self.tool.get_output() # obj 탐색
            # output을 바탕으로 사용가능한 bbox인지 체크 및 그리기
            
            # 발견한 오브젝트의 거리를 분석
            min_depth = self.cp.check_object(objs=objs, width=width, height=height, image_manager=self.image_manager)
            self.distance[0] = min_depth

            fps = round(1.0/(time.time() - start_time), 1)
            self.image_manager.append_text_img(objs=objs,
                                               labels=self.tool.get_labels(),
                                               dur=fps)          
            # bbox된 이미지 데이터를 다시 카메라 프레임으로 설정
            bboxed_frame = self.image_manager.get_frame()
            self.camera.set_object_frame(bboxed_frame)
            self.distance[0]=DIST_THRESHOLD+1

        self.info.remove_system("human_detection")
        self.info.terminate_thread("human_detection")
        return

    
    
    # 실행기
    def run_system(self):
        now_camera_set = self.camera.get_status()
        # 카메라 점검 있어야함
        if now_camera_set == 'hand':
            self.camera.swap_camera()

        self.status = 1 # 텐서 연산을 한다 : 1, 안한다 : 2
        self.info.add_system("human_detection")
        self.info.add_thread("human_detection")
        human_detector_thread = Thread(target=self.__human_detection)
        human_detector_thread.start()
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
            print("ERROR::System does not work")
        return






            
        
        
        
