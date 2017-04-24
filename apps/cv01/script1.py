import cv2

img = cv2.imread("galaxy.jpg", 0)

cv2.imshow("Galaxy.jpg", img)
cv2.waitKey(2000)
cv2.destroyAllWindows()