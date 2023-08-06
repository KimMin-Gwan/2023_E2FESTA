import cv2
import numpy as np

webcam = cv2.VideoCapture(0)  # 0번 카메라

class camera():
    def __init__(self):
        print("make camera")
        
    def StartHandCam(self):
        if not webcam.isOpened():  # 카메라가 켜지지 않았을 때
            print("Could not open webcam")  # 오류 메시지 출력
            exit()  # 종료

        while webcam.isOpened():  # 카메라가 켜졌을 때
            self.status, self.frame = webcam.read()
            if self.status:
                cv2.imshow("Camera", self.frame)  # 창 제목
    
            if cv2.waitKey(1) & 0xFF == ord('q'):  # q 누르면 나가기
                break
    
            if cv2.waitKey(1) & 0xFF == ord('a'):  # z 누르면 사진 찍기
                # start = time.time()  # 시작 시간 저장
                # current_dir = os.path.dirname(os.path.abspath(__file__))
                # image_path = os.path.join(current_dir, 'self_camera_test.jpg')
                # cv2.imwrite(image_path, self.frame)  # 사진 저장
                # cv2.imwrite('./selfcameratest.jpg', self.frame) # 사진 저장
                
                # 여기에서 frame을 원하는 로직에 따라 처리합니다.
                # 이 예시에서는 frame을 그대로 사용하겠습니다.


                # 행렬로 처리된 프레임을 변수에 할당
                processed_frame_array = self.frame
                
                break
            
                # 화면에 출력 (이미지를 저장하지 않고 화면에도 표시)
                # cv2.imshow("Processed Frame", processed_frame_array)
                
                # shutil.move(PATH + '/selfcameratest.jpg', PATH + '/develop/Tests/hyelim_test/selfcameratest.jpg') # (기존 폴더, 옮길 폴더)
                # print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간

        print(processed_frame_array)
        
        webcam.release()
        cv2.destroyAllWindows()
