__author__ = 'mlh'

import os
import math
import cv2
import pickle
import numpy as np
from bounds import *


class VideoTracker():
    """
    VideoTracker uses opencv to read a mp4 video file. It can determine the geometry of the world
    and record the geometry and hexbug positions in a pickled data file.
    """
    def __init__(self, source):
        self.source = source


    def record_geometry(self, display=True):
        cap = cv2.VideoCapture(self.source)
        hmin = (238 - 30) / 2
        hmax = (238 + 30) / 2
        smin = 255 / 2
        smax = 255
        vmin = int(0.20 * 255)
        vmax = int(1.0 * 255)
        lower = np.array([hmin, smin, vmin])
        upper = np.array([hmax, smax, vmax])

        centroid = []
        bounds = None
        length = []
        width = []
        ctr = 0

        while True:
            try:
                captured, frame = cap.read()
                if captured:
                    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    ctr += 1
                else:
                    break
            except:
                break

            mask = cv2.inRange(hsv, lower, upper)
            ret, thresh = cv2.threshold(mask, 127, 255, 0)
            contours, hierarchy = cv2.findContours(thresh, 1, 2)
            if contours:
                cnt = contours[0]
                rect = cv2.minAreaRect(cnt)
                box = cv2.cv.BoxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(frame, [box], 0, (0, 0, 255), 1)
                M = cv2.moments(cnt)
                if M['m00'] != 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    centroid.append([cx, cy])
                    cv2.circle(frame, (cx, cy), 2, (255, 0, 0))
                    if bounds:
                        bounds.expand_box(box)
                        w = self.distance_between(box[0], box[1])
                        l = self.distance_between(box[1], box[2])
                        if w > l:
                            temp = w
                            w = l
                            l = temp
                        length.append(l)
                        width.append(w)
                    else:
                        bounds = Bounds(cx, cy)
                else:
                    centroid.append([-1, -1])
            if bounds:
                cv2.rectangle(frame, (bounds.x, bounds.y), (bounds.x + bounds.w, bounds.y + bounds.h), (255, 255, 0), 2)
            cv2.imshow("Capture", frame)
            cv2.waitKey(1)

        l = np.int0(np.average(length))
        w = np.int0(np.average(width))
        properties = {"centroid": centroid, "bounds": bounds, "size": (l, w)}
        p = open("Data/" + os.path.basename(self.source) + ".p", 'wb')
        pickle.dump(properties, p)
        p.close()
        cap.release()
        cv2.destroyAllWindows()
        return centroid, bounds, (l, w)


    def distance_between(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))