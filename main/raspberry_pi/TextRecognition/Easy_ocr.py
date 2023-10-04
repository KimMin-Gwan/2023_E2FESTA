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
class Easy_ocr:
    def __init__(self):   #생성자
        self.one_frame=""  #받아올 프레임
        self.frame_list=[]  #전달할 img_list frame
        self.reader=""  # easy_ocr model
        self.results=""   #frame 좌표 위치 결과


    def detection_image(self):  #글자 디텍션 함수

        self.crop_range()
        #self.crop_image()


    def make_model(self):  #모델 생성 함수
        langs = ['ko', 'en']
        self.reader = Reader(lang_list=langs, gpu=False)


    def crop_range(self):  #크롭 범위 지정 현재 1씩 더 늘렸음
        self.results = self.reader.readtext(self.one_frame)

        print(self.results)
        for i in range(len(self.results)):
            self.frame_list.append(self.results[i][0])
            
    def crop_image(self): #크롭 함수
        i=0
        for i in range(len(self.results)):
            copy_image=copy.deepcopy(self.one_frame)
            coordinates = self.results[i][0]
            points = np.array(coordinates, np.int32)
            cv2.polylines(copy_image, [points], isClosed=True, color=(0, 255, 0), thickness=2)
            cropped_image = copy_image[coordinates[0][1]:coordinates[2][1], coordinates[0][0]:coordinates[1][0]]
            self.frame_list.append(cropped_image)
            i+=1

    def return_frame(self):  #return function
        return self.frame_list
    
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



    def run_easyocr_module(self,frame):  #외부에서 실행시킬 run_module 함수
        self.one_frame=frame
        self.make_model()   #모델 만들기
        self.detection_image()
        print(self.return_frame)
        return self.return_frame()



