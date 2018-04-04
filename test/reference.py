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

import testrun
    
if __name__ == '__main__' :
    if len(sys.argv) == 1 :
        print ('''usage: 
Run a single test with given coefficients:
  {0} <Type> <p> <i> <d> <deadband> <mag_bits> <stepcount>

Run a number of random tests with the specified random seed: 
  {0} <Type> <seed> <testcount>

Run 100,000 random tests:
  {0} <Type> 

** Type is "FastPID" or "ArduinoPID" 
'''.format(sys.argv[0]))
        exit(-1)
    
    pid = FastPID
    if sys.argv[1] == 'ArduinoPID' :
      pid = ArduinoPID
      
    if len(sys.argv) == 8 :
        p = float(sys.argv[2])
        i = float(sys.argv[3])
        d = float(sys.argv[4])
        db = int(sys.argv[5])
        mag = int(sys.argv[6])
        steps = int(sys.argv[7])
        print ("Running p={} i={} d={} db={} mag={} steps={}".format(p, i, d, db, mag, steps))
        test = testrun.testrun(steps, pid)
        test.configure(p, i, d, db, mag)
        test.run()
        test.show()

    elif len(sys.argv) == 4 : 
        seed = int(sys.argv[2])
        turns = int(sys.argv[3])
        random.seed(seed)
        print ("Random seed:", seed)
        print ("Number of turns:", turns)
        testrun.randomtest(seed, turns, True, pid)

    else:
        seed = int(time.time())
        turns = 100000
        random.seed(seed)
        print ("Random seed:", seed)
        print ("Number of turns:", turns)
        testrun.randomtest(seed, turns, False, pid)
