#showcam
from flask import Flask, render_template, Response
import cv2

cap = cv2.VideoCapture(0)

width=int(cap.get(3))
height=int(cap.get(4))
fps=20

app = Flask(__name__)

fcc=cv2.VideoWriter_fourcc('M','J','P','G')
out=cv2.VideoWriter('webcam.avi',fcc,fps,(width,height),isColor=False)
print(out.isOpened())

@app.route('/')
def index():
   return render_template('video_show.html')

def gen(camera):
    while(True):
    ret,frame=cap.read()
    if ret:
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        out.write(gray)
        cv2.imshow('frame',gray)

        if cv2.waitKey(1)&0xFF==ord('1'): break
    else:
        print("Fail to read frame!")
        break
    cap.release()
    out.release()
    cv2.destroyAllWindows()

@app.route('/video_feed')
def video_feed():
   return Response(gen(Camera()),
   mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
   app.run(host='165.229.125.125',port=7777)