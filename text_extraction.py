def backgroundElimination(img):
    imgCopy = np.copy(img)
    blockSize = 50
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