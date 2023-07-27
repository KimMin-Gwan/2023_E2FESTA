

from re import A


a = {'a' : 1, 'b' : 2, 'c' : 3 }
train_annotations = {f:[] for f in a.keys()}

print(train_annotations)

train_ids_img = {a[id_]:id_ for id_ in a}

print(train_ids_img)

exit()
import json
import os
import pandas as pd

file_path = './../../../../TextDataKr/'
file_name = 'handwriting_data_info_clean.json'

with open(file_path + file_name, 'r', encoding='UTF8') as f:
    json_data = json.load(f)
    
    # data_frame = pd.DataFrame(json_data)
    
    print(len(json_data['images']))
    
    # 파일 내의 ID 