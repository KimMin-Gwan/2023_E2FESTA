import cv2
import numpy as np
import pyrealsense2 as rs


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


    def StartWebCam(self):
        ## License: Apache 2.0. See LICENSE file in root directory.
        ## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.
        # Configure depth and color streams
        
        pipeline = rs.pipeline()
        config = rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))

        found_rgb = False
        for s in device.sensors:
            if s.get_info(rs.camera_info.name) == 'RGB Camera':
                found_rgb = True
                break
        if not found_rgb:
            print("The demo requires Depth camera with Color sensor")
            exit(0)

        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

        if device_product_line == 'L500':
            config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
        else:
            config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        # Start streaming
        pipeline.start(config)

        try:
            while True:

                # Wait for a coherent pair of frames: depth and color
                frames = pipeline.wait_for_frames()
                depth_frame = frames.get_depth_frame()
                color_frame = frames.get_color_frame()
                if not depth_frame or not color_frame:
                    continue

                # Convert images to numpy arrays
                depth_image = np.asanyarray(depth_frame.get_data())
                color_image = np.asanyarray(color_frame.get_data())

                # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
                depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

                depth_colormap_dim = depth_colormap.shape
                color_colormap_dim = color_image.shape

                # If depth and color resolutions are different, resize color image to match depth image for display
                if depth_colormap_dim != color_colormap_dim:
                    resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
                    images = np.hstack((resized_color_image, depth_colormap))
                else:
                    images = np.hstack((color_image, depth_colormap))

                # Show images
                cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('RealSense', images)
                cv2.waitKey(1)

        finally:
            # Stop streaming
            pipeline.stop()

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