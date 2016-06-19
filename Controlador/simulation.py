import numpy
import scipy.io as sio
from Model import Model
import matplotlib.pyplot as plt
from PlantOrig import PlantOrig
import time

if __name__ == "__main__":
    Kp = numpy.matrix([0.009929565527738, 0.011408478187796, -0.005109513121618, -0.001992502922351])
    Ki = 0.210261852863830

    # Kalman Matrices
    n = 4
    Ak = numpy.matrix([[0.993175847266250, 0.0997676389875316, 0.00447446153612418, 0.000154491807255262],
                       [-0.266442692060039, 0.989506934720158, 0.0794137333776907, 0.00441443534842949],
                       [-7.61331011046535, -0.371277877313592, 0.407916221277208, 0.0776985503560236],
                       [-134.001998512554, -9.45851595845769, -10.6078657460473, 0.377727256243161]])

    Bk = numpy.matrix([0.674742463375352, 3.50238796155364, -32.6963528822316, -364.795682866366]).transpose()
    Ck = numpy.matrix([1.0, 0.0, 0.0, 0.0])
    Q = 0.01 ** 2 * numpy.eye(4)
    R = 0.1 ** 2

    epsilon = 0.3
    Ts = 0.1

    A = numpy.matrix([[0.9191, -0.3712, 0, 0], [0.3712, 0.9191, 0, 0], [0, 0, 0.4651, -0.8733], [0, 0, 0.8733, 0.4651]])
    B = numpy.matrix([6.5818, 31.2517, -98.5991, -75.6695]).transpose()
    C = numpy.matrix([-0.000339110145869, 0.014769867793814, 0.000052840348719, -0.002915328311939])
    D = -0.068495332192496

    y_fundo = (sio.loadmat('data/y_fundo_30cm.mat'))['y_fundo'][0]
    y_topo = (sio.loadmat('data/y_topo_30cm.mat'))['y_topo'][0]
    # n_t = y_topo.size
    n_t = 70
    t = numpy.array(range(0, n_t)) * Ts
    y_out = numpy.zeros(n_t)
    y_out_open_loop = numpy.zeros(n_t)

    # instantiate the plant that will be used, it should be a subclass of Plant
    plant = PlantOrig()
    model = Model(n, A, B, C, D, Ak, Bk, Ck, Q, R, Kp, Ki, epsilon, Ts, plant)

    start = time.clock()
    for k in range(n_t):
        y_out[k] = model.closed_loop(y_topo[k], y_fundo[k])
        y_out_open_loop[k] = plant.compute_y(y_topo[k])

    print("Total simulation time: {}s".format(time.clock() - start))
    plt.plot(t, y_out[0:n_t], label='out')
    plt.plot(t, y_fundo[0:n_t], label='ref_out')
    plt.plot(t, y_topo[0:n_t], label='ref_in')
    plt.plot(t, y_out_open_loop[0:n_t], label='out open loop')
    plt.legend()
    plt.xlabel('time (s)')
    plt.ylabel('position (m)')
    plt.title('Position of cart')
    plt.grid(True)
    plt.show()
