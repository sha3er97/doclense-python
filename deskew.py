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

# new algo
####
def deskew(imgsk):
    imgsk = 1.0*imgsk
    img1 = copy.deepcopy(imgsk)

    imgsk = rescale(imgsk, 0.1, anti_aliasing=False)
    img = img_as_ubyte(imgsk)

    threshold = 50

    # make all pixels < threshold black
    binarized = copy.deepcopy(imgsk)
    binarized1 = copy.deepcopy(img)

    for i in range (binarized.shape[0]-1):
        for j in range (binarized.shape[1]):
            if(binarized[i][j]==0 and binarized[i+1][j]==1):
                binarized1[i][j]=1
            else:
                binarized1[i][j]=0
    #zero last row
    for i in range(binarized1.shape[1]):
        binarized1[binarized1.shape[0]-1][i]=0
    

    kernel = np.ones((1,2),np.uint8)
    binarized1 = cv2.morphologyEx(binarized1, cv2.MORPH_OPEN, kernel)

    ##  hough
    W = binarized1.shape[1]
    H = binarized1.shape[0]
    min_votes = np.sqrt(W*W+H*H).astype(np.uint8)

    lines = []
    while(lines == [] ):
        l = cv2.HoughLines(binarized1,1,np.pi/180,min_votes) 
        if(l is None):
            lines = []
        else:
            lines = l
        min_votes = min_votes-1
    
    thetas = np.squeeze(lines)
    thetas = thetas[1]
    median_theta =  np.degrees(np.median(thetas))-90
    rotated = rotate(img1,angle=median_theta,cval=1)
    plt.imshow(rotated)
    
    result = Image.fromarray((rotated * 255).astype(np.uint8))
    result.save('out1.bmp')
    
    #lines detected
    r=1
    theta = median_theta
    for x in range(len(lines)):
        for r,theta in lines[x]: 
            # Stores the value of cos(theta) in a 
            a = np.cos(theta) 

            # Stores the value of sin(theta) in b 
            b = np.sin(theta) 

            # x0 stores the value rcos(theta) 
            x0 = a*r 

            # y0 stores the value rsin(theta) 
            y0 = b*r 

            # x1 stores the rounded off value of (rcos(theta)-1000sin(theta)) 
            x1 = int(x0 + 1000*(-b)) 

            # y1 stores the rounded off value of (rsin(theta)+1000cos(theta)) 
            y1 = int(y0 + 1000*(a)) 

            # x2 stores the rounded off value of (rcos(theta)+1000sin(theta)) 
            x2 = int(x0 - 1000*(-b)) 

            # y2 stores the rounded off value of (rsin(theta)-1000cos(theta)) 
            y2 = int(y0 - 1000*(a)) 

            # cv2.line draws a line in img from the point(x1,y1) to (x2,y2). 
            # (0,0,255) denotes the colour of the line to be  
            #drawn. In this case, it is red.  
            cv2.line(img,(x1,y1), (x2,y2), (0,0,255),2) 

    # All the changes made in the input image are finally 
    # written on a new image houghlines.jpg 
    cv2.imwrite('linesDetected.jpg', img) 
    
    return rotated.astype("uint8")


