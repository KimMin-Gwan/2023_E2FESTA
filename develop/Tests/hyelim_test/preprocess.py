import json
import random
import os
import tqdm
import cv2


"""
# 이 프로그램이 하는 일
json file 가지고 와서 train, valid, test로 나눔

#데이터 형태
1. 필기체 , 인쇄체, 증강 인쇄체, 간판
    1-1. 필기체 - write/htr/word_check/ 경로에 이미지 파일이 존재
    1-2. 필기체 - write/j_file/ 경로에 json 파일이 존재
    
    1-3. 인쇄체 - write/ocr_test/word_check/ 경로에 이미지 파일이 존재
    1-4. 인쇄체 - write/j_file/ 경로에 json 파일이 존재

    1-5. 증강인쇄체 - write/print/check/[3]/ 경로에 각각 이미지 파일이 존재
    1-6. 증강인쇄체 - write/j_file/ 경로에 json 파일이 존재
    
    1-7. 간판 - write/Text/[4]/[1]/ 경로에 각각 이미지 파일이 존재
    1-8. 간판 - write/j_file/ 경로에 json 파일이 존재

수도코드
1. json 파일을 읽어온다
2. json 파일에 매칭된 이미지 폴더의 경로를 가지고 온다.
3. json 파일을 분할한다.
4. 분할된 json을 반환한다.
5. 위 과정을 json 파일 갯수만큼 반복한다.
6. 반환된 json 파일을 저장한다

7. 간판일때는 각각 잘 넣으면 됨(annotation)
8. 간판이 아닐때 : annotation을 넣으면 안 됨 (형태가 다름)
    8-1. annotation 형태를 만들어서 넣어줌

9. bbox가 없는 데이터는 버림
    9-1. bbox가 없는 맴버가 하나라도 존재하는 이미지는 버림
"""

FILE_PATH = 'D:/kor_dataset/write/'  # 모든 파일들이 들어있는 경로
data_type = {'필기체' : 'htr/word_check/', '인쇄체' : 'ocr_test/word_check/',
        '증강인쇄체' : 'print/check/', '간판' : 'Text/'}

data_root_path = FILE_PATH  
save_root_path = FILE_PATH


# 이미지 나누기
def image_read():
    for key, value in data_type.items():
        annotation_json = FILE_PATH

    test_annotations = json.load(open('./test_annotation.json'))
    gt_file = open(save_root_path + 'gt_test.txt', 'w')
    
    for file_name in tqdm(test_annotations):
        annotations = test_annotations[file_name]
        image = cv2.imread(data_root_path + file_name)
        
        for idx, annotation in enumerate(annotations):
            x, y, w, h = annotation['bbox']
            
            if x <= 0 or y <= 0 or w <= 0 or h <= 0:
                continue
            
            text = annotation['text']
            crop_img = image[y:y+h, x:x+w]
            crop_file_name = file_name[:-4]+'_{:03}.jpg'.format(idx+1)
            cv2.imwrite(save_root_path + 'test/' + crop_file_name, crop_img)
            gt_file.write('test/{}\t\n'.format(crop_file_name, text))

