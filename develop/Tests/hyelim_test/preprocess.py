import json
import random
import os

FILE_PATH = 'D:/kor_dataset/write/'  # 모든 파일들이 들어있는 경로
test = {'필기체' : 'htr/word_check/', '인쇄체' : 'ocr_test/word_check/',
        '증강인쇄체' : 'print/check/', '간판' : 'Text/'}


# 각 json 파일을 사용 용도(train, validation, test)에 따라 특정 비율로 분리
def process(json_path, ocr_files):
    file = json.load(open(json_path, 'rt', encoding='UTF8'))  # open('파일경로', 'rt', encoding='UTF8')
    file.keys()  # dict_keys(['info', 'images(모든 이미지 정보)', 'annotations', 'licenses']), key들로 이뤄짐
    file['info']  # {'name': 'Text in the wild Dataset', 'date_created': '2019-10-14 04:31:48'}
    type(file['images'])  # list
    ocr_good_files = os.listdir('d:/kor_dataset/write/Text_test/test/')  # 특정 폴더에 있는 특정 파일 리스트 찾기 (파일 이름 있삼)
    len(ocr_good_files) # 37220, 파일 내의 자료 개수 측정

    random.shuffle(ocr_good_files)

    # OCR 파일을 70:15:15의 비율로 3등분(train, validation, test) 나눠줌
    n_train = int(len(ocr_good_files) * 0.7)        # for train
    n_validation = int(len(ocr_good_files) * 0.15)  # for validation
    n_test = int(len(ocr_good_files) * 0.15)        # for test

    print(n_train, n_validation, n_test) # 26054 5583 5583

    # 각 "_files" 변수에 비율에 맞춰 나누어 넣기
    train_files = ocr_good_files[:n_train]
    validation_files = ocr_good_files[n_train: n_train+n_validation]
    test_files = ocr_good_files[-n_test:]

    ## train, validation, test 이미지들에 해당하는 id 값을 dict에 저장
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

    ## train, validation, test 이미지들에 해당하는 annotation들을 저장
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

    # 각 용도에 해당하는 id 값을 저장한 list 반환
    return train_annotations, validation_annotations, test_annotations

# 각 사용 용도에 따라 정리한 파일들을 '_annotation.json' 형태로 파일 저장
def save_file(file, train_annotations, validation_annotations, test_annotations):
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
    validation_data = {}
    test_data = {}

    for key, value in test.items():
        ocr_files = os.listdir(FILE_PATH + value)

        if key == '필기체':
            print(ocr_files[0:10])
            json_file = json.load(open(FILE_PATH + 'j_file/handwriting_data_info_clean.json', 'rt', encoding='UTF8'))
            #          ('D:/kor_dataset/write/') + 'j_file/handwriting_data_info_clean.json'
            train, val, test = process(json_file, ocr_files)
            train_data, val_data, test_data = dict_extend(train_data,
                                                            val_data, test_data,
                                                            train, val, test)
        if key == '인쇄체':
            print(ocr_files[0:10])
            json_file = json.load(open(FILE_PATH + 'j_file/printed_data_info.json', 'rt', encoding='UTF8'))
            #          ('D:/kor_dataset/write/') + 'j_file/printed_data_info.json'
            train, val, test = process(json_file, ocr_files)
            train_data, val_data, test_data = dict_extend(train_data,
                                                            val_data, test_data,
                                                            train, val, test)
            
        if key == '증강인쇄체' or key == '간판':
            for fold in ocr_files:
                print(FILE_PATH + value + fold)
                ocr_files = os.listdir(FILE_PATH + value + fold)
                
                if key == '간판':
                    for subfold in ocr_files:
                        print(FILE_PATH + value + fold + subfold)
                        ocr_files = os.listdir(FILE_PATH + value + fold + '/' + subfold)
                        print(ocr_files[0:10])
                        json_file = json.load(open(FILE_PATH + 'j_file/textinthewild_data_info.json', 'rt', encoding='UTF8'))
                        #          ('D:/kor_dataset/write/') + 'j_file/textinthewild_data_info.json'
                        train, val, test = process(json_file, ocr_files)
                        train_data, val_data, test_data = dict_extend(train_data,
                                                                      val_data, test_data,
                                                                      train, val, test)
                else:
                    print(ocr_files[0:10])
                    json_file = json.load(open(FILE_PATH + 'j_file/augmentation_data_info.json', 'rt', encoding='UTF8'))
        #     #          ('D:/kor_dataset/write/') + 'j_file/augmentation_data_info.json'
                    train, val, test = process(json_file, ocr_files)
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
    