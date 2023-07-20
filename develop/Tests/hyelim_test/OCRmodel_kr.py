import json
import random
import os

file = json.load(open('./../../../../TextDataKr/textinthewild_data_info.json', 'rt', encoding='UTF8'))
# open('파일경로', 'rt', encoding='UTF8')
file.keys()  # dict_keys(['info', 'images(모든 이미지 정보)', 'annotations', 'licenses']), key들로 이뤄짐
file['info']  # {'name': 'Text in the wild Dataset', 'date_created': '2019-10-14 04:31:48'}
type(file['images'])  # list


# './../../../../TextDataKr/' 얠 넣는 건가?
ocr_good_files = os.listdir('/data/ocr/Goods/')  # 특정 폴더에 있는 특정 파일 리스트 찾기 (파일 이름 있삼)
len(ocr_good_files) # 37220

random.shuffle(ocr_good_files)

# OCR 파일을 70:15:15의 비율로 3등분(train, validation, test) 나눠줌
n_train = int(len(ocr_good_files) * 0.7)        # for train
n_validation = int(len(ocr_good_files) * 0.15)  # for validation
n_test = int(len(ocr_good_files) * 0.15)        # for test

print(n_train, n_validation, n_test) # 26054 5583 5583

train_files = ocr_good_files[:n_train]
validation_files = ocr_good_files[n_train: n_train+n_validation]
test_files = ocr_good_files[-n_test:]

## train/validation/test 이미지들에 해당하는 id 값을 저장

train_img_ids = {}
validation_img_ids = {}
test_img_ids = {}

for image in file['images']:
    if image['file_name'] in train_files:
        train_img_ids[image['file_name']] = image['id']
    elif image['file_name'] in validation_files:
        validation_img_ids[image['file_name']] = image['id']
    elif image['file_name'] in test_files:
        test_img_ids[image['file_name']] = image['id']

## train/validation/test 이미지들에 해당하는 annotation 들을 저장

train_annotations = {f:[] for f in train_img_ids.keys()}  # 각각의 key의 list( [] )를 만들어줌
validation_annotations = {f:[] for f in validation_img_ids.keys()}
test_annotations = {f:[] for f in test_img_ids.keys()}

train_ids_img = {train_img_ids[id_]:id_ for id_ in train_img_ids}
validation_ids_img = {validation_img_ids[id_]:id_ for id_ in validation_img_ids}
test_ids_img = {test_img_ids[id_]:id_ for id_ in test_img_ids}

for idx, annotation in enumerate(file['annotations']):
    if idx % 5000 == 0:
        print(idx,'/',len(file['annotations']),'processed')
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