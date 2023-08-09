import cv2
import numpy as np
import pyrealsense2.pyrealsense2 as rs
import time
import threading


class Camera_Master():
    def __init__(self, info = None, web_monitor = None):
        print("make camera")
        # hand camera init
        self.info = info
        self.web_monitor = web_monitor
        # cv2.CAP_DSHOW : 다이렉트 쇼
        self.handcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 0번 카메라
        self.status = 1
        
        # Configure depth and color streams
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        # Enable RGB stream only
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        
    def RunCamera(self):
        
        self.thread = threading.Thread(target=self.StartWebCam, args=(True))
        self.thread.start()
        return
        
    def swap_camera(self):
        self.thread.join()
        if self.status == 1:
            
            self.thread = threading.Thread(target=self.StartHandCam, args=(True))
            self.thread.start()
            self.status = 2
        else:
            
            self.thread = threading.Thread(target=self.StartWebCam, args=(True))
            self.thread.start()
            self.status = 1
        
    # 카ㅔㅁ라 바뀌는 함수.ㅋㅏ메라 바꿔.
    #  : 
    # self.thread.join()  # 이 스레드 정지
    # thread2 = threading.Thread(target=self.StartHandCam, args=(True))
    
    # flag 를 True로 하면 화면에 출력이 나옴
    def StartHandCam(self, flag = False):
        processed_frame_array=[]

        self.frame = None
        if not self.handcam.isOpened():  # 카메라가 켜지지 않았을 때
            print("Could not open handcam")  # 오류 메시지 출력
            exit()  # 종료

        while self.handcam.isOpened():  # 카메라가 켜졌을 때
            ret, self.frame = self.handcam.read()

            if flag:
                cv2.imshow("Camera", self.frame)  # 창 제목
    
                # if cv2.waitKey(1) & 0xFF == ord('q'):  # q 누르면 나가고 웹캠으로 전환
                #     break
        
                if cv2.waitKey(1) & 0xFF == ord('a'):  # z 누르면 사진 찍기
                    processed_frame_array.extend(self.frame)  # 행렬로 처리된 프레임을 변수에 할당
                    break
            
            if not ret:
                print("Error : Camera did not captured")
                continue
            
            
       
        self.handcam.release()
        # cv2.destroyAllWindows()
        # self.StartWebCam()
        
        # 버튼 바꾸는 함수 실행해




    def StartWebCam(self, flag = False):
        ## License: Apache 2.0. See LICENSE file in root directory.
        ## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.
        # Configure depth and color streams
        # depth cam 제외, rgb 카메라만 사용할 수 있도록 기본 코드에서 수정.
        
        self.frame = None
        
        # Start streaming self.pipeline.start(self.config)
        try:
            while True:
                # Wait for a frame : color
                frames = self.pipeline.wait_for_frames()
                color_frame = frames.get_color_frame()
                
                #if not color_frame:
                #    continue

                # Convert image to numpy array
                self.frame = np.asanyarray(color_frame.get_data())
                if flag:
                    # Show RGB image
                    cv2.namedWindow('RGB Camera', cv2.WINDOW_AUTOSIZE)
                    cv2.imshow('RGB Camera', self.frame)
                    cv2.waitKey(1)
                    
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
                if self.web_monitor.get_swap_button():
                    self.swap_camera()
                    # break
                
            if flag:
                cv2.destroyAllWindows()
                
            self.StartHandCam(False)
    
        finally:
            # Stop streaming
            self.pipeline.stop()
       
    def get_frame(self):
        # 웹캠 return용 (while문 내 return 위치하면, 속도 저하) 
        return self.frame
