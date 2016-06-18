# -*- coding: utf-8 -*-
import numpy
from ReducedModel import ReducedModel
from DelayBlock import DelayBlock
from Kalman import Kalman
from Controller import Controller

class Model:
	def __init__(self,n,A,B,C,D,Ak,Bk,Ck,Q,R,epsilon,Ts):
		self.reduced_model = ReducedModel(n,A,B,C,D)
		#self.kalman_filter = Kalman(n,Ak,Bk,Ck,Q,R)
		#self.feedback_controller = Controller(y_err)
		self.delay_block = DelayBlock(epsilon,Ts)

	def closed_loop(self,y_top,y_bottom):
		return y_ref
