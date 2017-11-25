from video_streamer import read_stream
from auralizer import auralize, fake_auralize
from audio_player import play_audio


if __name__ == "__main__":
    video_data = read_stream()
    audio_data = fake_auralize(video_data)
    play_audio(audio_data)