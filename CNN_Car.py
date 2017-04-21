import tensorflow as tf
import numpy as np
import img2dataset as ids

batch_size = 10
test_size = 10
epoch = 50

def init_weights(shape):
    return tf.Variable(tf.random_normal(shape, stddev=0.01))

def model(X, w, w2, w3, w4, w5, w_o, b1, b2, b3, p_keep_conv, p_keep_hidden):
    l1a = tf.nn.relu(tf.nn.conv2d(X, w,                       # l1a shape=(?, 86, 86, 32)
                        strides=[1, 1, 1, 1], padding='SAME'))
    l1 = tf.nn.max_pool(l1a, ksize=[1, 2, 2, 1],              # l1 shape=(?, 43, 43, 32)
                        strides=[1, 2, 2, 1], padding='SAME')
    l1 = tf.nn.dropout(l1, p_keep_conv)

    l2a = tf.nn.relu(tf.nn.conv2d(l1, w2,                     # l2a shape=(?, 43, 43, 64)
                        strides=[1, 1, 1, 1], padding='SAME'))
    l2 = tf.nn.max_pool(l2a, ksize=[1, 2, 2, 1],              # l2 shape=(?, 22, 22, 64)
                        strides=[1, 2, 2, 1], padding='SAME')
    l2 = tf.nn.dropout(l2, p_keep_conv)

    l3a = tf.nn.relu(tf.nn.conv2d(l2, w3,                     # l3a shape=(?, 22, 22, 128)
                        strides=[1, 1, 1, 1], padding='SAME'))
    l3 = tf.nn.max_pool(l3a, ksize=[1, 2, 2, 1],              # l3 shape=(?, 11, 11, 128)
                        strides=[1, 2, 2, 1], padding='SAME')

    l3 = tf.reshape(l3, [-1, w4.get_shape().as_list()[0]])    # reshape to (?, 11*11*128)
    l3 = tf.nn.dropout(l3, p_keep_conv)

    l4 = tf.nn.relu(tf.add(tf.matmul(l3, w4),b1))
    l4 = tf.nn.dropout(l4, p_keep_hidden)

    l5 = tf.nn.relu(tf.add(tf.matmul(l4, w5),b2))
    l5 = tf.nn.dropout(l5, p_keep_hidden)

    py_x = tf.add(tf.matmul(l5, w_o),b3)
    return py_x

mnist = np.load("./iris_50.npz")
trX = mnist['trainimg']
trY = mnist['trainlabel']
teX = mnist['testimg']
teY = mnist['testlabel']
trX = trX.reshape(-1, 86, 86, 1)  # 86*86*1 input img
teX = teX.reshape(-1, 86, 86, 1)  # 86*86*1 input img

X = tf.placeholder("float", [None, 86, 86, 1])
Y = tf.placeholder("float", [None, 5])

w = init_weights([9, 9, 1, 32])       # 3x3x1 conv, 32 outputs
w2 = init_weights([7, 7, 32, 64])     # 3x3x32 conv, 64 outputs
w3 = init_weights([5, 5, 64, 128])    # 3x3x32 conv, 128 outputs
w4 = init_weights([128 * 11 * 11, 625]) # FC 128*11*11 inputs, 625 outputs
w5 = init_weights([625, 625])        # FC 625 inputs, 625 outputs
w_o = init_weights([625, 5])         # FC 625 inputs, 5 outputs (labels)
# FC bias
b1 = init_weights([625])
b2 = init_weights([625])
b3 = init_weights([5])

p_keep_conv = tf.placeholder("float")
p_keep_hidden = tf.placeholder("float")
py_x = model(X, w, w2, w3, w4, w5, w_o, b1, b2, b3, p_keep_conv, p_keep_hidden)

cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(py_x, Y))
train_op = tf.train.AdamOptimizer(learning_rate=0.00001).minimize(cost)
predict_op = tf.argmax(py_x, 1)

# Launch the graph in a session
with tf.Session() as sess:
    # you need to initialize all variables
    tf.initialize_all_variables().run()

    for i in range(epoch):
        training_batch = zip(range(0, len(trX), batch_size),
                             range(batch_size, len(trX)+1, batch_size))
        for start, end in training_batch:
            sess.run(train_op, feed_dict={X: trX[start:end], Y: trY[start:end],
                                          p_keep_conv: 0.8, p_keep_hidden: 0.5})
            '''
            print sess.run(cost, feed_dict={X: trX[start:end], Y: trY[start:end],
                                                  p_keep_conv: 1.0, p_keep_hidden: 1.0})/batch_size
            '''

        test_indices = np.arange(len(teX)) # Get A Test Batch
        np.random.shuffle(test_indices)
        test_indices = test_indices[0:test_size]
        '''
        print (sess.run(py_x, feed_dict={X:teX[test_indices],
                                        p_keep_conv: 1.0,
                                        p_keep_hidden: 1.0}))

        print (np.argmax(teY[test_indices], axis=1))
        print (sess.run(predict_op, feed_dict={X: teX[test_indices],
                                              p_keep_conv: 1.0,
                                              p_keep_hidden: 1.0}))
        '''

        print ("%04d" % (i+1), "test Accuracy : " ,np.mean(np.argmax(teY[test_indices], axis=1) ==
                         sess.run(predict_op, feed_dict={X: teX[test_indices],
                                                         p_keep_conv: 1.0,
                                                         p_keep_hidden: 1.0})))

    # test : number of 10
    print (np.argmax(teY[test_indices], axis=1))
    print (sess.run(predict_op, feed_dict={X: teX[test_indices],
                                              p_keep_conv: 1.0,
                                              p_keep_hidden: 1.0}))
    # Get one and predict
    import random
    r = random.randrange(teY.shape[0]-1)
    print 'Label: ', sess.run(tf.argmax(teY[r:r+1],1))
    print 'Prediction: ', sess.run(tf.argmax(py_x,1),{X: teX[r:r+1],
                                                         p_keep_conv: 1.0,
                                                         p_keep_hidden: 1.0})

    # transporm change 28x28
    import matplotlib.pyplot as plt
    feature1 = sess.run(l1a, feed_dict={X:teX[r:r+1]})
    plt.subplot(2,2,1)
    plt.imshow(feature1[:,:,:,1].reshape(86,86), cmap='Greys', interpolation='nearest')
    feature2 = sess.run(l2a, feed_dict={X:teX[r:r+1]})
    plt.subplot(2,2,2)
    plt.imshow(feature2[:,:,:,1].reshape(86,86), cmap='Greys', interpolation='nearest')
    feature3 = sess.run(l3a, feed_dict={X:teX[r:r+1]})
    plt.subplot(2,2,3)
    plt.imshow(feature3[:,:,:,1].reshape(86,86), cmap='Greys', interpolation='nearest')
    plt.subplot(2,2,4)
    plt.imshow(teX[r:r+1].reshape(86,86), cmap='Greys', interpolation='nearest')
    plt.show()

    print "Optimization Finished"

    # Test model
    correct_prediction = tf.equal(tf.argmax(py_x,1), tf.argmax(Y,1))
    #Calculate accuracy
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    print "Final Accuracy: ", accuracy.eval({X: teX, Y: teY,
                                       p_keep_conv: 1.0,
                                       p_keep_hidden: 1.0})
