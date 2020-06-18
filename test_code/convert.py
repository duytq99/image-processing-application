import cv2

img = cv2.imread("input/team.jpeg",1)
cv2.imwrite("team.png",img)