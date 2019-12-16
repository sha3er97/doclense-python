def avgFilter(img):
    padded_img = np.ones((img.shape[0]+2, img.shape[1]+2))
    padded_img[1:-1,1:-1] = img
    out_img = np.ones(img.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            out_img[i,j] = (padded_img[i,j]+padded_img[i,j+1]+padded_img[i,j+2] \
                            +padded_img[i+1,j]+padded_img[i+1,j+1]+padded_img[i+1,j+2] \
                            +padded_img[i+2,j+2]+padded_img[i+2,j+2]+padded_img[i+2,j+2]) / 9
    return out_img


def post_process(binarized):
    binarized = avgFilter(binarized)
    binarized = avgFilter(binarized)
    binarized = binarized>0.9
    binarized = 1-binarized
    binarized = binary_dilation(binarized)
    binarized = binary_erosion(binarized)
    binarized = binary_erosion(binarized)
    binarized = 1- binarized
    binarized = avgFilter(binarized)
    binarized = avgFilter(binarized)
    binarized = avgFilter(binarized)
    binarized = avgFilter(binarized)
    binarized = binarized>0.9
    return binarized

   