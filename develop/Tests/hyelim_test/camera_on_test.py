import cv2

webcam = cv2.VideoCapture(0)

if not webcam.isOpened():  # 카메라가 켜지지 않았을 때
    print("Could not open webcam")  # 오류 메시지 출력
    exit()  # 종료

while webcam.isOpened():  # 카메라가 켜졌을 때
    status, frame = webcam.read()

    # frame = cv2.flip(frame, 1)  # 1은 좌우, 0은 상하 반전
    # 글자를 카메라로 찍어서 읽으려면 좌우반전을 하면 안 됨
    
    if status:
        cv2.imshow("test", frame)  # 창 제목
    
    if cv2.waitKey(1) & 0xFF == ord('q'):  # q 누르면 나가기
        break
    
    if cv2.waitKey(1) & 0xFF == ord('a'):  # a 누르면 사진 찍기
        cv2.imwrite('self camera test.jpg', frame) # 사진 저장

    
webcam.release()
cv2.destroyAllWindows()


