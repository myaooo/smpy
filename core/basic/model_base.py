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
    def __init__(self, x, y, z=None):
        self.x = x
        self.y = y
        self.z = z


class Element():
    def __init__(self, joints, constraints, material_idx):
        self.joints = joints
        self.constraints = []
        c_length = len(constraints)
        self.constraints[0] = constraints[0:c_length/2]
        self.constraints[1] = constraints[c_length/2,c_length]
        self.material_idx = material_idx


class Support():
    def __init__(self, joint, constraints, settlements):
        self.joint = joint
        self.constraints = constraints
        self.settlements = settlements


class ModelBase():
    def __init__(self, dim=2):
        self.dim=dim
        self.joints=[]
        self.elements=[]
        self.materials=[]
        self.supports=[]
        pass

    def model_type(self):
        return None

    def get_element(self):
        pass

    def get_joint(self):
        pass

    def get_K(self, u=0):
        """

        :rtype: np.array
        """
        pass

    def get_P(self, t=0):
        """

        :rtype: np.array
        """
        pass

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
    def __init__(self):
        super(Model2N, self).__init__()

    def model_type(self):
        return ModelType.NORMAL


class Model2D(ModelBase):
    def __init__(self):
        super(Model2D, self).__init__()

    def model_type(self):
        return ModelType.DYNAMIC

# TODO: Add 3D model class


def create_model(dim, type):
    if dim==2:
        if type=='normal':
            return Model2N()
        if type=='dynamic':
            return Model2D()
    else:
        utils.print_err('Unable to create 3D model!')


if __name__ == '__main__':
    pass
