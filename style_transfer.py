import numpy as np
import scipy.misc, transform, os
import tensorflow as tf

def save_img(name, style, img):
    img = np.clip(img, 0, 255).astype(np.uint8)
    scipy.misc.imsave('static/out/'+style+'-'+name, img)

def process(src, style, batch_size=1, device_t='/cpu:0'):
    img = scipy.misc.imread(src, mode='RGB')
    img_shape = img.shape
    g = tf.Graph()

    soft_config = tf.ConfigProto(allow_soft_placement=True)
    soft_config.gpu_options.allow_growth = True

    with g.as_default(), g.device(device_t), tf.Session(config=soft_config) as sess:
        batch_shape = (batch_size,) + img_shape
        img_placeholder = tf.placeholder(tf.float32, shape=batch_shape, name='img_placeholder')

        preds = transform.net(img_placeholder)
        saver = tf.train.Saver()
        saver.restore(sess, style)

        X = np.zeros(batch_shape, dtype=np.float32)
        X[0] = img
        _preds = sess.run(preds, feed_dict={img_placeholder: X})

        save_img(os.path.basename(src), os.path.basename(style), _preds[0])
