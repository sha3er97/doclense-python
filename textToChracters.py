class linesegment:
    def __init__(self, startrow,endrow,imgdialated=0):
        self.startrwo = startrow
        self.endrow = endrow
        words=[]
        img
        imgdialated
class wordsegment:
    def __init__(self, startcol,endcol):
        self.startcol = startcol
        self.endcol = endcol
        self.wordimg=0
        self.chracters=[]
class char:
    def __init__(self, startcol=0,endcol=0):
        self.startcol = startcol
        self.endcol = endcol
        img

def texttolines(binary): #this function takes a binary image
# and returns array of linesegment objects 
#which contains (for every line) the image of the line + starting row and ending row 
#in the original image
    height=binary.shape[0]
    width=binary.shape[1]
    dialatedbinary=np.invert(binary_dilation(np.invert(binary)))
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
    for i in(linesegments):
        if(i.endrow-i.startrwo>=15):
            i.img=binary[i.startrwo-5:i.endrow+5,0:width]
            imagefromarr=Image.fromarray(i.img)
            imagefromarr.save("line "+str(countlines)+" "+'.png')
            d=np.invert(ndimage.binary_dilation(np.invert(i.img), iterations=2))
            #c=median(i.img)
            #c=np.invert(binary_closing(np.invert(i.img)))
            #c=np.invert(binary_closing(np.invert(c)))
            #c=np.invert(binary_closing(np.invert(c)))
            #imagefromarr=Image.fromarray(d)
            #imagefromarr.save("linedialated "+str(countlines)+" "+'.png')
            #imagefromarr=Image.fromarray(c)
            #imagefromarr.save("lineclosed "+str(countlines)+" "+'.png')
            i.imgdialated=d
            countlines+=1 
    
    return linesegments
    #plt.plot(linehistogram)
    #plt.show()
    #io.imshow(binary)
    #imagefromarr=Image.fromarray(binary)
    #imagefromarr.save('binarized.png')        
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
def wordstochracters(lines):# this function takes array of lines and
# adds the following (for each line):
#    for each word:
#       array of char objects which contains :
# image of the character + starting column + end column 
        countlines=0
        countwords=0
        countchar=0
        #show_images([l.img])
        for l in linesegments: #loop on every line
            if(l.endrow-l.startrwo>=15):
                for w in l.words:  #loop on every word in the line
                    height=w.wordimg.shape[0]
                    width=w.wordimg.shape[1]
                    charhistogram=np.zeros(width) #vertical histogram for the word
                    countchar=0
                    for j in range(width):
                        for i in range (height):
                            if(w.wordimg[i][j]==0):
                                charhistogram[j]+=1
    
                    k=0
                    end=-1
                    w.chracters=[]#set the variable 3shan kant btdrb
                    print(charhistogram)
                    charhistogramthresh=round(np.average(charhistogram))
                    charhistogramthresh/=2
                    charhistogramthresh=round(charhistogramthresh)
                    while k in range(len(charhistogram)):##loop on the histogram
                        if(charhistogram[k]>=0): #k is the first column to have a black pixel,so we save it
                            print("1st k=",k)
                            for end in range(k,len(charhistogram)-1): #loop starts with k till the end
                                if((charhistogram[end]==0  ) and (charhistogram[end+1]==0  ) ): #if we found an empty area,the char is completed
                                    w.chracters.append(char(k,end))#create an object with the coordinates
                                    k=end
                                    print("last k=",k)
                                    break
                            if(end+1==len(charhistogram)-1):
                                w.chracters.append(char(k,end))#create an object with the coordinates
                                k=end
                                print("last k=",k)
                                break
                                
                        k+=1
                    for m in(w.chracters): #loop on these coordinates to cut the word into chars
                        #print(m)
                        #print(m.startcol,m.endcol)
                        if(m.endcol-m.startcol>=3):
                            x=w.wordimg[0:height,m.startcol:m.endcol] #chop! chop!
                            #imagefromarr=Image.fromarray(x)
                            #imagefromarr.save('line '+str(countlines)+"- word  "+str(countwords)+" char "+str(countchar)+'.png')#saving the image
                            #wordstest.append(binary_dilation(x))
                            #show_images([x])
                            height=x.shape[0]
                            width=x.shape[1]
                            
                            factorheight=int(128/height)
                            newwidth=int(width*factorheight)
                            if(newwidth%2 !=0):
                                newwidth+=1
                            resized=img_as_bool(resize(x, (128,newwidth ),anti_aliasing=True))
                            
                            window=np.ones((128,128)) 
                            window[:,(64-int(newwidth/2)):(64+int(newwidth/2))]=resized
                            #window=np.logical_and(window==1 , resized)
                            window=img_as_bool(window)
                            #resized=img_as_bool(resize(x, (128, 128),anti_aliasing=True))
                            #show_images([window])
                            #imagefromarr=Image.fromarray(window)
                            #imagefromarr.convert('P')
                            #imagefromarr.save('line '+str(countlines)+"- word  "+str(countwords)+" char resized "+str(countchar)+'.png')
                            m.img=window
                            countchar+=1
                    countwords+=1
                countlines+=1
                countwords=0                 