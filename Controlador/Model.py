# -*- coding: utf-8 -*-
import numpy
from ReducedModel import ReducedModel
from DelayBlock import DelayBlock
from Kalman import Kalman
#from Controller import Controller

class Model:
	def __init__(self,n,A,B,C,D,Ak,Bk,Ck,Q,R,epsilon,Ts):
		self.reduced_model = ReducedModel(n,A,B,C,D)
		#self.kalman_filter = Kalman(n,Ak,Bk,Ck,Q,R)
		#self.feedback_controller = Controller(y_err)
		self.delay_block = DelayBlock(epsilon,Ts)

	def closed_loop(self,y_top,y_bottom):
		return y_ref

if __name__ == "__main__":
	n = 4
	A = numpy.random.rand(4,4)
	B = numpy.random.rand(4,1)
	C = numpy.random.rand(1,4)
	D = numpy.random.rand(1,1)
	Ak = numpy.random.rand(4,4)
	Bk = numpy.random.rand(4,1)
	Ck = numpy.random.rand(1,4)
	Q = 0.01**2 * numpy.eye(4)
	R = 0.1**2
	epsilon = 0.3
	Ts = 0.1
	model = Model(n,A,B,C,D,Ak,Bk,Ck,Q,R,epsilon,Ts)
	print(model.delay_block.dim)
	lst = []
	for i in range(0,6):
		lst.append(model.reduced_model.compute_y(1))
	print(lst)
