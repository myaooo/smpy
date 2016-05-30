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
from core.basic.model_base import *
from core.basic import model_material as mat
from core.basic.utils import *
from math import *


def parse_load(P_raw, n):
    assert isinstance(P_raw,dict)
    P = {}
    for key, value in P_raw.items():
        lamb_string = 'lambda t:' + str(value)
        P[key] = JointLoad(func = eval(lamb_string))
    return P

def parse_u_0(initial_status):
    assert isinstance(initial_status, dict)
    u_0 = {}
    for key, value in initial_status.items():
        if isfloat(value):
            u_0[key] = [value]
        else:
            u_str = value.split(',')
            u_0[key]=list(map(float, u_str))
    return (u_0['u'], u_0['v'], u_0['a'])


def parse_C(damp_raw):
    return np.zeros(1)
# TODO: fix this


def load_from_sm(filename):
    """

    :param filename: str
    :return: r_model
    :rtype: ModelBase
    """
    file = open(filename,'r')
    raw_hash = yaml.load(file.read())
    model_hash = raw_hash['model']
    model_dim = model_hash['dim']
    degree_per_joint = 3 * (model_dim-1) # 2 -> 3, 3 -> 6
    model_type = model_hash['type']
    materials_raw = model_hash['material']
    joints_raw = model_hash['joint']
    elements_raw = model_hash['element']
    P_raw = model_hash['load']


    # parsing materials
    materials = {}
    for id, parms in materials_raw.items():
        if (not 'type' in parms) or (parms['type']=='linear'):
            material = mat.LinearMaterial(parms=parms)
            materials[id] = material
        elif parms['type']=='nonlinear':
            material = mat.NonlinearMaterial(parms)
            materials[id] = material
        else:
            print_err('unknown material type!')

    # parsing joints
    joints = {}
    for id, pos_raw in joints_raw.items():
        pos_str = pos_raw.split(',')
        pos = list(map(float,pos_str))
        glb_code = list(map(int,pos[model_dim:(model_dim+degree_per_joint)]))
        joints[id] = Joint(pos[0:model_dim], glb_code)

    # parsing elements
    dof = 0
    elements = []
    for pos_raw, material_idx in elements_raw.items():
        pos_str = pos_raw.split(',')
        pos = tuple(map(int, pos_str))
        if not (pos[0] in joints and pos[1] in joints):
            print_err('element position undefined!')
        joint_1 = joints[pos[0]]
        joint_2 = joints[pos[1]]
        joint_pos = (joint_1, joint_2)

        glb_code = joint_1.glb_code + joint_2.glb_code
        print(glb_code)
        max_code = max(glb_code)
        dof = max(max_code, dof)
        elem = Element(joint_pos,materials[material_idx], glb_code)
        elements.append(elem)

    print_debug(dof)
    P = parse_load(P_raw, dof)

    # creating model
    r_model = create_model(model_dim, model_type, joints, elements, materials, P, dof)

    # specific for dynamic models
    if model_type == 'dynamic':
        # parsing mass
        mass = model_hash['joint_mass']
        r_model.mass = mass

        # parsing initial status
        initial_status = model_hash['initial_status']
        u_0 = parse_u_0(initial_status)
        r_model.u_0 = u_0

        # parsing damping matrix
        damp = np.zeros((dof,dof))
        if 'damp' in model_hash:
            damp_raw = model_hash['damp']
            damp = parse_C(damp_raw)
        r_model.C = damp


    return r_model

if __name__ == '__main__':
    print('testing..')
    model = load_from_sm('../../resource/dyn_exmp.sm')

    print(model.get_M())
    print(model.get_K())