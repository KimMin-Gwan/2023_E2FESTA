# camera_master.py
"""
* Program Purpose and Features :
* - Camera Module
* Author : HL YANG, SH PARK, MG KIM
* First Write Date : 2023.08.06
* =================================================================================
* Program history
* =================================================================================
* Author    		Date		    Version		History                                                                           code to fix
* SH PARK			2023.08.07      v0.10	    Making Camera Module
* SH PARK			2023.08.07      v0.11	    init structure
* SH PARK			2023.08.07      v0.12	    change function name
* HL YANG			2023.08.07      v0.20	    make hand camera
* SH PARK			2023.08.07      v0.30	    set intel camera modul
* SH PARK			2023.08.07      v0.31	    make test main file
* MG KIM			2023.08.09      v0.40	    초기 설계 세팅 및 수정
* HL YANG			2023.08.11      v0.50	    Edit Internal Code
* HL YANG			2023.08.13      v0.51	    Writing Internal Code & Annotation
* JH KIM            2023.08.18      v0.52       delete import .pyrealsense2
"""

from tkinter import Frame
import cv2
import numpy as np
import pyrealsense2.pyrealsense2 as rs
import time
import threading
from Camera.constant import *


class Camera_Master():
    def __init__(self, info = None):
        # hand camera init
        print("SYSTEM ALARM::Camera Configure initiating")
        self.info = info
        #self.web_monitor = web_monitor
        self.handcam = cv2.VideoCapture(0)  # 0번 카메라, cv2.CAP_DSHOW : 다이렉트 쇼
        self.status = 2  # 1: Web, 2: Hand
        self.swap_flag = 0  # 0: default, 1: for replacement

        # Configure depth and color streams
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = self.config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))

        # RGB & Depth
        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        self.wait_img = cv2.imread(WAIT_IMG_PATH)
        self.frame = self.wait_img   # 사람이 보기에 최적화된 프레임
        self.raw_frame = self.wait_img # 웹캠에서만 사용하는 날것의 프레임
        print("SYSTEM ALARM::Camera Configure Initiating Complete")


    

    # 카메라 ON
    def RunCamera(self):
        # webcam(기본값) 스레드 실행
        self.pipeline.start(self.config)
        #self.info.setSystemState(newSystem)
        self.info.add_system("camera")
        self.info.add_thread("camera")
        self.thread = threading.Thread(target=self.StartWebCam, args=(TEST_FLAG))  # True로 해둬야 테스트 과정에서 화면 확인 O (없을 시 스레드 종료 불가)
        self.thread.start()
        self.status = 1  # 1: Web, 2: Hand
        return
    

    # 카메라 전환 함수
    def swap_camera(self):
        # 그냥 join 해버리니까 스레드 종료과정에서 StartCam 내부의 while 부근에서 오류가 남
        # 그래서 플래그를 세워 StartCam 내부의 while 문을 종료시켜서 끌 것
        self.swap_flag = 1  # 기본 flag == 0, 멈추려고 할 때는 flag == 1로 설정해주기
        #self.thread.join()
        print('Now Status : ', self.status)

        time.sleep(0.5)
        # WebCam → HandCam
        if self.status == 1:  # Now: Web
            print('starg hand cam')
            self.swap_flag = 0
            self.thread = threading.Thread(target=self.StartHandCam, args=(TEST_FLAG))  # True로 해둬야 테스트 과정에서 화면 확인 O (없을 시 스레드 종료 불가)
            self.thread.start()
            self.status = 2  # Change Cam's status; web > hand
        
        # HandCam → WebCam
        else:
            print('starg web cam')
            self.swap_flag = 0
            self.pipeline.start(self.config)
            self.thread = threading.Thread(target=self.StartWebCam, args=(TEST_FLAG))  # True로 해둬야 테스트 과정에서 화면 확인 O (없을 시 스레드 종료 불가)
            self.thread.start()
            self.status = 1  # Change Cam's status; hand > web

        print('After Status : ', self.status)
        return
    

    # HandCam ON;  flag를 True로 하면 화면에 출력이 나옴
    def StartHandCam(self, flag = False):

        self.frame = None
        if not self.handcam.isOpened():  # 카메라가 켜지지 않았을 때
            print("Could not open handcam")  # 오류 메시지 출력
            exit()  # 종료

        check_flag = False

        #while self.handcam.isOpened():  # 카메라가 켜졌을 때
        while True:
            if self.swap_flag == 1:  # web에서 swap cam 버튼이 눌려 flag 0 > 1 변경, 카메라 전환을 하겠다는 의미
                break

            ret, self.frame = self.handcam.read()

            if flag:
                cv2.imshow("Camera", self.frame)  # 창 제목
    
                if cv2.waitKey(1) & 0xFF == ord('q'):  # q 누르면 나가기
                    break
            
            if not ret:
                if check_flag == False:
                    check_flag = True
                    print("Error : Camera did not captured")
                continue
            else:
                check_flag = False
                
            
        print("System : Terminate Handcam")
        #self.handcam.release()
        #cv2.destroyAllWindows()
        # self.StartWebCam()
        
        # 버튼 바꾸는 함수 실행해 < 필요없을 것 같아서 지움
        # self.swap_camera()


    # WebCam ON
    def StartWebCam(self, flag = False):
        ## License: Apache 2.0. See LICENSE file in root directory.
        ## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.
        # Configure depth and color streams
        # depth cam 제외, rgb 카메라만 사용할 수 있도록 기본 코드에서 수정.
        
        self.frame = None
        
        # Start streaming self.pipeline.start(self.config)
        while True:
            if self.swap_flag == 1:  # web에서 swap cam 버튼이 눌려 flag 0 -> 1 변경, 카메라 전환을 하겠다는 의미
                break

            # Wait for a frame : color
            frames = self.pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()

            #if not color_frame:
            #    continue

            # Convert image to numpy array
            self.depth_image = np.asanyarray(depth_frame.get_data())
            self.raw_frame = np.asanyarray(color_frame.get_data())
            #self.frame = np.asanyarray(color_frame.get_data())
            


            if flag:  # flag == 1로 설정 시(기본값 0) window에 카메라 화면 창 띄우기
                # Show RGB image
                cv2.namedWindow('RGB Camera', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('RGB Camera', self.frame)
                #cv2.imshow('RGB Camera', self.frame)
                cv2.waitKey(1)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):  # q 키 누르면 카메라 창을 종료하도록 설정 후 핸드캠으로 전환됨
                    break
            
            #if self.web_monitor.get_swap_button():  # web 화면에서 카메라 전환 버튼을 눌렀을 때 카메라 전환
                #   self.swap_camera()
                # break
            
        if flag:  # flag == 1로 설정 시(기본값 0) window에 띄워진 카메라 화면 창 닫기
            cv2.destroyAllWindows()
            
        print("System : Terminate Webcam")
        # Stop streaming
        self.pipeline.stop()
       
    def set_object_frame(self, bboxed_frame):
        self.frame = bboxed_frame
       
    # 모니터링용 데이터 처리 (Functions for the web only)
    """ 기존 함수 이름:: def get_frame(self):  // 수정되었다고 알려줘야 함 """
    def get_frame_bytes(self):
        # 웹캠 return용 (while문 내 return 위치할 때 속도 저하) 
        # 바이트 단위로 다시 인코딩
        try:
            _, buffer = cv2.imencode('.jpg', self.frame)
            frame = buffer.tobytes()
        except:
            _, buffer = cv2.imencode('.jpg', self.wait_img)
            frame = buffer.tobytes()
        return frame

    # (버튼을 눌렀을 때) 프레임 가지고 오는 함수
    def get_frame(self):
        return self.frame  # 프레임 반환
    
    def get_webcam_frame(self):
        return self.raw_frame
    
    def get_depth(self, x, y):
        try:
            depth = self.depth_image[x, y]
        except:
            depth = 0

        return depth
    
    def get_status(self):
        #self.status = 1  # 1: Web, 2: Hand
        if self.status == 1:
            return 'web'
        elif self.status == 2:
            return 'hand'
        else:
            return 'default'
        
    
        
