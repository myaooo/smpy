#!/usr/bin/env python
# encoding: utf-8

"""
@software: smpy
@author: Ming
@license: MIT Licence 
@contact: mingy.aser@gmail.com
@file: model_material.py
@created at: 16/4/21
"""


def func():
    pass

class MaterialBase():
    "Material Base Class"
    def __init__(self):
        pass

    def get_EA(self, u = 0):
        return 0

    def get_EI(self, u = 0):
        return 0

    def get_m(self):
        return 0

class LinearMaterial(MaterialBase):
    "Linear Material."
    def __init__(self, EA=0, EI=0, m=0, parms=None):
        super().__init__()
        if isinstance(parms, dict):
            self.EA = parms['EA']
            self.EI = parms['EI']
            self.m = parms['m']
        else:
            self.EA = EA
            self.EI = EI
            self.m = m

    def get_EA(self, u = 0):
        return self.EA

    def get_EI(self, u = 0):
        return self.EI

    def get_m(self):
        return self.m

class NonlinearMaterial(MaterialBase):
    def __init__(self, parms=None):
        super(NonlinearMaterial, self).__init__()


if __name__ == '__main__':
    pass