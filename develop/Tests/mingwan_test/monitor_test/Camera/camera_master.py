import cv2
import numpy as np
import time
import threading


class Camera_Master():
    def __init__(self, info = None, web_monitor = None):
        print("make camera")
        # hand camera init
        self.info = info
        self.web_monitor = web_monitor
        # cv2.CAP_DSHOW : 다이렉트 쇼
        self.handcam = cv2.VideoCapture(0 )  # 0번 카메라
        self.webcam= cv2.VideoCapture(1 )# 0번 카메라
        self.status = 1
        self.swap_flag = 0
        
        
    def RunCamera(self):
        self.thread = threading.Thread(target=self.StartWebCam, args=(True,))
        self.thread.start()
        return
        
    def swap_camera(self):
        self.swap_flag = 1
        time.sleep(0.1)
        cv2.destroyAllWindows()
        self.thread.join()
        time.sleep(0.1)
        if self.status == 1:
            self.swap_flag = 0
            self.thread = threading.Thread(target=self.StartHandCam, args=(True,))
            self.thread.start()
            self.status = 2
        else:
            self.swap_flag = 0
            self.thread = threading.Thread(target=self.StartWebCam, args=(True,))
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
            if self.swap_flag == 1:
                break

            ret, self.frame = self.handcam.read()

            if flag:
                cv2.imshow("Camera", self.frame)  # 창 제목
    
                # if cv2.waitKey(1) & 0xFF == ord('q'):  # q 누르면 나가고 웹캠으로 전환
                #     break
        
                if cv2.waitKey(1) & 0xFF == ord('q'):  # z 누르면 사진 찍기
                    self.handcam.release()
                    cv2.destroyAllWindows()
                    break

            if not ret:
                print("Error : Camera did not captured")
                continue
            
            
       
        #self.handcam.release()
        # cv2.destroyAllWindows()
        # self.StartWebCam()
        
        # 버튼 바꾸는 함수 실행해

    def StartWebCam(self, flag = False):
        processed_frame_array=[]

        self.frame = None
        if not self.webcam.isOpened():  # 카메라가 켜지지 않았을 때
            print("Could not open handcam")  # 오류 메시지 출력
            exit()  # 종료

        while self.webcam.isOpened():  # 카메라가 켜졌을 때
            if self.swap_flag == 1:
                break
            ret, self.frame = self.webcam.read()

            if flag:
                cv2.imshow("Camera", self.frame)  # 창 제목
    
                # if cv2.waitKey(1) & 0xFF == ord('q'):  # q 누르면 나가고 웹캠으로 전환
                #     break
        
                if cv2.waitKey(1) & 0xFF == ord('q'):  # z 누르면 사진 찍기
                    self.webcam.release()
                    cv2.destroyAllWindows()
                    break
            
            if not ret:
                print("Error : Camera did not captured")
                continue
        # 버튼 바꾸는 함수 실행해
       

    def get_frame(self):
        # 웹캠 return용 (while문 내 return 위치하면, 속도 저하) 
        _, buffer = cv2.imencode('.jpg', self.frame)
        frame = buffer.tobytes()
        return frame
        #return self.frame
