# -*- coding: utf-8 -*-
import numpy
from Plant import Plant


class PlantOPC(Plant):  # dummy class for now
    def __init__(self,server,position,speed):
        self.opc = server
		self.position = position
		self.speed = speed
		self.factor = 1000.0
		self.pos_old = server[position]
		self.spdfac = 71.32 ## mm/u
		self.Ts = 0.1

    def compute_y(self, u):
		speed_mm = (self.factor * u - self.pos_old) / self.Ts
		self.opc[self.speed] = speed_mm / self.spdfac
		self.pos_old = self.opc[self.position]
       	return self.opc[self.position] / self.factor
