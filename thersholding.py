def optimalThersholding(img):     
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

def global_thersholding(img):

    return int (0.4*255) #global thershold

#######################################################################################################

def choose_thersholding_type(img,mode=1):
    if(mode == 1):
        return optimalThersholding(img)
    elif(mode == 2):
        return threshold_otsu(img)
    else
        return global_thersholding(img)

#########################################################################################################