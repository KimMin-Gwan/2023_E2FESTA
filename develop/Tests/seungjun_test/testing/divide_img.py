import json
import random
import os
from tqdm import tqdm
import cv2
import matplotlib.pyplot as plt

FILE_PATH = 'D:/kor_dataset/write/'  # 모든 파일들이 들어있는 경로
data_type = {'필기체' : 'htr/word_check/', '인쇄체' : 'ocr_test/word_check/',
        '증강인쇄체' : 'print/check/', '간판' : 'Text/'}

data_root_path = FILE_PATH  
save_root_path = FILE_PATH

#이미지 나누기
obj_list = ['test', 'train', 'validation']
for key, value in data_type.items():
    annotation_json = FILE_PATH 

for obj in obj_list:
    obj_annotations = json.load(open(f'./{obj}_annotation.json'))
gt_file = open(save_root_path + f'gt_{obj}.txt', 'w')
for file_name in tqdm(obj_annotations):
    annotations = obj_annotations[file_name]
    image = cv2.imread(data_root_path + file_name)
    for idx, annotation in enumerate(annotations):
        x,y,w,h = annotation['bbox']
        if x<=0 or y<=0 or w<=0 or h<=0:
            continue
        text = annotation['text']
        crop_img = image[y:y+h, x:x+w]
        crop_file_name = file_name[:-4]+'_{:03}.jpg'.format(idx+1)
        cv2.imwrite(save_root_path + 'test/' + crop_file_name, crop_img)
        gt_file.write('test/{}\t\n'.format(crop_file_name, text))