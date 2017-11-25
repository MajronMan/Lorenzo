import wave
import random
import struct
import numpy as np

SAMPLE_LEN = 1024

def fake_auralize(video_data):
    noise_output = wave.open('noise.wav', 'w')
    noise_output.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))
    noise = np.zeros(SAMPLE_LEN)

    for i in range(0, SAMPLE_LEN):
        value = random.randint(-32767, 32767)
        packed_value = struct.pack('h', value)
        noise[i] = packed_value

    return noise


def auralize(video_data):
    pass