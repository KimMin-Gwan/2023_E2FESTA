import socket
import cv2
import numpy as np
from Socket_maker.Object_detect import Object_detector
from threading import Thread
from Socket_maker.constants import * 

class TCP_Server():
    def __init__(self):
        #TCP 사용 
        self.server_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print('Socket created')
        
        #서버의 아이피와 포트번호 지정
        #s.bind((HOST,PORT))
        self.server_sock.bind((HOST, PORT))
        print('Socket bind complete')
        # 클라이언트의 접속을 기다린다. (클라이언트 연결을 10개까지 받는다)
        self.server_sock.listen(10)
        print('Socket now listening')
        self.connections = []

    #  다중  사용자  처리용 함수
    def accept_client(self):
        while True:
            #연결, conn에는 소켓 객체, addr은 소켓에 바인드 된 주소
            conn, addr = self.server_sock.accept()
            print(f'Connected IP : {addr}')
            
            client_thread = Thread(target=self.handle_client, args=(conn,))
            client_thread.start()

            self.connections.append(conn)

    def handle_client(self, conn):
        try:
            # Object_detector 생성
            od = Object_detector()
            while True:
                #  프레임 받아오기
                frame = self.get_stream(conn)
                # frame 처리
                tf_result = od.object_detection(frame)
                # tf_result = (boxex, scores, classes, width, height)
                conn.send(tf_result.encode())
                # 전송

        except Exception as e:
            print("Socket Error : {e}, Line 49")
        finally:
            conn.close()
            self.connections.remove(conn)


    #cliet로 부터 웹캠 이미지(영상) 받아오기
    def get_stream(self):
        # client에서 받은 stringData의 크기 (==(str(len(stringData))).encode().ljust(16))
        length = self.recvall(16)
        stringData = self.recvall(int(length))
        data = np.fromstring(stringData, dtype = 'uint8')
        
        #data를 디코딩한다.
        frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
        #cv2.imshow('ImageWindow',frame)
        #cv2.waitKey(1)
        return frame

    #socket에서 수신한 버퍼를 반환하는 함수
    def recvall(self, count):
        # 바이트 문자열
        buf = b''
        while count:
            newbuf = self.conn.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf


    