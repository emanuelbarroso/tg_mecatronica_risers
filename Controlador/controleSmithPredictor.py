# -*- coding: utf-8 -*-

from __future__ import print_function
import time
from Model import Model
import OpenOPC
import numpy
import matplotlib.pyplot as plt

opc = OpenOPC.client() # Cria o cliente OPC; o servidor é o RSLinx
opc.connect('RSLinx OPC Server') # Essa string não muda; conecta ao RSLinx

try:
	input('Enter para iniciar: ')
except:
	pass

opc['[CLP_AB]Program:DeviceN.pyInit'] = True

dt = 0.1
n = 70
position = zeros(n)
time = linspace(0,10,n)
t = 0.0

file_topo = open('dataWin/y_topo.txt','r')
file_fundo = open('dataWin/y_fundo.txt','r')
linha_topo = file_topo.readline()
linha_fundo = file_fundo.readline()
y_topo = numpy.zeros(n_t)
y_fundo = numpy.zeros(n_t)
y_out = numpy.zeros(n_t)

j = 0
for i in linha_topo.split():
	y_topo[j] = float(i)
	j += 1
j = 0
for i in linha_fundo.split():
	y_fundo[j] = float(i)
	j += 1

file_topo.close()
file_fundo.close()

n_t = 70
t = numpy.array(range(0, n_t)) * Ts

# instantiate the plant that will be used, it should be a subclass of Plant
plant = PlantOPC(opc,'[CLP_AB]position','[CLP_AB]speed')
model = Model(n, A, B, C, D, Ak, Bk, Ck, Q, R, Kp, Ki, epsilon, Ts, plant)

start = time.clock()
for i in range(0, n):
	t = time[i]
	y_out[i] = model.closed_loop(y_topo[i],y_fundo[i])
	time.sleep(dt)

print("Total simulation time: {}s".format(time.clock() - start))
plt.plot(t, y_out[0:n_t], label='out')
plt.plot(t, y_fundo[0:n_t], label='ref fundo')
plt.plot(t, y_topo[0:n_t], label='ref topo (in)')
plt.legend()
plt.xlabel('time (s)')
plt.ylabel('position (m)')
plt.title('Position of cart')
plt.grid(True)
plt.show()

opc.close() # Encerra a sessão
