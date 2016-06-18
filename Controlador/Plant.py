# -*- coding: utf-8 -*-
import numpy

class Plant: # dummy class for now
	def __init__(self,n,A,B,C,D):
		self.A = numpy.matrix(A)
		self.B = numpy.matrix(B)
		self.C = numpy.matrix(C)
		self.D = numpy.matrix(D)
		self.order = n
		self.x = numpy.matrix(numpy.zeros((n,1)))

	def compute_y(self,u):
		U = numpy.matrix([[u]])
		y = self.C * self.x + self.D * U
		self.x = self.A * self.x + self.B * U
		return y[0,0]
