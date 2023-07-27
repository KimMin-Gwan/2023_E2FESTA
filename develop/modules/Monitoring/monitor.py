from flask import Flask, render_template, Response
from flask import send_file, json, make_response #인프라 서치에서 한국어 반환 위해
import cv2 #핸드카메라 위해
import io #스냅샷 위해

app=Flask(__name__)
app.config['JSON_AS_ASCII'] = False
streaming=True
stop_frame=None

def hand_cam():
    camera=cv2.VideoCapture(0) #0번캠(현재 내 카메라)
    
    while (streaming):
        # 프레임 단위로 캡쳐
        success, frame = camera.read()  #카메라 프레임 읽어오기      

        if (not success):
            break

        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            global stop_frame
            stop_frame=frame
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            #프레임 하나씩 보여준다


@app.route('/snapshot')
def snapshot():
    return send_file(io.BytesIO(stop_frame), mimetype='image/jpeg')

@app.route('/video_show')
def video_show():
    return Response(hand_cam(), 
        mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def hello_name():
    sub='지하철'
    bus='버스'
    traft='신호등'
    return render_template('index.html',name1=sub,name2=bus,name3=traft)

if __name__=='__main__':
    app.run(host="0.0.0.0", port="8080")