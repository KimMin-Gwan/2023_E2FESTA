from bluetooth import *

class remote():
    def __init__(self):
        self.socket=BluetoothSocket(RFCOMM)
        self.socket.connect(("00:19:09:03:43:2E",1))
    def run_moduel(self):
        while True:
            data=self.socket.recv(1024)
            print("Received: %s",data)
            if(data=="q"):
                break
        socket.close()



