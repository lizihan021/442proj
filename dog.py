"""
Dogs Dataset
    Class wrapper for interfacing with the dataset of dog images
    Usage:
        - from data.dogs import DogsDataset
        - python -m data.dogs
"""
import numpy as np
import pandas as pd
from scipy.misc import imread, imresize
import os
from utils import get
import re

class DogsDataset:

    def __init__(self):
        # Load in all the data we need from disk

        self.train_path = get('testing_file')
        self.test_path = get('training_file')

    def _load_data(self, partition='train'):
        """
        Loads a single data partition from file.
        """
        if partition == 'train':
            path = self.train_path
        else:
            path = self.test_path
        print("loading %s..." % partition)
        X, y = [], []
        point_location_vector = []
        with open(path) as f:
            lines = f.read().splitlines()
        new_pos = np.asarray([[128-1], [128-1]])
        for line in lines[:10]:
            image = imread(os.path.join(get('image_path'), line))
            row, col, _ = image.shape
            image = imresize(image,(get('image_dim'), get('image_dim')))

            # image
            X.append(image)

            # feature vector
            filename = line.rpartition('.')[0] + '.txt'
            f = open(get('point_location_path') + '/' + filename, 'r')
            one_feature = np.zeros(16)
            points = f.readlines()
            for i in range(len(points)):
                point_x, point_y = points[i].split()
                one_feature[2*i] = int(point_x)*127/(row-1)
                one_feature[2*i+1] = int(point_y)*127/(col-1)
            point_location_vector.append(one_feature)
            
            # dog class
            y.append(re.split('.', re.split('/', line)[0])[0])
        return np.array(X), np.array(y), point_location_vector
        

if __name__ == '__main__':
    dogs = DogsDataset()
    print("Train:\t", len(dogs.trainX))
    print("Test:\t", len(dogs.testX))
