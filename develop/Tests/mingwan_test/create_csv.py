import os
import pandas as pd
import json
import time

PATH = "./"
FOLDER_PATH = "./"  
column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']

def json_to_csv(path):
    json_file_list = os.listdir(path)
    data_list = []
    for idx, file_name in enumerate(json_file_list):
        if idx % 500 == 0:
            print(str(idx) +' / ' + str(len(json_file_list)))
        
        with open(path + file_name, 'r', encoding='UTF-8') as f:
            raw_data = json.load(f)
        
        for annotation in raw_data['annotations']:
            value = (str(raw_data['images']['file_named']),
                     int(raw_data['images']['width']),
                     int(raw_data['images']['height']),
                     str(annotation['category_id']),
                     int(annotation['bbox'][0]),
                     int(annotation['bbox'][1]),
                     int(annotation['bbox'][2]),
                     int(annotation['bbox'][3]),
                     )
            data_list.append(value)
    
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    df = pd.DataFrame(data_list, columns=column_name)
    return df

def main():
    data_folder_list = os.listdir(FOLDER_PATH)
    to_csv_file = pd.DataFrame(columns=column_name)
    total_folders = len(data_folder_list)
    
    for idx, folder in enumerate(data_folder_list):
        print("Now processing folder {}/{}: {}".format(idx+1, total_folders, folder))
        start_time = time.time()
        data_frame = json_to_csv(FOLDER_PATH + folder)
        to_csv_file = to_csv_file.append(data_frame)
        elapsed_time = time.time() - start_time
        remaining_time = (total_folders - idx - 1) * elapsed_time
        print("Elapsed time: {:.2f}s, Estimated remaining time: {:.2f}s".format(elapsed_time, remaining_time))
    
    to_csv_file.to_csv((FOLDER_PATH + 'dataset.csv'), index=None)
    print("Successfully converted json to csv")
 

if __name__ == "__main__":
    main()
    
        
            