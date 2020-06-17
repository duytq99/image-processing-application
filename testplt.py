from matplotlib import pyplot as plt 
import numpy as np
import math
x = np.array(list(range(256)))
print(np.max(x))
c = (256 - 1)/(np.log(np.max(x)))
x = x.astype(np.float) 

#y = np.log(x+1) * c
y = (np.exp(x)**(1/c)) -1
y = y.astype(np.uint8) 
plt.plot(x,y)
plt.show()


# import cv2 
# import numpy as np 
# import matplotlib.pyplot as plt 
   
# # Read an image 
# image = cv2.imread('input/team.jpg',0) 
# image = image.astype(np.float)
   
# # Apply log transformation method 
# c = (256 - 1)/np.log(256) 
# log_image = c * np.log(image + 1)

# # Specify the data type so that 
# # float value will be converted to int 
# log_image = np.array(log_image, dtype = np.uint8) 

# exp_image = np.power(np.exp(image),(1/c)) -1
# #print(np.max(exp_image))
# exp_image = np.array(exp_image, dtype = np.uint8) 
# #print(np.max(exp_image))
# #print(exp_image)   
# # Display both images 
# cv2.imshow("log",log_image)
# cv2.imshow("exp",exp_image)
# cv2.waitKey(0)
