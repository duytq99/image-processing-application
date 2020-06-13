import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

def avg_filter(img,size):
    kernel = np.ones((size,size),np.float32)
    kernel = kernel / (size**2)
    img_avg = cv2.filter2D(img,-1,kernel)
    return img_avg

def weighted_avg_filter(img,b):
    kernel = np.array([[1,b,1],[b,b*b,b],[1,b,1]],dtype= float) 
    kernel /=  (b+2)*(b+2)
    print(kernel)
    result = cv2.filter2D(img, -1, kernel)      
    #box_filter_img = cv2.blur(scr,(size,size))
    return result

def gaussian_filter(img,size,sigma):
    k = size // 2
    x, y = np.mgrid[-k:k+1, -k:k+1]
    normal = 1 / (2.0 * np.pi * sigma**2)
    kernel =  np.exp(-((x**2 + y**2) / (2.0*sigma**2))) * normal
    print(kernel)
    result = cv2.filter2D(img,-1,kernel)
    # result = cv2.GaussianBlur(img,(size,size),0)
    return result

def median_filter(img,size):
    denoise_img = cv2.medianBlur(img,size)
    return denoise_img

def laplacian_filter(img,size):
    result = cv2.Laplacian(img,cv2.CV_8U, None, size)
    return result

def gab_filter(img,size=(15,15),lamda=10,theta=1,phi=0,sigma=5,gamma=1):
    kernel = cv2.getGaborKernel((size, size), sigma, theta, lamda, gamma, phi, cv2.CV_32F)
    kernel /= math.sqrt((kernel * kernel).sum())
    filtered = cv2.filter2D(img, -1, kernel)
    return filtered

def sob_filter(img,ksize):
    ddepth = cv2.CV_16S 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grad_x = cv2.Sobel(gray, ddepth, 1, 0, ksize, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
    # Gradient-Y
    # grad_y = cv.Scharr(gray,ddepth,0,1)
    grad_y = cv2.Sobel(gray, ddepth, 0, 1, ksize, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    print(ksize)
    return grad

def pre_filter(img):
    kernelx = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
    kernely = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
    img_prewittx = cv2.filter2D(img, -1, kernelx)
    img_prewitty = cv2.filter2D(img, -1, kernely)
    result = img_prewittx + img_prewitty
    return result

if __name__ == "__main__":
    image_path = ""
    img = cv2.imread(image_path,1)

    #img = avg_filter(img,size=15)
    #img = weighted_avg_filter(img,b=2)
    #img = gaussian_filter(img,5,1)
    #img = median_filter(img,5)
    #img = laplacian_filter(img,size=3)
    #img = np.uint8(gab_filter(img))
    #img = sob_filter(img,3)
    #img = pre_filter(img)

    cv2.imshow("img",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    





