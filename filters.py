import numpy as np
import cv2


def six_colours(frame):
    kernel = np.ones((5, 5), np.float32) / 25
    dst = cv2.filter2D(frame, -1, kernel)

    ret, thresh = cv2.threshold(dst, 127, 255, cv2.THRESH_BINARY)

    kernel1 = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel1)


def blur(frame):
    kernel = np.ones((5, 5)) / 25
    return cv2.filter2D(frame, -1, kernel)


motionFilter = None


def registerMotionFilter(filter):
    global motionFilter
    motionFilter = filter


def boundingBoxes(frame):
    return motionFilter.filter(frame)

filters = {
    "NONE": lambda x: x,
    "SIX_COLOURS": six_colours,
    "BLUR": blur
}
