import cv2 as cv
import time

im = cv.imread('tbcfc2.jpg')
imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)

for i in range(0, 10):

    start_time = time.time()
    ret, thresh = cv.threshold(imgray, 180, 255, 0)
    end_time = time.time()
    basic_time = end_time-start_time
    print(end_time-start_time)
    start_time = time.time()
    cv.adaptiveThreshold(imgray, 80, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 57, 0)
    end_time = time.time()
    adaptive_time = end_time-start_time
    print(adaptive_time)
    slow_down = adaptive_time-basic_time
    print(slow_down)
    print("\n")

