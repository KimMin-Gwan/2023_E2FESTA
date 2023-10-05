import bluetooth
from PIL import Image
from io import BytesIO
import cv2
import io
import numpy as np
from PIL import ImageFile
import time
ImageFile.LOAD_TRUNCATED_IMAGES = True
# ESP32-CAM의 Bluetooth 주소
esp32_mac_address = '24:DC:C3:C3:33:C6'  # ESP32-CAM의 주소로 변경

# Bluetooth 서버 소켓 생성
server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

server_socket.connect(('24:DC:C3:C3:33:C6',1))
end_time=0
# ESP32-CAM 연결 대기
while True: 
    data_num=server_socket.recv(1024)
    print(data_num)
    if(data_num==b"3"):
    # 이미지 수신 및 저장
        print("now you can recieve data")
        image_data=b''
        server_socket.settimeout(6)
        ct=0
        while True:
            try:
                data = server_socket.recv(1024)  # 이미지 데이터를 1024 바이트씩 받음
                if not data:
                    break
                #=frame.reshape(480,640,3)
                # if not data:
                # image=Image.fromarray(frame,mode="L")
                # image.save("output.jpg",image)
                image_data+=data
                ct+=1
            except bluetooth.btcommon.BluetoothError as e:
                    if "timed out" in str(e):
                        print("timed out")
                        break 
                    elif "Bad" in str(e):
                        print("Bad file0")
                        break
            #     break  # 데이터 수신이 완료되면 종료

            # # 이미지 데이터를 메모리에 저장
            #print(type(data))
            #encoded_img = np.fromstring(data, dtype = np.uint8)
            #img = cv2.imdecode(encoded_img, cv2.IMREAD_COLGOR)​
            #cv2.imshow(img)
            # Pillow(PIL)을 사용하여 이미지 디코딩
            # image = Image.open(image_data)

            # # 이미지 저장
            # image.save("received_image_remote.jpg")  # 원하는 경로 및 파일 이름으로 변경 가능
        image=Image.open(io.BytesIO(image_data))
        image.save("test.jpg")
    