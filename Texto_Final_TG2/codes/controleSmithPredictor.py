# -*- coding: utf-8 -*-

from __future__ import print_function
import time
from Model import Model
from PlantOPC import PlantOPC
import OpenOPC
import numpy
import matplotlib.pyplot as plt

opc = OpenOPC.client() # Cria o cliente OPC; o servidor é o RSLinx
opc.connect('RSLinx OPC Server') # Essa string não muda; conecta ao RSLinx

pC = numpy.array([0.5, 0.6, 0.7, 0.5 + 0.4j, 0.5 - 0.4j])
Ki = 0.183111320328469
Kp = numpy.array([0.007993734748865, 0.009705988539721, -0.004630469582507, -0.000426479250745])

# Kalman Matrices
n = 4
Ak = numpy.matrix([[0.993175847266250, 0.0997676389875316, 0.00447446153612418, 0.000154491807255262],
                       [-0.266442692060039, 0.989506934720158, 0.0794137333776907, 0.00441443534842949],
                       [-7.61331011046535, -0.371277877313592, 0.407916221277208, 0.0776985503560236],
                       [-134.001998512554, -9.45851595845769, -10.6078657460473, 0.377727256243161]])

Bk = numpy.matrix([0.674742463375352, 3.50238796155364, -32.6963528822316, -364.795682866366]).transpose()
Ck = numpy.matrix([1.0, 0.0, 0.0, 0.0])
Q = 0.01 ** 2 * numpy.eye(4)
R = 0.4 ** 2

epsilon = 0.3
Ts = 0.1
A = numpy.matrix([[0.9191, -0.3712, 0, 0], [0.3712, 0.9191, 0, 0], [0, 0, 0.4651, -0.8733], [0, 0, 0.8733, 0.4651]])
B = numpy.matrix([6.5818, 31.2517, -98.5991, -75.6695]).transpose()
C = numpy.matrix([-0.000339110145869, 0.014769867793814, 0.000052840348719, -0.002915328311939])
D = -0.068495332192496

n_t = 200
y_topo = numpy.zeros(n_t)
y_fundo = numpy.zeros(n_t)
y_out = numpy.zeros(n_t)

file_topo = open('dataWin/y_topo.txt','r')
file_fundo = open('dataWin/y_fundo.txt','r')
linha_topo = file_topo.readline()
linha_fundo = file_fundo.readline()
j = 0

start = time.clock()
init_pos = opc.read('[CLP_AB]position',update=1)[0]
print('Read init_pos in {}s'.format(time.clock()-start))

for i in linha_topo.split():
        if j < n_t:
                y_topo[j] = float(i) + (init_pos / 1000.0)
                j += 1

j = 0
for i in linha_fundo.split():
        if j < n_t:
                y_fundo[j] = float(i) + (init_pos / 1000.0)
                j += 1

file_topo.close()
file_fundo.close()

try:
	input('Enter para iniciar: ')
except:
	pass

opc['[CLP_AB]Program:DeviceN.pyInit'] = True

t = numpy.array(range(0, n_t)) * Ts
# time = linspace(0,10,n_t)
# instantiate the plant that will be used, it should be a subclass of Plant

plant = PlantOPC(opc,'[CLP_AB]position','[CLP_AB]speed',init_pos)
model = Model(n, A, B, C, D, Ak, Bk, Ck, Q, R, Kp, Ki, epsilon, Ts, plant)

start = time.clock()
t_old = start
times_p = []
for i in range(0, n_t):
	y_out[i] = model.closed_loop(y_topo[i],y_fundo[i])
	#time.sleep(0.1)
plant.kill()
print("Total simulation time: {}s".format(time.clock() - start))

y_out_phased = y_out[5:n_t]
t_out_phased = t[0:n_t-5]
##plt.plot(t, y_out[0:n_t], label='out')
plt.plot(t_out_phased,y_out_phased, label='out_n')
plt.plot(t, y_fundo[0:n_t], label='ref fundo')
plt.plot(t, y_topo[0:n_t], label='ref topo (in)')
plt.legend(loc=4)
plt.xlabel('time (s)')
plt.ylabel('position (m)')
plt.title('Position of cart - close loop')
plt.grid(True)
# plt.show()
plt.savefig("resultados/closed_loop_trajetoria_rafael.png", format='png', dpi=200)
File = open('resultados/trajetoria_rafael.npz','wb')
numpy.savez(File, t=t, y_topo=y_topo, y_fundo=y_fundo, y_out=y_out, pC=pC, Ki=Ki, Kp=Kp)
File.close()

opc.close() # Encerra a sessão
