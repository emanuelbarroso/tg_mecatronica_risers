# -*- coding: utf-8 -*-

from __future__ import print_function

# Exemplo de programa para ler variáveis do CLP
# Funciona com TAGS locais e globais
 
#import os
#os.system("dir")
#os.system("net start zzzOpenOPCService") #antes de .client
#os.system("net stop zzzOpenOPCService") #No final do arquivo

from time import sleep
 
import OpenOPC
from numpy import *
opc = OpenOPC.client() # Cria o cliente OPC; o servidor é o RSLinx
opc.connect('RSLinx OPC Server') # Essa string não muda; conecta ao RSLinx

opc['[CLP_AB]Program:DeviceN.pyInit'] = True

dt = 0.01
n = 2001
position = zeros(n)
time = linspace(0,20, n)
t = 0.0

for i in range(0, n):
	t = time[i]
	tupla = opc.read('[CLP_AB]position') # Depende da variável a ser lida; retorna uma tupla
	position[i] = tupla[0]
	sleep(dt)
	print(position[i])

# Consertar o tempo utilizando o 3º eleme

#Quando for ler os valores, salvar em arrays numpy e pode usar o comando de salvar
#http://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.save.html
 
#importar tempo
#from time import sleep
#sleep(0.01) #a cada centésimo
#da time, pode importar a data também, para auxiliar na criação dos nomes de arquivos

#print(tupla)
 
opc.close() # Encerra a sessão
