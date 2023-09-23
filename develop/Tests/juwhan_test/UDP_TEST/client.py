import socket
import cv2

UDP_IP = '165.229.185.195'
UDP_PORT = 9505
print("1")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("2")
cap = cv2.VideoCapture(0)
for i in range(1):
    ret, frame = cap.read()
    d = frame.flatten()
    s = d.tostring()

    for i in range(20):
        sock.sendto(bytes([i]) + s[i*46080:(i+1)*46080], (UDP_IP, UDP_PORT))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
data,_ =sock.recvfrom(200)
print(data)