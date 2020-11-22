import cv2
import numpy as np
import scipy.optimize
from sklearn import linear_model
from enum import IntEnum
from PyQt5.QtCore import pyqtSlot, QObject


def wait(frames):
    for i in range(frames):
        yield True


def wait_until(cond):
    while cond():
        yield True


def estimation(camera_points, robot_points, dimention):
    coef = []
    intercept = []
    for i in range(dimention):
        robot_points_i = (np.array(robot_points).T)[i]
        ref_i = linear_model.LinearRegression().fit(camera_points, robot_points_i)
        coef.append(ref_i.coef_)
        intercept.append(ref_i.intercept_)
    coef = np.array(coef)
    intercept = np.array(intercept)
    return [coef, intercept]


def tikhonov_estimation(camera_points, robot_points, dimention):

    def _tikhonov(R, v, u):
        err = u - (R[:dimention] @ v + R[dimention])
        # return np.linalg.norm(err, ord=2)
        return np.linalg.norm(err, ord=2) + np.linalg.norm(R, ord=2)

    coef = []
    intercept = []
    for i in range(dimention):
        robot_data_i = (np.array(robot_points).T)[i]
        camera_data = np.array(camera_points).T
        x0 = np.ones(dimention+1)
        w_opt = scipy.optimize.minimize(fun=_tikhonov, x0=x0, args=(
            camera_data, robot_data_i), method="Powell")
        print(w_opt)
        coef.append(w_opt.x[:dimention])
        intercept.append(w_opt.x[dimention])

    coef = np.array(coef)
    intercept = np.array(intercept)
    return [coef, intercept]


class Frame:

    def __init__(self, cvgui, signal=None):
        self.image = None
        self.cvgui = cvgui
        self.signal = signal

    def set_image(self, image):
        self.image = image

    def add_rectangle(self, top_left, bottom_right):
        cv2.rectangle(self.image, top_left, bottom_right, (0, 0, 255), 3)

    def add_circle(self, point, radius):
        cv2.circle(self.image, point, radius, (0, 255, 0), 2)

    def add_marker(self, point):
        cv2.drawMarker(self.image, point, (0, 0, 255))

    def display(self, window):
        if self.cvgui:
            cv2.imshow(window, self.image)
        else:
            self.signal.emit(window, self.image)


class KeyCode(IntEnum):
    NULL = 0
    START = 32  # Space Key(Opencv)
    STOP = 27  # Esc Key(Opencv)
    EMERGENCY = 127  # Del Key(Opencv)

class Mode(IntEnum):
    MAIN = 1
    CALIBRATION_REALSENSE = 2
    CALIBRATION_WEBCAM = 3

class Layer(IntEnum):
    TOP = 0
    BOTTOM = 1
