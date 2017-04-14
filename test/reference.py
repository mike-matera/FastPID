#! /usr/bin/python3

import numpy 
import matplotlib.pyplot as plt
import PID_INT64
import random 
import datetime 
import os 
import sys

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
        self.p = round(random.uniform(0, 2), 3)
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
        if not PID_INT64.configure(self.p, self.i, self.d, self.db, 16, True) :
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
            dutout = PID_INT64.step(point, dutout)

        # Record result
        self.err = numpy.subtract(self.refdata, self.dutdata)
        swing = numpy.sum(numpy.abs(self.refdata))
        if swing == 0: 
            self.magerr = 0
        else:
            self.magerr = numpy.sum(numpy.square(self.err)) / swing**2

        return self.magerr
    
    def save(self) : 
        if not os.path.isdir('plots') :
            os.mkdir('plots')
        plotname = "plots/plot-p{}-i{}-d{}-db{}-mag{}-steps{}.png".format(self.p, self.i, self.d, self.db, self.mag, self.steps)
        print ("Saving plot:", plotname)
        plt.plot(self.sp, '', self.refdata, '--', self.dutdata, '', self.err, '*')
        plt.savefig(plotname)
        plt.close()

    def show(self):
        plt.plot(self.sp, '', self.refdata, '--', self.dutdata, '', self.err, '*')
        plt.show()

def randomtest(seed) :
    random.seed(seed)
    print ("Random seed:", seed)
    turns = 10000

    results = numpy.array([])
    results.resize((turns,))

    for test_num in range (turns) : 
        test = testrun(100)
        test.random()
        err = test.run()
        if err > 0.0001 : 
            test.save()
        results[test_num,] = err

    best = numpy.amin(results)
    worst = numpy.amax(results)
    avg = numpy.average(results)
    
    print ("Best: {} Worst: {} Avg: {}".format(best,worst,avg))
    plt.plot(results, '*')
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

    else:
        seed = datetime.time()
        randomtest(seed)
