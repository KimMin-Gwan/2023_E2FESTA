import os
import json

path = "/home/antl/Desktop/dataset/"
f_list = os.listdir(path)

with open(path + f_list[0], 'r', encoding="UTF-8") as f:
    data = json.load(f)
    
print(data['annotations'][0]['bbox'][0])