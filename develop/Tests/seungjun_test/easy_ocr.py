import easyocr 
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import cv2 
import random 
import matplotlib.pyplot as plt

reader = easyocr.Reader(['ko', 'en'], gpu=False)
result = reader.readtext("c:\\Users\\IT\\Desktop\\test\\kantata.jpg")
img    = cv2.imread("c:\\Users\\IT\\Desktop\\test\\kantata.jpg")
img = Image.fromarray(img)

font = ImageFont.truetype("C:\\Windows\\Fonts\\gulim.ttc",40)
draw = ImageDraw.Draw(img)
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(255, 3),dtype="uint8")
frame = []
for i in result :
    x = i[0][0][0] 
    y = i[0][0][1] 
    w = i[0][1][0] - i[0][0][0] 
    h = i[0][2][1] - i[0][1][1]

    color_idx = random.randint(0,255) 
    color = [int(c) for c in COLORS[color_idx]]
    draw.rectangle(((x, y), (x+w, y+h)), outline=tuple(color), width=2)
    draw.text((int((x + x + w) / 2) , y-2),str(i[1]), font=font, fill=tuple(color),)
    frame.append(i[1])
    print(frame)

#plt.imshow(img)
#plt.show()