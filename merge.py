#built in functions :

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
mpl.rcParams['figure.dpi'] = 150
##########################################

#import our files

from thersholding import *
from testing_functions import *
from textToChracters import *
from text_extraction import *
############################################

def read_image(name): #take image name return uint8 grayscale image ndarray

    gray_book1 = io.imread(name)
    hsv_img=rgb2hsv(gray_book1)
    #hsv_img[:,:,0]=hsv_img[:,:,0]/8
    S = hsv_img[:,:,1]
    hsv_img[:,:,1] = np.zeros((S.shape[0],S.shape[1]))
        
    gray_book1=hsv2rgb(hsv_img)
    #show_images([gray_book1],["gray_book1"])

    gray_book1=(rgb2gray(gray_book1)*255).astype(np.uint8)

    return gray_book1

############################################################
#main function

#read image
gray_img=read_image("./testCases/a.jpg")

#detect text regions
backgroundEliminatedImg = backgroundElimination(gray_img)
graphicalContentImg = graphicsSeparation(backgroundEliminatedImg)
#textualContentImg = backgroundEliminatedImg - graphicalContentImg
textualContentImg =graphicalContentImg - backgroundEliminatedImg 
textualContentImg = 255 - textualContentImg

print(textualContentImg,type(textualContentImg))
print(np.max(textualContentImg),np.min(textualContentImg),np.average(textualContentImg))
#binarize and denoise
binary_img = binarize(textualContentImg,mode=1)
binary_img2 = binarize(textualContentImg,mode=2)
binary_img4 = binarize(textualContentImg,mode=4)

'''
thershold modes :
1 : optimalThersholding
2 : threshold_otsu
3 : threshold_minimum
default : global thershold =0.4
'''
#filtered_img = apply_filter(binary_img,3,mode=1) #window size 3*3 

'''
filter modes :
1 : maxFilter
2 : minFilter
default : medianFilter
'''
show_images([binary_img,binary_img2,binary_img4],["1","2","4"])
print(binary_img,binary_img2,binary_img4)
print (type(binary_img),type(binary_img2),type(binary_img4))

saveImages([binary_img,binary_img2,binary_img4])
