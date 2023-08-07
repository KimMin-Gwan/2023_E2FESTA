import cv2
import numpy as np

handcam = cv2.VideoCapture(0)  # 0번 카메라


class Camera():
    def __init__(self):
        print("make camera")
        
    def Starthandcam(self):
        if not handcam.isOpened():  # 카메라가 켜지지 않았을 때
            print("Could not open handcam")  # 오류 메시지 출력
            exit()  # 종료

        while handcam.isOpened():  # 카메라가 켜졌을 때
            self.status, self.frame = handcam.read()

            if self.status:
                cv2.imshow("Camera", self.frame)  # 창 제목
    
            if cv2.waitKey(1) & 0xFF == ord('q'):  # q 누르면 나가기
                break
    
            if cv2.waitKey(1) & 0xFF == ord('a'):  # z 누르면 사진 찍기
                processed_frame_array = self.frame  # 행렬로 처리된 프레임을 변수에 할당
                break

        print(processed_frame_array)
        
        handcam.release()
        cv2.destroyAllWindows()

    

def main():
    camera=Camera()
    camera.Starthandcam()

if __name__ == "__main__":
    main()