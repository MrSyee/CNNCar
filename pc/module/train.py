import tensorflow as tf
import numpy as np
import model
import model_op
import time
import sys
import os

config = tf.app.flags
config.DEFINE_integer("epoch", 2000, "Epoch to train [1000]")
config.DEFINE_float("learning_rate", 0.0001, "Learning rate of for adam [0.0001]")
config.DEFINE_integer("batch_size", 64, "The size of batch images [10]")
config.DEFINE_integer("input_height", 48, "The size of image to use [48]")
config.DEFINE_integer("input_width", 128, "The size of image to use [128]")
config.DEFINE_integer("input_channel", 1, "Dimension of image color. [1]")
config.DEFINE_integer("number_classes", 1, "The size of the output label [1]")
config.DEFINE_integer("conv_1st_filter_n", 16, "The size of 1st conv filter [16]")
config.DEFINE_integer("conv_2nd_filter_n", 32, "The size of 2nd cov filter [32]")
config.DEFINE_integer("model_save_period", 1000, "")
config = config.FLAGS

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

# 입출력 Data 정보
Car_data = np.load("data.npz");
raw_img = Car_data['image']
#images
trainX = []
for img in raw_img:
    trainX.append(rgb2gray(img))
trainX = np.array(trainX) / 255
trainX = np.reshape(trainX, (trainX.shape[0], config.input_height, config.input_width, config.input_channel))
# angles
trainy = Car_data['angle']/100
trainy = np.reshape(trainy, (trainy.shape[0], config.number_classes))
data_size = trainX.shape[0]


slim = tf.contrib.slim
log_dir = './logs'
checkpoint_dir = './checkpoint'
# 저장될 model 이름
model_name = "{}_{}_{}_{}".format('CNN_Car', config.batch_size, config.input_height, config.input_width)

image_summary = tf.summary.image
scalar_summary = tf.summary.scalar
histogram_summary = tf.summary.histogram
merge_summary = tf.summary.merge
SummaryWriter = tf.summary.FileWriter

def train():
    image = tf.placeholder(tf.float32, [config.batch_size, config.input_height, config.input_width, config.input_channel], name = 'image')
    label = tf.placeholder(tf.float32, [config.batch_size, config.number_classes], name = 'label')

    logit = model._net(image, config.batch_size, config.conv_1st_filter_n, config.conv_2nd_filter_n)

    loss = tf.reduce_mean(tf.square(tf.subtract(logit,label)), name = 'loss')

    is_top1_correct = tf.equal(tf.argmax(label, 1), tf.argmax(logit, 1))

    image_summary_ = image_summary('image', image)
    loss_summary = scalar_summary('loss', loss)

    saver = tf.train.Saver()

    Adam = tf.train.AdamOptimizer(config.learning_rate)
    optim = Adam.minimize(loss)

    tot_summary = merge_summary([image_summary_, loss_summary])

    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        train_writer = SummaryWriter(log_dir + '/train', sess.graph)

        print("[*] DataLoader loading starts...")
        # 입출력 Data 정보
        #trainX = np.genfromtxt('./data/train.csv', delimiter = ',')
        #trainX = np.reshape(trainX, (trainX.shape[0], config.input_height, config.input_width, config.input_channel))
        #trainy = np.genfromtxt('./data/train_label.csv', delimiter = ',')

        start_time = time.time()
        counter = 1
        batch_idxs = len(trainX) // config.batch_size
        #batch_idxs = data_size // config.batch_size
        print("[*] Training starts...")
        for epoch in range(config.epoch + 1):
            top1_correct_num = 0
            for idx in range(batch_idxs):
                # Train Image
                train_batch_images = trainX[idx*config.batch_size:(idx+1)*config.batch_size]
                train_batch_labels = trainy[idx*config.batch_size:(idx+1)*config.batch_size]
                train_data = {image : train_batch_images, label : train_batch_labels}

                #train_l, train_t_s, top1_correct, _ = sess.run([loss, tot_summary, is_top1_correct, optim], feed_dict = train_data)
                train_l = sess.run(loss, feed_dict = train_data)
                train_t_s = sess.run(tot_summary, feed_dict = train_data)
                top1_correct = sess.run(is_top1_correct, feed_dict = train_data)
                _ = sess.run(optim, feed_dict = train_data)

                train_writer.add_summary(train_t_s, counter)

                top1_correct_num += np.sum(top1_correct)
                accuracy = top1_correct_num / float((idx+1)*config.batch_size)

                sys.stdout.write('\r')
                sys.stdout.write("Epoch: [%2d] [%4d/%4d] time: %4.4f Train_loss:%.8f" \
                                        % (epoch, idx, batch_idxs, time.time() - start_time, train_l))
                sys.stdout.flush()
                counter += 1

            print('')
            model_op.model_save(model_name, checkpoint_dir, counter, sess, saver)

if __name__ == '__main__':
    if not tf.gfile.Exists(log_dir):
        tf.gfile.MakeDirs(log_dir)
    train()
