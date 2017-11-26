import cv2
import video_streamer
import auralizer
import audio_player
import time
import threading

def stream_thread(frame, cont):
    while cont[0]:
        frame[0] = video_streamer.read_stream()
        cv2.imshow('Video', frame[0])
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            cont[0] = False


def auralizer_thread(frame, cont):
    prev_frame = frame[0]
    while cont[0]:
        t0 = time.time()
        video_data = frame[0]
        audio_data = auralizer.auralize(video_data, prev_frame)
        print(audio_data)
        audio_player.play(*audio_data)
        prev_frame = video_data
        time.sleep(max(0, DELTA - (time.time() - t0)))


DELTA = 0.25
if __name__ == "__main__":
    audio_player.init()
    prev_frame = None
    cont = [True]
    frame = [video_streamer.read_stream()]
    t1 = threading.Thread(target=stream_thread, args=(frame, cont))
    t1.start()
    t2 = threading.Thread(target=auralizer_thread, args=(frame, cont))
    t2.start()
    t1.join()
    t2.join()
    audio_player.quit()
