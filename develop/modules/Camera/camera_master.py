import cv2
import numpy as np
import pyrealsense2.pyrealsense2 as rs

handcam = cv2.VideoCapture(0)  # 0번 카메라

class Camera():
    def __init__(self):
        print("make camera")
        
    def StartHandCam(self):
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


    def process_video(self, image):
        return image


    def StartWebCam(self):
        ## License: Apache 2.0. See LICENSE file in root directory.
        ## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.
        # Configure depth and color streams
        # depth cam 제외, rgb 카메라만 사용할 수 있도록 기본 코드에서 수정.
        
        # Configure depth and color streams
        pipeline = rs.pipeline()
        config = rs.config()

        # Enable RGB stream only
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        # Start streaming
        pipeline.start(config)

        try:
            while True:
                # Wait for a frame : color
                frames = pipeline.wait_for_frames()
                color_frame = frames.get_color_frame()
                
                if not color_frame:
                    continue

                # Convert image to numpy array
                color_image = np.asanyarray(color_frame.get_data())

                self.process_video(color_image)

                # Show RGB image
                cv2.namedWindow('RGB Camera', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('RGB Camera', color_image)
                cv2.waitKey(1)

        finally:
            # Stop streaming
            pipeline.stop()

        

    def changeCam(self):
        pass
       


def main():
    camera=Camera()

    while True:
        # if-else문: 특정 버튼 누르면 각각의 함수 실행
        if cv2.waitKey(1) & 0xFF == ord('q'): # key 수정 필요
            camera.StartHandCam()
        
        else:
            camera.StartWebCam()
            

if __name__ == "__main__":
    main()