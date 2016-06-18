# -*- coding: utf-8 -*-

class DelayBlock:
	def __init__(self,epsilon,Ts):
		self.epsilon = epsilon;
		self.dim = int(0.01 + epsilon/Ts)
		self.hold = [0 for i in range(0,self.dim)]

	def update(self,newval):
		self.hold.insert(0,newval)
		self.hold.pop()

	def get_last_entry(self):
		return self.hold[-1]
