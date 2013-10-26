import numpy as np
import cv2
import freenect

cv2.namedWindow("Tresh")
cv2.moveWindow("Tresh", 800, 30)
cv2.namedWindow("Image")

ref = freenect.sync_get_video()[0]
ref = cv2.cvtColor(ref, cv2.cv.CV_BGR2GRAY)

key = ''
while True:
    key = cv2.waitKey(1)

    if key == ord('q'):
        break
    
    image = np.zeros((480,640))
    
    orig = freenect.sync_get_video()[0]
    image = cv2.cvtColor(orig, cv2.cv.CV_BGR2GRAY)

    diff = image - ref
    image[diff > 50] = 0
    
    cv2.imshow("Tresh", diff)
    cv2.imshow("Image", image)
