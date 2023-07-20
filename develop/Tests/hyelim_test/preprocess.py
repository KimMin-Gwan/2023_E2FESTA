import json
import random
import os

FILE_PATH = 'D:/kor_dataset/write/'
test = ['htr/word_check', 'ocr_test/word_check', 'print/check', 'Text']
for arg in test:
    ocr_files = os.listdir(FILE_PATH + arg)
    print(ocr_files)

exit()


def save_file(file, train_annotations, validation_annotations, test_annotations):
    with open('train_annotation.json', 'w',encoding='UTF-8') as file:
        json.dump(train_annotations, file, indent=6,ensure_ascii=False)
    with open('validation_annotation.json', 'w',encoding='UTF-8') as file:
        json.dump(validation_annotations, file,indent=6,ensure_ascii=False)
    with open('test_annotation.json', 'w',encoding='UTF-8') as file:
        json.dump(test_annotations, file,indent=6,ensure_ascii=False)


def main():

    pass

if __name__ == '__main__':
    main()