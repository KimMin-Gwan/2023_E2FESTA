import cv2
import numpy as np
import pyrealsense2.pyrealsense2 as rs
import time


class Camera():

    def __init__(self):
        print("make camera")
        
    def StartHandCam(self):
        handcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 0번 카메라
        processed_frame_array=[]

        if not handcam.isOpened():  # 카메라가 켜지지 않았을 때
            print("Could not open handcam")  # 오류 메시지 출력
            exit()  # 종료

        while handcam.isOpened():  # 카메라가 켜졌을 때
            self.status, self.frame = handcam.read()

            if self.status:
                cv2.imshow("Camera", self.frame)  # 창 제목
    
            if cv2.waitKey(1) & 0xFF == ord('q'):  # q 누르면 나가고 웹캠으로 전환
                break
    
            if cv2.waitKey(1) & 0xFF == ord('a'):  # z 누르면 사진 찍기
                processed_frame_array.extend(self.frame)  # 행렬로 처리된 프레임을 변수에 할당
                break
            
        
        #print(processed_frame_array)
       
        handcam.release()
        cv2.destroyAllWindows()
        self.StartWebCam() 


    def web_video(self, image):
        # 웹캠 return용 (while문 내 return 위치하면, 속도 저하)
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

                # Show RGB image
                cv2.namedWindow('RGB Camera', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('RGB Camera', color_image)
                cv2.waitKey(1)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                self.web_video(color_image)
            
            cv2.destroyAllWindows()
            self.StartHandCam()
    
        finally:
            # Stop streaming
            pipeline.stop()
        
       
  


def main():
    camera=Camera()
    camera.StartHandCam()
            

if __name__ == "__main__":
    main()