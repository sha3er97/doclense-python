#built in functions :

import matplotlib.pyplot as plt
from skimage.color import rgb2gray,rgb2hsv,hsv2rgb
import skimage.io as io
from skimage.exposure import histogram
from matplotlib.pyplot import bar
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
#from skimage.filters import threshold_otsu
import copy
from scipy.signal import convolve2d
import skimage.io as io
import numpy as np
from skimage.color import rgb2gray
from scipy import fftpack
from scipy.signal import convolve2d
from skimage.util import random_noise
from skimage.exposure import rescale_intensity
from skimage.filters import *
from skimage.morphology import binary_erosion, binary_dilation, binary_closing,skeletonize, thin
from PIL import Image  
import PIL 
import scipy.ndimage as ndimage
from skimage.measure import find_contours
from skimage.filters import threshold_minimum,median
from skimage.transform import resize
from skimage import img_as_bool
from skimage import io
import numpy as np
from matplotlib import pyplot as plt
from skimage import color
from PIL import Image
from skimage.color import rgb2gray
from scipy import fftpack
from scipy.signal import convolve2d
from skimage.util import random_noise
from skimage.exposure import rescale_intensity
import math
from scipy.ndimage.interpolation import rotate
import statistics
import copy 
from PIL import Image 
import cv2 
import numpy as np 
from skimage.transform import rescale, resize, downscale_local_mean
from skimage import img_as_ubyte
from skimage import io
from skimage import io
import numpy as np
from matplotlib import pyplot as plt
from skimage import color
from PIL import Image
from skimage.color import rgb2gray
from scipy import fftpack
from scipy.signal import convolve2d
from skimage.util import random_noise
from skimage.exposure import rescale_intensity
import math
from scipy.ndimage.interpolation import rotate
import statistics
import copy 
from PIL import Image 
import cv2 
import numpy as np 
from skimage.transform import rescale, resize, downscale_local_mean
from skimage import img_as_ubyte
from skimage import io
# Show the matlpotlib figures inside the notebook
from skimage.morphology import binary_erosion, binary_dilation, binary_closing,skeletonize, thin
from commonfunctions import *
from autocorrect import Speller


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
# Show the matlpotlib figures inside the notebook
##########################################

#import our files

from thersholding import *
from testing_functions import *
from textToChracters import *
from text_extraction import *
from deskew import *
from postprocess import *
from model import *

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


def predictword(word):
    w = ''
    for c in word.chracters:
        chartxt = predict (c.img)
        w = w + chartxt
    #w=Speller(w)+' '
    return w


def predictline(line):
    l = ''
    for w in line.words:
        word = predictword(w)
        l = l + word
    return l

def predicttxt(lines):
    txt = []
    for l in lines:
        line = predictline(l)
        txt.append(line)
    return txt

def main():
    gray_img=read_image("testomar.jpg")

    #detect text regions
    backgroundEliminatedImg = backgroundElimination(gray_img)
    graphicalContentImg = graphicsSeparation(backgroundEliminatedImg)
    #textualContentImg = backgroundEliminatedImg - graphicalContentImg
    textualContentImg =graphicalContentImg - backgroundEliminatedImg 
    textualContentImg = 255 - textualContentImg
    
    #print(textualContentImg,type(textualContentImg))
    #print(np.max(textualContentImg),np.min(textualContentImg),np.average(textualContentImg))
    #binarize and denoise
    img = binarize(textualContentImg,mode=1)
    #binary_img2 = binarize(textualContentImg,mode=2)
    #binary_img4 = binarize(textualContentImg,mode=4)
    
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
    #show_images([binary_img,binary_img2,binary_img4],["1","2","4"])
    #print(binary_img,binary_img2,binary_img4)
    #print (type(binary_img),type(binary_img2),type(binary_img4))
    
   # saveImages([binary_img,binary_img2,binary_img4])






    #img = read_image("testomar.jpg")
    ## to be deleted
    #img = rgb2gray(io.imread("testomar.jpg"))
    #img = img /255
    #img = 1*(img>0.2)
    ####
    
    ### deskew
    img = deskew(img)
    ### segment lines
    #print(np.min(img))
    lines = texttolines(img)
    ###
    ### deskew  lines
   # for i in range(len(lines)):
   #     if(lines[i].endrow-lines[i].startrwo>=lines[i].img.shape[0]/10):
   #         lines[i].img = deskew(lines[i].img)
   #         lines[i].imgdialated = deskew(lines[i].imgdialated)
    ###segment words and chars
    linestowords(lines)
    wordstochracters(lines)
    ###
    ###predict
    txt = predicttxt(lines)
    ###
    for i in txt:
        print(i+'\n')

main()

