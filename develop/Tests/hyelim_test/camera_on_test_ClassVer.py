
from camera_on_test_Class import camera as cam  # 하면 camera() 클래스 받아와짐 ~!


def main():
    카메라 = cam()
    result = 카메라.StartHandCam()
    
    # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(result)
    # for i in range(len(result[0])):
    #     print(result[0][i])
        
if __name__ == "__main__":
    main()

##############################################################################################

# webcam = cv2.VideoCapture(0)  # 0번 카메라

# if __name__ == "__main__":
#     카메라 = cam()
#     카메라.StartHandCam()