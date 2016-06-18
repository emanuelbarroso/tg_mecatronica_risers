# -*- coding: utf-8 -*-
import numpy

class ReducedModel:
	A = numpy.matrix(numpy.eye(1))
	B = numpy.matrix(numpy.eye(1))
	C = numpy.matrix(numpy.eye(1))
	D = numpy.matrix(numpy.eye(1))
	x = numpy.matrix(numpy.eye(1))
	order = 1

	def __init__(self,A,B,C,D,n):
		self.A = numpy.matrix(A)
		self.B = numpy.matrix(B)
		self.C = numpy.matrix(C)
		self.D = numpy.matrix(D)
		self.order = n
		self.x = numpy.zeros(n,1)

	def compute_y(self,u):
		y = self.C * self.x + self.D * self.u
		self.x = self.A * self.x + self.B * self.u
		return y
