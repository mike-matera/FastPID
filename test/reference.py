#! /usr/bin/python3

import numpy 
import scipy 
import matplotlib.pyplot as plt
import FastPID
import random 
import datetime 
import os 
import sys
import time 
import math

class refpid : 
    def __init__(self, p, i, d, db) : 
        self.kp = p
        self.ki = i
        self.kd = d 

        if i == 0 and d == 0 :
            self.dband = 0
        else:
            self.dband = db

        self.out = 0 
        self.sum = 0
        self.lasterr = 0
        self.lastsp = 0
        self.stepno = 0

    def step(self, sp, fb) :
        err = sp - fb 

        P = err * self.kp

        if self.stepno > 0 : 
            self.sum += err 
            I = self.sum * self.ki

            D = self.kd * ((sp - self.lastsp) - (err - self.lasterr))
            self.lasterr = err  
            self.lastsp = sp 

        else:
            I = 0
            D = 0
            
        delta = P + I + D 

        if (abs(delta) > self.dband) :
            self.out += delta 

        if self.out > 32767 :
            self.out = 32767
        elif self.out < -32768 : 
            self.out = -32768

        self.stepno += 1
        return round(self.out)

class testrun : 

    def __init__(self, st): 
        self.steps = st
    
    def random(self) : 
        self.p = round(random.uniform(0, 1), 3)
        self.i = round(random.uniform(0, self.p), 3)
        self.d = round(random.uniform(0, self.i), 3)
        self.db = round(random.uniform(0, 32))
        self.mag = round(random.uniform(-1,1) * 32767)

    def configure(self, p, i, d, db, mag) : 
        self.p = p;
        self.i = i; 
        self.d = d; 
        self.db = db; 
        self.mag = mag; 

    def impulse(self, steps) :
        ar = numpy.array([0,1,0])
        ar.resize((steps,))
        return ar

    def run(self): 
        self.sp = self.impulse(self.steps) * self.mag
        if not FastPID.configure(self.p, self.i, self.d, self.db, 16, True) :
            print ("Configuration ERROR!")    
        ref = refpid(self.p, self.i, self.d, self.db) 
        self.refdata = numpy.array([], dtype=int)
        self.dutdata = numpy.array([], dtype=int)
        self.refdata = numpy.resize(self.refdata, self.sp.shape)
        self.dutdata = numpy.resize(self.dutdata, self.sp.shape)
        refout = 0
        dutout = 0
        for x, point in enumerate(self.sp) : 
            self.refdata[x,] = refout
            self.dutdata[x,] = dutout
            refout = ref.step(point, refout)
            dutout = FastPID.step(point, dutout)

        # Record result
        errf = numpy.square(numpy.subtract(self.refdata, self.dutdata))
        self.err = numpy.cumsum(errf) / numpy.arange(1, self.dutdata.size+1, dtype=float)
        self.chi2 = numpy.sum(errf) / self.dutdata.size
        return self.chi2
    
    def save(self) : 
        if not os.path.isdir('plots') :
            os.mkdir('plots')
        plotname = "plots/plot-p{}-i{}-d{}-db{}-mag{}-steps{}.png".format(self.p, self.i, self.d, self.db, self.mag, self.steps)
        print ("saving plot:", plotname)
        plt.plot(self.sp, '', self.refdata, '--', self.dutdata, '')
        plt.savefig(plotname)
        plt.close()

    def show(self):
        plt.plot(self.sp, '', self.refdata, '--', self.dutdata, '', self.err, '-.')
        plt.show()

def randomtest(seed, turns, plot) :
    results = numpy.array([])
    results.resize((turns,))

    for test_num in range (turns) : 
        test = testrun(100)
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
    
if __name__ == '__main__' : 
    if len(sys.argv) == 7 :
        p = float(sys.argv[1])
        i = float(sys.argv[2])
        d = float(sys.argv[3])
        db = int(sys.argv[4])
        mag = int(sys.argv[5])
        steps = int(sys.argv[6])
        print ("Running p={} i={} d={} db={} mag={} steps={}".format(p, i, d, db, mag, steps))
        test = testrun(steps)
        test.configure(p, i, d, db, mag)
        test.run()
        test.show()

    elif len(sys.argv) == 3 : 
        seed = int(sys.argv[1])
        turns = int(sys.argv[2])
        random.seed(seed)
        print ("Random seed:", seed)
        print ("Number of turns:", turns)
        randomtest(seed, turns, True)

    else:
        seed = int(time.time())
        turns = 100000
        random.seed(seed)
        print ("Random seed:", seed)
        print ("Number of turns:", turns)
        randomtest(seed, turns, False)
