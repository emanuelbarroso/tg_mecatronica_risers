module GenerateABC
export generateA, generateB, generateC
export generateABC, getABC_M, getABC_R
export manuscript_p48

#Gera A, B, C to sistema completo
function generateABC(n)
	tau = 0.2426			# tau do barbante (1/s) para excursão de 30cm
	taul = 0.1133			# tau da bolinha (1/s) para excursão de 30cm
	ms = 0.0006				# massa linear do barbante (kg/m)
	mb = 0.00015			# massa da bolinha (kg)
	g = 9.80665				# aceleração da gravidade (m/s^2)
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
		d[k] = b[k] - c
		e[k] = b[k] + c
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
	M[n,n] = -2*b[n]

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

function getT(n, A)
	eig_A = eigvals(A)
	Tcomplex = eigvecs(A)

	T = zeros(2*n, 2*n)
	i = 1
	while i <= 2*n #será que tem algo errado? tem de testar
		if abs(imag(eig_A[i])) > 1e-10
			T[:,i] = real(Tcomplex[:,i])
			T[:,i+1] = -imag(Tcomplex[:,i])
			i = i + 2
		else
			T[:,i] = Tcomplex[:,i]
			i = i + 1
		end
	end

	return T
end

function getABC_M(n, A, B, C)
	T = getT(n,A)

	A_M = T \ A * T
	B_M = T \ B
	C_M = C * T

	return A_M, B_M, C_M
end

function getABC_R(n, A_M, B_M, C_M)
	C_M_diag = diagm(vec(C_M)) #matriz diagonal
	G = C_M_diag / A_M * B_M #ganhos
	subsystems = getSubsystems(n, eigvals(A_M), G)
	n_out = 4
	A_R = zeros(n_out,n_out)
	B_R = zeros(n_out)
	C_R = zeros(1,n_out)

	#Construir matrizes
	i = 1
	j = 1
	while i <= n_out
		index = subsystems[j][2]
		if  length(index) == 2 #complexo
			A_R[i:i+1,i:i+1] = A_M[index, index]
			B_R[[i,i+1]] = B_M[index]
			C_R[1,[i,i+1]] = C_M[index]
			i = i + 2
		else
			A_R[i,i] = A_M[index[1],index[1]]
			B_R[i] = B_M[index[1]]
			C_R[1,i] = C_M[index[1]]
			i = i + 1
		end
		j = j + 1
	end
	return A_R, B_R, C_R
end

function getSubsystems(n, eig_A, G)
	i = 1
	subsystems = []
	while i <= 2*n
		if abs(imag(eig_A[i])) > 1e-10 #complexo
			gain = abs(G[i] + G[i+1]) #considera sinal na soma como aqui ou soma os módulos?
			append!(subsystems, [(gain, [i,i+1])])
			i = i + 2
		else #real
			gain = abs(G[i])
			append!(subsystems, [(gain, [i])])
			i = i + 1
		end
	end
	sort!(subsystems) #ordena pelo primeiro elemento da tupla
	return subsystems
end

function manuscript_p48()
	n = 2
	M = [[-1 1]; [1 -3]]
	L = -2 * eye(n)
	A = [[zeros(n,n) eye(n)];[M L]]
	B = generateB(2,2)
	C = generateC(n)

	A_M, B_M, C_M = getABC_M(n,A,B,C)
	A_R, B_R, C_R = getABC_R(n, A_M, B_M, C_M)

	return A_R, B_R, C_R
end

end
