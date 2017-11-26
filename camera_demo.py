import cv2
# import imutils

from MotionFilter import MotionFilter
from VideoStream import VideoStream

# stream = XiaoYiActionCamera().open_stream()
stream = VideoStream(cv2.VideoCapture(0))

key = -1
frame = stream.read_frame()

motion = MotionFilter(frame.shape)
while frame is not None and key != ord('q'):
    cv2.imshow('Motion', motion.filter(frame)[0])
    cv2.imshow('Live', frame)
    key = cv2.waitKey(1) & 0xFF
    frame = stream.read_frame()

stream.close()
cv2.destroyAllWindows()
