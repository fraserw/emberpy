# emberpy

A basic python script to make use of the emberpy camera for nozzle calibration.

Launch as:

> ./emberpy.py

Options:

--mirror_h and --mirror_v will mirror the image in horizontal and vertical axes
which is useful if your printer has reversed motion.

--rotate swaps the x and y axis labels in case you put your camera in rotated

--camera_index is an index used to select the correct usb camera. This defaults
to 0, but may need to be increased to other positive integers if the user has
more than one usb camera connected.

Requirements:
matplotlib
opencv-python (also known as cv2)
numpy


Tested on python 3.8 but should work with any python 3.+ variant.

Tested with numpy 1.21.5, matplotlib 3.6.0, and cv2 (opencv) 4.7.0
