import tensorflow as tf
import numpy as np
import module.model as model
import module.model_op as model_op

class Tensor():
        def __init__(self):


                print( " [*]: tensorflow loading start...")
                self.batch_size = 1
                self.input_height = 48
                self.input_width = 128
                self.input_channel = 1
                self.conv_1st_filter_n = 16
                self.conv_2nd_filter_n = 32

                self.checkpoint_dir = 'module/checkpoint'

                self.model_name = "CNN_Car_10_48_128"

                self.image = tf.placeholder(tf.float32, [self.batch_size, self.input_height, self.input_width, self.input_channel], name = 'image')
                self.logit = model._net(self.image, self.batch_size, self.conv_1st_filter_n, self.conv_2nd_filter_n)
                self.saver = tf.train.Saver()
                self.sess = tf.Session()
                self.sess.run(tf.global_variables_initializer())

                model_op.model_load(self.checkpoint_dir, self.model_name, self.sess, self.saver)
                self.out_label= self.logit
                print( " [*] tensorflow loading finished")

        def get_tran(self, x):
                x = np.dot(x[...,:3],[0.299,0.587,0.114])

                '''
                value = 70 - np.average(x)
                x = x.astype('uint32')

                x_min = np.min(x)
                x_max = np.max(x)

                if value > 0:
                        x = np.where( x + value > 255, 255, (x + value)*255/(x_max - x_min) )
                else:
                        x = np.where( x + value < 0, 0, (x + value)*255/(x_max - x_min) )
                x = x.astype('uint8')
                '''
                x = np.array(x)/255
                x = x[48:96]


                x = np.reshape(x, (1, 48, 128, 1))

                return x

        def run(self, img):
                value = self.sess.run( self.out_label, feed_dict = {self.image : self.get_tran(img)} )
                return value[0][0]
