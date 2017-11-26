import numpy as np
import cv2
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(0)

#Setup SimpleBlobDetector parameters.
# params = cv2.SimpleBlobDetector_Params()

# Change thresholds
# params.minThreshold = 10
# params.maxThreshold = 200

# Filter by Area.
# params.filterByArea = True
# params.minArea = 1500

# Filter by Circularity
# params.filterByCircularity = True
# params.minCircularity = 0.1

#Filter by Convexity
# params.filterByConvexity = True
# params.minConvexity = 0.7

# Filter by Inertia
# params.filterByInertia = True
# params.minInertiaRatio = 0.01

# Create a detector with the parameters
# detector = cv2.SimpleBlobDetector_create(params)
while True:
    _, frame = cap.read()
    # ret, thresh1 = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
    # ret, thresh2 = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY_INV)
    # ret, thresh3 = cv2.threshold(frame, 127, 255, cv2.THRESH_TRUNC)
    # ret, thresh4 = cv2.threshold(frame, 127, 255, cv2.THRESH_TOZERO)
    # ret, thresh5 = cv2.threshold(frame, 127, 255, cv2.THRESH_TOZERO_INV)
    kernel = np.ones((5, 5), np.float32) / 25
    dst = cv2.filter2D(frame, -1, kernel)

    ret, thresh = cv2.threshold(dst, 127, 255, cv2.THRESH_BINARY)

    kernel1 = np.ones((5, 5), np.uint8)
    open = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel1)
    # close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel1)
    #
    #
    # keypoints = detector.detect(open)
    # im_with_keypoints = cv2.drawKeypoints(open, keypoints, np.array([]), (0, 0, 255),
    #                                        cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #
    # lower_red = np.array([150,150,50])
    # upper_red = np.array([180,255,150])
    #
    # lower_blue = np.array([100,150,50])
    # upper_blue = np.array([150,255,150])
    #
    # lower_green = np.array([60,150,50])
    # upper_green = np.array([100,255,255])
    #
    # maskr = cv2.inRange(hsv, lower_red, upper_red)
    # maskb = cv2.inRange(hsv, lower_blue, upper_blue)
    # maskg = cv2.inRange(hsv, lower_green, upper_green)
    # res = cv2.bitwise_and(frame, frame, mask = cv2.bitwise_or(maskr, cv2.bitwise_or(maskb,maskg)))
    # cv2.imshow('res',res)
    # xr = cv2.countNonZero(maskr)
    # xb = cv2.countNonZero(maskb)
    # xg = cv2.countNonZero(maskg)
    # print(xr,xb,xg)
    cv2.imshow('Video', open)


    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()





# plt.subplot(1,4,1),plt.imshow(frame)
# plt.xticks([]),plt.yticks([])
# plt.subplot(1,4,2),plt.imshow(thresh)
# plt.xticks([]),plt.yticks([])
# plt.subplot(1,4,3),plt.imshow(open)
# plt.xticks([]),plt.yticks([])
# plt.subplot(1,4,4),plt.imshow(close)
# plt.xticks([]),plt.yticks([])
# plt.show()