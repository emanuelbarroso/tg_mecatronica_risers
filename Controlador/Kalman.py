# -*- coding: utf-8 -*-
import numpy

class Kalman:
    def __init__(self, n, A, B, C, Q, R):
        self.x = numpy.matrix(numpy.zeros(n)).transpose()
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
        resid = y_err - self.C * self.x

        self.P = (numpy.eye(K.shape[1]) - K*self.C) * self.P
        return (self.x, self.x[0])

if __name__ == "__main__":
    n = 4
    A = numpy.random.rand(4,4)
    B = numpy.random.rand(4,1)
    C = numpy.random.rand(1,4)
    Q = 0.01**2 * numpy.eye(4)
    R = 0.1**2
    kalman_object = Kalman(n,A,B,C,Q,R)
    kalman_object.compute_kalman(1,1)
