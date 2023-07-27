path = 'D:/dataset/037.Small object detection을 위한 이미지 데이터/01.데이터/1.Training/1.원천데이터/TS_바다_항구_강/mnt/nas2/Projects/TTA_2022_jgcha/jhbae/037.Small object detection을 위한 이미지 데이터/01.데이터/1.Training/1.원천데이터/TS_바다_항구_강sea01'
import os
filelist=os.listdir(path)
print(filelist[0])

import shutil
for file in filelist:
    shutil.move(path+'/'+file,'D:/dataset/037.Small object detection을 위한 이미지 데이터/01.데이터/1.Training/1.원천데이터/TS_바다_항구_강')