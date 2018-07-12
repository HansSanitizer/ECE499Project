from matplotlib import pyplot as plt
import cv2 as cv
print(cv.__version__)
import numpy as np
import time

runs = range(0,10)

for run in runs:

    print("Beginning run " + str(run))
    start_time = time.time()

    bw = cv.imread('tbcfc2.jpg', cv.IMREAD_GRAYSCALE)
    #plt.imshow(bw, cmap='gray'), plt.show()

    # IF THIS NEXT LINE CAUSES TROUBLE, JUST REMOVE IT, IT IS SUPPOSED TO SPEED THINGS UP USING OPENCL
    # REFLINK: https://www.learnopencv.com/opencv-transparent-api/
    bwUmat = cv.UMat(bw)
    height, width = bw.shape
    #print("The original image height is ", height)
    #print("The original image width is ", width)
    black = np.zeros(bw.shape, np.uint8)
    retval, dst = cv.threshold(bw, 45, 255, cv.THRESH_BINARY)
    # plt.imshow(dst), plt.show()

    centerSmall = (7330, 5832)
    #centerSmall = (8765, 6782)
    radiusSmall = 2100

    #print("Record Center(x, y) is: ", centerSmall)
    black2 = np.zeros(bw.shape, np.uint8)
    circOut = cv.circle(black2, centerSmall, (radiusSmall + 1100), (255, 255, 255), -1)
    circIn = cv.circle(black2, centerSmall, (radiusSmall + 1000), (0, 0, 0), -1)
    fin = cv.bitwise_and(bw, black2)
    # plt.imshow(fin), plt.show()

    # Apply Threshold and detect contours
    thresh_adapt = cv.adaptiveThreshold(fin, 80, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 57, 0)
    # plt.imshow(thresh_adapt), plt.show()

    thresh_adapt_copy = thresh_adapt
    element = cv.getStructuringElement(cv.MORPH_CROSS,(3,3))
    done = False
    size = np.size(bw)
    skel = np.zeros(bw.shape,np.uint8)
    while not done:
        eroded = cv.erode(thresh_adapt_copy,element)
        temp = cv.dilate(eroded,element)
        temp = cv.subtract(thresh_adapt_copy,temp)
        skel = cv.bitwise_or(skel,temp)
        thresh_adapt_copy = eroded.copy()

        zeros = size - cv.countNonZero(thresh_adapt_copy)
        if zeros==size:
            done = True

    # plt.imshow(skel), plt.show()
    # Need to convert skel to xy locations, rather than rows and columns of intensity values,
    # where rows and column index's are positions
    indices = np.where(skel > [0])

    rhos = []
    x = indices[1][0] - centerSmall[0]
    y = indices[0][0] + centerSmall[1]      # fix?
    contoursXY = np.array([x, y])
    rho = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    if theta < 0:
        theta = theta + 2*np.pi
    #print(len(indices[:]))
    contoursThetaRho = np.array([theta, rho])
    #print("Printing Theta Rho:")
    #print(contoursThetaRho)
    for i in range(1, len(indices[0])):
        x = indices[1][i] - centerSmall[0]
        y = centerSmall[1] - indices[0][i]
        rho = np.sqrt(x**2 + y**2)
        rhos.append(rho)
        theta = (np.arctan2(y, x))
        if theta < 0:
            theta = theta + 2*np.pi
        b = np.array([theta, rho])
        # keep adding new rows
        contoursThetaRho = np.column_stack((contoursThetaRho.T, b)).T
        b = np.array([x, y])
        contoursXY = np.column_stack((contoursXY.T, b)).T
    # sort our theta data, don't ask me to explain what this is doing
    # does it actually need to be sorted? The graph will still draw regardless.
    #print("sorting")
    contoursThetaRhoSorted = np.lexsort((contoursThetaRho[:, 1], contoursThetaRho[:, 0]))
    contoursThetaRhoSorted = contoursThetaRho[contoursThetaRhoSorted]
    #print(contoursThetaRho)
    #plt.figure()
    #plt.hist(rhos, bins='fd'), plt.show()
    #plt.figure()
    #plt.scatter([contoursThetaRho[:,0]], [contoursThetaRho[:,1]], s=0.2), plt.show()
    end_time = time.time()
    elapsed_time = end_time-start_time
    print("Run " + str(run) + " elapsed time was: " + str(elapsed_time) + "\n")
