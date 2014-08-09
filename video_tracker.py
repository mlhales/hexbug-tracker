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


    def record_geometry(self):
        """
        Finds the centroid of the hexbug, as well as the size, and the world boundaries.
        Also records speed, and rotational information to use in modeling the hexbug motion later.
        Adapted from the original hexbug_tracker.py run provided with the project.
        :return: properties, a dictionary with the recorded world observations.
        """
        cap = cv2.VideoCapture(self.source)
        hmin = (238 - 30) / 2
        hmax = (238 + 30) / 2
        smin = 255 / 2
        smax = 255
        vmin = int(0.20 * 255)
        vmax = int(1.0 * 255)
        lower = np.array([hmin, smin, vmin])
        upper = np.array([hmax, smax, vmax])

        bounds = None
        last = None
        last_orientation = None

        centroid = []
        length = []
        width = []
        speed = []
        turn = []
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
                # Find the outer size of the hexbug
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
                        w = distance_between(box[0], box[1])
                        l = distance_between(box[1], box[2])
                        if w > l:
                            temp = w
                            w = l
                            l = temp
                        length.append(l)
                        width.append(w)
                    else:
                        bounds = Bounds(cx, cy)
                    if last:
                        #Record speed and orientation information.
                        s = distance_between((cx, cy), last)
                        speed.append(s)
                        cv2.line(frame, (cx, cy), last, (255, 255, 0), 2)
                        o = get_orientation(last, (cx, cy))
                        if last_orientation:
                            turn.append(o - last_orientation)
                        last_orientation = o
                    last = (cx, cy)
                else:
                    centroid.append([-1, -1])
                    last = None
                    last_orientation = None
            if bounds:
                cv2.rectangle(frame, (bounds.x, bounds.y), (bounds.x + bounds.w, bounds.y + bounds.h), (255, 255, 0), 2)
            cv2.imshow("Measure the World", frame)
            cv2.waitKey(1)

        l = np.int0(np.average(length))
        w = np.int0(np.average(width))

        #Record the world measurements in a dictionary and "pickle it" in a binary file.
        properties = {"centroid": centroid,
                      "bounds": bounds,
                      "size": (l, w),
                      "turn_mu": np.median(turn),
                      "turn_var": np.var(turn),
                      "turn_max": max(turn),
                      "speed_mu": np.median(speed),
                      "speed_var": np.var(speed),
                      "speed_max": max(speed)}
        p = open("Data/" + os.path.basename(self.source) + ".p", 'wb')
        pickle.dump(properties, p)
        p.close()
        cap.release()
        cv2.destroyAllWindows()
        return properties


