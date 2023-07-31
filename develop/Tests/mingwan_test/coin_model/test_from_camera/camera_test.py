import cv2

camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()
    
    if ret:
        cv2.imshow('test_window', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    
camera.release()
cv2.destroyAllWindows()
        
        


