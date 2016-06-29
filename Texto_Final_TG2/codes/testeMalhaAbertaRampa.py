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

start = time.clock()
init_pos = (opc.read('[CLP_AB]position',update=1)[0])
print('Read init_pos in {:.2f}s'.format(time.clock()-start))
print("Initial position: {}mm".format(init_pos))
try:
	input('Enter para iniciar: ')
except:
	pass

opc['[CLP_AB]Program:DeviceN.pyInit'] = True


# criando rampa
Ts = 0.1
n_t = 200
y_out = numpy.zeros(n_t)

t = numpy.array(range(0, n_t)) * Ts
out_max = 0.3
y_topo= numpy.ones(n_t)*out_max + init_pos / 1000.0
zero_time = 2.0
start = int(zero_time/Ts)
y_topo[0:start] = 0.0 + init_pos / 1000.0
movement_period = 2.5
total_movement_time= int(movement_period/Ts)
for i in range(0, total_movement_time):
        y_topo[i+start] = i * out_max / total_movement_time + init_pos / 1000.0

# instantiate the plant that will be used, it should be a subclass of Plant

plant = PlantOPC(opc,'[CLP_AB]position','[CLP_AB]speed',init_pos)

start = time.clock()
t_old = start
times_p = []
for i in range(0, n_t):
        if i > 20 and i < 45:
                y_out[i] = plant.apply_speed(out_max/movement_period)
        else:
                y_out[i] = plant.apply_speed(0.0)

plant.kill()
print("Total simulation time: {}s".format(time.clock() - start))

##y_out_phased = y_out[5:n_t]
##t_out_phased = t[0:n_t-5]
##plt.plot(t_out_phased,y_out_phased, label='out_n')
plt.plot(t[2:n_t], y_out[2:n_t], label='saida fundo')
plt.plot(t[2:n_t], y_topo[2:n_t], label='ref topo')
plt.legend(loc=4)
plt.xlabel('time (s)')
plt.ylabel('position (m)')
plt.title('Position of cart - open loop')
plt.grid(True)
##plt.show()
plt.savefig('resultados/open_loop_ramp.png', format="png", dpi = 200)

File = open('resultados/open_loop_ramp.npz','wb')
numpy.savez(File,t=t,y_topo=y_topo,y_out=y_out)
File.close()

opc.close() # Encerra a sessão
