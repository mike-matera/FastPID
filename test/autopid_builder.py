#! /usr/bin/python3

import distutils.sysconfig 
from distutils.core import setup, Extension

# build the harness. 
ext = Extension('AutoPID',
                     sources = ['autopid_wrapper.cpp', 'autopid_lib/AutoPID.cpp'],
                     include_dirs = ['AutoPID/']
)

# install
setup (name = 'AutoPID',
       version = '1.0',
       description = 'Test harness for my a reference PID controller',
       ext_modules = [ext],
       script_args = ['install', '--install-platlib=./']
)

# test
import AutoPID
