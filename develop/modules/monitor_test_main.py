import Camera
import Monitoring
import threading
import TextRecognition
# import Speaker

def main():
    monitor = Monitoring.Monitor()
    camera = Camera.Camera_Master(web_monitor=monitor)
    # speaker = Speaker.  < 얘도 나중에 추가하기
    #text_recognizer = TextRecognition.TxtRecognizer(camera) #, speaker (나중에 추가하기)
    camera.RunCamera()
    # thread = threading.Thread(target=camera.RunCamera, args=(True))
    #thread = threading.Thread(target=text_recognizer.RunRecognition)
    monitor.start_monitor()
    
    

if __name__ == "__main__":
    main()