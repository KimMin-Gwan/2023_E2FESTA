import os
import sys
import json
import shutil

PATH = "D:/kor_dataset/write/dataset/"
DEST_PATH = "D:/kor_dataset/dataset"
JSON_FILE = {'train' : "D:/kor_dataset/write/train_annotation.json",
             'validation' : "D:/kor_dataset/write/validation_annotation.json",
             'test' : "D:/kor_dataset/write/test_annotation.json"}

#img_file = os.listdir(PATH)

for TYPE, json_path in JSON_FILE.items():
    print(TYPE, " Working")

    with open(json_path, 'r', encoding='UTF-8') as f:
        json_list = json.load(f)

    for idx, file_name in enumerate(json_list.keys()):
        if idx % 1000 == 0:
            print({idx}, " / ", len(json_list))

        value = json_list[file_name]
        if value is None:
            json_list.pop(idx, value) 
            print(1)
        else:
            shutil.move(PATH + file_name,
                    DEST_PATH + "/"+ TYPE + "/"+ file_name)
            
        

print("end of process")

    
    

