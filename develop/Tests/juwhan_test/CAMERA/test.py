import io
import socket
from picamera2 import Picamera2
import cv2
import time
from PIL import Image

# UDP 서버 설정
UDP_IP = '165.229.185.195'
UDP_PORT = 8000

# 카메라 설정 (해상도, 화면 회전 등)

picam2 = Picamera2()
picam2.preview_configuration.main.size = (480,640)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()



# 이미지를 UDP 소켓을 통해 서버로 전송

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.settimeout(1)

#while True:
#    im=picam2.capure_array()
#    time.sleep(2)  # 이미지 전송 간격 (2초로 설정)
    

# 이미지 확인
im=picam2.capture_array()
cv2.imwrite("output.jpg",im)

with open('output.jpg', 'rb') as output_file:
    image_bytes=output_file.read()


#d=image_bytes.flatten()
#s=d.tostring()
print(len(image_bytes))
print(image_bytes[0:1])
#socket.sendto(image_bytes,(UDP_IP,UDP_PORT))



# for i in range(20):


#     print(bytes([i]) + s[i*46080:(i*1)*46080])
#     print("======================")
#     print(i)
#     socket.sendto(bytes([i]) + s[i*46080:(i*1)*46080] ,(UDP_IP,UDP_PORT))

  