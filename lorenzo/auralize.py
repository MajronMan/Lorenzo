import random

import cv2
import numpy as np

from lorenzo.Auralizer import Auralizer
from lorenzo.auralization import six_colour_distribution, random_with_distribution, get_bounding_boxes

prev_vol = [47]

rhythms = [
    [1],
    [0.5, 0.5],
    [0.5, 0.25, 0.25],
    # [0.25, 0.5, 0.25],
    # [0.25, 0.25, 0.5],
    [0.25, 0.25, 0.25, 0.25],
    # [0.125, 0.25, 0.25, 0.25, 0.125]
]


def auralize(video_data, prev_frame, current_scale, base_sound):
    auralizer = Auralizer(current_scale, base_sound)
    if prev_frame is None:
        prev_frame = np.zeros(video_data.shape)
    n, m, _ = video_data.shape
    hsv = cv2.cvtColor(video_data, cv2.COLOR_BGR2HSV)
    hue_vals, hue_counts = np.unique(hsv[..., 0], return_counts=True)

    probs, cumulative = six_colour_distribution(video_data)
    up = -1 if random.random() > 0.5 else 1
    step = random_with_distribution(cumulative)

    dom = hue_vals[np.argmax(hue_counts)]
    dominant = max(1, min(int(8 * dom / 129), 8))
    #     hue_vals = np.unique(hsv[..., 0])
    color_count = len(hue_vals)
    sat = np.mean(hsv[..., 1])

    saturation = 47 + int(80 * sat / 256)
    bblen, bb = get_bounding_boxes(video_data)
    diff = int(bb * len(rhythms))
    # print(diff)
    # volume = 30 + int(diff * 97)
    volume = (prev_vol[0] * 2 + min(127, 47 + int(10 * bblen))) // 3
    prev_vol[0] = volume
    rh = min(diff, len(rhythms) - 1)
    return [(auralizer.build_chord(dominant), volume, rhythms[rh][i]) for i in range(len(rhythms[rh]))]
