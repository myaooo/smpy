#!/usr/bin/env python
# encoding: utf-8

"""
@software: smpy
@author: Ming
@license: MIT Licence 
@contact: mingy.aser@gmail.com
@file: model_parser.py
@created at: 16/4/20
"""

import yaml
import re
from . import model_base
from .model_base import *
from . import model_material as mat
from .utils import *


def load_from_yaml(filename):
    """

    :param filename: str
    :return: r_model
    :rtype: ModelBase
    """
    file = open(filename,'r')
    raw_hash = yaml.load(file.read())
    model_hash = raw_hash['model']
    model_dim = model_hash['dim']
    model_type = model_hash['type']
    materials_raw = model_hash['material']
    joints_raw = model_hash['joint']
    elements_raw = model_hash['element']
    supports_raw = model_hash['support']

    # creating model
    r_model = create_model(model_dim, model_type)

    # parsing materials
    materials = {}
    for id, parms in materials_raw:
        if (not parms.has_key('type')) or (parms['type']=='linear'):
            material = mat.LinearMaterial(parms=parms)
            materials[id] = material
        elif parms['type']=='nonlinear':
            material = mat.NonlinearMaterial(parms)
            materials[id] = material
        else:
            print_err('unknown material type!')
    r_model.materials = materials

    # parsing joints
    joints = {}
    for id, pos_raw in joints_raw:
        pos_str = pos_raw.split(',')
        pos = list(map(float,pos_str))
        joints[id] = pos
    r_model.joints = joints

    # parsing elements
    elements = []
    for pos_raw, parms in elements_raw:
        pos_str = pos_raw.split(',')
        pos = tuple(map(int, pos_str))
        constraints_str = parms['C'].split(',')
        constraints = list(map(int, constraints_str))
        material_idx = parms['M']
        elem = Element(pos,constraints,material_idx)
        elements.append(elem)
    r_model.elements=elements

    # parsing supports
    supports = []
    for id, parms in supports_raw:
        constraints_str = parms['C'].split(',')
        constraints = list(map(int, constraints_str))
        settlements_str = parms['S'].split(',')
        settlements = list(map(float, settlements_str))
        support = Support(id, constraints, settlements)
        supports.append(support)
    r_model.supports = supports

    return r_model


if __name__ == '__main__':
    print('testing..')
    model = load_from_yaml('resource/example.yaml')