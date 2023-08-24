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

import time
import picamera
import cv2
import numpy as np

# 카메라 초기화
camera = picamera.PiCamera()

try:
    # 카메라 미리보기 시작 (선택 사항)
    camera.start_preview()

    # 일정 시간 대기 (미리보기를 위해)
    time.sleep(2)

    # 사진 찍기
    stream = np.empty((camera.resolution[1], camera.resolution[0], 3), dtype=np.uint8)
    camera.capture(stream, 'bgr')

    # OpenCV로 사진 표시
    cv2.imshow('Captured Image', stream)
    cv2.waitKey(0)  # 아무 키나 누를 때까지 대기
    cv2.destroyAllWindows()

finally:
    # 카메라 리소스 해제
    camera.stop_preview()
    camera.close()
