#!/usr/bin/env python
# encoding: utf-8

"""
@software: smpy
@author: Ming
@license: MIT Licence 
@contact: mingy.aser@gmail.com
@file: utils.py
@created at: 16/5/28
"""
DEBUG = True

def print_err(string):
    print('Error:',string)

def print_debug(string):
    if DEBUG == True:
        print(string)

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    print(isfloat('2d2'))