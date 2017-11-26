import os
import subprocess
import numpy as np


class FFmpegVideoCapture:
    def __init__(self, source, width, height, mode="bgr24"):
        """
        :param mode: rgb24,bgr24
        """

        self.source = source
        self.width = width
        self.height = height
        self.mode = mode
        self.px_per_frame = width * height * 3

        self.dev_null = open(os.devnull, 'w')
        ffmpeg_command = ["D:/Portable/ffmpeg-20171123-a60b242-win64-static/bin/ffmpeg.exe", '-i', source, "-f",
                          "rawvideo", "-pix_fmt", mode, "-"]

        self.ffmpeg = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=self.dev_null)
        self.output = self.ffmpeg.stdout

    def read(self):
        if self.ffmpeg.poll():
            return False, None

        raw_frame = self.output.read(self.px_per_frame)
        if not raw_frame:
            return False, None

        return True, np.frombuffer(raw_frame, dtype=np.uint8).reshape((self.height, self.width, 3))

    def release(self):
        self.ffmpeg.kill()
        self.dev_null.close()
