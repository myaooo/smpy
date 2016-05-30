#!/usr/bin/env python
# encoding: utf-8

"""
@author: Ming
@license: MIT Licence 
@contact: mingy.aser@gmail.com
@file: model_base.py
@created at: 16/4/20
"""

import numpy as np
from . import model_material as mat
from enum import Enum
from . import utils


class ModelType(Enum):
    NORMAL = 1
    DYNAMIC = 2


class Joint():
    def __init__(self, u, glb_code):
        self.u = u
        self.glb_code = glb_code

class Element():
    def _cal_k_e_l(self):
        """

        :rtype: np.array
        """
        EA = self.material.get_EA()
        EI = self.material.get_EI()
        l = self.l
        a1 = EA / l
        i0 = 2 * EI / l
        i1 = 2 * i0
        i2 = 3 * i0 / l
        i3 = 2 * i2 / l
        k_raw = []
        k_raw.append([a1, 0, 0, -a1, 0, 0])
        k_raw.append([0, i3, i2, 0, -i3, i2])
        k_raw.append([0, i2, i1, 0, -i2, i0])
        k_raw.append([-a1, 0, 0, a1, 0, 0])
        k_raw.append([0, -i3, -i2, 0, i3, -i2])
        k_raw.append([0, i2, i0, 0, -i2, i1])
        k_e = np.array(k_raw)
        return k_e

    def _cal_T(self):
        ca = self.cos_a
        sa = self.sin_a
        t_raw = []
        t_raw.append([ca, sa, 0, 0, 0, 0])
        t_raw.append([-sa, ca, 0, 0, 0, 0])
        t_raw.append([0, 0, 1, 0, 0, 0])
        t_raw.append([0, 0, 0, ca, sa, 0])
        t_raw.append([0, 0, 0, -sa, ca, 0])
        t_raw.append([0, 0, 0, 0, 0, 1])
        t = np.array(t_raw)
        return t


    def __init__(self, joints, material, glb_code=None):
        self.joints = joints
        self.constraints = []
        # c_length = len(constraints)
        # self.constraints.append(constraints[0:int(c_length / 2)])
        # self.constraints.append(constraints[int(c_length / 2):c_length])
        self.material = material
        du = []
        dim = len(joints[0].u)
        sigma_u2 = 0
        for i in range(dim):
            du.append(joints[0].u[i] - joints[1].u[i])
            sigma_u2 += du[-1]**2
        l = self.l = sigma_u2 ** 0.5
        self.cos_a = du[0] / l
        self.sin_a = du[1] / l
        T = self.T = self._cal_T()
        k_e_l = self.k_e_l = self._cal_k_e_l()
        self.k_e_g = (T.transpose().dot(k_e_l)).dot(T)
        self.glb_code = glb_code


class JointLoad():
    def __init__(self, func = lambda t: 0):
        self.func = func

    def get_load(self, t):
        return self.func(t)


class ModelBase():

    def _integrate_K(self):
        n = self.dof
        K = np.zeros((n,n))
        for elem in self.elements:
            k_e_g = elem.k_e_g
            glb_code = elem.glb_code
            for i, code_i in enumerate(glb_code):
                if code_i == 0:
                    continue
                for j, code_j in enumerate(glb_code):
                    if code_j == 0:
                        continue
                    K[code_i-1, code_j-1] += k_e_g[i,j]
        return K

    def __init__(self, dim=2, joints = None, elements = None, materials = None, P = None, dof = 0):
        self.dim = dim
        self.joints = joints if isinstance(joints, dict) else {}
        self.elements = elements if isinstance(elements, list) else []
        self.materials = materials if isinstance(materials, dict) else {}
        self.P = P if isinstance(P, dict) else {}
        self.dof = dof
        self.K = self._integrate_K() if (bool(self.joints) and bool(self.elements) and bool(self.materials)) else None

    def model_type(self):
        return None

    def get_element(self, i):
        return self.elements[i-1]

    def get_joint(self, i):
        return self.joints[i]

    def get_K(self, u=0):
        """

        :rtype: np.array
        """
        return self.K

    def get_P(self, t=0):
        """

        :rtype: np.array
        """
        r_P = np.zeros(self.dof)
        for key, load in self.P.items():
            r_P[key-1] = load.get_load(t)

        return r_P


    def get_M(self):
        """

        :rtype: np.array
        """
        pass

    def get_C(self):
        """

        :rtype: np.array
        """
        pass

    def get_u_0(self):
        """

        :rtype: np.array
        """
        pass


class Model2N(ModelBase):
    def __init__(self, joints = None, elements = None, materials = None, P = None, dof = 0):
        super(Model2N, self).__init__(2, joints, elements, materials, P, dof)

    def model_type(self):
        return ModelType.NORMAL


class Model2D(ModelBase):
    def __init__(self, joints = None, elements = None, materials = None, P = None, dof = 0):
        super(Model2D, self).__init__(2, joints, elements, materials, P, dof)
        self.u_0 = ([],[],[])
        self.mass = None
        self.C = None

    def model_type(self):
        return ModelType.DYNAMIC

    def get_M(self):
        M_diag = np.zeros(self.dof)
        for key, value in self.mass.items():
            joint_dof = self.joints[key].glb_code
            for i in joint_dof:
                if i != 0:
                    M_diag[i-1] = value
        return np.diag(M_diag)

    def get_C(self):
        return self.C

    def get_u_0(self):
        return self.u_0


# TODO: Add 3D model class


def create_model(dim, type, joints = None, elements = None, materials = None, P = None, dof = 0):
    if dim == 2:
        if type == 'normal':
            return Model2N(joints, elements, materials, P, dof)
        if type == 'dynamic':
            return Model2D(joints, elements, materials, P, dof)
        else:
            utils.print_err('Unkown model type!')
    else:
        utils.print_err('Unable to create 3D model!')


if __name__ == '__main__':
    pass
