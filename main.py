import cv2

import filters
import video_streamer
import auralizer
import audio_player
import time
import threading

from VideoStream import VideoStream
from XiaoYiActionCamera import XiaoYiActionCamera

CURRENT_FILTER = "BLUR"


def stream_thread(video_stream, frame, cont):
    while cont[0]:
        frame[0] = video_stream.read_frame()
        frame[0] = filters.filters[CURRENT_FILTER](frame[0])
        cv2.imshow('Video', frame[0])
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            cont[0] = False


def auralizer_thread(frame, cont):
    prev_frame = frame[0]
    while cont[0]:
        t0 = time.time()
        video_data = frame[0]
        audio_data = auralizer.auralize(video_data, prev_frame)
        print(audio_data)
        audio_player.play(audio_data)
        prev_frame = video_data
        time.sleep(max(0, DELTA - (time.time() - t0)))


DELTA = audio_player.METRUM * 60 / audio_player.BPM

if __name__ == "__main__":
    audio_player.init()

    prev_frame = None
    cont = [True]

    video_stream = XiaoYiActionCamera().open_stream()
    frame = [video_stream.read_frame()]

    t1 = threading.Thread(target=stream_thread, args=(video_stream, frame, cont))
    t1.start()

    t2 = threading.Thread(target=auralizer_thread, args=(frame, cont))
    t2.start()

    t1.join()
    t2.join()

    video_stream.close()

    audio_player.quit()
