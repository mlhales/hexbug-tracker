__author__ = 'mlh'

import os
import sys
import getopt
import cv2
import numpy as np
from bounds import *
import pickle
from video_tracker import *
from hexbug_predictor import *


def predict_from_video(source, steps, prediction_filename):
    """
    Measure the world geometry and record centroid data from the video source,
    then run the prediction.
    """
    if os.path.isfile(source):
        video_tracker = VideoTracker(source)
        world_properties = video_tracker.record_geometry()
        return predict(world_properties, source, steps, prediction_filename)
    else:
        print >> sys.stderr, source + " could not be found."
        return 2


def predict_from_saved_data(data, steps, prediction_filename, source=None):
    """
    Load the recorded world geometry and centroid data from the binary file,
    then run the prediction.
    """
    if os.path.isfile(data):
        p = open(data, 'r')
        world_properties = pickle.load(p)
        p.close()
        return predict(world_properties, steps, prediction_filename, source)
    else:
        print >> sys.stderr, data + " could not be found."
        return 2


def predict(world_properties, steps, prediction_filename, source=None):
    """
    Create a HexbugPredictor, train it over the centroid data,
    then predict into the future the specified number of steps.
    """
    predictor = HexbugPredictor(world_properties, source)
    predictor.train()
    predictions = predictor.predict(steps)
    write_predictions(predictions, prediction_filename)
    return 0


def write_predictions(predictions, filename="predictions.txt"):
    """
    Write the predictions to the specified file.
    """
    f = open(filename, "w")
    f.write("[")
    for i in range(len(predictions) - 1):
        f.write("%s\n" % predictions[i])
    f.write("%s" % predictions[len(predictions) - 1])
    f.write("]")
    f.close()


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            options, args = getopt.getopt(argv[1:], "hv:d:s:o", ["help", "video=", "data=", "steps=", "output="])

        except getopt.error, msg:
            raise Usage(msg)

        video_filename = "Video/hexbug-testing_video.mp4"
        data_filename = None
        steps = 63
        predictions_filename = "prediction.txt"

        for opt, arg in options:
            if opt in ('-h', '--help'):
                print >> sys.stdout, help_text()
                return 0
            if opt in ('-v', '--video'):
                video_filename = arg
            if opt in ('-d', '--data'):
                data_filename = arg
            if opt in ('-s', '--steps'):
                steps = int(float(arg))
            if opt in ('-o', '--output'):
                predictions_filename = arg

        if video_filename and data_filename:
            return predict_from_saved_data(data_filename, steps, predictions_filename, video_filename)
        elif video_filename:
            return predict_from_video(video_filename, steps, predictions_filename)
        elif data_filename:
            return predict_from_saved_data(data_filename, steps, predictions_filename)

    except Usage, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "For help use --help"
        return 2


def help_text():
    return """

Usage:

$python hexbug_tracker-py [--video video_path] [--data data_path]
[--steps number_predictions] [--output output_path]

Examples:

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
a file hexbug-testing_video-predictions.

$python hexbug_tracker.py --video Video/hexbug-testing_video.mp4
--data Data/hexbug-testing_video.p --steps 63 --output prediction.txt

Runs the program on "pickled" data, but displays results overlaid on the video.
Predicts 63 time steps into the future and saves the predictions in the file
named prediction.txt."""


if __name__ == "__main__":
    sys.exit(main())