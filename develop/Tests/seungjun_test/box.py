import cv2
import matplotlib.pyplot as plt
import numpy as np

# 이미지 로드
image_path = 'C:\\Users\\IT\\Desktop\\test\\kantata.jpg'
image = cv2.imread(image_path)
# 좌표 설정
coordinates = [[48, 140], [128, 140], [128, 164], [48, 164]]
points = np.array(coordinates, np.int32)

# 좌표로 사각형 그리기
cv2.polylines(image, [points], isClosed=True, color=(0, 255, 0), thickness=2)

# 좌표로 이미지 자르기
cropped_image = image[coordinates[0][1]:coordinates[2][1], coordinates[0][0]:coordinates[1][0]]

# 잘린 이미지 저장
output_path = 'C:\\Users\\IT\\Desktop\\save\\save.jpg'
cv2.imwrite(output_path, cropped_image)

# 이미지 창 열기 (확인용)
plt.imshow("orignal",cropped_image)