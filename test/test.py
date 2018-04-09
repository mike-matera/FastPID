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
import argparse
import matplotlib.pyplot as plt

import FastPID
import ArduinoPID
import AutoPID

import refpid
import process

def randomtest(seed, steps, turns, pid) :
    results = numpy.array([])
    results.resize((turns,))

    for test_num in range (turns) : 
        kp = round(random.uniform(0, 1), 3)
        ki = round(random.uniform(0, kp), 3)
        kd = round(random.uniform(0, ki), 3)
        bits = 16
        sign = False
        pid.configure(kp, ki, kd, bits, sign)
        reference = refpid.refpid(kp, ki, kd, bits, sign)
        ref = process.Process(reference, steps, turns)
        dut = process.Process(pid, steps, turns)
        ref.run()
        dut.run()

        # Check for fit
        errf = numpy.square(numpy.subtract(ref.output, dut.output))
        err = numpy.cumsum(errf) / numpy.arange(1, ref.output.size+1, dtype=float)
        chi2 = numpy.sum(errf) / ref.output.size

        results[test_num,] = chi2

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
    parser = argparse.ArgumentParser(description="Run PID tests")
    parser.add_argument('test', help='The test to execute.', choices=['reference', 'random', 'load'])
    parser.add_argument('-p', help='Kp', type=float, default=1)
    parser.add_argument('-i', help='Ki', type=float, default=0)
    parser.add_argument('-d', help='Kd', type=float, default=0)
    parser.add_argument('-n', help='Number of steps to simulate.', type=int, default=100)
    parser.add_argument('-t', help='Number of random turns to test.', type=int, default=100)
    parser.add_argument('--obits', help='Number of output bits.', type=int, default=16)
    parser.add_argument('--osign', help='Signedness of the output.', type=bool, default=False)
    parser.add_argument('--pid', help='PID implementation to use.', choices=['FastPID', 'ArduinoPID', 'AutoPID'], default='FastPID')
    parser.add_argument('--seed', help='Random seed to use.', default=int(time.time()))
    
    args = parser.parse_args()

    if args.pid == 'FastPID' :
        pid = FastPID
    elif args.pid == 'ArduinoPID' :
        pid = ArduinoPID
    else:
        pid = AutoPID        

    if not pid.configure(args.p, args.i, args.d, args.obits, args.osign) :
        print ('Error configuring the PID.')
        exit(-1)
    
    if args.test == 'reference' :
        # Test the PID against the reference implementation.
        reference = refpid.refpid(args.p, args.i, args.d, args.obits, args.osign)
        ref = process.Process(reference, 100, args.n)
        dut = process.Process(pid, 100, args.n)
        ref.run()
        dut.run()
        plt.plot(ref.setpoint, '', ref.output, '--', dut.output, '')
        plt.show()

    if args.test == 'random' :
        # Test random parameters vs. the reference implementation. Look for outliers. 
        randomtest(args.seed, args.n, args.t, pid)

    if args.test == 'load' :
        factory_f = process.DifferentialFactory(lambda x : math.log(x *.1) * 0.1 )
        dut = process.Process(pid, 100, args.n)

        x = numpy.arange(0, args.n) 
        dut.run()
        fig, ax1 = plt.subplots()
        ax1.set_xlabel('Step')
        ax1.set_ylabel('Setpoint (green), Feedback (red)')
        ax1.tick_params('y', color='r')
        ax1.plot(x, dut.setpoint, 'g--', dut.feedback, 'r')

        ax3 = ax1.twinx()
        ax3.set_ylabel('Output (blue)')
        ax3.plot(x, dut.output)

        #fig.tight_layout()
        plt.show()
        pass

if __name__ == '__main__' :
    main()
    
