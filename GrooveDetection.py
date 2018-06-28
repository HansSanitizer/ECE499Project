""" Groove Detection:

    These functions are for detecting grooves on a record.
    The order of the functions in this file is the order of
    expected use.
"""
import cv2 as cv
import numpy as np


def load_grey_scale(path):

    bw = cv.imread(path, cv.IMREAD_GRAYSCALE)

    return bw


def slice_image(image, center, inner_radius, outer_slice_radius, inner_slice_radius):

    black2 = np.zeros(image.shape, np.uint8)
    cv.circle(black2, center, (inner_radius + outer_slice_radius), (255, 255, 255), -1)
    cv.circle(black2, center, (inner_radius + inner_slice_radius), (0, 0, 0), -1)
    return cv.bitwise_and(image, black2)


def apply_threshold(image):

    image_threshold = cv.adaptiveThreshold(image, 80, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 57, 0)

    return image_threshold


def image_to_skeleton(image):

    element = cv.getStructuringElement(cv.MORPH_CROSS, (3, 3))
    done = False
    size = np.size(image)
    skeleton = np.zeros(image.shape, np.uint8)

    while not done:
        eroded = cv.erode(thresh_adapt_copy, element)
        temp = cv.dilate(eroded, element)
        temp = cv.subtract(thresh_adapt_copy, temp)
        skeleton = cv.bitwise_or(skeleton, temp)
        thresh_adapt_copy = eroded.copy()

        zeros = size - cv.countNonZero(thresh_adapt_copy)
        if zeros == size:
            done = True

    indices = np.were(skeleton > [0])
    return indices


def skeleton_to_points(indices, center):

    x = indices[1][0] - center[0]
    y = center[1] - indices[0][0]
    contours_points = np.array([x, y])
    rho = np.sqrt(x ** 2 + y ** 2)
    theta = np.arctan2(y, x)

    if theta < 0:
        theta = theta + 2 * np.pi
    print(len(indices[:]))
    contours_theta_rho = np.array([theta, rho])

    for i in range(1, len(indices[0])):
        x = indices[1][i] - center[0]
        y = center[1] - indices[0][0]
        rho = np.sqrt(x ** 2 + y ** 2)
        theta = (np.arctan2(y, x))
        if theta < 0:
            theta = theta + 2 * np.pi
        b = np.array([theta, rho])
        contours_theta_rho = np.column_stack((contours_theta_rho.T, b)).T
        b = np.array([x, y])
        contours_points = np.column_stack((contours_points.T, b)).T

    contours_theta_rho_sorted = np.lexsort((contours_theta_rho[:, 1], contours_theta_rho[:, 0]))
    contours_theta_rho_sorted = contours_theta_rho[contours_theta_rho_sorted]
    return contours_theta_rho_sorted
