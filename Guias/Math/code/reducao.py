# -*- coding: utf-8 -*-

import numpy
from numpy import linalg

def print_matriz(a,n):
	for i in range(0,n):
		st = ''
		for j in range(0,n):
			st += ('%10.1f' % a[i][j])
			if (j != n - 1):
				st += ' '
		print(st)
	print()

n = 6
tau = 0.2426			# tau do barbante
taul = 0.1133			# tau da bolinha
ms = 0.0006				# massa linear do barbante (kg/m)
mb = 0.00015			# massa da bolinha (kg)
g = 9.807				# aceleração da gravidade (m/s^2)
mlinha = mb				# massa a ser considerada da bolinha - despreza-se a massa de fluido adicionado
L = 0.82				# Comprimento total do barbante (m)
l = L/n					# distância entre dois pontos de discretização
T0 = mb*g				# Tração no ponto 0 (logo acima da bolinha) - considerando peso da bolinha (N)

b = numpy.zeros(shape=(n,1))
c = g/(2*l)
d = numpy.zeros(shape=(n,1))
e = numpy.zeros(shape=(n,1))
b[0] = mb*g/(mlinha*(n-1)*l)
for k in range(2,n+1):
	b[k-1] = (T0 + ms*g*(k-1)*l)/(ms*l**4)
	d[k-1] = b[k-1] - c
	e[k-1] = b[k-1] + c

O = numpy.zeros(shape=(n,n))
I = numpy.eye(n)
L = (-tau) * numpy.eye(n)
L[0][0] = (-taul)
M = numpy.zeros(shape=(n,n))

# b = [1,2,3,4,5,6]
# d = [0,0.2,0.3,0.4,0.5,0.6] # Teste
# e = [0,12,13,14,15,16]

for k in range(0,n):
	M[k][k] = -2*b[k] if k != 0 else -b[k]
	if k != n-1:
		M[k+1][k] = d[k+1]
		M[k][k+1] = e[k] if k != 0 else b[k]

A = numpy.vstack((numpy.hstack((O,I)),numpy.hstack((M,L))))
B = numpy.zeros(shape=(2*n,1))
B[2*n-1] = e[n-1]
C = numpy.zeros(shape=(1,2*n))
C[0] = 1

eig_A,T = linalg.eig(A)	# eig_A são os autovalores de A, e T é a matriz de autovetores
T_inv = linalg.inv(T)
A_M = numpy.array(numpy.matrix(T_inv) * numpy.matrix(A) * numpy.matrix(T))
B_M = numpy.array(numpy.matrix(T_inv) * numpy.matrix(B))
C_M = numpy.array(numpy.matrix(C) * numpy.matrix(T))
C_M_diag = numpy.zeros(shape=(2*n,2*n), dtype=complex)
for i in range(0,2*n):
	C_M_diag[i][i] = C_M[0][i]
# TODO descobrir como evitar casting de complexo para real.
#print_matriz(A,2*n)