# 각 json 파일을 사용 용도(train, validation, test)에 따라 특정 비율로 분리
# flag가 1이면 간판 데이터임
def process(file, ocr_files, now_path, flag = 0):
    #file = json.load(open(json_path, 'rt', encoding='UTF8'))  # open('파일경로', 'rt', encoding='UTF8')
    file.keys()  # dict_keys(['info', 'images(모든 이미지 정보)', 'annotations', 'licenses']), key들로 이뤄짐
    file['info']  # {'name': 'Text in the wild Dataset', 'date_created': '2019-10-14 04:31:48'}
    type(file['images'])  # list
    ocr_good_files = ocr_files  # 특정 폴더에 있는 특정 파일 리스트 찾기 (파일 이름 있삼)
    len(ocr_good_files) # 37220, 파일 내의 자료 개수 측정

    random.shuffle(ocr_good_files)

    # OCR 파일을 70:15:15의 비율로 3등분(train, validation, test) 나눠줌
    n_train = int(len(ocr_good_files) * 0.7)        # for train
    n_validation = int(len(ocr_good_files) * 0.15)  # for validation
    n_test = int(len(ocr_good_files) * 0.15)        # for test

    print(n_train, n_validation, n_test) # 26054 5583 5583

    # 각 "_files" 변수에 비율 맞춰 나누어 넣기
    train_files = ocr_good_files[:n_train]
    validation_files = ocr_good_files[n_train: n_train+n_validation]
    test_files = ocr_good_files[-n_test:]

    ## train, validation, test 이미지들에 해당하는 id 값을 dict에 저장
    train_img_ids = {}
    validation_img_ids = {}
    test_img_ids = {}

    # dict 형태로 만들어줌 { image_name : image_id, ... }
    for idx, image in enumerate(file['images']):
        if idx % 5000 == 0:
            print(idx,'/',len(file['images']),'make imge data')
        if image['file_name'] in train_files:
            train_img_ids[image['file_name']] = image['id']
        elif image['file_name'] in validation_files:
            validation_img_ids[image['file_name']] = image['id']
        elif image['file_name'] in test_files:
            test_img_ids[image['file_name']] = image['id']

    ## train, validation, test 이미지들에 해당하는 annotation들을 저장
    train_annotations = {f:[] for f in train_img_ids.keys()}  # 각각의 key의 list( [] )를 만들어줌
    validation_annotations = {f:[] for f in validation_img_ids.keys()}
    test_annotations = {f:[] for f in test_img_ids.keys()}

    train_ids_img = {train_img_ids[id_]:id_ for id_ in train_img_ids}
    validation_ids_img = {validation_img_ids[id_]:id_ for id_ in validation_img_ids}
    test_ids_img = {test_img_ids[id_]:id_ for id_ in test_img_ids}


    # 간판일 때는 그냥 annotation 집어넣어주면 됨
    if flag == 1:
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
    else:
        annotations = []
        annotation_temp = {}
        for idx, annotation in enumerate(file['annotations']):
            if idx % 5000 == 0:
                print(idx, '/', len(file['annotations']), "making annotation")
            annotation_temp['id'] = annotation['id']
            annotation_temp['image_id'] = annotation['image_id']
            annotation_temp['text'] = annotation['text']
            annotation_temp['attributes'] = {"class" : "word"}

            # for image_data in file['images']:
            #     if image_data['id'] == annotation['image_id']:
            #         x = image_data['width']
            #         y = image_data['height']
            #         break

            # 각 이미지의 크기 측정 후 반환하여 bbox 값으로 사용
            CheckImageSize = cv2.imread(os.path.join(now_path + '/', imgName))
            y, x, NotUse = print(CheckImageSize.shape) # 세로, 가로, 색?(근데 얜 사용 X)

            annotation_temp['bbox'] = [0,
                                       0,
                                       x,
                                       y]
            annotations.append(annotation_temp)
                  # annotation을 만드는 부분
        """
        'id': "000000000",
        'image_id': "00000000",
        'text" : "text",
        attributes:{ class : "word" },
        bbox: [x1, y1, x2, y2]
        """  
        # 실제로 분할되는 부분
        for idx, annotation in enumerate(annotations):
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

    # 각 용도에 해당하는 id 값을 저장한 list 반환
    return train_annotations, validation_annotations, test_annotations

# 각 사용 용도에 따라 정리한 파일들을 '_annotation.json' 형태로 파일 저장
def save_file(train_annotations, validation_annotations, test_annotations):
    with open('train_annotation.json', 'w', encoding='UTF-8') as file:
        json.dump(train_annotations, file, indent=6, ensure_ascii=False)  # indent: 6개씩 잘라서 줄 바꿈
    with open('validation_annotation.json', 'w', encoding='UTF-8') as file:
        json.dump(validation_annotations, file, indent=6, ensure_ascii=False)
    with open('test_annotation.json', 'w', encoding='UTF-8') as file:
        json.dump(test_annotations, file, indent=6, ensure_ascii=False)

