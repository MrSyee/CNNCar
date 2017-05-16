import tensorflow as tf
import os
# model 학습 후 학습 정보 save
def model_save(model_name, checkpoint_dir, step, sess, saver):
  checkpoint_dir = os.path.join(checkpoint_dir, model_name) # ./checkpoint/model_name 경로
  print(checkpoint_dir)
  # directory가 없으면 새로 만듬
  if not os.path.exists(checkpoint_dir):
    os.makedirs(checkpoint_dir)

  saver.save(sess,
          os.path.join(checkpoint_dir, model_name),
          global_step=step)

def model_load(checkpoint_dir, model_name, sess, saver):
  print(" [*] Reading checkpoints...")
  checkpoint_dir = os.path.join(checkpoint_dir, model_name)

  ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
  if ckpt and ckpt.model_checkpoint_path:
    ckpt_name = os.path.basename(ckpt.model_checkpoint_path)
    saver.restore(sess, os.path.join(checkpoint_dir, ckpt_name))
    print(" [*] Success to read {}".format(ckpt_name))
    return True
  else:
    print(" [*] Failed to find a checkpoint")
    return False
