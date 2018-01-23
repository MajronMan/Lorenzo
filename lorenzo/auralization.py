import random
import struct

import cv2
import numpy as np

from lorenzo import filters

# SAMPLE_LEN = 1024
# MAX_PIXEL_DELTA = np.sqrt(3) * 100
prev_frame = None

scales = {
    "minor": [0, 2, 3, 5, 7, 8, 11, 12],
    "major": [0, 2, 4, 5, 7, 9, 11, 12],
    "gypsy": [0, 1, 4, 5, 7, 8, 11, 12],
    "phrygian": [0, 1, 4, 5, 7, 8, 10, 12],
    "japanese": [0, 2, 3, 7, 8, 12, 14, 15]
}


def octave(x, base_sound):
    return base_sound + (x % 4) * 12


def get_scale_octaves(current_scale, base_sound):
    scale = scales[current_scale]
    return np.ndarray.flatten(
        np.array(
            [base_sound + np.array(scale) + i * 12 for i in range(5)]
        )
    )


def scale_in_octave(x, current_scale, base_sound):
    y = 64 * x // 256
    o = octave(y // 8, base_sound)
    scale = np.array(scales[current_scale])
    return np.ndarray.flatten(np.array([scale + o - 12, scale, scale + o + 12]))


# def frobenius(a, b):
#     max = MAX_PIXEL_DELTA * a.shape[0] * a.shape[1]
#     d1 = np.asarray((a[..., 0] - b[..., 0]) ** 2, dtype=np.float64)
#     d2 = np.asarray((a[..., 1] - b[..., 1]) ** 2, dtype=np.float64)
#     d3 = np.asarray((a[..., 2] - b[..., 2]) ** 2, dtype=np.float64)
#     return np.sum(np.sqrt((d1 + d2 + d3))) / max


def six_colour_distribution(video_data):
    six_hues = filters.six_colours(video_data)
    six_hsv = cv2.cvtColor(six_hues, cv2.COLOR_BGR2HSV)
    six_vals, six_counts = np.unique(six_hsv[..., 0], return_counts=True)
    d = dict(zip(six_vals, six_counts))
    o = sorted(d.items(), key=lambda x: x[0])
    pixels_count = video_data.shape[0] * video_data.shape[1]
    probs = []
    cumulative = [0]
    total = pixels_count - o.pop(0)[1]
    for (val, count) in o:
        probs.append(count / total)
        cumulative.insert(0, count / total + cumulative[0])
    return (probs, cumulative)


def random_with_distribution(cumulative):
    r = random.random()
    for i in range(len(cumulative) - 1):
        if r > cumulative[i + 1]:
            return i
    return len(cumulative)


def bounded_add(base, additive, minimum, maximum):
    r = base + additive
    m1 = minimum - r
    m2 = r - maximum
    if m1 > 0:
        r += 2 * m1
    elif m2 > 0:
        r -= 2 * m2
    return r


def get_bounding_boxes(frame):
    processed, boxes = filters.boundingBoxes(frame)
    # boxes = sorted(boxes, key=lambda b: -b.area())[:5]
    boxes = np.array(boxes)
    maximum = filters.motionFilter.full_frame_area
    return len(boxes), np.sum((box.area() for box in boxes)) / maximum
