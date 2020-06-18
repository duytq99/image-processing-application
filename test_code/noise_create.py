import cv2
import numpy as np
from skimage.util import random_noise
 
# Load the image
img = cv2.imread("input/Lenna.png")
 
# Add salt-and-pepper noise to the image.
noise_img = random_noise(img, mode='s&p',amount=0.3)
 
# The above function returns a floating-point image
# on the range [0, 1], thus we changed it to 'uint8'
# and from [0,255]
noise_img = np.array(255*noise_img, dtype = 'uint8')
 
# Display the noise image
cv2.imshow('noise',noise_img)
cv2.imwrite("s&p_noise_lenna.png",noise_img)
cv2.waitKey(0)

# Generate Gaussian noise
gauss_noise_img = random_noise(img, mode='gaussian',mean=0,var=0.01)
gauss_noise_img = np.array(255*gauss_noise_img, dtype = 'uint8')
cv2.imwrite("gaussian_noise_lenna.png",gauss_noise_img)
# Display the image
cv2.imshow('a',gauss_noise_img)
cv2.waitKey(0)