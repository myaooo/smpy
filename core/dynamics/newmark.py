#!/usr/bin/env python
# encoding: utf-8

"""
@software: smpy
@author: Ming
@license: MIT Licence 
@contact: mingy.aser@gmail.com
@file: newmark.py
@created at: 16/5/27
"""

from ..basic import model_base as mb
from ..basic import model_material as material
import numpy as np


class DynamicSimulatorBase():
    def __init__(self):
        pass


class Newmark(DynamicSimulatorBase):
    def __init__(self, model=0, dh=0.01, T=1, beta=1 / 4, gamma=1 / 2):
        super().__init__()
        if not isinstance(model, mb.ModelBase):
            self.model = mb.ModelBase()
        self.beta = beta
        self.gamma = gamma
        self.dh = dh
        self.T = T
        self.u = []
        self.v = []
        self.a = []
        self.current_t = 0

    def set_model(self, model):
        """

        :type model: model.ModelBase
        """
        self.model = model

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
        self.u.append(u)
        self.v.append(v)
        self.a.append(a)

    def _cal_next_step(self):
        u = self.u[-1]
        v = self.v[-1]
        a = self.a[-1]

        K = self.model.get_K(u)
        M = self.model.get_M()
        C = self.model.get_C()
        P = self.model.get_K(self.current_t)

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
        v_new = u + _a[6] * a + _a[7] * a_new

        # store the next step
        self.u.append(u_new)
        self.v.append(v_new)
        self.a.append(a_new)

    def simulate(self):
        """"""
        self._pre_calculations()
        while self.current_t < self.T:
            # calculate the next time step
            self._cal_next_step()
            # increase current time by dh
            self.current_t += self.dh


class NewmarkAdapt(Newmark):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    pass
