#! /usr/bin/python3

import subprocess 
import matplotlib.pyplot as plt
import numpy 

import distutils.sysconfig 
from distutils.core import setup, Extension

# build the harness. 
harn_ext = Extension('harness',
                     sources = ['harness.cpp', '../PID_INT64.cpp'],
                     include_dirs = ['../']
)

# install
setup (name = 'Harness',
       version = '1.0',
       description = 'Test harness for my PID controller',
       ext_modules = [harn_ext],
       script_args = ['install', '--install-platlib=./']
)
import harness

def main() :
    p = 0.01
    i = 0.0001
    d = 0.001
    db = 0.01

    sp = 100
    steps = 2000

    if not harness.configure(p, i, d, db, 16, True) :
        print ("There was a configuration error.")
        exit(-1)

    out = 0;
    data = numpy.array([])
    for step in range(0, steps) :
        data = numpy.append(data, [sp, out])
        out = harness.step(sp, out)

    plt.plot(data[0:-1:2], '', data[1:-1:2], '')            
    plt.show()
 
if __name__ == "__main__" : 
    main()
