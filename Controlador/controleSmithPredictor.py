# -*- coding: utf-8 -*-

from __future__ import print_function
from time import sleep

import OpenOPC
from numpy import *
opc = OpenOPC.client() # Cria o cliente OPC; o servidor é o RSLinx
opc.connect('RSLinx OPC Server') # Essa string não muda; conecta ao RSLinx

opc['[CLP_AB]Program:DeviceN.pyInit'] = True

dt = 0.1
n = 201
position = zeros(n)
time = linspace(0,20,n)
t = 0.0

for i in range(0, n):
	t = time[i]
	tupla = opc.read('[CLP_AB]position') # Depende da variável a ser lida; retorna uma tupla
    y_out = tupla[0]
	position[i] = y_out
    next_u = compute_next_u(y_out)
    opc['[CLP_AB]Program:Controller.u'] = next_u
	sleep(dt)

opc.close() # Encerra a sessão
