import cv2
import time

capture = cv2.VideoCapture(0)
def read_stream():
    return capture.read()[1]

def read_period(period):
    t0 = time.time()
    res = []
    while time.time() - t0 < period:
        res.append(read_stream())
    return res

def quit_video():
    capture.release()
    cv2.destroyAllWindows()
