import random
import struct

import cv2
import numpy as np
import colorsys

import time

SAMPLE_LEN = 1024
MAX_PIXEL_DELTA = np.sqrt(3) * 256
prev_frame = None
CURRENT_SCALE = "major"
BASE_SOUND = 44


def octave(x):
    return BASE_SOUND + (x % 4) * 12


scales = {
    "minor": [0, 2, 3, 5, 7, 8, 11, 12],
    "major": [0, 2, 4, 5, 7, 9, 11, 12],
    "gypsy": [0, 1, 4, 5, 7, 8, 11, 12],
    "phrygian": [0, 1, 4, 5, 7, 8, 10, 12]
}


def scale_in_octave(x):
    return np.array(scales[CURRENT_SCALE]) + x


rhythms = [
    [1, 0.5, 0.5, 1, 0.25, 0.25, 0.5],
    [0.5, 0.5, 1, 0.5, 0.5, 0.5, 0.5],
    [0.5, 0.25, 0.25, 1, 0.5, 0.5, 1],
    [0.25, 0.25, 0.25, 0.5, 0.25, 0.5, 1, 0.5, 0.5]
]


def get_sound(x):
    # assuming x in range(256)
    y = 64 * x // 256
    return octave(y // 8)


def fake_auralize(video_data):
    noise = np.zeros(SAMPLE_LEN)

    for i in range(0, SAMPLE_LEN):
        value = random.randint(-32767, 32767)
        packed_value = struct.pack('h', value)
        noise[i] = packed_value

    return noise


def frobenius(a, b):
    max = MAX_PIXEL_DELTA * a.shape[0] * a.shape[1]
    d1 = np.asarray((a[..., 0] - b[..., 0]) ** 2, dtype=np.float64)
    d2 = np.asarray((a[..., 1] - b[..., 1]) ** 2, dtype=np.float64)
    d3 = np.asarray((a[..., 2] - b[..., 2]) ** 2, dtype=np.float64)
    return np.sum(np.sqrt((d1 + d2 + d3))) / max


def gram(x):
    return frobenius(np.transpose(x, (1, 0, 2)), x)


def pixel_val(pixel, range):
    return int(range * np.sqrt(pixel[0] ** 2 + pixel[1] ** 2 + pixel[2] ** 2) / MAX_PIXEL_DELTA)


def auralize(video_data, prev_frame):
    if prev_frame is None:
        prev_frame = np.zeros(video_data.shape)
    n, m, _ = video_data.shape
    hsv = cv2.cvtColor(video_data, cv2.COLOR_BGR2HSV)
    hue_vals, hue_counts = np.unique(hsv[..., 0], return_counts=True)
    dom = hue_vals[np.argmax(hue_counts)]
    dominant = int(len(rhythms) * dom / 129)
    #     hue_vals = np.unique(hsv[..., 0])
    color_count = len(hue_vals)
    sat = np.mean(hsv[..., 1])

    saturation = 47 + int(80 * sat / 256)
    diff = int(frobenius(video_data, prev_frame) * 100)
    # print(diff)
    # volume = 30 + int(diff * 97)
    volume = saturation
    s = get_sound(color_count)
    r = random.Random()
    rh = diff % len(rhythms)
    return [(scale_in_octave(s), random.randint(0, 7), volume, rhythms[rh][i]) for i in range(len(rhythms[rh]))]
