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

def show_images(images,titles=None):
    #This function is used to show image(s) with titles by sending an array of images and an array of associated titles.
    # images[0] will be drawn with the title titles[0] if exists
    # You aren't required to understand this function, use it as-is.
    n_ims = len(images)
    if titles is None: titles = ['(%d)' % i for i in range(1,n_ims + 1)]
    fig = plt.figure()
    n = 1
    for image,title in zip(images,titles):
        a = fig.add_subplot(1,n_ims,n)
        if image.ndim == 2: 
            plt.gray()
        plt.imshow(image)
        a.set_title(title)
        n += 1
    fig.set_size_inches(np.array(fig.get_size_inches()) * n_ims)
    plt.show() 


def showHist(img):
    # An "interface" to matplotlib.axes.Axes.hist() method
    plt.figure()
    imgHist = histogram(img, nbins=256)
    
    bar(imgHist[1].astype(np.uint8), imgHist[0], width=0.8, align='center')

def saveImages(imgs):
    for i in range(len(imgs)):
        io.imsave("./results/step "+str(i)+" .jpg",imgs[i],check_contrast=False)
