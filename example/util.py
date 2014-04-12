from threading import Thread
import time

import numpy as np

class Master:
    def __init__(self):
        self.w = None
        self.nseconds = 5

    def start(self):
        if self.w and self.w.is_alive():
            print 'already running!'
        else:
            self.w = Worker(self.nseconds)
            self.w.start()

    def is_alive(self):
        return self.w.is_alive()

    def time(self):
        return self.w.time

    def x(self):
        return self.w.x

    def y(self):
        return self.w.y

    def stopped(self):
        return self.w.stopped

    def stop(self):
        self.w.stopped = True

class Worker(Thread):

    def __init__(self,nseconds):
        Thread.__init__(self)
        self.nseconds = nseconds
        self.n = 40
        self.x = np.linspace(0, 2*np.pi, 40)
        self.y = np.zeros( (40,) )
        self.stopped = False
        self.time = 0

    def run(self):
        for i in range(self.nseconds * 100):
            if self.stopped:
                break
            t = i / 100.
            self.time = t
            self.y = np.sin(self.x) * np.sin(t)
            time.sleep(0.01)

def gaussian2d(x,y,A=1,x0=0,y0=0,sx=1,sy=1):
    xpart = (x-x0)**2 / (2*sx**2)
    ypart = (y-y0)**2 / (2*sy**2)
    return A * np.exp(-(xpart+ypart))

def gaussian2d_translated(t,gridx,gridy,velocity=1):
    xmin = gridx.min()
    xmax = gridx.max()
    lx = xmax-xmin
    period = lx / velocity
    x0 = xmin + t*velocity
    data_a = util.gaussian2d(gridx,gridy,x0=x0)
    return data_a
