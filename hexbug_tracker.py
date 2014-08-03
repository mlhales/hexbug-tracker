import sys
import getopt
import cv2
import numpy as np
from bounds import *
import pickle
from video_tracker import *
from hexbug_predictor import *


def track_video(source):
    video_tracker = VideoTracker(source)
    centroid, bounds, bug_size = video_tracker.record_geometry()
    return track(centroid, bounds, bug_size, source)


def track_data(data, source = None):
    p = open(data, 'r')
    d = pickle.load(p)
    centroid = d["centroid"]
    bounds = d["bounds"]
    bug_size = d["size"]
    p.close()
    return track(centroid, bounds, bug_size, source)


def track(centroid, bounds, bug_size, source = None):
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
            options, args = getopt.getopt(argv[1:], "h:v:d", ["help", "video=", "data="])
        except getopt.error, msg:
            raise Usage(msg)
        if len(options) > 0:
            for opt, arg in options:
                if opt in ('-v', '--video'):
                    video_filename = arg
                else:
                    video_filename = None
                if opt in ('-d', '--data'):
                    data_filename = arg
                else:
                    data_filename = None
            if video_filename and data_filename:
                track_data(data_filename, video_filename)
            elif video_filename:
                track_video(video_filename)
            elif data_filename:
                track_data(data_filename)
        else:
            raise Usage("You must pass at least one command line option.")
    except Usage, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "For help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())