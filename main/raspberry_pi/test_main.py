"""
camera test
# 일반 카메라 테스팅 부분 -------------------------------------
import cv2

camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()
    
    if ret:
        cv2.imshow('test_window', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    
camera.release()
cv2.destroyAllWindows()
"""
"""
# 뎊스 카메라 테스팅 부분 -------------------------------------
import Camera
import cv2
import time

def main():
    camera = Camera.Camera_Master()
    camera.RunCamera()


    count = 0
    while True:
        time.sleep(1)
        count += 1
        print(count)
        if count == 5:
            print("Swap camera")
            camera.swap_camera()
            count = 0

  
if __name__ == '__main__':
    main()
"""
"""
#모니터링 테스트

import Camera
import Monitoring


def main():
    monitor = Monitoring.Monitor()
    camera = Camera.Camera_Master()
    camera.RunCamera()
    monitor.start_monitor(camera)

if __name__ == '__main__':
    main()
"""

import Object_detect
import Camera
import Monitoring

def main():
    monitor = Monitoring.Monitor()
    camera = Camera.Camera_Master()
    camera.RunCamera()
    od = Object_detect.Object_detector(camera=camera)

    od.run_system()
    monitor.start_monitor(camera)
      
if __name__ == '__main__':
    main()
"""

import TextRecognition
import Camera
import Object_detect
import Monitoring
import time
from threading import Thread

def main_loop(tr):
    count = 0
    while True:
        time.sleep(1)
        count+=1
        print(count)
        if count == 10:
            print("start txt recog")
            tr.RunRecognition()
            break
    return

def main():
    monitor = Monitoring.Monitor()
    camera = Camera.Camera_Master()
    camera.RunCamera()
    od = Object_detect.Object_detector(camera=camera)
    tr = TextRecognition.TxtRecognizer(camera=camera)

    od.run_system()
    thread1 = Thread(target=main_loop, args=(tr,))
    thread1.start()
    monitor.start_monitor(camera)


if __name__=="__main__":
    main()
"""