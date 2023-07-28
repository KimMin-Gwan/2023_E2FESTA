import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

#텐서 플로우에서 제공하는 옷 사진 튜플 받아오기
(trainX, trainY), (testX, testY) = tf.keras.datasets.fashion_mnist.load_data()

#list안에 포함된 데이터는모두 픽셀 단위 정보
#print(trainX[0])

#데이터의 형태(크기, 가로길이, 세로길이)
print(trainX.shape)

#데이터의 라벨 출력
#print(trainY)

#trainY = [0,1,2,3,4,5,6,7,8,9]
class_names = ['T-shirt/top', 'Trouser','Pullover','Dress','Coat','Sandal','Shirt','Sneaker','Bag','Ankelboot']

#plt.imshow(trainX[10])
#plt.show()

trainX = trainX.reshape((trainX.shape[0],28,28,1))
testX=testX.reshape((testX.shape[0],28,28,1))
print(trainX.shape)

#dropout : 이 layer지나갈 때 앞의 a% 버림
#padding : 공백추가
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D( 32, (3, 3), padding="same", activation= "relu", input_shape=(28, 28, 1) ),
    #창의력증가 layer
    tf.keras.layers.MaxPooling2D( (2, 2) ),
    tf.keras.layers.Conv2D( 64, (3, 3), padding="same", activation= "relu", input_shape=(28, 28, 1) ),
    tf.keras.layers.MaxPooling2D( (2, 2) ),
    #tf.keras.layers.Dense(128, input_shape=(28,28), activation = "relu"),
    tf.keras.layers.Flatten(), #출력은 1차원으로 할것이라서
    tf.keras.layers.Dense(128, activation = "relu"),
    tf.keras.layers.Dense(10, activation = "softmax") #sigmoid의 여러개 버전
])

#adam 경사하강법 가짜 최소값 넘어가는 방법, metrics 추가?
model.compile(loss="sparse_categorical_crossentropy", optimizer="adam",metrics=['accuracy'])
#epochs 학습 횟수
model.fit(trainX, trainY, epochs = 10)
score=model.evaluate(testX, testY)
print(score)