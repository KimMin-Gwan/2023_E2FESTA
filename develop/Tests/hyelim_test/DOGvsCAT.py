import os
import tensorflow as tf
import shutil

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
print(len(os.listdir('./../../../../dogs-vs-cats-redux-kernels-edition/train/train/')))

for i in os.listdir('./../../../../dogs-vs-cats-redux-kernels-edition/train/train/'):
    if 'cat' in i:
        shutil.copyfile('./../../../../dogs-vs-cats-redux-kernels-edition/train/train/' + i, './../../../../dogs-vs-cats-redux-kernels-edition/dataset/cat/' + i)
    if 'dog' in i:
        shutil.copyfile('./../../../../dogs-vs-cats-redux-kernels-edition/train/train/' + i, './../../../../dogs-vs-cats-redux-kernels-edition/dataset/dog/' + i)