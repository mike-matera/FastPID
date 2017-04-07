#! /usr/bin/python3

import subprocess 
import matplotlib.pyplot as plt
import numpy 

import PID_INT64 as pid

def impulse() :
    return numpy.array([0,1,0])

def run(sp) : 
    out = 0
    data = numpy.array([], dtype=int)
    for point in sp : 
        data = numpy.append(data, out)
        out = pid.step(point, out)

    return data

def main() :
    p = 0.5
    i = 0
    d = 0
    db = 0.1

    steps = 100
    sp = impulse() * 1000
    sp.resize((steps,)) 

    if not pid.configure(p, i, d, db, 16, True) :
        print ("There was a configuration error.")
        exit(-1)

    out = run(sp)
    print (out)

    if numpy.array_equal(sp, out) : 
        print ("Pass!")
    else:
        print ("Fail!")

    plt.plot(sp, '', out, '')            
    plt.show()
 
if __name__ == "__main__" : 
    main()
