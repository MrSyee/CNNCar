import tensorflow as tf
import tensorflow.contrib.slim as slim

def _net(input, batch_size, conv_1st_filter_n = 16, conv_2nd_filter_n = 32):
    with tf.name_scope('conv_model'):
        # Convolution Layer
        net = slim.conv2d(input, 32, [5, 5], scope = 'conv1') # 124 x 44
        net = slim.max_pool2d(net, [2, 2], scope = 'maxpool1') # 62 x 22
        net = slim.conv2d(net, 64, [5, 5], scope = 'conv2') # 58 x 28
        net = slim.max_pool2d(net, [2, 2], scope = 'maxpool2') # 29 x 14
        net = slim.conv2d(net, 64, [5, 5], scope = 'conv3') # 25 x 10
        net = slim.max_pool2d(net, [2,2], scope = 'maxpool3') # 14 x 5
        # Fully connected Layer
        net = tf.reshape(net, [batch_size, -1])
        net = slim.fully_connected(net, 10, activation_fn = tf.nn.relu, scope = 'fc_hidden')
        net = slim.fully_connected(net, 1, activation_fn = tf.nn.sigmoid, scope = 'fc_output')
        print(net.get_shape())
        return net
