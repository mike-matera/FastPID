#! /usr/bin/python3

import distutils.sysconfig 
from distutils.core import setup, Extension

# build the harness. 
ext = Extension('PID_INT64',
                     sources = ['wrapper.cpp', '../PID_INT64.cpp'],
                     include_dirs = ['../']
)

# install
setup (name = 'PID_INT64',
       version = '1.0',
       description = 'Test harness for my PID controller',
       ext_modules = [ext],
       script_args = ['install', '--install-platlib=./']
)

# test
import PID_INT64
