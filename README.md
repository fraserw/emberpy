# emberpy

A basic python script to make use of the emberpy camera for nozzle calibration.

Launch as:

> ./emberpy.py

Options:

--mirror_h and --mirror_v will mirror the image in horizontal and vertical axes
which is useful if your printer has reversed motion.

--rotate swaps the x and y axis labels in case you put your camera in rotated

This script defaults to the first camera plugged in, and so will probably not
work if you have more than one attached.

Requirements:
matplotlib
opencv-python (also known as cv2)
numpy


Tested on python 3.8 but should work with any python 3.+ variant.
