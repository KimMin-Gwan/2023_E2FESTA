# import cv2
# import os
 
# path = 'C:/Users/y2h75/Desktop/hyelim/# 공모전/2023_E2FESTA/500651.jpg'
# imgName = 'photoo'
 
# img = cv2.imread(os.path.join(path, imgName))
# print(img.shape) # h, w, c

import cv2
import os
import time

path = 'D:/kor_dataset/write/'
imgName = '500651.jpg'

start_time = time.time()
img = cv2.imread(os.path.join(path, imgName))
end_time = time.time()
print(end_time - start_time)

print(img.shape) # h, w, c
