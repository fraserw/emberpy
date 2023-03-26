#! /usr/bin/env python

import cv2
import pylab as pyl, numpy as np
from matplotlib.widgets import Slider, CheckButtons

# my best focus is at z=26.5

class Ember():
    """
    Base class called ember which provides the functionality of the ember camera

    When launched, will show a window with the camera FOV drawn, and refresh
    every delay seconds (0.5s default). A white reticle is drawn to help
    centre the nozzle.

    Use gcode to move the print heads around and record the locations.
    """

    def __init__(self, camera_index = 0, delay = 0.5, swap_xy = False, mirror_h = False, mirror_v = False):
        self.camera = cv2.VideoCapture(camera_index)

        self.fig = pyl.figure()

        self.swap_xy = swap_xy
        self.mirror_h = mirror_h
        self.mirror_v = mirror_v
        self.zoom = 1


        ## for mirror check buttons
        self.mirror_sp = self.fig.add_axes([0.05,0.05,0.18,0.15])
        self.mirror_x_radio = CheckButtons(self.mirror_sp,
                                                ('Mirror Hor.', 'Mirror Vert.'),
                                                (self.mirror_h, self.mirror_v))
        self.mirror_x_radio.on_clicked(self.mirror_swap)

        ## for swap axes check button
        self.swap_sp = self.fig.add_axes([0.3,0.05,0.18,0.15])
        self.swap_radio = CheckButtons(self.swap_sp,
                                                ('Swap X/Y',),
                                                (self.swap_xy,))
        self.swap_radio.on_clicked(self.mirror_swap)

        self.zoom_sp = self.fig.add_axes([0.57,0.05,0.35,0.15])
        self.zoom_slider = Slider(ax=self.zoom_sp, label='Zoom',
                                  valmin=1, valmax=4, valinit=1,
                                  valstep=[1,2,3,4]
                                  )
        self.zoom_slider.on_changed(self.set_zoom)



        ## the main plot
        #self.sp = self.fig.add_subplot(111)
        self.sp = self.fig.add_axes([0.1,0.2,0.85,0.85])

        #self.cid = self.fig.canvas.mpl_connect('button_press_event', self._find_click)
        self.cid = self.fig.canvas.mpl_connect('key_press_event', self.key_grab)
        self.closer = self.fig.canvas.mpl_connect('close_event', self.close)
        self.new_frame = None

        self.delay = delay


    def enter(self):
        pyl.ion()

        while True:
            self.grab_frame()
            (A,B) = self.new_frame.shape[:2]
            self.draw_im(x=int(B/2), y=int(A/2))
            pyl.pause(self.delay)


    def grab_frame(self):
        frame = None
        while frame is None:
            ret, frame = self.camera.read()

        if self.zoom !=0:
            (A,B) = frame.shape[:2]
            a,b = int(A/(self.zoom*2)),int(B/(self.zoom*2))
            if len(frame.shape) == 3:
                frame = frame[ int(A/2)-a:int(A/2)+a+1, int(B/2)-b:int(B/2)+b+1, :]
            else:
                frame = frame[ int(A/2)-a:int(A/2)+a+1, int(B/2)-b:int(B/2)+b+1,]


        if len(frame.shape) == 3:
            if self.swap_xy: frame = np.transpose(frame, axes=(1,0,2))
            if self.mirror_h: frame = frame[:, ::-1, :]
            if self.mirror_v: frame = frame[::-1, :, :]
        else:
            if self.swap_xy: frame = np.transpose(frame, axes=(1,0))
            if self.mirror_h: frame = frame[:, ::-1]
            if self.mirror_v: frame = frame[::-1, :]

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
            if not self.swap_xy:
                self.sp.set_xlabel('Y')
                self.sp.set_ylabel('X')
            else:
                self.sp.set_xlabel('X')
                self.sp.set_ylabel('Y')


    def mirror_swap(self, labels):
        if 'Mirror Hor.' in labels:
            self.mirror_h = False if self.mirror_h else True
        if 'Mirror Vert.' in labels:
            self.mirror_v = False if self.mirror_v else True
        if 'Swap X/Y' in labels:
            self.swap_xy = False if self.swap_xy else True


    def set_zoom(self,val):
        self.zoom = val


    def key_grab(self, event):
        if event.key in ['q', 'Q']:
            self.close()

    def close(self, event):
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
    parser.add_argument('--swap_xy',
                        help = 'Swap the x and y axes. DEFAULT=%(default)s',
                        default = False, action = 'store_true')
    parser.add_argument('--camera_index', help='The index of the camera to use. Adjust this number if the wrong usb camera shows up in the window. DEFAULT=%(default)s',
                        default = '0')
    args = parser.parse_args()

    ember = Ember(mirror_h = args.mirror_h, mirror_v = args.mirror_v,
                  swap_xy = args.swap_xy,
                  camera_index = int(float(args.camera_index)))
    ember.enter()
