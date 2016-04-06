module GenerateABC
export generateA, generateB, generateC

#Gera A, B, C to sistema completo
function generateABC(n)
	tau = 0.2426			# tau do barbante (1/s)
	taul = 0.1133			# tau da bolinha (1/s)
	ms = 0.0006				# massa linear do barbante (kg/m)
	mb = 0.00015			# massa da bolinha (kg)
	g = 9.807				# aceleração da gravidade (m/s^2)
	L = 0.82				# Comprimento total do barbante (m)
	l = L/n					# distância entre dois pontos de discretização (m)
	T0 = mb*g				# Tração no ponto 0 (logo acima da bolinha) - considerando peso da bolinha (N)

	b = zeros(n)
	c = g/(2l)
	d = zeros(n)
	e = zeros(n)

	b[1] = g/(n-1)/l
	for k = 2:n
		b[k] = (T0 + ms*g*(k-1)*l)/(ms*l^2)
		d[k] = b[k-1] - c
		e[k] = b[k-1] + c
	end

	A = generateA(n, b, d, e, tau, taul)
	B = generateB(n,e[n])
	C = generateC(n)

	return A, B, C
end

function generateA(n, b, d, e, tau, taul)
	M = zeros(n,n)
	#Primeira linha de M
	M[1,1] = -b[1]
	M[1,2] = b[1]

	#Linhas 2 ate n-1
	for i = 2:n-1
		M[i,i-1] = d[i]
		M[i,i] = -2*b[i]
		M[i,i+1] = e[i]
	end

	#Linha n
	M[n,n-1] = d[n]
	M[n,n] = -5*b[n]

	L = eye(n)
	for i = 1:n
		L[i,i] = i == 1 ? -taul : -tau
	end

	#Concatenar matrizes, gerando matriz (2n,2n)
	A = [[zeros(n,n) eye(n)]; [M L]]

	return A
end

function generateB(n, eN)
	B = zeros(2*n)
	B[2*n] = eN

	return B
end

function generateC(n)
	C = zeros(1,2*n)
	C[1,1] = 1

	return C
end
end
