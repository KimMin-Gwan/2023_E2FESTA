# monitor.py
"""
* Program Purpose and Features :
* - data processer class
* Author : SH PARK, MG KIM
* First Write Date : 2023.07.27
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		    Version		History                                                                                 code to fix
* SH PARK			2023.07.27      v0.10	    make monitoring system
* SH PARK			2023.07.31      v0.20	    set packaging and seperate files
* SH PARK			2023.08.08      v0.30	    html modify&swap video
* SH PARK			2023.08.09      v0.31	    bug fix & test system
* MG KIM			2023.08.10      v0.40	    swap button make, check system
"""

from flask import Flask, render_template, Response
from flask import send_file # 인프라 서치에서 한국어 반환 위해
import cv2, io # 핸드카메라&스냅샷 위해
from constant import SUB,BUS,TRAFT
import numpy as np
#import pyrealsense2.pyrealsense2 as rs

class Monitor:
    def __init__(self):
        self.app=Flask(__name__)
        self.app.config['JSON_AS_ASCII'] = False
        self.streaming=True
        self.stop_frame=None
        self.route()
    
    def hand_cam(self):
        camera=cv2.VideoCapture(1,cv2.CAP_DSHOW)
         # 0번캠(현재 내 카메라)
        while (self.streaming):
         # 프레임 단위로 캡쳐
            success, frame = camera.read()  # 카메라 프레임 읽어오기      
            if (not success):
                break
            
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                global stop_frame
                stop_frame=frame
            
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                 # 프레임 하나씩 보여준다. 즉 프레임 반환(return과 비슷)

    # 위의 hand_cam과 동일한 역할
    def get_frame(self):
        while(True):
            data = self.camera.get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n')

    def route(self):
        @self.app.route('/snapshot')
        def snapshot():
            return send_file(io.BytesIO(stop_frame), mimetype='image/jpeg')
        
        # 도메인 디렉토리 변경
        @self.app.route('/swap')
        def swap_video():
            # 받아오는 프레임 변경
            self.camera.swap_camera()
            return render_template('index.html', 
                                   name1=SUB, name2=BUS, name3=TRAFT)
        
        @self.app.route('/video_show')
        def video_show():
            return Response(self.hand_cam(), 
                mimetype='multipart/x-mixed-replace; boundary=frame')
         # mimetype~=> return받은 것 (프레임)을 서버로 푸쉬하는듯

        @self.app.route('/')
        def hello_name():
            return render_template('index.html', 
                                   name1=SUB, name2=BUS, name3=TRAFT)

    def start_monitor(self, camera):
        # 카메라 객체 생성
        self.camera = camera
        self.app.run(host="0.0.0.0", port="7777")

if __name__=="__main__":
    monitor=Monitor()
    monitor.start_monitor()
