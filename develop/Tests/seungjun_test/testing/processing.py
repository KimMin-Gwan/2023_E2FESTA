import json
import random
import os
from tqdm import tqdm
import cv2
import matplotlib.pyplot as plt

## aihub 데이터 annotation을 읽어서 단어 단위로 잘라서 data에 저장하기
data_root_path = f'./kor_dataset/aihub_data/{data_type}/images/'
save_root_path = f'./ocr_english/{data_type}_data/'


obj_list = ['test', 'train', 'validation']
for obj in obj_list:
    total_annotations = json.load(open(f'./{data_type}_{obj}_annotation.json'))
    gt_file = open(f'{save_root_path}gt_{obj}.txt', 'w')
    for file_name in tqdm(total_annotations):
        annotations = total_annotations[file_name]
        for idx, annotation in enumerate(annotations):
            text = annotation['text']
            gt_file.write(f'{obj}/{file_name}\t{text}')


test_annotations = json.load(open('./test_annotataion.json'))
gt_file = open(save_root_path + 'gt_test.txt', 'w')
for file_name in tqdm(test_annotations):
    annotations = test_annotations[file_name]
    image = cv2.imread(data_root_path + file_name)
    for idx, annotation in enumerate(annotations):
        x,y,w,h = annotation['bbox']
        if x<=0 or y<=0 or w<=0 or h<=0:
            continue
        text = annotation['text']
        crop_img = image[y:y+h, x:x+w]
        crop_file_name = file_name[:-4]+'_{:03}.jpg'.format(idx+1)
        cv2.imwrite(save_root_path+'test/'+crop_file_name, crop_img)
        gt_file.write("test/{}\t\n".format(crop_file_name, text))

validation_annotations = json.load(open('./validation_annotataion.json'))
gt_file = open(save_root_path + 'gt_validation.txt', 'w')
for file_name in tqdm(validation_annotations):
    annotations = validation_annotations[file_name]
    image = cv2.imread(data_root_path + file_name)
    for idx, annotation in enumerate(annotations):
        x,y,w,h = annotation['bbox']
        if x<=0 or y<=0 or w<=0 or h<=0:
            continue
        text = annotation['text']
        crop_img = image[y:y+h, x:x+w]
        crop_file_name = file_name[:-4]+'_{:03}.jpg'.format(idx+1)
        cv2.imwrite(save_root_path+'validation/'+crop_file_name, crop_img)
        gt_file.write("validation/{}  \n".format(crop_file_name, text))

train_annotations = json.load(open('./train_annotataion.json'))
gt_file = open(save_root_path + 'gt_train.txt', 'w')
for file_name in tqdm(train_annotations):
    annotations = train_annotations[file_name]
    image = cv2.imread(data_root_path + file_name)
    for idx, annotation in enumerate(annotations):
        x,y,w,h = annotation['bbox']
        if x<=0 or y<=0 or w<=0 or h<=0:
            continue
        text = annotation['text']
        crop_img = image[y:y+h, x:x+w]
        crop_file_name = file_name[:-4]+'_{:03}.jpg'.format(idx+1)
        cv2.imwrite(save_root_path+'train/'+crop_file_name, crop_img)
        gt_file.write("train/{}  \n".format(crop_file_name, text))
