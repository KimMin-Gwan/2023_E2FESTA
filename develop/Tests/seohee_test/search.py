#
from flask import Flask, render_template, Response
from flask import json, make_response #인프라 서치에서 한국어 반환 위해
import cv2 #핸드카메라 위해

app=Flask(__name__)
app.config['JSON_AS_ASCII'] = False

def hand_cam():
    camera=cv2.VideoCapture(0) #0번캠(현재 내 카메라)

    while (True):
        # 프레임 단위로 캡쳐
        success, frame = camera.read()  #카메라 프레임 읽어오기      

        if (not success):
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            #프레임 하나씩 보여준다


@app.route('/infra_search',methods=['POST'])
def infra_search():
    result = '지하철'
    # result = json.dumps(result, ensure_ascii=False)
    # res = make_response(result)
    return result

@app.route('/video_show')
def video_show():
    return Response(hand_cam(), 
        mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def find():
    result=infra_search
    return render_template('search_index.html',result=result) #html 실행

if (__name__ == '__main__'):
   app.run(host='127.0.0.1',port=80) #사용중인 인터넷 실행(localhost:80)