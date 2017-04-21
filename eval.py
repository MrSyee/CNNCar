import tensorflow as tf
import numpy as np
import model
import model_op
import time
import sys
import os

config = tf.app.flags
config.DEFINE_integer("epoch", 1, "Epoch to train [1]")
config.DEFINE_float("learning_rate", 0.000002, "Learning rate of for adam [0.0002]")
config.DEFINE_integer("batch_size", 1, "The size of batch images [1]")
config.DEFINE_integer("input_height", 96, "The size of image to use [96]")
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
testX = []
for img in raw_img[150]:
    testX.append(rgb2gray(img))
testX = np.array(testX) / 255
testX = np.reshape(testX, (1, config.input_height, config.input_width, config.input_channel))
# angles
testy = Car_data['angle']/100
testy = np.reshape(testy[150], (1, config.number_classes)) # 출력 : 61
data_size = testX.shape[0]

slim = tf.contrib.slim
log_dir = './logs'
checkpoint_dir = './checkpoint'
model_name = "{}_{}_{}_{}".format('CNN_Car', config.batch_size, config.input_height, config.input_width)

image_summary = tf.summary.image
scalar_summary = tf.summary.scalar
histogram_summary = tf.summary.histogram
merge_summary = tf.summary.merge
SummaryWriter = tf.summary.FileWriter

def test():
    image = tf.placeholder(tf.float32, [config.batch_size, config.input_height, config.input_width, config.input_channel], name = 'image')
    label = tf.placeholder(tf.float32, [config.batch_size, config.number_classes], name = 'label')

    logit = model._net(image, config.batch_size, config.conv_1st_filter_n, config.conv_2nd_filter_n)

    loss = tf.reduce_mean(tf.square(tf.subtract(logit,label)), name = 'loss')

    # 목표 출력과 신경망 출력이 같은지 확인
    is_top1_correct = tf.equal(tf.argmax(label, 1), tf.argmax(logit, 1))

    # 신경망 출력
    out_label = logit

    # 데이터 시각화를 위한 요약 데이터 만드는 작업
    image_summary_ = image_summary('image', image)
    loss_summary = scalar_summary('loss', loss)

    saver = tf.train.Saver()

    Adam = tf.train.AdamOptimizer(config.learning_rate)
    optim = Adam.minimize(loss)

    tot_summary = merge_summary([image_summary_, loss_summary])

    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        test_writer = SummaryWriter(log_dir + '/test', sess.graph)

        # model loading
        print("Model loading starts...")
        model_op.model_load(checkpoint_dir, model_name, sess, saver)
        print(" [*] Load SUCCESS")

        start_time = time.time()
        counter = 1
        batch_idxs = len(testX) // config.batch_size
        print("[*] evaluating starts...")
        for epoch in range(config.epoch):
            top1_correct_num = 0
            for idx in range(batch_idxs):
                # test Image
                test_batch_images = testX[idx*config.batch_size:(idx+1)*config.batch_size]
                test_batch_labels = testy[idx*config.batch_size:(idx+1)*config.batch_size]
                test_data = {image : test_batch_images, label : test_batch_labels}

                # Do not train
                test_l, test_t_s, top1_correct, out_label = sess.run([loss, tot_summary, is_top1_correct, out_label], feed_dict = test_data)
                test_writer.add_summary(test_t_s, counter)

                top1_correct_num += np.sum(top1_correct)
                accuracy = top1_correct_num / float((idx+1)*config.batch_size)

                sys.stdout.write('\r')
                sys.stdout.write("Epoch: [%2d] [%4d/%4d] time: %4.4f Train_loss:%.4f, Out_desire:%.4f, Out_label:%.4f" \
                                        % (epoch, idx, batch_idxs, time.time() - start_time, test_l, testy, out_label))
                sys.stdout.flush()
                counter += 1

            print('')

if __name__ == '__main__':
    if not tf.gfile.Exists(log_dir):
        tf.gfile.MakeDirs(log_dir)
    test()