# process() 함수의 반환값인 '_annotations'을 train, val, test라는 이름으로 추가 (update())
def dict_extend(train_dict, val_dict, test_dict, train, val, test):
    train_dict.update(train)
    val_dict.update(val)
    test_dict.update(test)

    return train_dict, val_dict, test_dict

# main
def main():
    train_data = {}  # dict
    val_data = {}
    test_data = {}

    for key, value in data_type.items():
        now_path = FILE_PATH + value
        ocr_files = os.listdir(now_path)

        if key == '필기체':
            #print(ocr_files[0:10])
            print('processing now : ', key)
            json_file = json.load(open(FILE_PATH + 'j_file/handwriting_data_info_clean.json', 'rt', encoding='UTF8'))
            #          ('D:/kor_dataset/write/') + 'j_file/handwriting_data_info_clean.json'
            train, val, test = process(json_file, ocr_files, now_path)
            train_data, val_data, test_data = dict_extend(train_data,
                                                            val_data, test_data,
                                                            train, val, test)
        if key == '인쇄체':
            #print(ocr_files[0:10])
            print('processing now : ', key)
            json_file = json.load(open(FILE_PATH + 'j_file/printed_data_info.json', 'rt', encoding='UTF8'))
            #          ('D:/kor_dataset/write/') + 'j_file/printed_data_info.json'
            train, val, test = process(json_file, ocr_files, now_path)
            train_data, val_data, test_data = dict_extend(train_data,
                                                            val_data, test_data,
                                                            train, val, test)
            
        if key == '증강인쇄체' or key == '간판':
            for fold in ocr_files:
                #print(FILE_PATH + value + fold)
                now_path = FILE_PATH + value + fold
                ocr_files = os.listdir(now_path)

                if key == '간판':
                    for subfold in ocr_files:
                        print('processing now : ', key)
                        #print(FILE_PATH + value + fold + subfold) # IMAGE 파일 경로
                        now_path = FILE_PATH + value + fold + '/' + subfold
                        ocr_files = os.listdir(FILE_PATH + value + fold + '/' + subfold)
                        #print(ocr_files[0:10])
                        json_file = json.load(open(FILE_PATH + 'j_file/textinthewild_data_info.json', 'rt', encoding='UTF8'))
                        #          ('D:/kor_dataset/write/') + 'j_file/textinthewild_data_info.json'
                        train, val, test = process(json_file, ocr_files, now_path, flag = 1)
                        train_data, val_data, test_data = dict_extend(train_data,
                                                                      val_data, test_data,
                                                                      train, val, test)
                else:
                    print('processing now : ', key)
                    #print(ocr_files[0:10])
                    json_file = json.load(open(FILE_PATH + 'j_file/augmentation_data_info.json', 'rt', encoding='UTF8'))
                    #          ('D:/kor_dataset/write/') + 'j_file/augmentation_data_info.json'
                    train, val, test = process(json_file, ocr_files, now_path)
                    train_data, val_data, test_data = dict_extend(train_data,
                                                                    val_data, test_data,
                                                                    train, val, test)

        # else:
        #     print(ocr_files[0:10])
        #     json_file = json.load(open(FILE_PATH + 'j_file/augmentation_data_info.json', 'rt', encoding='UTF8'))
        #     #          ('D:/kor_dataset/write/') + 'j_file/augmentation_data_info.json'
        #     train, val, test = process(ocr_files)
        #     train_data, val_data, test_data = dict_extend(train_data,
        #                                                     val_data, test_data,
        #                                                     train, val, test)
        
    save_file(train_data, val_data, test_data)

if __name__ == '__main__':
    main()



#annotation['attributes']['class'] = 'ignored', 'character', 'word',
                                