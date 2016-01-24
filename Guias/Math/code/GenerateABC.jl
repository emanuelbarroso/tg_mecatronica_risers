module GenerateABC
export generateA, generateB, generateC

function generateA(n, b, tau)
	M = zeros(n,n)
	#Primeira linha de M
	M[1,1] = 2*b
	M[1,2] = -5*b
	M[1,3] = 4*b
	M[1,4] = -b

	#Linhas 2 ate n-2
	for i = 2:n-2
		M[i,i-1] = b
		M[i,i] = -2*b
		M[i,i+1] = b
	end

	#Linha n-1
	M[n-1,n-2] = b
	M[n-1,n-1] = -2*b

	#Linha n
	M[n,n-3] = -b
	M[n,n-2] = 4*b
	M[n,n-1] = -5*b

	#Concatenar matrizes, gerando matriz (2n,2n)
	A = [[zeros(n,n) eye(n)]; [M -tau*eye(n)]]

	return A
end

function generateB(n, b, tau)
	B = zeros(2*n)
	B[2*n-1] = b
	B[2*n] = 2*b

	return B
end

function generateC(n,b,tau)
	C = zeros(2*n)
	C[1] = 1

	return C
end
end
