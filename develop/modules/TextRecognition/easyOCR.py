from matplotlib import pyplot as plt
from imutils.perspective import four_point_transform
from imutils.contours import sort_contours
import imutils
from easyocr import Reader
import cv2
import requests
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import time
import copy
import pickle
import torch
px=[-1,1,1,-1]
py=[-1,-1,1,1]


def plt_imshow(title='image', img=None, figsize=(8 ,5)):
    plt.figure(figsize=figsize)
 
    if type(img) == list:
        if type(title) == list:
            titles = title
        else:
            titles = []
 
            for i in range(len(img)):
                titles.append(title)
 
        for i in range(len(img)):
            if len(img[i].shape) <= 2:
                rgbImg = cv2.cvtColor(img[i], cv2.COLOR_GRAY2RGB)
            else:
                rgbImg = cv2.cvtColor(img[i], cv2.COLOR_BGR2RGB)
 
            plt.subplot(1, len(img), i + 1), plt.imshow(rgbImg)
            plt.title(titles[i])
            plt.xticks([]), plt.yticks([])
 
        plt.show()
    else:
        if len(img.shape) < 3:
            rgbImg = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        else:
            rgbImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
 
        plt.imshow(rgbImg)
        plt.title(title)
        plt.xticks([]), plt.yticks([])
        plt.show()

def detection_image(org_image):
    i=0
    list_crop_image=[]
    copy_image=copy.deepcopy(org_image)
    langs = ['ko', 'en']
    reader = Reader(lang_list=langs, gpu=False)
    
    results = reader.readtext(org_image)
    
    
    for i in range(len(results[0][0])):
        for k in range(4):
            results[i][0][k][0]+=px[k]
            results[i][0][k][1]+=py[k]
    for i in range(len(results)):
        coordinates = results[i][0]
        points = np.array(coordinates, np.int32)
        cv2.polylines(copy_image, [points], isClosed=True, color=(0, 255, 0), thickness=2)
        cropped_image = copy_image[coordinates[0][1]:coordinates[2][1], coordinates[0][0]:coordinates[1][0]]
        list_crop_image.append(cropped_image)
        i+=1
        copy_image=copy.deepcopy(org_image)
    return list_crop_image
        
    
    
if __name__=="__main__":
    image_path = 'C:\\Users\\IT\\Desktop\\df\\letsb.png'
    image = cv2.imread(image_path)
    st_time=time.time()
    list_images=detection_image(image)
    end_time=time.time()
    print("여기서 총 걸린 시간 출력",end_time-st_time)
    
    for i in range(len(list_images)):
        plt_imshow("Original",list_images[i])