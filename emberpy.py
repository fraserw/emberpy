import cv2
import matplotlib.pyplot as pyl


class Ember():
    """
    Base class called ember which provides the functionality of the ember camera
    """

    def __init__(self, camera_index = 0, delay = 0.2):
        self.camera = cv2.VideoCapture(camera_index)
        self.fig = pyl.figure()
        self.sp = self.fig.add_subplot(111)

        self.new_frame = None

        self.delay = delay

    def enter(self):
        pyl.ion()

        self.grab_frame()
        self.im = self.sp.imshow(self.new_frame)
        while True:
            self.grab_frame()
            self.im.set_data(self.new_frame)
            pyl.pause(self.delay)

        pyl.ioff()
        pyl.show()

    def grab_frame(self):
        ret, frame = self.camera.read()
        self.new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

if __name__ == "__main__":

    ember = Ember()
    ember.enter()
