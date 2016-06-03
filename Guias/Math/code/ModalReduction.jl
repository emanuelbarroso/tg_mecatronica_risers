module ModalReduction
export generateA, generateB, generateC
export generateABC, getABC_M, getABCD_R
export manuscript_p48, simulation
export generateMATLABSimulationScript


function simulation(n,original=false)
	A, B, C = generateABC(n)
	A_M, B_M, C_M = getABC_M(n, A, B, C)
	A_R, B_R, C_R, D_R = getABCD_R(n, A_M, B_M, C_M)
	if original
		generateMATLABSimulationScriptToCompare("simulacaoN" * string(n) * "Compare.m", A, B, C, A_R, B_R, C_R, D_R)
		generateMATLABSimulationScript(n, "simulacaoN" * string(n) * "Reduced.m", A_R, B_R, C_R, D_R)
	else
		generateMATLABSimulationScript(n, "simulacaoN" * string(n) * "Reduced.m", A_R, B_R, C_R, D_R)
	end
end

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

	b[1] = g/l
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

function getABCD_R(n, A_M, B_M, C_M)
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

	D_R = C_M / A_M * B_M - C_R / A_R * B_R
	return A_R, B_R, C_R, D_R
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
	#ordena pelo primeiro elemento da tupla
	#ordem descendente
	sort!(subsystems,rev=true)
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
	A_R, B_R, C_R, D_R = getABCD_R(n, A_M, B_M, C_M)

	return A_R, B_R, C_R, D_R
end

function generateMATLABSimulationScript(n, filename, A, B, C, D)
	output = "A = " * string(A) * ";\n\n"
	output = output * "B = " * string(B) * "';\n\n"
	output = output * "C = " * string(C) * ";\n\n"
	output = output * "D = " * string(D) * ";\n\n"
	output = output * "sys = ss(A, B, C, D);\n"
	output = output * "opt = stepDataOptions;"
	output = output * "opt.InputOffset = 0;\n"
	output = output * "opt.StepAmplitude = 0.3;\n"
	output = output * "t = (0:0.01:50)';\n"
	output = output * "y = step(sys, t, opt);"

	output = output * "fig = figure;\n"
	output = output * "hold on;\n"
	output = output * "plot(t,y,'k-');\n"
	output = output * "xlabel('Time (s)'), ylabel('Position (m)');\n"
	output = output * "title('Sistema original N = " * string(n) * ", simulacao reduzida para ordem 4');\n"
	output = output * "print('SimulationReduceN" * string(n) * "', '-dpng', '-r300');\n"
	output = output * "close(fig);\n"

	file = open(filename, "w")
	write(file, output)
	close(file)
end

function generateMATLABSimulationScriptToCompare(filename, A, B, C, A_R, B_R, C_R, D_R)
	output = "A_R = " * string(A_R) * ";\n\n"
	output = output * "B_R = " * string(B_R) * "';\n\n"
	output = output * "C_R = " * string(C_R) * ";\n\n"
	output = output * "D_R = " * string(D_R) * ";\n\n"
	output = output * "sysR = ss(A_R, B_R, C_R, D_R);\n\n"

	output = output * "A = " * string(A) * ";\n\n"
	output = output * "B = " * string(B) * "';\n\n"
	output = output * "C = " * string(C) * ";\n\n"
	output = output * "sysO = ss(A, B, C, [0]);\n\n"

	output = output * "opt = stepDataOptions;"
	output = output * "opt.InputOffset = 0;\n"
	output = output * "opt.StepAmplitude = 0.3;\n\n"

	output = output * "t = (0:0.01:50)';\n"
	output = output * "yR = step(sysR, t, opt);\n"
	output = output * "yO = step(sysO, t, opt);\n\n"

	output = output * "fig = figure;\n"
	output = output * "hold on;\n"
	output = output * "plot(t,yR,'k--');\n"
	output = output * "plot(t,yO,'k');\n"
	output = output * "legend('Reduzido', 'Original');\n"
	output = output * "xlabel('Time (s)'), ylabel('Position (m)');\n"
	n = round(Int,size(A)[1]/2)
	output = output * "title('Simulacao com sistema original N = " * string(n) * " e reduzido N = 4');\n"
	output = output * "print('SimulationN" * string(n) * "', '-dpng', '-r300');\n"
	output = output * "close(fig);\n"

	file = open(filename, "w")
	write(file, output)
	close(file)
end


end
