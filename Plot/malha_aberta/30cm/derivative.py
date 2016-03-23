#!/usr/bin/env python3

import os, os.path
import struct

from numpy import *
from matplotlib import *
from matplotlib.pyplot import *
import scipy.io as sio #read matlab files
from scipy import interpolate

#filename = "position.bin"
#
##Número de bytes do arquivo
#sizebytes = os.stat(filename).st_size
#
##Número de elementos dos arra16
#
##Abrir arquivo
#f = open(filename, 'rb')
#
##Inicializar variáveis
#p = 1.0*arange(n)

#t = 1.0*arange(n)
#
##Ler do arquivo
#for k in range(0,n):
#    t[k] = struct.unpack('d',f.read(8))[0]
#    p[k] = struct.unpack('d',f.read(8))[0]
#
#f.close()

topo = sio.loadmat('topo.mat')
t = topo['t'][0]
p = abs(topo['Y'][0])

v = 1.0*arange(n)

#fundo = sio.loadmat('fundo.mat')

dt = t[1] - t[0]

#Velocidade v obtida está em m/s
#Calcular derivada (velocidade) em todos os pontos
v[0] = ((-3/2)*p[0] + 2*p[1] + (-1/2)*p[2])/dt
v[1] = (1/2)*(p[2] - p[0])/dt
for k in range(2,n-2):
    v[k] = (1/12)*(p[k-2] -8*p[k-1] + 8*p[k+1] - p[k+2])/dt

v[n-2] = (1/2)*(p[n-1] - p[n-3])/dt
v[n-1] = ((3/2)*p[n-1] - 2*p[n-2] + (1/2)*p[n-3])/dt
# --------------------------------------------------

#Realizar conversão para unidades/s que é a entrada do CLP
m_per_u = 0.07132083333 #metros por unidade
vu = v/m_per_u

#A partir da primeira derivada negativa, zerar as velocidades
for i in range(0,n):
    if abs(vu[i]) < 1e-2:
        vu[i] = 0.0

# afterZero = False
# for i in range(vu.argmax(),n):
#     if vu[i] == 0.0:
#         afterZero = True
#     if afterZero:
#         vu[i] = 0.0
for i in range(int(3/dt),n):
    vu[i] = 0.0


plot(t,vu*1000*m_per_u)
xlabel('tempo - segundos')
ylabel('Velocidade - mm/s')
title('Referência Malha Aberta de Velocidade - 20cm')
# show()
savefig('velocidade.png', dpi=300)
close()


#Criar structured text para inicialização
f = open('init.st', 'w')
f.write('/* Universidade de Brasilia\n')
f.write('Trabalho de Graduacao em Engenharia Mecatronica\n')
f.write('Alunos: \n')
f.write('Ataias Pereira Reis 10/0093817\n')
f.write('Emanuel Pereira Barroso Neto 11/0115716\n')
f.write('This code must be executed only once. */\n\n')
f.write('MSO(drive_axis,MSO_1);\n\n')
for i in range(0,n):
    f.write('speed[' + str(i) + '] := ' + str(vu[i]) + ';\n')
f.write('\ndataInitialized := 1;\n')
f.close()
