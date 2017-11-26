import cv2

from ImageFilter import ImageFilter


class MotionFilter(ImageFilter):
    def __init__(self, shape, min_contour_area=0.01, max_contour_area=0.5, max_background_age=1):
        self.max_background_age = max_background_age
        self.background_age = max_background_age + 1

        full_frame_area = shape[0] * shape[1]

        self.min_contour_area = min_contour_area * full_frame_area
        self.max_contour_area = max_contour_area * full_frame_area
        self.background_frame = None
        self.last_frame = None

    def filter(self, frame):
        current = self.preprocess_frame(frame)

        if self.background_age > self.max_background_age:
            self.background_frame = current
            self.background_age = 0
            if self.last_frame is not None:
                current = self.last_frame  # prevent comparing background with itself

        self.last_frame = current
        self.background_age += 1

        frame_delta = cv2.absdiff(self.background_frame, current)
        # show(frame_delta, 'delta')
        result = cv2.threshold(frame_delta, 30, 255, cv2.THRESH_BINARY)[1]
        # show(result, 'threshold')

        result = cv2.dilate(result, None, iterations=20)
        # show(result, 'dilated')
        img, contours, _ = cv2.findContours(result.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        bounding_boxes = []
        for contour in contours:
            if self.min_contour_area < cv2.contourArea(contour) < self.max_contour_area:
                bounding_boxes.append(cv2.boundingRect(contour))
                # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        return result, bounding_boxes

    def preprocess_frame(self, frame):
        # frame = imutils.resize(frame, width=500)
        # show(frame, 'resized')
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # show(frame, 'grayscale')
        frame = cv2.GaussianBlur(frame, (21, 21), 0)
        # show(frame, 'gaussian')
        return frame
