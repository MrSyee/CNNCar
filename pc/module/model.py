import tensorflow as tf
import tensorflow.contrib.slim as slim

def _net(input, batch_size, conv_1st_filter_n = 16, conv_2nd_filter_n = 32):
    with tf.name_scope('conv_model'):
        # Convolution Layer
        net = slim.conv2d(input, 32, [3, 3], scope = 'conv1')
        net = slim.max_pool2d(net, [2, 2], scope = 'maxpool1')
        net = slim.conv2d(net, 64, [3, 3], scope = 'conv2')
        net = slim.max_pool2d(net, [2, 2], scope = 'maxpool2')
        net = slim.conv2d(net, 128, [3, 3], scope = 'conv3')
        net = slim.max_pool2d(net, [2, 2], scope = 'maxpool3')
        # Fully connected Layer
        net = tf.reshape(net, [batch_size, -1])
        net = slim.fully_connected(net, 512, activation_fn = tf.nn.sigmoid, scope = 'fc_hidden')
        net = slim.dropout(net, 0.7, scope='dropout')
        net = slim.fully_connected(net, 512, activation_fn = tf.nn.sigmoid, scope = 'fc_hidden2')
        net = slim.dropout(net, 0.7, scope='dropout')
        net = slim.fully_connected(net, 1, activation_fn = tf.nn.sigmoid, scope = 'fc_output')
        print(net.get_shape())
        return net
