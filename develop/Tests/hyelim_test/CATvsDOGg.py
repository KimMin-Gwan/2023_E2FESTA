import os
import tensorflow as tf
import shutil
"""
os.environ['TF_CPP_MIN_LOG_LEVEL']='3'
print( len( os.listdir('./../../../../dogs-vs-cats-redux-kernels-edition/train/')))

for i in os.listdir('./../../../../dogs-vs-cats-redux-kernels-edition/train/'):
    if 'cat' in i:
        shutil.copyfile('./../../../../dogs-vs-cats-redux-kernels-edition/train/' + i , './../../../../dogs-vs-cats-redux-kernels-edition/dataset/cat/' + i)
    if 'dog' in i:
        shutil.copyfile('./../../../../dogs-vs-cats-redux-kernels-edition/train/' + i , './../../../../dogs-vs-cats-redux-kernels-edition/dataset/dog/' + i)
"""


# Image Aumentation
# -> overfitting 줄이기 위해 이미지 변화주기 

from tensorflow.keras.preprocessing.image import ImageDataGenerator

generator = ImageDataGenerator(
    rescale = 1./255,
    rotation_range = 20,  # 회전
    zoom_range = 0.15,   # 확대
    width_shift_range = 0.2,  # 이동
    height_shift_range = 0.2,
    shear_range = 0.15,  # 굴절
    horizontal_flip = True,  # 가로 반전
    fill_mode = "nearest"
)

generator_tarin = generator.flow_from_directory(
    './../../../../dogs-vs-cats-redux-kernels-edition/dataset/',
    class_mode = 'binary', # 두 개면 binary, 그 이상이면 categorical
    shuffle = True,
    seed = 123,  # random seed
    color_mode = 'rgb', #  'gray'
    batch_size = 64,
    target_size = (64, 64)
)
"""
#-----------------------------------------------------------------------------------------

# batch size -> epoch에 한번에 모든 데이터를 넣는 게 아니고, batch size 만큼만 넣어줌
# train data = ( (xxxxxx (실제 데이터) ), (0 or 1 (정답) ) )
# seed -> random한 정도

# validation_split = 0.2 -> 80% 만큼 쪼개서 사용함
"""
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    './../../../../dogs-vs-cats-redux-kernels-edition/dataset/', 
    image_size = (64, 64),
    batch_size = 64 ,
    subset = 'training',  # 이름 같은 역할...?
    validation_split = 0.2,  # 20%만큼 validation으로 빼고 나머지 80%는 training으로 사용
    seed = 1234  # 랜덤한 정도 (아무 값이나 상관 X)
)

print()

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    './../../../../dogs-vs-cats-redux-kernels-edition/dataset/', 
    image_size = (64, 64),
    batch_size = 64,
    subset = 'validation',
    validation_split = 0.2,  # 20%만큼 validation으로 사용
    seed = 1234
)

"""
print()

print(train_ds)

# 모든 데이터를 255로 나눠서 0 ~ 1 사이로 압축하기 (RGB 값이 0~255이기 때문)
# 학습 속도를 빠르게 하기 위함 (정수 < 실수)

def 전처리함수(i, 정답):
    i = tf.cast( i / 255.0, tf.float32 )
    return i, 정답

#train_ds = train_ds.map(전처리함수)
#val_ds = val_ds.map(전처리함수)

for i, 정답 in train_ds.take(1):
    print(i)
    print(정답)

#학습------------------------------------------------------

import matplotlib.pyplot as plt

for i, 정답 in train_ds.take(1):
    print(i[0].numpy())
    print(정답)
    plt.imshow( i[0].numpy())
    plt.imshow( i[0].numpy().astype('uint8') )
    plt.show()


#input_shape -> RGB라서 64 64 3
#마지막 dense는 sigmoid -> binary_crossentropy는 sigmoid를 필요로 함
#마지막 dense는 개인지 고양이인지만 확인하면됨. 따라서 1개의 레이어에 sigmoid로 확률 출력
#Dropout(0.2) -> 현재 레이어에서 20%를 제거하여 정형화된 데이터 생성을 막음 -> overfitting을 막는다.

model = tf.keras.Sequential([
    tf.keras.layers.experimental.preprocessing.RandomFlip('horizontal'), # 이미지 뒤집기 (50% 확률)
    tf.keras.layers.experimental.preprocessing.RandomRotation(0.1), # 이미지 돌리기 (50% 확률)
    tf.keras.layers.experimental.preprocessing.RandomZoom(0.1), # 이미지 확대 (50% 확률)

    tf.keras.layers.Conv2D( 32, (3, 3), padding = "same", activation = 'relu', input_shape= (64, 64, 3) ),
    tf.keras.layers.MaxPooling2D( (2, 2) ),
    tf.keras.layers.Conv2D( 64, (3, 3), padding = "same", activation = 'relu', input_shape= (64, 64, 3) ),
    tf.keras.layers.MaxPooling2D( (2, 2) ),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Conv2D( 128, (3, 3), padding = "same", activation = 'relu', input_shape= (64, 64, 3) ),
    tf.keras.layers.MaxPooling2D( (2, 2) ),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation = "relu" ),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(1, activation = "sigmoid" ),
])

# model.summary()

model.compile( loss = "binary_crossentropy", optimizer = "adam", metrics = ['accuracy'] )
model.fit(train_ds, validation_data = val_ds, epochs = 5 )


"""
#model.evaluate(val_ds)
model = tf.keras.models.load_model('./model2/')
#model.save('./model2')

#sample_predictions = model.predict(test_data[10])
import cv2
import matplotlib.pyplot as plt
import numpy as np


test = cv2.imread('./../../../../dogs-vs-cats-redux-kernels-edition/test/27.jpg')
#print(pred)


resized_img_1 = cv2.resize(test, dsize=(64, 64))
print(resized_img_1.shape)

# 차원 변경
modified_array = np.expand_dims(resized_img_1, axis=0)
pred = model.predict(modified_array)

plt.imshow( resized_img_1)
if pred < 0.5:
    print('고양이')
else:
    print('강아지')
plt.show()


print(pred)
"""
# 결과 출력
print(modified_array.shape)

#print(sample_predictions[10])
#print(test)
plt.imshow(test)
plt.show()

"""