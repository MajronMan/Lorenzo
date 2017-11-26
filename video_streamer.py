import cv2
import time
import numpy as np
import filters

capture = cv2.VideoCapture(0)



def read_stream():
    frame = capture.read()[1]
    return filters.filters[CURRENT_FILTER](frame)


def read_period(period, fps):
    t0 = time.time()
    frames = fps * period
    res = np.zeros(frames)
    i = 0
    while time.time() - t0 < period:
        res[i] = read_stream()
        i += 1

    return res


def quit_video():
    capture.release()
    cv2.destroyAllWindows()
