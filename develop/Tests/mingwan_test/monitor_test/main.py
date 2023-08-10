import Camera
import Monitoring
import time

def main():
    monitor = Monitoring.Monitor()
    camera = Camera.Camera_Master(web_monitor=monitor)
    #camera = Camera.Camera_Master()
    camera.RunCamera()
    """
    count = 0
    for i in range(5):
        time.sleep(1)
        count += 1
        print(count)
    camera.swap_camera()
    """

    monitor.start_monitor(camera=camera)







if __name__=="__main__":
    main()
