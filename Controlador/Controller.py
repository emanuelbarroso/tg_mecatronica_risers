# -*- coding: utf-8 -*-

import numpy
from Kalman import Kalman


class Controller:
    def __init__(self, Kp, Ki, n, A, B, C, Q, R):
        self.Kp = Kp
        self.Ki = Ki
        self.u = 0.0
        self.err = 0.0
        self.kalman = Kalman(n, A, B, C, Q, R)

    def compute_next_u(self, y_err):
        (x_out, y_out) = self.kalman.compute_kalman(self.u, y_err)
        self.err = (self.err - y_out)[0, 0]
        self.u = (self.Ki * self.err - self.Kp * x_out)[0, 0]
        return self.u


if __name__ == "__main__":
    Kp = numpy.matrix([0.0101, 0.0123, -0.0050, -0.0022])
    Ki = 0.2326

    # Kalman Matrices
    n = 4
    A = numpy.matrix([[0.993175847266250, 0.0997676389875316, 0.00447446153612418, 0.000154491807255262],
                      [-0.266442692060039, 0.989506934720158, 0.0794137333776907, 0.00441443534842949],
                      [-7.61331011046535, -0.371277877313592, 0.407916221277208, 0.0776985503560236],
                      [-134.001998512554, -9.45851595845769, -10.6078657460473, 0.377727256243161]])
    B = numpy.matrix([0.674742463375352, 3.50238796155364, -32.6963528822316, -364.795682866366]).transpose()
    C = numpy.matrix([1.0, 0.0, 0.0, 0.0])
    Q = 0.01 ** 2 * numpy.eye(4)
    R = 0.1 ** 2
    controller = Controller(Kp, Ki, n, A, B, C, Q, R)
    for i in range(0, 10):
        print(controller.compute_next_u(1.0))
