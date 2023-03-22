#! /usr/bin/env python

import cv2
import pylab as pyl, numpy as np

# my best focus is at z=26.5


class Ember():
    """
    Base class called ember which provides the functionality of the ember camera

    When launched, will show a window with the camera FOV drawn, and refresh
    every delay seconds (0.5s default). A white reticle is drawn to help
    centre the nozzle.

    Use gcode to move the print heads around and record the locations.
    """

    def __init__(self, camera_index = 0, delay = 0.5, rotate = 0.0, mirror_h = False, mirror_v = False):
        self.camera = cv2.VideoCapture(camera_index)
        self.fig = pyl.figure()
        self.sp = self.fig.add_subplot(111)
        #self.cid = self.fig.canvas.mpl_connect('button_press_event', self._find_click)
        self.cid = self.fig.canvas.mpl_connect('key_press_event', self.key_grab)

        self.new_frame = None

        self.delay = delay

        self.rotate = rotate
        self.mirror_h = mirror_h
        self.mirror_v = mirror_v

        if rotate%90!=0:
            print('Please provide a rotation that is in a 90 degree increment.')
            print('e.g., 0, 90, 180, 270 in degrees')
            exit()

    def enter(self):
        pyl.ion()

        while True:
            self.grab_frame()
            (A,B) = self.new_frame.shape[:2]
            self.draw_im(x=int(B/2), y=int(A/2))
            pyl.pause(self.delay)

        #pyl.ioff()
        #pyl.show()

    def grab_frame(self):
        ret, frame = self.camera.read()

        if self.mirror_h: frame = frame[:, ::-1, :]
        if self.mirror_v: frame = frame[::-1, :, :]

        if frame is not None:
            self.new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def draw_im(self, x=None, y=None):
        pyl.cla()
        self.draw_reticle(x, y)
        self.im = self.sp.imshow(self.new_frame, origin='lower')

        self.label_axes()

        self.fig.canvas.draw()

    def draw_reticle(self, x, y, length = 100, offset=5):
        if x is not None and y is not None:
            (A,B) = self.new_frame.shape[:2]

            X,Y = x,y
            if X<0:
                X = 0
            elif X>=B:
                X = B-1
            if Y<0:
                Y = 0
            elif Y>=A:
                Y = A-1

            if len(self.new_frame.shape) == 3:
                self.new_frame[0:Y-offset, X, :] = 255
                self.new_frame[Y+offset:A, X, :] = 255
                self.new_frame[Y, 0:X-offset, :] = 255
                self.new_frame[Y, X+offset:B, :] = 255
            elif len(self.new_frame.shape) == 2:
                self.new_frame[Y-offset-length:Y-offset, X] = 255
                self.new_frame[Y+offset:Y+offset+length, X] = 255
                self.new_frame[Y, X-offset-length:X-offset] = 255
                self.new_frame[Y, X+offset:X+offset+length] = 255

    def label_axes(self):
            if self.rotate in np.arange(-630, 720, 180):
                self.sp.set_xlabel('Y')
                self.sp.set_ylabel('X')
            else:
                self.sp.set_xlabel('X')
                self.sp.set_ylabel('Y')

    def key_grab(self, event):
        if event.key in ['q', 'Q']:
            pyl.ioff()
            print('Quitting')
            exit()

    def _find_click(self, event):
        """
        Testing
        """
        self.draw_im(int(event.xdata), int(event.ydata))

    def _show_spot(self):
        """
        Testing
        """
        im = np.zeros((800, 1280))
        im[200,1100] = 255
        im[200,1101] = 255
        im[201,1100] = 255
        im[201,1101] = 255
        self.new_frame = im

        self.draw_im()

        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.find_click)
        self.cid = self.fig.canvas.mpl_connect('key_press_event', self.key_grab)
        pyl.show()

if __name__ == "__main__":

    from argparse import ArgumentParser

    #usage = "Launch as > python emberpy.py"
    parser = ArgumentParser()#usage = usage)
    parser.add_argument('--mirror_h',
                        help = 'Mirror in the horizontal image axis.',
                        default = False, action = 'store_true')
    parser.add_argument('--mirror_v',
                        help = 'Mirror in the vertical image axis.',
                        default = False, action = 'store_true')
    parser.add_argument('--rotate',
                        help = 'Rotate n degrees. Values in increments of 90. Negatives allowed. DEFAULT=%(default)s',
                        default = '0')
    parser.add_argument('--camera_index', help='The index of the camera to use. Adjust this number if the wrong usb camera shows up in the window. DEFAULT=%(default)s',
                        default = '0')
    args = parser.parse_args()

    ember = Ember(mirror_h = args.mirror_h, mirror_v = args.mirror_v,
                  rotate = int(float(args.rotate)),
                  camera_index = int(float(args.camera_index)))
    ember.enter()
