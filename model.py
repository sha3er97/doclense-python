# All the imports you will need in the whole lab
from skimage.feature import greycomatrix, greycoprops
from skimage import io
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import os
import numpy 
from PIL import Image
#from commonfunctions import *
import copy
#from sklearn.cluster import KMeans
#from commonfunctions import *
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage.morphology import binary_erosion, binary_dilation, binary_closing,skeletonize, thin ,opening,closing
from skimage.measure import find_contours
from skimage.draw import rectangle
#from sklearn.svm import SVC
#from sklearn.preprocessing import normalize
#from tensorflow.keras.layers import Dense, Dropout
import numpy as np 
import pandas as pd
from skimage.feature import hog
import matplotlib.pyplot as plt
#from sklearn.model_selection import train_test_split
#from sklearn.naive_bayes import GaussianNB
#from sklearn.model_selection import cross_val_score
#from sklearn.metrics import accuracy_score, roc_curve
#from sklearn.preprocessing import normalize
#from tensorflow.keras.models import Sequential
#from tensorflow.keras.layers import Dense, Dropout,BatchNormalization
#from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
#from commonfunctions import *
import pickle
from skimage.feature import (corner_harris, corner_peaks, BRIEF)
from skimage.exposure import rescale_intensity
from skimage.transform import rescale, resize, downscale_local_mean
#import tensorflow as tf
#from tensorflow.keras.models import load_model



alphabet = [
        'a',
        'b',
        'c',
        'd',
        'e',
        'f',
        'g',
        'h',
        'i',
        'j',
        'k',
        'l',
        'm',
        'n',
        'o',
        'p',
        'q',
        'r',
        's',
        't',
        'u',
        'v',
        'w',
        'x',
        'y',
        'z',
        'A',
        'B',
        'D',
        'E',
        'F',
        'G',
        'H',
        'I',
        'J',
        'L',
        'M',
        'N',
        'Q',
        'R',
        'T',
        'Y',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9'
    ]
def random_shuffle(a, b):
    assert len(a) == len(b)
    a = numpy.asarray(a)
    b = numpy.asarray(b)
    p = numpy.random.permutation(len(a))
    return a[p], b[p]


def harris_features(X, imgshape=(128, 128)):
    features = []
    img = X.reshape(imgshape)
    img_features_harris = corner_peaks(corner_harris(img), min_distance=1)
    img_harris = np.zeros(imgshape)
    img_harris[img_features_harris[:,0],img_features_harris[:,1]] = 1
    img_harris = rescale(img_harris, 0.4, anti_aliasing=True)>0
    img_harris = np.reshape(img_harris,(img_harris.shape[0]*img_harris.shape[1],))
    features=img_harris
    return np.array(features)

def hog_features(X, imgshape=(128, 128), pixels_per_cell=(8, 8)):
    features = []
    img = X.reshape(imgshape)
    features = hog(img, orientations=8, pixels_per_cell=pixels_per_cell, cells_per_block=(1, 1))
    return np.array(features)

def edge_features(X, imgshape=(128, 128)):
    features = []
    img = X.reshape(imgshape)
    img = rescale(img, 0.4, anti_aliasing=True)>0
    img_edge = canny(img, sigma=3, low_threshold=0.3, high_threshold=0.8)
    img_edge = 1*(np.reshape(img_edge,(img_edge.shape[0]*img_edge.shape[1],)))
    features=img_edge
    return np.array(features)

def skeleton_features(X, imgshape=(128, 128)):
    features = []
    img = X.reshape(imgshape)
    img = 1-rescale(img, 0.4, anti_aliasing=True)>0
    img_skeleton = skeletonize(img)
    img_skeleton = 1*(np.reshape(img_skeleton,(img_skeleton.shape[0]*img_skeleton.shape[1],)))
    features=img_skeleton
    return np.array(features)

def features(X, imgshape=(128, 128), pixels_per_cell=(8, 8)):
    features = []
    i = 0
    for row in X:
        i = i+1
        img_features = []
        row=row.astype(numpy.float32)
        img_features = np.concatenate((hog_features(row),harris_features(row)), axis=None)
        features.append(img_features)
        print(i)
    return np.array(features)


def predict (char):
    model = load_model('model.h5')
    char = np.asarray(char)
    char = numpy.reshape(char,[1,-1])
    char = features(char, pixels_per_cell=(8, 8))
    char_normalized = normalize(char)
    y_pred = model.predict_classes(char_normalized)
    return alphabet[y_pred[0]]




