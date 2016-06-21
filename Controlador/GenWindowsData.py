import scipy.io as sio

def gen_line(lista):
	st = ''
	z = len(lista)
	for i in range (0,z):
		if i > 0:
			st += ' '
		st += str(lista[i])
	st += '\n'
	return st

y_fundo = (sio.loadmat('data/y_fundo_30cm.mat'))['y_fundo'][0]
y_topo = (sio.loadmat('data/y_topo_30cm.mat'))['y_topo'][0]

fp_topo = open("dataWin/y_topo.txt","w")
fp_topo.write(gen_line(y_topo))
fp_topo.close()

fp_fundo = open("dataWin/y_fundo.txt","w")
fp_fundo.write(gen_line(y_fundo))
fp_fundo.close()
