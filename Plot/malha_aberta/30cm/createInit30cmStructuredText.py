#!/usr/bin/env python3

import os, os.path
import struct

from numpy import *
import matplotlib.pyplot as plt
import scipy.io as sio #read matlab files
from scipy import interpolate

"""dt de entrada e o desejado, nao o atual da entrada t"""
def getInterpolation(dt, tmax, t, x):
    tck = interpolate.splrep(t, x, s=0)
    tnew = arange(0, tmax, dt)
    xnew = interpolate.splev(tnew, tck, der=0)
    return xnew

def obterVelocidadeDeTopo(filename, T_MAX, DT):
    #--------------------- TOPO -----------------------
    topo = sio.loadmat(filename)
    t = topo['t'][0]
    p = abs(topo['Y'][0])
    dt = t[1] - t[0]
    n = t.size
    
    v = 1.0*arange(n)
    
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


    v_interpolated = getInterpolation(DT, T_MAX, t, vu)
    for i in range(0,v_interpolated.size):
        if abs(v_interpolated[i]) < 0.05:
            v_interpolated[i] = 0.0
    return v_interpolated

def obterPosicaoDeTopo(filename, T_MAX, DT):
    topo = sio.loadmat(filename)
    t = topo['t'][0]
    p = abs(topo['Y'][0])
    
    p_interpolated = getInterpolation(DT, T_MAX, t, p)
    for i in range(0,p_interpolated.size):
        if abs(p_interpolated[i]) < 0.001:
            p_interpolated[i] = 0.0
    return p_interpolated

def obterPosicaoDeFundo(filename, T_MAX, DT):
    topo = sio.loadmat(filename)
    t = topo['XData'][0]
    p = abs(topo['YData'][0])
    
    p_interpolated = getInterpolation(DT, T_MAX, t, p)
    for i in range(0,p_interpolated.size):
        if abs(p_interpolated[i]) < 0.001:
            p_interpolated[i] = 0.0
    return p_interpolated

def plotSpeedMMS(t, x):
    m_per_u = 0.07132083333
    plt.plot(t,x*1000*m_per_u)
    plt.xlabel('tempo - segundos')
    plt.ylabel('Velocidade - mm/s')
    plt.title('Velocidade Topo Malha Aberta - 30cm')
    plt.savefig('velocidade.png', dpi=300)
    plt.close()

def plotPositionMMTopo(t,x):
    plt.plot(t,x)
    plt.xlabel('tempo - segundos')
    plt.ylabel('Velocidade - mm/s')
    plt.title('Posição Topo Malha Aberta - 30cm')
    plt.savefig('posicaoTopo.png', dpi=300)
    plt.close()

def main():
    topo = sio.loadmat('topo.mat')
    fundo = sio.loadmat('fundo.mat')
    T_MAX = min(max(topo['t'][0]), max(fundo['XData'][0]))
    DT = 0.05
    
    t = arange(0, T_MAX, DT)
    position_topo = obterPosicaoDeTopo('topo.mat', T_MAX, DT)
    position_fundo = obterPosicaoDeFundo('fundo.mat', T_MAX, DT)
    speed_topo = obterVelocidadeDeTopo('topo.mat', T_MAX, DT)
    
    plotSpeedMMS(t, speed_topo)
    plotPositionMMTopo(t, position_topo)

    n = position_fundo.size
    createInit(DT, n, position_topo, position_fundo, speed_topo)


def createInit(dt, n, position_topo, position_fundo, speed_topo):
    #Criar structured text para inicialização
    f = open('init.st', 'w')
    f.write('/* Universidade de Brasilia\n')
    f.write('Trabalho de Graduacao em Engenharia Mecatronica\n')
    f.write('Alunos: \n')
    f.write('Ataias Pereira Reis 10/0093817\n')
    f.write('Emanuel Pereira Barroso Neto 11/0115716\n')
    f.write('This code must be executed only once. */\n\n')
    f.write('MSO(drive_axis,MSO_1);\n\n')
    f.write('/*Passo de tempo em segundos*/\n')
    f.write('dt := ' + str(dt) + ';\n\n')
    
    f.write('/*Velocidade esta em unidades/s*/\n')
    for i in range(0,n):
        f.write('speed[' + str(i) + '] := ' + str(speed_topo[i]) + ';\n')
    f.write('\n')

    f.write('/*Posicao esta em mm*/\n')
    for i in range(0,n):
        f.write('position_topo[' + str(i) + '] := ' + str(position_topo[i]) + ';\n')
    f.write('\n')

    for i in range(0,n):
        f.write('position_fundo[' + str(i) + '] := ' + str(position_fundo[i]) + ';\n')
    f.write('\n')

    f.write('\ndataInitialized := 1;\n')
    f.close()

if __name__ == '__main__':
    main()
