# -*- coding: utf-8 -*-

from numpy import *
from numpy.linalg import *

#a is a numpy matrix
def print_matriz(a):
	(I,J) = a.shape	# Determina as dimensões da matriz a ser impressa
	for i in range(0,I):
		st = ''
		for j in range(0,J):
			#Números de valor absoluto menor que um threshold são mostrados como 0 para facilitar visualização
			st += '{:12.2}'.format((a[i,j] if (abs(a[i,j]) > 1e-10) else 0.0))
			if (j != J - 1):
				st += ' '
		print(st)
	print()

#Returns a string with the matriz being initialized
def initializeMatlabMatrix(M, matrixName):
	(I,J) = M.shape	# Determina as dimensões da matriz a ser impressa
	st = matrixName + ' = ['
	for i in range(0,I):
		for j in range(0,J):
			#Números de valor absoluto menor que um threshold são mostrados como 0 para facilitar visualização
			st += str(M[i,j])
			if (j != J - 1):
				st += ' '
		if (i != I - 1):
			st += ';\n'
	st += '];\n'
	return st

def generateSimulationMfile(A, B, C, D, filename):
	with open(filename, 'w') as f:
		f.write(initializeMatlabMatrix(A, 'A'))
		f.write(initializeMatlabMatrix(B, 'B'))
		f.write(initializeMatlabMatrix(C, 'C'))
		f.write(initializeMatlabMatrix(D, 'D'))
		f.write('\nsys = ss(A, B, C, D);\n')
		f.write('opt = stepDataOptions;\n')
		f.write('opt.InputOffset = 0;\n')
		f.write('opt.StepAmplitude = 0.3;\n')
		f.write("t = (0:0.01:50)';\n")
		f.write('y = step(sys, t, opt);')

def generateA(n, b, d, e, tau, taul):
	L = (-tau) * eye(n)
	L[0][0] = (-taul)
	M = zeros((n,n))
	for k in range(0,n):
		M[k][k] = -2*b[k] if k != 0 else -b[k]
		if k != n-1:
			M[k+1][k] = d[k+1]
			M[k][k+1] = e[k] if k != 0 else b[k]
	A = vstack((hstack((zeros((n,n)),eye(n))),hstack((M,L))))
	return matrix(A)

def generateB(n, e):
	B = zeros((2*n,1))
	B[2*n-1,0] = e[n-1]
	return matrix(B)

def generateC(n):
	C = zeros((1,2*n))
	C[0,0] = 1				# Como C é uma matriz linha, as duas dimensões são necessárias; senão, toda a matriz C valerá 1.
	return matrix(C)

