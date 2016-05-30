#!/usr/bin/env python
# encoding: utf-8

"""
@software: smpy
@author: Ming
@license: MIT Licence 
@contact: mingy.aser@gmail.com
@file: plotlib.py
@created at: 16/5/29
"""

import matplotlib.pyplot as plt
from core.dynamics.simulator import *


def plot_u(simulat, i, attr):
    assert isinstance(simulat, DynamicSimulatorBase)
    assert hasattr(simulat, attr)
    plt.plot(simulat.t, getattr(simulat,attr)[:,i])
    plt.show()


if __name__ == '__main__':
    from core.basic.model_parser import load_from_sm
    from math import *

    print('testing..')
    model = load_from_sm('../../resource/dyn_exmp2.sm')

    print(model.get_M())
    print(model.get_K())
    simulator = Newmark(model, 0.05, 10, 1 / 4, 1 / 2)
    simulator.simulate()
    length = len(simulator.t)
    print(length)
    # print(len(simulator.u[:,0]))

    theta = 2
    w = (12 / 1)**0.5
    y_st = 1 / w**2
    alpha = theta / w
    real_func = lambda t: y_st / (1 - alpha**2) * (sin(theta*t) - alpha * sin(w*t))
    y_real = np.zeros(length)
    for i in range(length):
        y_real[i] = real_func(simulator.t[i])

    plt.plot(simulator.t, y_real)
    plot_u(simulator, 0, 'u')

