import cv2
from ImageFilter import ImageFilter

from lorenzo.BoundingBox import BoundingBox


class MotionFilter(ImageFilter):
    def __init__(self, shape, min_contour_area=0.01, max_contour_area=0.5, max_background_age=1):
        self.max_background_age = max_background_age
        self.background_age = max_background_age + 1

        self.full_frame_area = shape[0] * shape[1]

        self.min_contour_area = min_contour_area * self.full_frame_area
        self.max_contour_area = max_contour_area * self.full_frame_area
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
        result = cv2.threshold(frame_delta, 30, 255, cv2.THRESH_BINARY)[1]

        result = cv2.dilate(result, None, iterations=20)
        img, contours, _ = cv2.findContours(result.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        bounding_boxes = []
        for contour in contours:
            if self.min_contour_area < cv2.contourArea(contour) < self.max_contour_area:
                bounding_boxes.append(BoundingBox(*cv2.boundingRect(contour)))

        return result, bounding_boxes

    def preprocess_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.GaussianBlur(frame, (21, 21), 0)
        return frame