def getReducedSystem(A,B,C,n):
	eig_A,T = eig(A)	# eig_A são os autovalores de A, e T é a matriz de autovetores
	T = matrix(T)
	#print('Autovalores de A')
	#print_matriz(matrix(eig_A))

	print('Matriz T')
	print_matriz(T)
	print()

	#A Matriz T não é a que deve ser utilizada para a transformação de similaridade!
	#Ela tem números complexos e isso é ruim
	#Ela deve ser convertida em uma matriz que tenha só números reais

	Tnew = matrix(zeros((2*n,2*n))) #real! não é complexo
	i = 0
	while i < 2*n: #será que tem algo errado? tem de testar
		if abs(imag(eig_A[i])) > 1e-10: # Procuramos algum elemento complexo de cada autovetor representado em T, não da matriz de autovalores de A
			Tnew[:,i] = real(T[:,i])
			Tnew[:,i+1] = -imag(T[:,i])
			i = i + 2
		else:
			Tnew[:,i] = T[:,i]
			i = i + 1

	print('Matriz T nova')
	print_matriz(Tnew)
	print()

	del T
	T = Tnew

	T_inv = matrix(inv(T))
	A_M = T_inv * A * T
	B_M = T_inv * B
	C_M = C * T
	C_M_diag = matrix(zeros((2*n,2*n), complex))


	print('Matriz A_M')
	print_matriz(A_M)
	print()
	#
	# print('Matrix B_M')
	# print_matriz(B_M)
	# print()
	#
	# print('Matrix C_M transposta')
	# print_matriz(C_M.transpose())
	# print()

	for i in range(0,2*n):
		C_M_diag[i,i] = C_M[0,i]
	A_M_inv = inv(A_M)
	Gains = C_M_diag * A_M_inv * B_M
	# print('Ganhos:')
	# print_matriz(Gains)
	# print()

	gdim = (Gains.shape[0] // 2)
	GainSum = zeros((gdim,1))

	#Como todos os autovalores são complexos, cada subsistema 2x2 é composto
	#de um autovalor e seu conjugado que é um outro autovalor
	for i in range(0,Gains.shape[0],2):
		GainSum[i//2] = real(abs(Gains[i] + Gains[i+1]))

	# print('Ganhos dos subsistemas 2x2 (todos os autovalores são complexos):')
	# print_matriz(GainSum)
	# print()

	#Obter maiores ganhos e índices
	gain = array([max(GainSum)])
	lines = array([argmax(GainSum)*2-2, argmax(GainSum)*2-1])
	GainSum = delete(GainSum, argmax(GainSum))
	beginning = 0
	gain = insert(gain, beginning, max(GainSum))
	lines = insert(lines, beginning, array([argmax(GainSum)*2-2, argmax(GainSum)*2-1]))
	print('Maiores ganhos')
	print(gain)
	print('Índices')
	print(lines)
	print()

	print('Autovalores')
	print_matriz(matrix(eig_A[lines]))
	print()

	print('Matriz A_R')
	eig1 = eig_A[lines[0]]
	eig2 = eig_A[lines[2]]
	A_R = matrix(array([[real(eig1), imag(eig1),  0,                    0],
						[-imag(eig1), real(eig1), 0,                    0],
						[0,           0,          real(eig2),  imag(eig2)],
						[0,           0,         -imag(eig2),  real(eig2)]]))
	print_matriz(A_R)
	print()

	print('Polos de A_R')
	print_matriz(matrix(eigvals(A_R)))
	print()

	print('Vetor B_R')
	B_R = B_M[lines]
	print_matriz(B_R)
	print()

	print('Vetor C_R')
	C_R = C_M[0,lines]
	print_matriz(C_R)
	print()

	print('Constante D_R')
	D_R = C*inv(A)*B - C_R*inv(A_R)*B_R
	print_matriz(D_R)
	print()

	generateSimulationMfile(A_R, B_R, C_R, D_R, 'simulacao.m')

def main():
	n = 2
	tau = 0.2426	# tau do barbante (0.2426)
	taul = 0.1133	# tau da bolinha (0.1133)
	ms = 0.0006		# massa linear do barbante (0.0006 kg/m)
	mb = 0.00015	# massa da bolinha (0.00015 kg)
	g = 9.80665		# aceleração da gravidade (9.807 m/s^2)
	L = 0.82		# Comprimento total do barbante (0.82 m)
	l = L/n			# distância entre dois pontos de discretização
	T0 = mb*g		# Tração no ponto 0 (logo acima da bolinha) - considerando peso da bolinha (N)

	b = zeros((n,1))
	c = g/(2*l)
	d = zeros((n,1))
	e = zeros((n,1))
	b[0] = g/((n-1)*l)
	for k in range(2,n+1):
		b[k-1] = (T0 + ms*g*(k-1)*l)/(ms*l**2)
		d[k-1] = b[k-1] - c
		e[k-1] = b[k-1] + c

	# b = [1,2,3,4,5,6]
	# d = [0,0.2,0.3,0.4,0.5,0.6] # Teste
	# e = [0,12,13,14,15,16]

	A = generateA(n, b, d, e, tau, taul)
	# print('Matriz A:')
	# print_matriz(A)
	# print()
	B = generateB(n,e)
	# print('Matriz B:')
	# print_matriz(B)
	# print()
	C = generateC(n)
	# print('Matriz C:')
	# print_matriz(C)
	# print()
	getReducedSystem(A,B,C,n)

def manuscript_p48():
	n = 2
	M = zeros((n,n))
	M[0,0] = -1
	M[0,1] = 1
	M[1,0] = 1
	M[1,1] = -3
	L = -2 * eye(n)
	A = vstack((hstack((zeros((n,n)),eye(n))),hstack((M,L))))
	B = zeros((2*n,1))
	B[2*n-1,0] = 2
	C = generateC(n)
	getReducedSystem(A, B, C, n)

# if __name__ == "__main__":
# 	main()
