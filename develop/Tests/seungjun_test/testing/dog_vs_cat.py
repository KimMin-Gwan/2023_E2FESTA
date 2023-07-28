#CNN practice

import tensorflow as tf
import os
import shutil

os.environ['TF_CPP_MIN_LOG_LEVEL']='3'
print(len(os.listdir("./../../../../dogs-vs-cats-redux-kernels-edition/train")))
"""
for i in os.listdir("./../../../../dogs-vs-cats-redux-kernels-edition/train"):
    if 'cat' in i:
        shutil.copyfile("./../../../../dogs-vs-cats-redux-kernels-edition/train/"+i, "./../../../../dogs-vs-cats-redux-kernels-edition/dataset/cat/"+i)
    if 'dog' in i:
        shutil.copyfile("./../../../../dogs-vs-cats-redux-kernels-edition/train/"+i, "./../../../../dogs-vs-cats-redux-kernels-edition/dataset/dog/"+i)
"""
#"C:\Users\yangs\OneDrive\바탕 화면\CDP\dogs-vs-cats-redux-kernels-edition\train"
from tensorflow.keras.preprocessing.image import ImageDataGenerator

generator = ImageDataGenerator(
    rescale = 1./255,
    rotation_range = 20,     #회전
    zoom_range = 0.15,       #확대
    width_shift_range = 0.2,    #이동
    height_shift_range = 0.2,    
    shear_range = 0.15,      #굴절
    horizontal_flip = True,  #가로반전
    fill_mode = "nearest"
)

generator_train = generator.flow_from_directory(
    './../../../../dogs-vs-cats-redux-kernels-edition/dataset',
    class_mode = 'binary',      #2개면 binary, 2개이상 catergorical
    shuffle = True,
    seed = 123,     #random seed
    color_mode = 'rgb',
    batch_size = 64,
    target_size = (64, 64)
)

"""
생성기2 = ImageDataGenerator(rescale = 1./255)

검증용 = 생성기2.flow_from_directory(
    './../../../../dogs-vs-cats-redux-kernels-edition/dataset',
    class_mode = 'binary',
    shuffle = True,
    seed = 123,         #seed : random한 정도
    color_mode = 'rgb',
    batch_size = 64,        #epoch에 모든 데이터를 넣지않고, 이 사이즈만큼 넣음
    target_size = (64, 64)
)
"""
#validation_split = 0.2 -> 20%만큼 검증용으로 사용
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    './../../../../dogs-vs-cats-redux-kernels-edition/dataset',
    image_size = (64, 64),
    batch_size=64,
    subset = 'training',
    validation_split = 0.2,
    seed = 1234
)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    './../../../../dogs-vs-cats-redux-kernels-edition/dataset',
    image_size = (64, 64),
    batch_size=64,
    subset= 'validation',
    validation_split = 0.2,
    seed=1234
)

print(train_ds)

#모든 데이터를 255로 나눠서 0~1 사이로 압축 > 학습속도 개선위해
def 전처리함수(i, 정답):
    i=tf.cast(i / 255.0, tf.float32)
    return i, 정답

train_ds = train_ds.map(전처리함수)
val_ds = val_ds.map(전처리함수)

"""
for i, 정답 in train_ds.take(1):
    print(i)
    print(정답)
"""
#학습--------------------------------------------
import matplotlib.pyplot as plt

"""
for i, 정답 in train_ds.take(1):
    print(i)
    print(정답)
    plt.imshow(i[0].numpy().astype('uint8'))
    plt.show()
"""

#model 생성
model = tf.keras.Sequential([
    tf.keras.layers.experimental.preprocessing.RandomFlip('horizontal'), #이미지 뒤집기 (50%확률)
    tf.keras.layers.experimental.preprocessing.RandomRotation(0.1), #이미지 돌리기
    tf.keras.layers.experimental.preprocessing.RandomZoom(0.1), #이미지 확대

    tf.keras.layers.Conv2D(32, (3, 3), padding = 'same', activation ='relu', input_shape = (64, 64, 3)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), padding = 'same', activation ='relu', input_shape = (64, 64, 3)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Conv2D(128, (3, 3), padding = 'same', activation ='relu', input_shape = (64, 64, 3)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation = "relu"),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(1, activation = "sigmoid"),
])

model.compile(loss="binary_crossentropy", optimizer = "adam", metrics = ['accuracy'])
model.fit(train_ds, validation_data = val_ds, epochs =5)

model.evaluate(val_ds)
