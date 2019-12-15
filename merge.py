#built in functions :

%matplotlib inline
%load_ext autoreload
%autoreload 2
from skimage.color import rgb2gray,rgb2hsv,hsv2rgb
import skimage.io as io
from skimage.exposure import histogram
from matplotlib.pyplot import bar
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from skimage.filters import threshold_otsu
import copy
from scipy.signal import convolve2d

##########################################

#import our files

import thersholding.py
import testing_functions.py

############################################

def read_image(name): #take image name return uint8 grayscale image ndarray

    gray_book1 = io.imread(name)
    hsv_img=rgb2hsv(gray_book1)
    #hsv_img[:,:,0]=hsv_img[:,:,0]/8
    S = hsv_img[:,:,1]
    hsv_img[:,:,1] = np.zeros((S.shape[0],S.shape[1]))
    
    #show_images([gray_book1,Hue,S],["gray_book1","Hue","S"])
    
    gray_book1=hsv2rgb(hsv_img)
    show_images([gray_book1],["gray_book1"])

    gray_book1=(rgb2gray(gray_book1)*255).astype(np.uint8)

    return gray_book1

