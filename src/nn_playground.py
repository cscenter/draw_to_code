import keras
import keras.layers as L

import numpy as np

from geometry_generator import generate_circle
from geometry import Circle, Point
from pil_pic_generator import generate_pil_image, save_pil_image

IMAGE_SIZE = 64

model = keras.models.Sequential()
model.add(L.InputLayer(input_shape=[IMAGE_SIZE, IMAGE_SIZE, 3]))
model.add(L.Conv2D(filters=40, kernel_size=(3, 3)))
model.add(L.BatchNormalization())
model.add(L.Activation('relu'))
model.add(L.Conv2D(filters=40, kernel_size=(3, 3)))
model.add(L.MaxPooling2D(pool_size=(2, 2)))
model.add(L.Activation('relu'))
model.add(L.Dropout(0.15))

model.add(L.Conv2D(filters=80, kernel_size=(3, 3)))
model.add(L.BatchNormalization())
model.add(L.Activation('relu'))
model.add(L.Conv2D(filters=80, kernel_size=(3, 3)))
model.add(L.MaxPooling2D(pool_size=(2, 2)))
model.add(L.Activation('relu'))
model.add(L.Dropout(0.15))

model.add(L.Conv2D(filters=160, kernel_size=(3, 3)))
model.add(L.BatchNormalization())
model.add(L.Activation('relu'))
model.add(L.MaxPooling2D(pool_size=(2, 2)))
model.add(L.Activation('relu'))
model.add(L.Dropout(0.15))

model.add(L.Flatten())
model.add(L.Dense(700, activation='relu'))
model.add(L.Dropout(0.2))
model.add(L.Dense(3))

model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

X_train = []
y_train = []

for i in range(5000):
    circle = generate_circle(IMAGE_SIZE)
    im = generate_pil_image([circle], IMAGE_SIZE)
    x, y = np.array(im), np.array([circle.center.x, circle.center.y, circle.radius])
    X_train.append(x)
    y_train.append(y)

X_train = np.array(X_train)
y_train = np.array(y_train)

model.fit(X_train, y_train, epochs=3)

circle = generate_circle(IMAGE_SIZE)
im = generate_pil_image([circle], IMAGE_SIZE)
x = np.array([np.array(im)])
result = model.predict(x)

print(circle.center.x)
print(circle.center.y)
print(circle.radius)
print(result)

result_im = generate_pil_image([circle, Circle(Point(result[0][0], result[0][1]), result[0][2], color=(255, 13, 13))], IMAGE_SIZE)
save_pil_image(result_im, "test.png")
