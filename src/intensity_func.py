import cv2
import numpy as np

def img_neg(img):
    img_negative = 255 - img
    return img_negative

def img_thres(img,threshold):
    img[img<threshold] = 0
    img[img>=threshold] =255
    return img

def img_log(image):
    image = image.astype(np.float)
    c = 255 / np.log(1 + 255)
    log_image = c * (np.log(image + 1)) 
    log_image = np.array(log_image, dtype = np.uint8) 
    
    return log_image

def img_invlog(image):
    image = image.astype(np.float)
    c = 255 / np.log(1 + 255) 
    
    exp_image = (np.exp(image)**(1/c)) -1
    exp_image = np.array(exp_image, dtype = np.uint8)
    
    return exp_image

def img_gamma_correction(img,c,gamma):
    r = img/255
    img_gamma = c * (r**gamma)
    img_gamma = np.array(img_gamma*255,dtype = np.uint8)
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
 
    eight_bit_img = (np.array([int(i[0]) for i in lst],dtype = np.uint8) * 128).reshape(img.shape[0],img.shape[1])
    seven_bit_img = (np.array([int(i[1]) for i in lst],dtype = np.uint8) * 64).reshape(img.shape[0],img.shape[1])
    six_bit_img = (np.array([int(i[2]) for i in lst],dtype = np.uint8) * 32).reshape(img.shape[0],img.shape[1])
    five_bit_img = (np.array([int(i[3]) for i in lst],dtype = np.uint8) * 16).reshape(img.shape[0],img.shape[1])
    four_bit_img = (np.array([int(i[4]) for i in lst],dtype = np.uint8) * 8).reshape(img.shape[0],img.shape[1])
    three_bit_img = (np.array([int(i[5]) for i in lst],dtype = np.uint8) * 4).reshape(img.shape[0],img.shape[1])
    two_bit_img = (np.array([int(i[6]) for i in lst],dtype = np.uint8) * 2).reshape(img.shape[0],img.shape[1])
    one_bit_img = (np.array([int(i[7]) for i in lst],dtype = np.uint8) * 1).reshape(img.shape[0],img.shape[1])
 
    finalr = cv2.hconcat([eight_bit_img,seven_bit_img,six_bit_img,five_bit_img])
    finalv =cv2.hconcat([four_bit_img,three_bit_img,two_bit_img,one_bit_img])
 
    final = cv2.vconcat([finalr,finalv])
    return final



def arguments_parser():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', default='data/Lenna.png', required=False, help='Path to image')
    parser.add_argument('-f', '--function', choices=['negative', 'threshold', 'log', 'invlog', 'gamma', 'linear', 'bitplane'], required=True, help='Chosse transformation function')
    parser.add_argument('-thr', '--threshold', default=127, required=False, help='Threshold value')
    parser.add_argument('-g', '--gamma', default=0.5, required=False, help='Gamma correction coefficient')
    parser.add_argument('-s', '--save', action='store_true', help='Save output image')
    return parser.parse_args()

def main():
    args = arguments_parser()
    img = cv2.imread(args.path,1)

    if args.function == 'negative':
        output = img_neg(img)
    elif args.function == 'threshold':
        output = img_thres(img, args.threshold)
    elif args.function =='log':
        output = img_log(img)
    elif args.function == 'invlog':
        output = img_invlog(img)
    elif args.function == 'gamma':
        output = img_gamma_correction(img, 1, args.gamma)
    elif args.function == 'linear':
        output = img_linear(img, r1=5, s1=10, r2=100, s2=200)
    elif args.function == 'bitplane':
        output = img_bit_trans(img)
    else:
        raise NotImplementedError

    if args.save:
        cv2.imwrite('output/intensity_demo.png', output)

    cv2.imshow("img",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

