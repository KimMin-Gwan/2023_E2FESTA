import cv2
# import shutil
# import time


webcam = cv2.VideoCapture(0)  # 0번 카메라
# PATH = 'C:/Users/y2h75/Desktop/hyelim/# 공모전/2023_E2FESTA'

class camera():
    def __init__(self):
        #self.webcam = cv2.VideoCapture(0)  # 0번 카메라
        print("make camera")
        
    def StartHandCam(self):
        if not webcam.isOpened():  # 카메라가 켜지지 않았을 때
            print("Could not open webcam")  # 오류 메시지 출력
            exit()  # 종료

        while webcam.isOpened():  # 카메라가 켜졌을 때
            self.status, self.frame = webcam.read()
            if self.status:
                cv2.imshow("test", self.frame)  # 창 제목
    
            if cv2.waitKey(1) & 0xFF == ord('q'):  # q 누르면 나가기
                break
    
            if cv2.waitKey(1) & 0xFF == ord('a'):  # z 누르면 사진 찍기
                # start = time.time()  # 시작 시간 저장
                # current_dir = os.path.dirname(os.path.abspath(__file__))
                # image_path = os.path.join(current_dir, 'self_camera_test.jpg')
                # cv2.imwrite(image_path, self.frame)  # 사진 저장
                cv2.imwrite('./selfcameratest.jpg', self.frame) # 사진 저장
                # shutil.move(PATH + '/selfcameratest.jpg', PATH + '/develop/Tests/hyelim_test/selfcameratest.jpg') # (기존 폴더, 옮길 폴더)
                # print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간


        webcam.release()
        cv2.destroyAllWindows()
        
#################################################################

# import cv2

# webcam = cv2.VideoCapture(0)  # 0번 카메라

# class camera():
#     def __init__(self):
#         #self.webcam = cv2.VideoCapture(0)  # 0번 카메라
#         print("make camera")
        
#     def StartHandCam(self):
#         if not webcam.isOpened():  # 카메라가 켜지지 않았을 때
#             print("Could not open webcam")  # 오류 메시지 출력
#             exit()  # 종료

#         while webcam.isOpened():  # 카메라가 켜졌을 때
#             self.status, self.frame = webcam.read()
        
#             if self.status:
#                 cv2.imshow("test", self.frame)  # 창 제목
    
#     # i       if cv2.waitKey(1) & 0xFF == ord('q'):  # q 누르면 나가기
#     #             break
    
#     #         if cv2.waitKey(1) & 0xFF == ord('a'):  # a 누르면 사진 찍기
#     #             cv2.imwrite('self camera test.jpg', self.frame) # 사진 저장
                
#         webcam.release()
#         cv2.destroyAllWindows()