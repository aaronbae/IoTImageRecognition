import numpy as np
import os
import platform
classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')
cifar10_dir = './cifar-10-batches-py/'

img_rows, img_cols = 32, 32
input_shape = (img_rows, img_cols, 3)
def load_pickle(f):
    version = platform.python_version_tuple()
    if version[0] == '2':
        import cPickle as pickle
        return  pickle.load(f)
    elif version[0] == '3':
        import pickle
        return  pickle.load(f, encoding='latin1')
    raise ValueError("invalid python version: {}".format(version))

def load_CIFAR_batch(filename):
    """ load single batch of cifar """
    with open(filename, 'rb') as f:
        datadict = load_pickle(f)
        X = datadict['data']
        Y = datadict['labels']
        X = X.reshape(10000,3072)
        Y = np.array(Y)
        return X, Y

def load_CIFAR10(ROOT):
    """ load all of cifar """
    xs = []
    ys = []
    for b in range(1,6):
        f = os.path.join(ROOT, 'data_batch_%d' % (b, ))
        X, Y = load_CIFAR_batch(f)
        xs.append(X)
        #ys.append(Y) # We don't need the labels
    # We don't need train-test split
    X, Y = load_CIFAR_batch(os.path.join(ROOT, 'test_batch'))
    xs.append(X)
    #xs.append(Y) # We don't need the labels
    all_X = np.concatenate(xs)
    #all_Y = np.concatenate(ys) # We don't need the labels
    del X, Y
    first_500_only = all_X.reshape(60000, 3, 32, 32).transpose(0,2,3,1).astype("uint8")[:500]
    return first_500_only
def get_CIFAR10_data(num_training=49000, num_validation=1000, num_test=10000):
    # Load the raw CIFAR-10 data
    return load_CIFAR10(cifar10_dir)

if __name__ == '__main__':
    # just to test to see if the images are visible
    import numpy as np
    import cv2 
    all_images = get_CIFAR10_data()
    first_image = all_images[3]
    print(first_image.shape)
    cv2.imshow('image',first_image)
    cv2.waitKey()