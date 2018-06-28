""" Center Location:

    These functions are for locating the center of a record.
    The order of the functions in this file is the order of
    expected use.
"""
import cv2 as cv
import numpy as np
import BasicGeometry as bg


def enhance_edges(image, filter_window_size=5, filter_colour_smear=175, filter_range_smear=175):

    bilateral_filtered_image = cv.bilateralFilter(image, filter_window_size, filter_colour_smear, filter_range_smear)

    return bilateral_filtered_image


def detect_edges(image, edge_thresh_min=10, edge_thresh_max=50):

    edges = cv.Canny(image, edge_thresh_min, edge_thresh_max)

    return edges


def find_contours(image):

    _, contours, _ = cv.findContours(image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    return contours


def find_circle_candidates(contours, min_area=270, max_area=700):

    contours_circle_candidates = list()

    for contour in contours:
        approx = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)
        area = cv.contourArea(contour)
        if (len(approx) > 8) & (area > min_area) & (area < max_area):
            contours_circle_candidates.append(contour)

    return contours_circle_candidates


def enclose_candidates(contours_circle_candidates):

    circles = list()

    for contour in contours_circle_candidates:
        (x, y), rho = cv.minEnclosingCircle(contour)
        circles.append(bg.Circle((int(x), int(y)), rho))

    return circles


def find_best_circle(circles, best_dif=1, expected_area=176460, area_tolerance=0.05):

    best_circle = bg.Circle()

    for circle in circles:
        dif = np.abs(expected_area - circle.area) / expected_area
        if (dif < area_tolerance) & (dif < best_dif):
            best_circle = circle
            best_dif = dif

    return best_circle
