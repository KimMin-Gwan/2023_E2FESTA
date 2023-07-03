from flask import Flask, request, Response, stream_with_context, render_template
import imutils
import queue as Queue
import cv2
import streamer1 as st

streamer = st.Streamer()

cap = cv2.VideoCapture(0)

app = Flask(__name__)

def bytescode(que):
    frame = imutils.resize(que.get(), width=int(640) )

    cv2.rectangle( frame, (0,0), (120,30), (0,0,0), -1)
    return cv2.imencode('.jpg', frame )[1].tobytes()

@app.route('/')
def index():
   return render_template('index.html')

def gen(src):
    streamer.run( src )
    while True:
        frame = streamer.bytescode()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        

@app.route('/video_feed')
def video_feed():
    src = request.args.get( 'src', default = 0, type = int )
    #return Response(print('hello camera'))
    return Response(
                    stream_with_context( gen( src ) ),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
   app.run(host='0.0.0.0', debug=True, threaded=True)