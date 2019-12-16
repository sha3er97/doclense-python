import matplotlib.pyplot as plt
from skimage.color import rgb2gray,rgb2hsv,hsv2rgb
import skimage.io as io
from skimage.exposure import histogram
from matplotlib.pyplot import bar
import matplotlib as mpl
import numpy as np
import copy
from scipy.signal import convolve2d
from skimage.util import random_noise
from skimage.exposure import rescale_intensity
from skimage.morphology import binary_erosion, binary_dilation, binary_closing,reconstruction,dilation, erosion, opening, closing
import PIL 
import scipy.ndimage as ndimage
from skimage.measure import find_contours
from skimage.filters import threshold_minimum,median,threshold_otsu
from skimage.transform import resize
from skimage import img_as_bool

def backgroundElimination(img):
    imgCopy = np.copy(img)
    blockSize = 30
    for i in range(0,img.shape[0],blockSize):
        for j in range(0, img.shape[1], blockSize):
            block = img[i:i + blockSize, j:j + blockSize]
            Gmin = np.amin(block)
            Gmax = np.amax(block)
            Tfixed = 100
            Tmin = 50
            Tvar = ((Gmin - Tmin ) - min(Tfixed , Gmin - Tmin )) * 2
            T = Tvar + Tfixed
            intensityVariance = Gmax - Gmin
            if(intensityVariance < T):
                imgCopy[i:i + blockSize, j:j + blockSize] = 255
    return imgCopy

###################################################################################################

def graphicsSeparation(img):
    structural_element = np.array([[1,1,1]
                                  ,[1,1,1]
                                  ,[1,1,1]])
    imgCopy = np.copy(img)
    
    for i in range(10):
        imgCopy = dilation(imgCopy, structural_element)
        
    for i in range(10):
        imgCopy = reconstruction(imgCopy, img, 'erosion', structural_element)
        
    return imgCopy    