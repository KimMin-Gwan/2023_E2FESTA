import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

(trainX, trainY), (testX, testY) = tf.keras.datasets.fashion_mnist.load_data()

"""
print(trainX[0])
"""

# print(trainX.shape)

# plt.imshow(trainX[10])
# plt.show()

class_name = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneakers', 'Bag', 'Ankelboots']


# 3차원에서 4차원으로 바꿔줌
trainX = trainX.reshape((trainX.shape[0], 28, 28, 1))
testX = testX.reshape((testX.shape[0], 28, 28, 1))

print(trainX.shape)

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), padding="same", activation= "relu", input_shape=(28, 28, 1)),
    tf.keras.layers.MaxPooling2D( (2, 2) ),
    tf.keras.layers.Conv2D( 64, (3, 3), padding="same", activation= "relu", input_shape=(28, 28, 1) ),
    tf.keras.layers.MaxPooling2D( (2, 2) ),
    # tf.keras.layers.Dense(128, input_shape=(28,28), activation = "relu"),
    tf.keras.layers.Flatten(),  # 출력은 1차원으로 할것이라서
    tf.keras.layers.Dense(128, activation = "relu"),
    tf.keras.layers.Dense(10, activation = "softmax")  # sigmoid의 여러개 버전
])

# loss 계산, optimizer = 경사하강법에서 씀 / accuracy
model.compile(loss = "sparse_categorical_crossentropy", optimizer="adam", metrics=['accuracy'])
model.fit(trainX, trainY, epochs = 10)  # 10번 학습시킴

score = model.evaluate(testX, testY)
print(score)