# -*- coding: utf-8 -*-
import numpy

class ReducedModel:
	def __init(self,A,B,C,D,n):
		self.A = A
		self.B = B
		self.C = C
		self.D = D
		self.order = n
		self.x = numpy.zeros(n,1)

	def compute_y(self,u):
		y = self.C * self.x + self.D * self.u
		self.x = self.A * self.x + self.B * self.u
		return y
