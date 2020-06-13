import cv2
import numpy as np

def img_neg(img):
    img_negative = 255 - img
    return img_negative

def img_thres(img,threshold):
    img[img<threshold] = 0
    img[img>=threshold] =255
    return img

def img_log(img,c):
    img_logarithmic = c * np.log(1 + img /255)
    return img_logarithmic

def img_gamma_correction(img,c,gamma):
    r = img/255
    img_gamma = c * (r**gamma)
    return img_gamma

def pix_linear(img,r1,s1,r2,s2):
    if (0 <= img and img <= r1): 
        return (s1 / r1)*img 
    elif (r1 < img and img <= r2): 
        return ((s2 - s1)/(r2 - r1)) * (img - r1) + s1 
    else: 
        return ((255 - s2)/(255 - r2)) * (img - r2) + s2

def img_linear(img,r1,s1,r2,s2):
    pixelVal_vec = np.vectorize(pix_linear) 
  
    # Apply contrast stretching. 
    contrast_stretched = pixelVal_vec(img, r1, s1, r2, s2) 
    return contrast_stretched
    
def img_bit_trans(img):
    lst = []
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
         lst.append(np.binary_repr(img[i][j] ,width=8)) # width = no. of bits
 
# We have a list of strings where each string represents binary pixel value. To extract bit planes we need to iterate over the strings and store the characters corresponding to bit planes into lists.
# Multiply with 2^(n-1) and reshape to reconstruct the bit image.
    eight_bit_img = (np.array([int(i[0]) for i in lst],dtype = np.uint8) * 128).reshape(img.shape[0],img.shape[1])
    seven_bit_img = (np.array([int(i[1]) for i in lst],dtype = np.uint8) * 64).reshape(img.shape[0],img.shape[1])
    six_bit_img = (np.array([int(i[2]) for i in lst],dtype = np.uint8) * 32).reshape(img.shape[0],img.shape[1])
    five_bit_img = (np.array([int(i[3]) for i in lst],dtype = np.uint8) * 16).reshape(img.shape[0],img.shape[1])
    four_bit_img = (np.array([int(i[4]) for i in lst],dtype = np.uint8) * 8).reshape(img.shape[0],img.shape[1])
    three_bit_img = (np.array([int(i[5]) for i in lst],dtype = np.uint8) * 4).reshape(img.shape[0],img.shape[1])
    two_bit_img = (np.array([int(i[6]) for i in lst],dtype = np.uint8) * 2).reshape(img.shape[0],img.shape[1])
    one_bit_img = (np.array([int(i[7]) for i in lst],dtype = np.uint8) * 1).reshape(img.shape[0],img.shape[1])
 
#Concatenate these images for ease of display using cv2.hconcat()
    finalr = cv2.hconcat([eight_bit_img,seven_bit_img,six_bit_img,five_bit_img])
    finalv =cv2.hconcat([four_bit_img,three_bit_img,two_bit_img,one_bit_img])
 
# Vertically concatenate
    final = cv2.vconcat([finalr,finalv])
    return final


# if 1:
    
#     import matplotlib.pyplot as plt
    
#     path = '/home/quangduy/BTL_XLA/input/Lenna.png'
#     img = cv2.imread(path,0)
#     # img_negative = img_neg(img)
#     # img_threshold = img_thres(img,threshold=120)
#     img_logarithmic = img_log(img,c=1)
#     print(img_logarithmic)
#     # img_gamma = img_gamma_correction(img,1,0.2)
#     # img_linear_trans = img_linear(img, r1=50, s1=0, r2=100, s2=255)
#     # img_bit = img_bit_trans(img)
#     cv2.imshow("Image Processing",img_logarithmic)

#     cv2.waitKey(0)
