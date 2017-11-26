import cv2


def show(frame, caption='Frame'):
    cv2.imshow(caption, frame)
    cv2.waitKey(0)
    cv2.destroyWindow(caption)
