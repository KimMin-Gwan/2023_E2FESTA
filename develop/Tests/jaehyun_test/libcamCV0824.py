"""
* Project : 2023CDP camera module 3 test file
* Program Purpose and Features :
* - amera module 3 test
* Author : JH KIM
* First Write Date : 2023.08.24
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		Version		History
* JH KIM            2023.08.24		v1.00		First Write
"""

import sys
import libcamera
import cv2
import numpy as np

try:
    libcamera.start()

    # 카메라 초기화
    manager = libcamera.CameraManager()
    camera = manager.get(0)

    # 카메라 해상도 설정 (선택 사항)
    camera_configuration = camera.generate_configuration()
    camera_configuration.at(0).size.width = 1920  # 가로 해상도 설정
    camera_configuration.at(0).size.height = 1080  # 세로 해상도 설정
    camera.configure(camera_configuration)

    # 사진 찍기
    frame = camera.capture()

    # 사진을 OpenCV 형식으로 변환
    frame_np = np.asarray(frame.planes[0].to_ndarray())

    # print out image
    cv2.imshow(frame_np)

finally:
    libcamera.stop()
