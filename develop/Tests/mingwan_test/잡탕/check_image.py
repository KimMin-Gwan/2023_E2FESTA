import cv2
import matplotlib.pyplot as plt

img = cv2.imread("/home/antl/Desktop/1000088_603.jpg")

img = cv2.rectangle(img, (1836+116, 989+149), (1837, 989), (10, 255, 0), 10)


plt.imshow(img)
plt.show()