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
#from commonfunctions import *
#from autocorrect import spell
class linesegment:
    def __init__(self, startrow,endrow,imgdialated=0):
        self.startrwo = startrow
        self.endrow = endrow
        self.words=[]
        self.img = []
        self.imgdialated = []
class wordsegment:
    def __init__(self, startcol,endcol):
        self.startcol = startcol
        self.endcol = endcol
        self.wordimg=[]
        self.chracters=[]
class char:
    def __init__(self, startcol=0,endcol=0):
        self.startcol = startcol
        self.endcol = endcol
        self.img = []

def texttolines(binary): #this function takes a binary image
# and returns array of linesegment objects 
#which contains (for every line) the image of the line + starting row and ending row 
#in the original image
    height=binary.shape[0]
    width=binary.shape[1]
    b = np.copy(binary)
    dialatedbinary=binary_erosion(b)
    linehistogram=np.zeros(height)
    for j in range(width):
        for i in range (height):
            if(dialatedbinary[i][j]==0):
                linehistogram[i]+=1
    linesegments=[]  
    k=0
    start=0
    end=0
    linehistogramthresh=np.average(linehistogram)
    linehistogramthresh/=10
    #print(linehistogramthresh)
    while k in range(len(linehistogram)):
        if(linehistogram[k]>=linehistogramthresh):
            #print(linehistogram[k])
            start=k
            for end in range(start,len(linehistogram)):
               # print("end is ",end)
                if(linehistogram[end]<=linehistogramthresh):
                    linesegments.append(linesegment(start,end))
                    k=end
                   # print("inner k =",k)
                    break
            if(end>=len(linehistogram)-1):
                break
        
        k+=1

    #print(linesegments)
    #dialated_lines=[] #for word extraction
    countlines=0
    g=0
    while g <len(linesegments):
        if(linesegments[g].endrow-linesegments[g].startrwo>=60):
            plt.imshow(binary)
            linesegments[g].img=binary[linesegments[g].startrwo-5:linesegments[g].endrow+5,0:width]
            linesegments[g].img=median(linesegments[g].img)
            imagefromarr=Image.fromarray(linesegments[g].img*255)
            imagefromarr.save("line "+str(countlines)+" "+'.png')
            n = np.copy(linesegments[g].img)
            d=1-(ndimage.binary_dilation(1-n, iterations=round(width/319)))
            
            #c=np.invert(binary_closing(np.invert(i.img)))
            #c=np.invert(binary_closing(np.invert(c)))
            #c=np.invert(binary_closing(np.invert(c)))
            #imagefromarr=Image.fromarray(d)
            #imagefromarr.save("linedialated "+str(countlines)+" "+'.png')
            #imagefromarr=Image.fromarray(c)
            #imagefromarr.save("lineclosed "+str(countlines)+" "+'.png')
            linesegments[g].imgdialated=d
            imagefromarr=Image.fromarray(d*255)
            imagefromarr.save("linedialated "+str(countlines)+" "+'.png')
            countlines+=1 
        else:
            del linesegments[g]
            g = g-1
        g = g+1
    return linesegments
    #plt.plot(linehistogram)
    #plt.show()
    #io.imshow(binary)
    #imagefromarr=Image.fromarray(binary)
    #imagefromarr.save('binarized.png')        

####################################################################################################

def linestowords(linesegments): #this function takes array of lines and adds
#the following (for each line ):
# array of wordsegment objects which contains (for each word):
# word image + start column + end column 
    countlines=0
    for l in linesegments:
        countwords=0
        #show_images([l.img])
        if(l.endrow-l.startrwo>=15):
            height=l.imgdialated.shape[0]
            width=l.imgdialated.shape[1]
            
            wordhistogram=np.zeros(width)
            for j in range(width):
                for i in range (height):
                    if(l.imgdialated[i][j]==0):
                        wordhistogram[j]+=1
    
            #print("histogram fpr words @ line "+str(countlines)+" : ",wordhistogram)
            k=0
            l.words=[]#set the variable 3shan kant btdrb
            #print(wordhistogram)
            wordhistogramthresh=round(np.average(wordhistogram))
            wordhistogramthresh/=1.5
            print("threshold = ",wordhistogramthresh)
            while k in range(len(wordhistogram)):
                if(wordhistogram[k]>=wordhistogramthresh):
                    #print("1st k=",k)
                    for end in range(k,len(wordhistogram)-2):
                        if(wordhistogram[end]<1 and wordhistogram[end+1]<1  and wordhistogram[end+2]<1):
                            l.words.append(wordsegment(k,end))
                            k=end
                           # print("last k=",k)
                            break
                
                k+=1
            #wordstest=[]
            for m in(l.words):
                #print(m)
                print(m.startcol,m.endcol)
                x=l.img[0:height,m.startcol:m.endcol]
                m.wordimg=x
                #imagefromarr=Image.fromarray(x)
                #imagefromarr.save(str(countlines)+"-"+str(countwords)+'.png')
                #wordstest.append(binary_dilation(x))
                #show_images([binary_dilation(x)])
                countwords+=1
            countlines+=1  

