import os
import shutil
import json

# json 파일의 key 값과 사진의 이름을 비교해서 같으면 각각의 train/vaild/test 폴더에 넣기

FILE_PATH = 'D:/kor_dataset/write/'  # 모든 파일들이 들어있는 경로
FILE_PATH_IMG = 'dataset_all/'  # 모든 파일들이 들어있는 경로

def main():
    json_names = ['train', 'val', 'test']
    # fold_list = os.listdir(FILE_PATH + FILE_PATH_IMG)
    
    for name in json_names:
        with open(json_names[name] + '.json', 'w', encoding='UTF8') as f
        json_list = json.load(f)
        
        for json_ImgName in json_list.keys():
            move_photo(FILE_PATH + FILE_PATH_IMG + json_ImgName, # 'D:/kor_dataset/write/'dataset_all/__.jpg'
                       FILE_PATH + name + '/' + json_ImgName)    # 'D:/kor_dataset/write/name/__.jpg'

# 'D:/kor_dataset/write/' 안에 폴더 3개 만들기: train, val, test 폴더
        
            
if __name__ == '__main__':
    main()