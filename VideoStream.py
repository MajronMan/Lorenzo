import time

import numpy as np


class VideoStream:
    def __init__(self, video_capture):
        self.video_capture = video_capture

    def read_frame(self):
        return self.video_capture.read()[1]

    def read_period(self, period, fps):
        frames = int(fps * period)

        period_start = time.time()

        first_frame = self.read_frame()
        res = np.ndarray((frames, *first_frame.shape))
        res[0] = first_frame

        i = 1
        while time.time() - period_start < period:
            res[i] = self.read_frame()
            i += 1

        return res

    def close(self):
        return self.video_capture.release()
