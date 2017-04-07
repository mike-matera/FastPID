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
    p = 0
    i = 1
    d = 1
    db = 0

    steps = 100
    sp = numpy.zeros(steps, dtype=int)
    sp[1] = 1

    if not harness.configure(p, i, d, db, 16, True) :
        print ("There was a configuration error.")
        exit(-1)

    out = 0;
    data = numpy.array([])
    for step in range(0, steps) :
        sp_num = sp[step]
        data = numpy.append(data, [sp_num, out])
        out = harness.step(sp_num, out)

    plt.plot(data[0:-1:2], '', data[1:-1:2], '')            
    plt.show()
 
if __name__ == "__main__" : 
    main()
