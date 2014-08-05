import os
import sys
import getopt
import cv2
import numpy as np
from bounds import *
import pickle
from video_tracker import *
from hexbug_predictor import *


def track_video(source):
    if os.path.isfile(source):
        video_tracker = VideoTracker(source)
        centroid, bounds, bug_size = video_tracker.record_geometry()
        return track(centroid, bounds, bug_size, source)
    else:
        print >> sys.stderr, source + " could not be found."
        return 2


def track_data(data, source=None):
    if os.path.isfile(data):
        p = open(data, 'r')
        d = pickle.load(p)
        centroid = d["centroid"]
        bounds = d["bounds"]
        bug_size = d["size"]
        p.close()
        return track(centroid, bounds, bug_size, source)
    else:
        print >> sys.stderr, data + " could not be found."
        return 2


def track(centroid, bounds, bug_size, source=None):
    predictions = []
    for i in range(62):
        predictions.append([0, 0])
    f = open("prediction.txt", "w")
    print >> f, predictions
    f.close()
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
                if opt in ('-h', '--help'):
                    print >> sys.stdout, help_text()
                if opt in ('-v', '--video'):
                    video_filename = arg
                else:
                    video_filename = None
                if opt in ('-d', '--data'):
                    data_filename = arg
                else:
                    data_filename = None
            if video_filename and data_filename:
                return track_data(data_filename, video_filename)
            elif video_filename:
                return track_video(video_filename)
            elif data_filename:
                return track_data(data_filename)
        else:
            raise Usage("You must pass at least one command line option.")
    except Usage, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "For help use --help"
        return 2


def help_text():
    return """

Usage:

$python hexbug_tracker.py --video Video/hexbug-testing_video.mp4

Runs the program on the specified video file. This will result in two passes
over the video. The first to compute the geometry of the world and the hexbug,
and record the centroid locations. This data is written to a file
Data/hexbug-testing_video.p in the form of a "pickled" dictionary of Python
objects.

The second pass will perform the particle filter to determine the best model of
the world, and perform the predictions. Predictions will be written to a file
hexbug-testing_video-predictions.

$python hexbug_tracker.py --data Data/hexbug-testing_video.p

Runs the program on the "pickled" data produced when running the program using
the --video option. It will perform the particle filter to determine the best
model of the world, and perform the predictions. Predictions will be written to
a file hexbug-testing_video-predictions."""


if __name__ == "__main__":
    sys.exit(main())