#test_show_camera
from flask import Flask, render_template, Respoonse
import cv2

app=Flask(__name__)

cap = cv2.VideoCapture(0)

width=int(cap.get(3))
height=int(cap.get(4))
fps=20

fcc=cv2.VideoWriter_fourcc('M','J','P','G')
out=cv2.VideoWriter('webcam.avi',fcc,fps,(width,height),isColor=False)
print(out.isOpened())

@app.route('/')
def video_show():
    return render_template('video_show.html')

def gen_frames():
    while True:
       ret,frame=cap.read()
    if ret:
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2BGR)
        out.write(gray)
        cv2.imshow('frame',gray)

        if cv2.waitKey(1)&0xFF==ord('1'): 
            break
            
    else:
        print("Fail to read frame!")
        break

    yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    return Respoonse(gen_frames(), mimetype='multipart/x-mized-replace; boundary=frame')

if __name__=='__main__':
    app.run(host='165.229.125.90',port=7777)