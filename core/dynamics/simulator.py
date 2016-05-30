#!/usr/bin/env python
# encoding: utf-8

"""
@software: smpy
@author: Ming
@license: MIT Licence 
@contact: mingy.aser@gmail.com
@file: simulator.py
@created at: 16/5/27
"""

from core.basic import model_base as mb
import numpy as np


class DynamicSimulatorBase():
    def __init__(self, model=None, dh=0.01, T=1):
        self.model = model if isinstance(model, mb.ModelBase) else mb.ModelBase()
        self.dh = dh
        self.T = T
        self.u = np.array(0)
        self.v = np.array(0)
        self.a = np.array(0)
        self.t = []

    def _pre_calculations(self):
        pass

    def _cal_next_step(self, current_t = 0):
        pass

    def _get_next_dh(self):
        return self.dh

    def simulate(self):
        """"""
        self._pre_calculations()
        current_t = 0
        self.t.append(current_t)
        while current_t < self.T:
            # calculate the next time step
            u, v, a = self._cal_next_step(current_t)
            # store the next step
            self.u = np.vstack((self.u, u))
            self.v = np.vstack((self.v, v))
            self.a = np.vstack((self.a, a))
            # increase current time by dh
            current_t += self._get_next_dh()
            self.t.append(current_t)


class Newmark(DynamicSimulatorBase):
    def __init__(self, model=None, dh=0.01, T=1, beta=1 / 4, gamma=1 / 2):
        super().__init__(model, dh, T)
        self.beta = beta
        self.gamma = gamma

    def set_parms(self, beta, gamma):
        """

        :type beta: float
        :type gamma: float
        """
        self.beta = beta
        self.gamma = gamma

    def _pre_calculations(self):

        # calculate the _a parms
        beta = self.beta
        dh = self.dh
        gamma = self.gamma
        _a = []
        _a.append(1 / (beta * dh ** 2))
        _a.append(gamma / (beta * dh))
        _a.append(1 / (beta * dh))
        _a.append(0.5 / beta - 1)
        _a.append(gamma / beta - 1)
        _a.append(0.5 * dh * (gamma / beta - 2))
        _a.append(dh * (1 - gamma))
        _a.append(gamma * dh)
        self._a = _a

        # get the initial settlements
        u, v, a = self.model.get_u_0()
        self.u = np.array(u)
        self.v = np.array(v)
        self.a = np.array(a)

    def _cal_next_step(self, current_t = 0):
        u = self.u[-1]
        v = self.v[-1]
        a = self.a[-1]

        K = self.model.get_K(u)
        M = self.model.get_M()
        C = self.model.get_C()
        P = self.model.get_P(current_t)

        _a = self._a
        # equivalent K
        K_h = K + _a[0] * M + _a[1] * C

        # equivalent P
        _P_1 = M.dot(_a[0] * u + _a[2] * v + _a[3] * a)
        _P_2 = C.dot(_a[1] * u + _a[4] * v + _a[5] * a)
        P_h = P + _P_1 + _P_2

        # calculate the next step
        u_new = np.linalg.solve(K_h, P_h)
        a_new = _a[0] * (u_new - u) - _a[2] * v - _a[3] * a
        v_new = v + _a[6] * a + _a[7] * a_new

        return u_new, v_new, a_new



class NewmarkAdapt(Newmark):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    from core.basic.model_parser import load_from_sm
    print('testing..')
    model = load_from_sm('../../resource/dyn_exmp2.sm')

    print(model.get_M())
    print(model.get_K())
    simulator = Newmark(model,0.08,1,1/6,1/2)
    simulator.simulate()
    print(simulator.u)
    print(simulator.v)
    print(simulator.a)


