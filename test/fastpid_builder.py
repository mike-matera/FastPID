#! /usr/bin/python3

import distutils.sysconfig 
from distutils.core import setup, Extension

# build the harness. 
ext = Extension('FastPID',
                     sources = ['fastpid_wrapper.cpp', '../src/FastPID.cpp'],
                     include_dirs = ['../src/']
)

# install
setup (name = 'FastPID',
       version = '1.0',
       description = 'Test harness for my PID controller',
       ext_modules = [ext],
       script_args = ['install', '--install-platlib=./']
)

# test
import FastPID
