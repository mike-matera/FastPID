#! /usr/bin/python3

import distutils.sysconfig 
from distutils.core import setup, Extension

# build the harness. 
ext = Extension('ArduinoPID',
                     sources = ['arduino_pid_reference.cpp', 'Arduino-PID-Library/PID_v1.cpp'],
                     include_dirs = ['Arduino-PID-Library/']
)

# install
setup (name = 'ArduinoPID',
       version = '1.0',
       description = 'Test harness for my a reference PID controller',
       ext_modules = [ext],
       script_args = ['install', '--install-platlib=./']
)

# test
import ArduinoPID
