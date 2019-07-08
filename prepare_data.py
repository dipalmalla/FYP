# modified from source https://github.com/jazzsaxmafia/Weakly_detector/blob/master/src/train.caltech.py#L27

import numpy as np
import os
import pandas as pd
from params import TrainingParams, HyperParams, CNNParams

hparams = HyperParams(verbose=False)
tparam = TrainingParams(verbose=False)

image_dir_list = os.listdir(tparam.images_path)

label_pairs = map(lambda x: x.split('.'), image_dir_list)
labels, label_names = zip(*label_pairs)
labels = map(lambda x: int(x), labels)

# label_pairs = [x.split('.') for x in image_dir_list]
# labels, label_names = list(zip(*label_pairs))
# labels = [int(x) for x in labels]

label_dict = pd.Series(labels, index=label_names) - 1
image_paths_per_label = map(lambda one_dir: map(lambda one_file: os.path.join(tparam.images, one_dir, one_file),
                                                os.listdir(os.path.join(tparam.images, one_dir))), image_dir_list)
image_paths_train = np.hstack(map(lambda one_class: one_class[:-10], image_paths_per_label))

# image_paths_per_label = [
#     [os.path.join(tparam.images, one_dir, one_file) for one_file in os.listdir(os.path.join(tparam.images, one_dir))]
#     for one_dir in image_dir_list]
# image_paths_train = np.hstack([one_class[:-10] for one_class in image_paths_per_label])

image_paths_test = np.hstack(map(lambda one_class: one_class[-10:], image_paths_per_label))
# image_paths_test = np.hstack([one_class[-10:] for one_class in image_paths_per_label])

trainset = pd.DataFrame({'image_path': image_paths_train})
testset = pd.DataFrame({'image_path': image_paths_test})

trainset = trainset[trainset['image_path'].map(lambda x: x.endswith('.jpg'))]
trainset['label'] = trainset['image_path'].map(lambda x: int(x.split('/')[-2].split('.')[0]) - 1)
trainset['label_name'] = trainset['image_path'].map(lambda x: x.split('/')[-2].split('.')[1])

testset = testset[testset['image_path'].map(lambda x: x.endswith('.jpg'))]
testset['label'] = testset['image_path'].map(lambda x: int(x.split('/')[-2].split('.')[0]) - 1)
testset['label_name'] = testset['image_path'].map(lambda x: x.split('/')[-2].split('.')[1])

if not os.path.exists(tparam.data_train_path.split('/')[0]):
    os.makedirs(tparam.data_train_path.split('/')[0])

trainset.to_pickle(tparam.data_train_path)
testset.to_pickle(tparam.data_test_path)