import keras
import keras.layers as L


def _get_base_model(image_size):
    model = keras.models.Sequential()
    model.add(L.InputLayer(input_shape=[image_size, image_size, 1]))
    model.add(L.Conv2D(filters=100, kernel_size=(3, 3), strides=3))
    model.add(L.BatchNormalization())
    model.add(L.Activation('relu'))
    model.add(L.Conv2D(filters=80, kernel_size=(3, 3)))
    model.add(L.MaxPooling2D(pool_size=(2, 2)))
    model.add(L.Activation('relu'))
    model.add(L.Dropout(0.15))

    model.add(L.Conv2D(filters=20, kernel_size=(4, 4)))
    model.add(L.MaxPooling2D(pool_size=(2, 2)))
    model.add(L.Activation('relu'))
    model.add(L.Dropout(0.15))

    model.add(L.Conv2D(filters=20, kernel_size=(5, 5)))
    model.add(L.BatchNormalization())
    model.add(L.Activation('relu'))

    model.add(L.Flatten())
    model.add(L.Dense(900, activation='relu'))
    model.add(L.Dropout(0.15))
    model.add(L.Dense(200, activation='relu'))
    model.add(L.Dropout(0.15))

    return model


def get_segment_model(image_size):
    model = _get_base_model(image_size)
    model.add(L.Dense(4))

    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    return model


def find_segment_model(image_size):
    model = _get_base_model(image_size)
    model.add(L.Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model
