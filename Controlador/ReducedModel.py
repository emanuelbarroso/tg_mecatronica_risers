# -*- coding: utf-8 -*-
import numpy


class ReducedModel:
    def __init__(self, n, A, B, C, D):
        self.A = numpy.matrix(A)
        self.B = numpy.matrix(B)
        self.C = numpy.matrix(C)
        self.D = numpy.matrix(D)
        self.order = n
        self.x = numpy.matrix(numpy.zeros((n, 1)))

    def compute_y(self, u):
        y = self.C * self.x + self.D * u
        self.x = self.A * self.x + self.B * u
        return y[0, 0]


if __name__ == "__main__":
    n = 2
    A = numpy.matrix([[0.0, 1.0], [-1.3, -2.2]])
    B = numpy.matrix([[0.0], [1.0]])
    C = numpy.matrix([[1.0, 0.0]])
    D = numpy.matrix([[0.0]])
    sys = ReducedModel(n, A, B, C, D)
    lst = []
    u = 0.3
    for i in range(0, 20):
        lst.append(sys.compute_y(u))
    print(lst)
