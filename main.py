import time

import video_streamer
import auralizer
import audio_player
import time

DELTA = 0.25
if __name__ == "__main__":
    audio_player.init()
    prev_frame = None
    for i in range(1000):
        t0 = time.time()
        video_data = video_streamer.read_stream()
        audio_data = auralizer.auralize(video_data, prev_frame)
        print(audio_data)
        audio_player.play(*audio_data)
        prev_frame = video_data
        time.sleep(max(0, DELTA - (time.time() - t0)))
    audio_player.quit()