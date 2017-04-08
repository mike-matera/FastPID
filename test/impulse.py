#! /usr/bin/python3

import subprocess 
import matplotlib.pyplot as plt
import numpy 
import random 
import pytest 

random.seed(0)
turns = 10 

import PID_INT64 as pid

def impulse(steps) :
    ar = numpy.array([0,1,0])
    ar.resize((steps,))
    return ar

def run(sp) : 
    out = 0
    data = numpy.array([], dtype=int)
    for point in sp : 
        data = numpy.append(data, out)
        out = pid.step(point, out)

    return data

def test_overunity() : 
    for t in range(turns) : 
        steps = int(random.uniform(4, 16383))
        p = random.uniform(1,2)
        sp = impulse(steps)
        sp = sp * steps
        pid.configure(p, 0, 0, 0, 16, True)
        resp = run(sp)
        mmax = numpy.amax(resp)
        #plt.plot(sp, '', resp, '')            
        #plt.show()
        assert abs(mmax - p * steps) <= (steps / 100), "Peak is not within 1% of the setpoint"
        assert abs(resp[2] - p * steps) <= (steps / 100), "Peak is not in resp[2]"
        #assert resp[steps-1] == 0, "The system did not converge after {} steps".format(steps)
        
def test_underunity() : 
    for t in range(turns) :
        steps = int(random.uniform(4, 32767))
        p = random.uniform(0,1)
        sp = impulse(steps)
        sp = sp * steps
        pid.configure(p, 0, 0, 0, 16, True)
        resp = run(sp)
        mmax = numpy.amax(resp)
        assert abs(mmax - p * steps) <= (steps / 100), "Peak is not within 1% of the setpoint"
        assert abs(resp[2] - p * steps) <= (steps / 100), "Peak is not in resp[2]"
        assert resp[steps-1] == 0, "The system did not converge after {} steps".format(steps)

#def main() :
#    test_underunity()
#
#    plt.plot(sp, '', out, '')            
#    plt.show()
# 
#if __name__ == "__main__" : 
#    main()
