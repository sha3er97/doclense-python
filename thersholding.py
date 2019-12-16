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

def optimalThersholding(img): #utility function
    H=np.zeros(256)
    Tint=0
    for x in img.flatten():
        H[int(x)] +=1
    for x in range(H.shape[0]):
        Tint += x*H[int(x)]
    H_C=np.zeros(256)
    H_C[0]=H[0]
    for i in range(1,256):
        H_C[i]=H[i]+H_C[i-1] 
    Tint = int(round(Tint/H_C[-1]))
    iterator =0
    while(1):
        iterator +=1
        TintL=0
        TintHI=0
        L=H[0:Tint]
        HI =H[Tint:256]
        for x in range(L.shape[0]):
            TintL += x*L[int(x)]    
        if(H_C[Tint]==0):
            TintL=0
        else:
            TintL = int(round(TintL/(H_C[Tint])))

        for x in range(HI.shape[0]):
            TintHI += x*HI[int(x)]
        if((H_C[-1]==H_C[Tint])):
            TintHI=0
        else:
            TintHI = int(round(TintHI/(H_C[-1]-H_C[Tint])))

        TintPREV =Tint
        Tint = round(TintHI+TintL / 2)
        if(TintPREV==Tint or iterator > 1000):
            break
    
    return int(Tint)

#####################################################################################################

def global_thersholding(img): #utility function

    return int (0.4*255) #global thershold

#######################################################################################################

def choose_thersholding_type(img,mode): #utility function
    if(mode == 1): #default
        return optimalThersholding(img)
    elif(mode == 2):
        return threshold_otsu(img)
    elif(mode == 3):
        return threshold_minimum(img)
    else:
        return global_thersholding(img)

#########################################################################################################

def medianFilter (img,size): #utility function
    M=img.shape[0]
    N=img.shape[1]
    img2=np.ones((M,N))
    W=int(size/2)
    L=int(size/2)
    for i in range (W,M-W):
        for j in range(L,N-L):
            temp=img[i-W:i+W+1,j-L:j+L+1]
            med=np.median(temp.flatten())
            img2[i,j]=int(med)
    return img2

#########################################################################################
def maxFilter (img,size): #utility function
    M=img.shape[0]
    N=img.shape[1]
    img2=np.ones((M,N))
    W=int(size/2)
    L=int(size/2)
    for i in range (W,M-W):
        for j in range(L,N-L):
            temp=img[i-W:i+W+1,j-L:j+L+1]
            maxim=np.median(temp.flatten())
            img2[i,j]=int(maxim)
    return img2
###############################################################################################
def minFilter (img,size): #utility function
    M=img.shape[0]
    N=img.shape[1]
    img2=np.ones((M,N))
    W=int(size/2)
    L=int(size/2)
    for i in range (W,M-W):
        for j in range(L,N-L):
            temp=img[i-W:i+W+1,j-L:j+L+1]
            mini=np.median(temp.flatten())
            img2[i,j]=int(mini)
    return img2
################################################################################################
def binarize(img,mode=1): #interface function
    return 1*(img > choose_thersholding_type(img,mode))

################################################################################################

def apply_filter(img,size,mode=1): #interface function
    if(mode == 1): #default
        return maxFilter(img,size) #brighter image
    elif(mode == 2):
        return minFilter(img,size) #darker image
    else:
        return medianFilter(img,size)
