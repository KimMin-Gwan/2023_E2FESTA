import io
import socket
from picamera2 import Picamera2
import time
from PIL import Image

# UDP 서버 설정
UDP_IP = '165.229.185.195'
UDP_PORT = 8000

# 카메라 설정 (해상도, 화면 회전 등)

picam2 = Picamera2()
picam2.preview_configuration.main.size = (1280,720)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()



# 이미지를 UDP 소켓을 통해 서버로 전송
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(1)

    #while True:
    #    im=picam2.capure_array()
    #    time.sleep(2)  # 이미지 전송 간격 (2초로 설정)
        
    stream = io.BytesIO()
    picam2.capture(stream, format='jpeg')
    image_data = stream.getvalue()
    
    # 이미지 확인
    image = Image.open(io.BytesIO(image_data))
    image.show()  # 이미지를 보여줍니다.
    
    # 이미지를 서버로 전송
    client_socket.sendto(image_data, (UDP_IP, UDP_PORT))
    time.sleep(2)  # 이미지 전송 간격 (2초로 설정)
finally:
    picam2.close()