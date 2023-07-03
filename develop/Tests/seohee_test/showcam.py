
from flask import Flask, render_template, Response
from camera import Camera

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('video_show.html')

def gen(camera):
   while True:
       frame = camera.get_frame()
       yield (b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
   return Response(gen(Camera()),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
   app.run(host='165.229.125.90',port=7777)