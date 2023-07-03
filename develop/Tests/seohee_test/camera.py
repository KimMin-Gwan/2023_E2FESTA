import cv2

cap = cv2.VideoCapture(0)

width=int(cap.get(3))
height=int(cap.get(4))
fps=20

fcc=cv2.VideoWriter_fourcc('M','J','P','G')
out=cv2.VideoWriter('webcam.avi',fcc,fps,(width,height),isColor=False)
print(out.isOpened())
while(True):
    ret,frame=cap.read()
    if ret:
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        out.write(gray)
        cv2.imshow('frame',gray)

        if cv2.waitKey(1)&0xFF==ord('1'): break
    else:
        print("Fail to read frame!")
        break
    print(frame)
        
cap.release()
out.release()
cv2.destroyAllWindows()