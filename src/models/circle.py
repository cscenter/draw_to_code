import keras
import keras.layers as L


def get_circle_model(image_size):
    model = keras.models.Sequential()
    model.add(L.InputLayer(input_shape=[image_size, image_size, 1]))
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
    return model


def find_circle_model(image_size):
    model = keras.models.Sequential()
    model.add(L.InputLayer(input_shape=[image_size, image_size, 1]))
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
    model.add(L.Dense(1, activation='softmax'))

    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model
