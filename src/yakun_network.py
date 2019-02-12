import tensorflow as tf


def first_nn(input_layer):
    lay1 = tf.layers.dense(input_layer, 5, 3,
                           activation=tf.nn.relu,
                           kernel_initializer=tf.variance_scaling_initializer,
                           kernel_regularizer=tf.contrib.layers.l2_regularizer(0.1))
    lay2 = tf.layers.dense(lay1, )





def nn_for_circles(input):
    pass

