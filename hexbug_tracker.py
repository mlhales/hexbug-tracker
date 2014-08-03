import sys
import getopt
import cv2
import numpy as np
from bounds import *
import pickle
from video_tracker import *


def track_video(source):
    video_tracker = VideoTracker(source)
    centroid, bounds, bug_size = video_tracker.record_geometry()
    return track(centroid, bounds, bug_size)


def track_data(data):
    p = open(data, 'r')
    d = pickle.load(p)
    centroid = d["centroid"]
    bounds = d["bounds"]
    bug_size = d["size"]
    return track(centroid, bounds, bug_size)


def track(centroid, bounds, bug_size):
    for c in centroid:
        print c
    return 0

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h:v:d", ["help", "video=", "data="])
        except getopt.error, msg:
            raise Usage(msg)
        if len(opts) == 1:
            if opts[0] == 'video':
                return track_video(opts[1])
            else:
                return track_data(opts[1])
        else:
            raise Usage("Only one option expected.")
    except Usage, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "For help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())