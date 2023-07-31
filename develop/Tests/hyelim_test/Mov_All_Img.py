import os
import shutil

FILE_PATH = 'D:/kor_dataset/write/'  # 모든 파일들이 들어있는 경로
data_type = {'필기체' : 'htr/word_check/', '인쇄체' : 'ocr_test/word_check/',
           '증강인쇄체' : 'print/check/', '간판' : 'Text/'}

def move_photo(path, file_list):
    for idx, photo in enumerate(file_list):
        if idx % 5000  == 0:
            print(idx,'/',len(file_list),'move imge data')
            
        shutil.move(path + '/' + photo, FILE_PATH + 'dataset/' + photo) # (기존 폴더, 옮길 폴더)
        
        
def main():
    for key, value in data_type.items():
        print()
        
        now_path = FILE_PATH + value  # 'D:/kor_dataset/write/-----'
        ocr_files = os.listdir(now_path)

        # if key == '필기체':
        #     print('processing now : ', key)
        #     move_photo(now_path, ocr_files)
            
        # if key == '인쇄체':
        #     print('processing now : ', key)
        #     move_photo(now_path, ocr_files)
            
        if key == '증강인쇄체' or key == '간판':
            if key == '간판':
                for fold in ocr_files:
                    now_path = FILE_PATH + value + fold
                    ocr_files = os.listdir(now_path + '/')
                    
                    if key == '간판':
                        for subfold in ocr_files:
                            if ocr_files == 'Thumbs.db':
                                continue
                            now_path = FILE_PATH + value + fold + '/' + subfold
                            print('processing now : ', key)
                            ocr_files = os.listdir(now_path)# + '/' + subfold)
                            move_photo(now_path, ocr_files)
                        
                # else:
                #     print('processing now : ', key)
                #     move_photo(now_path, ocr_files)              
        
if __name__ == '__main__':
    main()