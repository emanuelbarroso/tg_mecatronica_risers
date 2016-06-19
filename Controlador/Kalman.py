# -*- coding: utf-8 -*-
import numpy


class Kalman:
    def __init__(self, n, A, B, C, Q, R):
        self.x = numpy.zeros((n, 1))
        self.P = numpy.matrix(numpy.zeros((n, n)))
        self.A = numpy.matrix(A)
        self.B = numpy.matrix(B)
        self.C = numpy.matrix(C)
        self.Q = numpy.matrix(Q)
        self.R = numpy.matrix(R)

    def compute_kalman(self, u, y_err):
        # Propagate the state estimate and covariance matrix:
        self.x = self.A * self.x + self.B * u
        self.P = self.A * self.P * self.A.transpose() + self.Q

        # Calculate the Kalman gain
        K = self.P * self.C.transpose() / (self.C * self.P * self.C.transpose() + self.R)

        # Calculate the measurement residual
        residual = y_err - self.C * self.x

        # Update the state and error covariance estimate
        self.x = self.x + K * residual
        self.P = (numpy.eye(K.shape[0]) - K * self.C) * self.P

        return self.x, (self.C * self.x)


if __name__ == "__main__":
    n = 4
    A = numpy.random.rand(4, 4)
    B = numpy.random.rand(4, 1)
    C = numpy.random.rand(1, 4)
    Q = 0.01 ** 2 * numpy.eye(4)
    R = 0.1 ** 2
    kalman_object = Kalman(n, A, B, C, Q, R)
    print(kalman_object.compute_kalman(1, 1))
