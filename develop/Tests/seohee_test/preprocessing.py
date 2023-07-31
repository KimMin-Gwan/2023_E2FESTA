import os
import shutil


path = ['C:/Users/shp67/zf_file/소스코드','C:/Users/shp67/zf_file/자바']
dest='C:/Users/shp67/zf_file'

for i in path:
    filelist=os.listdir(i)
    
    for file in filelist:
        shutil.move(os.path.join(i, file), dest)


print(filelist[0])

