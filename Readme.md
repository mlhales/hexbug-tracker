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

1. Collision
2. Acceleration

###Collision

The hexbug moves in a bounded world in which it collides with its boundaries. Any
accurate model of the hexbug world must be able to predict the change in hexbug
motion when it collides with a wall.

###Acceleration

The hexbug moves in the real world. When it collides with a wall, its forward momentum
is converted to angular momentum and it changes velocity and orientation. There is friction
that opposes its movement, and a driving force or impulse that accelerates it up to its
maximum speed. It is assumed that the driving force is constant, and the maximum speed
is attained when the friction force equals the driving force.

###Model

This program will attempt to determine measurements of the world and hexbug. A Python Class
will represent possible hexbug states including the following values:
 
-Centroid (x, y)
-Orientation

In addition the above mutable values, the hexbug class will also represent immutable values
that describe physical properties of the hexbug.

-Dimensions (length, width)
-Mass
-Friction Coefficients
-Impulse

We do not know from the input video what the actual physical properties of the hexbug are,
so these must be determined empirically. This program will use a *particle filter* to create
a large number of hexbug objects with different possible physical properties, and select the
hexbug objects that best model the measurements of the actual hexbug position.

Finally the hexbug object with the least error will be used to iteratively predict the
position for 63 frames or time steps beyond the current position.

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