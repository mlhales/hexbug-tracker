#Hexbug Tracker

GA Tech OMCS
Programming a Self Driving Car

Final Project

Author - Michael Hales


--------------------------------------------

##Project Description

The program will track a hexbug toy as it moves around within a rectangular area.
It will predict the location of the hexbug for approximately 2.5 seconds (63 frames)
after the end of the provided video.


--------------------------------------------

##Proposed Solution

After watching the video of the hexbug motion several times, I have decided to
address the following major problems that set this problem apart from the
more simple problems we have addressed previously in the class.

1. World Measurement
2. Smoothing
3. Collision

###World Measurement

In order to accurately model any interaction with the world, its bounds must be determined.
A simple solution to this is to measure the hexbug motion through the entire video first.
In both the test and training video the hexbug interacts with all four walls, so the world
bounds can be established. I also modified the original code to measure the bounding rectangle
of the hexbug, so that I could determine when a collision would occur based on its actual size,
not just its centroid.

###Smoothing

The hexbug motion must be smoothed in order to provide stable predictions of its
trajectory based on its current motion. My first implementation used a particle
filter, but this turned out to be counter productive. I settled on using a simple
low-pass filter then correcting for the lag.

###Collision

The hexbug moves in a bounded world in which it collides with its boundaries. Any
accurate model of the hexbug world must be able to predict the change in hexbug
motion when it collides with a wall. It appears that the hexbug likes to turn right when
it hits the wall, so I modeled the collision as a right turn based on the angle of impact.


###Model

This program will attempt to determine measurements of the world and hexbug. A Python class (Hexbug)
will represent the hexbug state including the following values:
 
-Centroid (x, y)
-Orientation
-Size (length, width)

As the state is updated, filtered values for the centroid and orientation are determined,
and used to calculate the speed (delta position), and turn (delta orientation). 

Finally the hexbug object with the least error will be used to iteratively predict the
position for 63 frames or time steps beyond the current position.


--------------------------------------------

##Future Work

If I had time to continue to work on this project I would address the following items to
improve the sophistication of my program.

1. Physics
2. Improved Smoothing

Initially, I thought that this would be one of the important pieces of the project, but I did
not have time to address it. The hexbug loses velocity when it collides with the walls, then
accelerates again. The system could be improved by modeling the mass, impulse and friction of
the hexbug to better predict both its motion in the center of the world, and its reaction with
the walls of the world.

I planned to use a particle filter for this as well, where the particles represent physical
constants in the system, and the physics could be improved on line. This could also be done
using twiddle, or any other optimization technique with multiple runs over the video, but would
be more fun on-line.

I looked at several other methods to smooth the hexbug motion, such as local regression and 
more sophisticated low pass techniques like Savitzky-Golay etc.


--------------------------------------------

##Program Requirements

The only required libraries are OpenCV and NumPy. It is assumed that the program will be
run in an environment where these are available.

The program was developed and tested on a Mac (OSX Mavericks)


--------------------------------------------

##Program Usage

`$python hexbug_tracker.py --help`

Prints the usage options for the program.

`$python hexbug_tracker.py --video Video/hexbug-testing_video.mp4`

Runs the program on the specified video file. This will result in two passes over the video. The
first to compute the geometry of the world and the hexbug, and record the centroid locations. This
data is written to a file Data/hexbug-testing_video.p in the form of a "pickled" dictionary of Python
objects.

The second pass will perform the particle filter to determine the best model of the world, and
perform the predictions. Predictions will be written to a file hexbug-testing_video-predictions.

`$python hexbug_tracker.py --data Data/hexbug-testing_video.p`

Runs the program on the "pickled" data produced when running the program using the --video option.
It will perform the particle filter to determine the best model of the world, and
perform the predictions. Predictions will be written to a file hexbug-testing_video-predictions.