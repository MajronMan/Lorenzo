import random
import struct
from collections import OrderedDict

import cv2
import numpy as np
import colorsys
import filters

import time

SAMPLE_LEN = 1024
MAX_PIXEL_DELTA = np.sqrt(3) * 256
prev_frame = None
CURRENT_SCALE = "phrygian"
BASE_SOUND = 44


def octave(x):
    return BASE_SOUND + (x % 4) * 12


scales = {
    "minor": [0, 2, 3, 5, 7, 8, 11, 12],
    "major": [0, 2, 4, 5, 7, 9, 11, 12],
    "gypsy": [0, 1, 4, 5, 7, 8, 11, 12],
    "phrygian": [0, 1, 4, 5, 7, 8, 10, 12]
}


def get_scale_octaves():
    scale = scales[CURRENT_SCALE]
    return np.ndarray.flatten(
        np.array(
            [BASE_SOUND + np.array(scale) + i * 12 for i in range(5)]
        )
    )

def scale_in_octave(x):
    y = 64 * x // 256
    o = octave(y // 8)
    scale = np.array(scales[CURRENT_SCALE])
    return np.ndarray.flatten(np.array([scale + o - 12, scale, scale + o + 12]))


rhythms = [
    [1],
    [0.5, 0.5],
    [0.5, 0.25, 0.25],
    # [0.25, 0.5, 0.25],
    # [0.25, 0.25, 0.5],
    [0.25, 0.25, 0.25, 0.25],

]


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

class Auralizer:
    prev_base = None

    def __init__(self):
        self.scale = get_scale_octaves()
        self.prev_base_ind = None
        minimum = self.scale[0]
        maximum = self.scale[-1]
        self.prob = lambda x: x / (minimum - maximum) - maximum / (minimum - maximum)

    def get_next_base(self, cumulative):
        if self.prev_base_ind is None:
            self.prev_base_ind = 8

        r = random_with_distribution(cumulative)
        last_pitch = self.scale[self.prev_base_ind]
        move_right = self.prob(last_pitch)
        r = (r if random.random() < move_right else -r)
        new_base_ind = bounded_add(self.prev_base_ind, r, 0, len(self.scale)-1)
        new_base = self.scale[new_base_ind]

        self.prev_base_ind = new_base_ind
        return (new_base_ind, new_base)

    def build_chord(self, cumulative):
        new_base_ind, new_base = self.get_next_base(cumulative)
        pitches = [new_base]
        for i in range(1, 4):
            if random.random() < (0.2) ** i:
                pitches.append(self.scale[bounded_add(new_base_ind, 2 * i, 0, len(self.scale)-1)])
        return pitches


auralizer = Auralizer()

def auralize(video_data, prev_frame):
    if prev_frame is None:
        prev_frame = np.zeros(video_data.shape)
    n, m, _ = video_data.shape
    hsv = cv2.cvtColor(video_data, cv2.COLOR_BGR2HSV)
    hue_vals, hue_counts = np.unique(hsv[..., 0], return_counts=True)

    probs, cumulative = six_colour_distribution(video_data)
    up = -1 if random.random() > 0.5 else 1
    step = random_with_distribution(cumulative)

    dom = hue_vals[np.argmax(hue_counts)]
    dominant = min(int(8 * dom / 129), 8)
    #     hue_vals = np.unique(hsv[..., 0])
    color_count = len(hue_vals)
    sat = np.mean(hsv[..., 1])

    saturation = 47 + int(80 * sat / 256)
    diff = int(frobenius(video_data, prev_frame) * 100)
    # print(diff)
    # volume = 30 + int(diff * 97)
    volume = saturation
    rh = diff % len(rhythms)
    return [(auralizer.build_chord(cumulative), volume, rhythms[rh][i]) for i in range(len(rhythms[rh]))]
