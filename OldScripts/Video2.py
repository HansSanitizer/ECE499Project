import cv2,platform
import numpy as np

def larger(x):
    gray = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)
    image = cv2.Canny(gray,35,200)
    (_,cnts,_) = cv2.findContours(image.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    c = max(cnts, key=cv2.contourArea)
    return cv2.minAreaRect(c)

capture = cv2.VideoCapture(0)

if capture.isOpened():
    while(True):
        retval, im = capture.read()
        y = larger(im)
        box = np.int0(cv2.boxPoints(y))
        cv2.drawContours(im,[box],-1,(0,255,0),2)
        cv2.imshow("Image",im)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            capture.release()
            break

else:
    print ("No camera detected.")


cv2.destroyAllWindows()