import json
import random
import os

FILE_PATH = 'D:/kor_dataset/write/'
test = {'필기체' : 'htr/word_check/', '인쇄체' : 'ocr_test/word_check/',
        '증강인쇄체' : 'print/check/', '간판' : 'Text/'}

def process(PATH):
    ocr_good_files = os.listdir('d:/kor_dataset/write/Text_test/test/')  # 특정 폴더에 있는 특정 파일 리스트 찾기 (파일 이름 있삼)
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

    return train_annotations, validation_annotations, test_annotations

    

def save_file(file, train_annotations, validation_annotations, test_annotations):
    with open('train_annotation.json', 'w',encoding='UTF-8') as file:
        json.dump(train_annotations, file, indent=6,ensure_ascii=False)
    with open('validation_annotation.json', 'w',encoding='UTF-8') as file:
        json.dump(validation_annotations, file,indent=6,ensure_ascii=False)
    with open('test_annotation.json', 'w',encoding='UTF-8') as file:
        json.dump(test_annotations, file,indent=6,ensure_ascii=False)


def dict_extend(train_dict, val_dict, test_dict, train, val, test):
    train_dict.update(train)
    val_dict.update(val)
    test_dict.update(test)

    return train_dict, val_dict, test_dict


def main():   
    train_data = {}
    validation_data = {}
    test_data = {}

    for key, value in test.items():
        ocr_files = os.listdir(FILE_PATH + value)

        if key == '증강인쇄체' or key == '간판':
            for arg in ocr_files:
                print(FILE_PATH + value + arg)
                ocr_files = os.listdir(FILE_PATH + value + arg)
                
                if key == '간판':
                    for argg in ocr_files:
                        print(FILE_PATH + value + arg + argg)
                        ocr_files = os.listdir(FILE_PATH + value + arg + '/' + argg)
                        print(ocr_files[0:10])
                        train, val, test = process(ocr_files)
                        train_data, val_data, test_data = dict_extend(train_data,
                                                                      val_data, test_data,
                                                                      train, val, test)
                else:
                    print(ocr_files[0:10])
                    train, val, test = process(ocr_files)
                    train_data, val_data, test_data = dict_extend(train_data,
                                                                      val_data, test_data,
                                                                      train, val, test)

        else:
            print(ocr_files[0:10])
            train, val, test = process(ocr_files)
            train_data, val_data, test_data = dict_extend(train_data,
                                                                      val_data, test_data,
                                                                      train, val, test)



exit()



if __name__ == '__main__':
    main()