####################################################################################################
# this function takes array of lines and
# adds the following (for each line):
#    for each word:
#       array of char objects which contains :
# image of the character + starting column + end column 
def wordstochracters(lines):
        countlines=0
        countwords=0
        countchar=0
        #show_images([l.img])
        for l in range (len(lines)): #loop on every line
            if(lines[l].endrow-lines[l].startrwo>=15):
                for w in range(len(lines[l].words)):  #loop on every word in the line
                    heightw=lines[l].words[w].wordimg.shape[0]
                    widthw=lines[l].words[w].wordimg.shape[1]
                    charhistogram=np.zeros(widthw) #vertical histogram for the word
                    countchar=0
                    for j in range(widthw):
                        for i in range (heightw):
                            if(lines[l].words[w].wordimg[i][j]==0):
                                charhistogram[j]+=1
    
                    k=0
                    end=-1
                    lines[l].words[w].chracters=[]#set the variable 3shan kant btdrb
                    print(charhistogram)
                    charhistogramthresh=round(np.average(charhistogram))
                    charhistogramthresh/=2
                    charhistogramthresh=round(charhistogramthresh)
                    while k in range(len(charhistogram)):##loop on the histogram
                        if(charhistogram[k]>0): #k is the first column to have a black pixel,so we save it
                            print("1st k=",k)
                            for end in range(k,len(charhistogram)-1): #loop starts with k till the end
                                if((charhistogram[end]==0  ) and (charhistogram[end+1]==0  ) ): #if we found an empty area,the char is completed
                                    lines[l].words[w].chracters.append(char(k,end))#create an object with the coordinates
                                    k=end
                                    print("last k=",k)
                                    break
                            if(end+1==len(charhistogram)-1):
                                lines[l].words[w].chracters.append(char(k,end))#create an object with the coordinates
                                k=end
                                print("last k=",k)
                                break
                                
                        k+=1
                    for m in range(len(lines[l].words[w].chracters)): #loop on these coordinates to cut the word into chars
                        #print(m)
                        #print(m.startcol,m.endcol)
                        if(lines[l].words[w].chracters[m].endcol-lines[l].words[w].chracters[m].startcol>=3):
                            x=lines[l].words[w].wordimg[0:heightw,lines[l].words[w].chracters[m].startcol:lines[l].words[w].chracters[m].endcol] #chop! chop!
                            #imagefromarr=Image.fromarray(x)
                            #imagefromarr.save('line '+str(countlines)+"- word  "+str(countwords)+" char before "+str(countchar)+'.png')#saving the image
                            #wordstest.append(binary_dilation(x))
                            #show_images([x])
                            #resizing the image into 128 x 128 
                            height=x.shape[0]
                            width=x.shape[1]
                            ystart=-1
                            yend=-1
                            xstart=-1
                            xend=-1
                            for i in range (height):
                                for j in range(width):
                                    if(x[i][j]==0):
                                       ystart=i
                                       break
                                    else:
                                        continue
                                if(ystart!=-1):
                                    break
                            for i in range (height):
                                for j in range(width):
                                     if(x[i][j]==0):
                                       yend=i
                            for j in range(width):
                                for i in range (height):
                                     if(x[i][j]==0):
                                       xstart=j 
                                       break
                                     else:
                                        continue
                                if(xstart!=-1):
                                    break
                            for j in range(width):
                               for i in range (height):
                                     if(x[i][j]==0):
                                       xend=j 
                            if(ystart>3 and yend < height-2 and xstart > 2 and xend < width-2 ) :
                                x=x[ystart-3:yend+2,xstart-2:xend+2]
                            elif(ystart>3 and yend < height-2):
                                x=x[ystart-3:yend+2,xstart:xend]
                            elif(xstart > 2 and xend < width-2):
                                x=x[ystart:yend,xstart-2:xend+2]
                            
                            height=x.shape[0]
                            width=x.shape[1]
                            #imagefromarr=Image.fromarray(x)
                            #imagefromarr.save('line '+str(countlines)+"- word  "+str(countwords)+" char "+str(countchar)+'.png')
                            #show_images([x])
                            if(height>=width):
                                factorheight=int(108/height)
                                newwidth=int(width*factorheight)
                                if(newwidth%2 !=0):
                                    newwidth+=1
                                resized=img_as_bool(resize(x, (118,newwidth),anti_aliasing=True))
                                window=np.ones((128,128)) 
                                window[5:123,(64-int(newwidth/2)):(64+int(newwidth/2))]=resized
                                #window=np.logical_and(window==1 , resized)
                            else:
                                factorwidth=int(108/width)
                                newheight=int(height*factorwidth)
                                if(newheight%2 !=0):
                                    newheight+=1
                                resized=img_as_bool(resize(x, (newheight,118),anti_aliasing=True))
                                window=np.ones((128,128)) 
                                window[(64-int(newheight/2)):(64+int(newheight/2)),5:123]=resized
                            window=img_as_bool(window)
                            #resized=img_as_bool(resize(x, (128, 128),anti_aliasing=True))
                            #show_images([window])
                            imagefromarr=Image.fromarray(window)
                            imagefromarr.convert('P')
                            imagefromarr.save('./results/line '+str(countlines)+"- word  "+str(countwords)+" char resized "+str(countchar)+'.png')
                            lines[l].words[w].chracters[m].img=window
                            countchar+=1
                    countwords+=1
                countlines+=1
                countwords=0 