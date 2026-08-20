import cv2
import numpy as np


def detect_green_laser(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_green = np.array([40, 80, 150])
    upper_green = np.array([90, 255, 255])

    mask = cv2.inRange(
        hsv,
        lower_green,
        upper_green
    )

    mask = cv2.GaussianBlur(
        mask,
        (3, 3),
        0
    )

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        return None, mask

    largest_contour = max(
        contours,
        key=cv2.contourArea
    )

    area = cv2.contourArea(
        largest_contour
    )

    if area <= 2:
        return None, mask

    moments = cv2.moments(
        largest_contour
    )

    if moments["m00"] == 0:
        return None, mask

    x = int(
        moments["m10"] / moments["m00"]
    )

    y = int(
        moments["m01"] / moments["m00"]
    )

    return (x, y), mask