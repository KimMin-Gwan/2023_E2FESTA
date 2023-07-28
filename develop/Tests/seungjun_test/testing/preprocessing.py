import json
import random
import os
from tqdm import tqdm

# htr / ocr
data_type = 'ocr'
# handwriting_data_info1.json / printed_data_info.json
labeling_filename = 'printed_data_info.json'

#Check json file
#file = json.load(open('./kor_dataset/aihub_data/ocr/printed_data_info.json'))
file = json.load(open('./kor_dataset/aihub_data/ocr/printed_data_info.json','r', encoding="UTF-8"))
#데이터 분리
image_files = os.listdir(f'./kor_dataset/aihub_data/{data_type}/images/')
total = len(image_files)

random.shuffle(image_files)

n_train=int(len(image_files)*0.7) #70%
n_valid=int(len(image_files)*0.15) #15%
n_test=int(len(image_files)*0.15) #15%

print(n_train,n_valid,n_test)

train_files=image_files[:n_train]
validation_files=image_files[n_train:n_train+n_valid]
test_files=image_files[-n_test:] #??
import cv2
import matplotlib.pyplot as plt


'''
ocr_files = os.listdir('/경로')
len(ocr_files) #파일 개수

random.shuffle(ocr_files)

n_train=int(len(ocr_files)*0.8) #80%
n_valid=int(len(ocr_files)*0.15) #15%
n_test=int(len(ocr_files)*0.05) #5%

print(n_train,n_valid,n_test)

train_files=ocr_files[:n_train]
validation_files=ocr_files[n_train:n_train+n_valid]
test_files=ocr_files[-n_test:] #??
'''
## train/validation/test 이미지들에 해당하는 id값저장
train_image_ids = {}
validation_image_ids = {}
test_image_ids = {}

for image in file['images']: #file은 json파일 로드?
    if image['file_name'] in train_files:
        train_image_ids[image['file_name']] = image['id']
    elif image['file_name'] in validation_files:
        validation_image_ids[image['file_name']] = image['id']
    elif image['file_name'] in test_files:
        test_image_ids[image['file_name']] = image['id']

## train/validation/test 이미지들에 해당하는 annotation 값저장
train_annotations = {f:[] for f in train_image_ids.keys()}
validation_annotations = {f:[] for f in validation_image_ids.keys()}
test_annotations = {f:[] for f in test_image_ids.keys()}

train_ids_img = {train_image_ids[id_]:id_ for id_ in train_image_ids}
validation_ids_img = {validation_image_ids[id_]:id_ for id_ in train_image_ids}
test_ids_img = {test_image_ids[id_]:id_ for id_ in train_image_ids}

for idx, annotation in enumerate(file['annotations']):
    if idx % 5000 == 0:
        print(idx, '/', len(file['annotations']),'processed')
    if annotation['attributes']['class'] != 'word':
        continue
    if annotation['image_id'] in train_ids_img:
        train_annotations[train_ids_img[annotation['image_id']]].append(annotation)
    elif annotation['image_id'] in validation_ids_img:
        validation_annotations[validation_ids_img[annotation['image_id']]].append(annotation)
    elif annotation['image_id'] in test_ids_img:
        test_annotations[test_ids_img[annotation['image_id']]].append(annotation)

with open('train_annotation.json', 'w') as file:
    json.dump(train_annotations, file)
with open('validation_annotation.json', 'w') as file:
    json.dump(validation_annotations, file)
with open('test_annotation.json', 'w') as file:
    json.dump(test_annotations, file)

'''
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
'''