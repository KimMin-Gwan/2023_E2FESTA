# -*- coding: utf8 -*-
import cv2
import socket
import numpy as np
from Object_detect.Socket_Server.constants import *

class TCP_connector():
    def __init__(self, info):
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        self.info = info
        self.IP = info.get_IP()
        self.PORT = info.get_tcp_PORT()

    # 서버 연결
    def client_sock(self, status):
        ## TCP 사용
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        ## server에 연결 ip, port
        self.sock.connect((self.IP, self.PORT))

        status[0] = True
        
        return 

    #서버로 데이터(웹캡) 보내기
    def send(self, frame):
        # cv2. imencode(ext, img [, params])
        # encode_param의 형식으로 frame을 jpg로 이미지를 인코딩한다.
        _, frame = cv2.imencode('.jpg', frame, self.encode_param)
        # frame을 String 형태로 변환
        data = np.array(frame)
        stringData = data.tostring()
        
        #서버에 데이터 전송
        #(str(len(stringData))).encode().ljust(16)
        self.sock.sendall((str(len(stringData))).encode().ljust(16) + stringData)

        #cam.release(repr(data.decode()))

        #서버에서 데이터 받아오기

    def get(self):
        #데이터 받아오기 (버퍼 사이즈 1024)
        recv_data = self.sock.recv(1024)
        #받아온 데이터를 decode하여 data에 저장
        data = recv_data.decode()
        #확인용 출력

        return data
        