import cv2

from XiaoYiActionCamera import XiaoYiActionCamera

stream = XiaoYiActionCamera().open_stream()

key = -1
frame = stream.read_frame()
while frame is not None and key == -1:
    cv2.imshow('Live', frame)
    key = cv2.waitKey(1)
    frame = stream.read_frame()

stream.close()
