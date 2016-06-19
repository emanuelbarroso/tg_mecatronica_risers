# -*- coding: utf-8 -*-
import numpy
from Plant import Plant
import scipy.io as sio


class PlantOrig(Plant):
    def __init__(self):
        plant_mat = sio.loadmat('data/plant.mat')
        self.A = numpy.matrix(plant_mat['A_orig'])
        self.B = numpy.matrix(plant_mat['B_orig'])
        self.C = numpy.matrix(plant_mat['C_orig'])
        self.D = numpy.matrix(plant_mat['D_orig'])
        self.order = self.A.shape[0]
        self.x = numpy.matrix(numpy.zeros((self.order, 1)))

    def compute_y(self, u):
        self.x = self.A * self.x + self.B * u
        y = self.C * self.x + self.D * u
        return y[0, 0]

if __name__ == "__main__":
    p = PlantOrig()
    for i in range(0,10):
        u = p.compute_y(i*0.1)
        print("Output: {}".format(u))