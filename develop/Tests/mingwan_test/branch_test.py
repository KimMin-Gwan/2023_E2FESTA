"""
* Project : 2023CDP Theadind Test of User Button
* Program Purpose and Features :
* - multi threading test user button input
* Author : JH KIM
* First Write Date : 2023.07.13
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		Version		History
* JH KIM            2023.07.13		v1.00		First Write
"""
from modules.Button import *
import threading
import time

def print_a():
    while True:
        print("a")
        time.sleep(0.1)

    # 글자를 카메라로 찍어서 읽으려면 좌우반전을 하면 안 됨
    
    if status:
        cv2.imshow("test", frame)  # 창 제목
    
    if cv2.waitKey(1) & 0xFF == ord('q'):  # q 누르면 나가기
        break
    
    if cv2.waitKey(1) & 0xFF == ord('a'):  # a 누르면 사진 찍기
        cv2.imwrite('self camera test.jpg', frame) # 사진 저장