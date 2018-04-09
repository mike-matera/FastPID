#! /usr/bin/python3

import numpy 
import scipy 
import matplotlib.pyplot as plt
import random 
import datetime 
import os 
import sys
import time 
import math

import FastPID
import ArduinoPID
import AutoPID

import testrun
    
def randomtest(seed, turns, plot, pid) :
    results = numpy.array([])
    results.resize((turns,))

    for test_num in range (turns) : 
        test = testrun.testrun(100, pid)
        test.random()
        err = test.run()
        if plot and err > 200 :
            print ('OUTLIER: (chi^2 == {}) '.format(err), end='')
            test.save()
        results[test_num,] = err

    best = numpy.amin(results)
    worst = numpy.amax(results)
    avg = numpy.average(results)
    std = numpy.std(results)
    
    print ("Best: {} Worst: {} Avg: {} Std. Dev: {}".format(best,worst,avg,std))

    rmax = math.log(results.max())
    if rmax < 11 :
        rmax  = 11
    lbins = numpy.logspace(0, rmax, 50, base=2)
    plt.hist(results, bins=lbins)
    plt.show()


def main() :
    if len(sys.argv) == 1 :
        print ('''usage: 
Run a single test with given coefficients:
  {0} <Type> <p> <i> <d> <mag_bits> <stepcount>

Run a number of random tests with the specified random seed: 
  {0} <Type> <seed> <testcount>

Run 100,000 random tests:
  {0} <Type> 

** Type is "FastPID" or "ArduinoPID" or "AutoPID"
'''.format(sys.argv[0]))
        exit(-1)
    
    pid = FastPID
    if sys.argv[1] == 'ArduinoPID' :
      pid = ArduinoPID
    if sys.argv[1] == 'AutoPID' :
      pid = AutoPID
      
    if len(sys.argv) == 6 :
        p = float(sys.argv[2])
        i = float(sys.argv[3])
        d = float(sys.argv[4])
        steps = int(sys.argv[5])
        print ("Running p={} i={} d={} steps={}".format(p, i, d, steps))
        test = testrun.testrun(steps, pid)
        test.configure(p, i, d)
        test.run()
        test.show()

    elif len(sys.argv) == 4 : 
        seed = int(sys.argv[2])
        turns = int(sys.argv[3])
        random.seed(seed)
        print ("Random seed:", seed)
        print ("Number of turns:", turns)
        randomtest(seed, turns, True, pid)

    else:
        seed = int(time.time())
        turns = 100000
        random.seed(seed)
        print ("Random seed:", seed)
        print ("Number of turns:", turns)
        randomtest(seed, turns, False, pid)

    
    
if __name__ == '__main__' :
    main()
    
