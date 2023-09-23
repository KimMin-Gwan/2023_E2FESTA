import socket
import cv2
import numpy as np
from Socket_maker.Object_detect import Object_detector
from threading import Thread
from Socket_maker.constants import * 
import pickle

class UDP_Server():
    def __init__(self):
        #UDP 사용, IPv4
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.sock.bind((HOST, PORT))

        self.sock.bind(('165.229.50.47', PORT))
        # 이미지  생성을  위한  빈  리스트를  생성,  이미지를 20 개의  조각으로 나누기
        self.client_data = {}

    #   스트림  받는 부분
    def get_stream(self):
        try:
            od = Object_detector()
            while True:
                buf, addr = self.__recvall()

                # frame 처리
                frame = np.fromstring(buf, dtype=np.uint8)
                frame = frame.reshape(480, 640, 3)
                #  객체 탐지
                tf_result = od.object_detection(frame)
                # tf_result = (boxex, scores, classes, width, height)
                # byte 단위로 직렬화진행
                result_bytes = pickle.dumps(tf_result)
                #  사용자에게 전송
                print("server send")
                self.sock.sendto(result_bytes, addr)

        except Exception as e:
            print(f"Socket Error : {e}, Line 31")

    # 20 등분되어  전송된  데이터를  결합
    def __recvall(self):
        buf = b''
        while True:
            #  데이터 수신
            print("waiting recvfrom")
            data, addr = self.sock.recvfrom(46081)
            print("input data",data)
            # addr 에  따라   따로  모아서 저장
            if addr not in self.client_data.keys():
                buf_slice= [b'\xff' * 46080 for x in range(20)]
                self.client_data[addr] = {'buf_slice':buf_slice}
            
            index = self.client_data[addr]['buf_slice']
            index[data[0]] = data[1:46081]

            if data[0] == 19:
                for i in range(20):
                    buf += index[i]
                break
        return buf, addr
    


    
    