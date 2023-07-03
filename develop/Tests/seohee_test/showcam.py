#test_show_camera
from flask import Flask, render_template, Respoonse
import cv2

app=Flask(__name__)

video_path=""
cap=cv2.VideoCapture(video_path)

@app.route('/')
def video_show():
    return render_template('video_show.html')

def gen_frames():
    while True:
        _, frame=cap.read()
        if not _:
            break
        else:
            results=model(frame)
            annotated_frame=results.render()

            ret, buffer=cv2.imencodde('.jpg', frame)
            frmae=buffer.tobytes()

        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    return Respoonse(gen_frames(), mimetype='multipart/x-mized-replace;boundary=frame')

if __name__=='__main__':
    app.run(host='165.229.125.90',port=7777)