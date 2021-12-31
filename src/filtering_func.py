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
    result = cv2.filter2D(img, -1, kernel)      
    return result

def gaussian_filter(img,size,sigma):
    result = cv2.GaussianBlur(img,(size,size),0)
    return result

def median_filter(img,size):
    denoise_img = cv2.medianBlur(img,size)
    return denoise_img

def laplacian_filter(img,size):
    result = cv2.Laplacian(img,cv2.CV_8U, None, size)
    return result

def gab_filter(img,size,lamda=10,theta=1,phi=0,sigma=5,gamma=1):
    kernel = cv2.getGaborKernel((size,size), sigma, theta, lamda, gamma, phi, cv2.CV_32F)
    kernel /= math.sqrt((kernel * kernel).sum())
    filtered = cv2.filter2D(img, -1, kernel)
    return filtered

def sob_filter(img,ksize):
    ddepth = cv2.CV_16S 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grad_x = cv2.Sobel(gray, ddepth, 1, 0, ksize, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
    grad_y = cv2.Sobel(gray, ddepth, 0, 1, ksize, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    return grad

def pre_filter(img):
    kernelx = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
    kernely = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
    img_prewittx = cv2.filter2D(img, -1, kernelx)
    img_prewitty = cv2.filter2D(img, -1, kernely)
    result = img_prewittx + img_prewitty
    return result


def arguments_parser():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', default='data/Lenna.png', required=False, help='Path to image')
    parser.add_argument('-f', '--function', choices=['average', 'w_average', 'gaussian', 'median', 'laplacian', 'gabor', 'sobel', 'prewitt'], required=True, help='Chosse filter function')
    parser.add_argument('-ks', '--kernel_size', default=3, required=False, help='Kernel size')
    parser.add_argument('-w', '--weight', default=2, required=False, help='Weight of weighted avg filter')
    parser.add_argument('-sig', '--sigma', default=1, required=False, help='Sigma of Gaussian filter')
    parser.add_argument('-l', '--ld', default=10, required=False, help='Lambda of Gabor filter')
    parser.add_argument('-t', '--theta', default=1, required=False, help='Theta of Gabor filter')
    parser.add_argument('-ph', '--phi', default=0, required=False, help='Phi of Gabor filter')
    parser.add_argument('-g', '--gamma', default=1, required=False, help='Gamma of Gabor filter')
    parser.add_argument('-s', '--save', action='store_true', help='Save output image')
    return parser.parse_args()


def main():
    args = arguments_parser()
    img = cv2.imread(args.path,1)
    if args.function == 'average':
        output = avg_filter(img, args.kernel_size)
    elif args.function == 'w_average':
        output = weighted_avg_filter(img, args.weight)
    elif args.function =='gaussian':
        output = gaussian_filter(img, args.kernel_size, args.sigma)
    elif args.function == 'median':
        output = median_filter(img, args.kernel_size)
    elif args.function == 'laplacian':
        output = laplacian_filter(img, args.kernel_size)
    elif args.function == 'gabor':
        output = gab_filter(img, args.kernel_size, args.ld, args.theta, args.phi, int(args.sigma), args.gamma)
    elif args.function == 'sobel':
        output = sob_filter(img, args.kernel_size)
    elif args.function == 'prewitt':
        output = pre_filter(img)
    else:
        raise NotImplementedError

    if args.save:
        cv2.imwrite('output/filtering_demo.png', output)

    cv2.imshow("img",output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
