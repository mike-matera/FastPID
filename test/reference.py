#! /usr/bin/python3

import numpy 
import matplotlib.pyplot as plt
import PID_INT64
import random 
import datetime 

class refpid : 
    def __init__(self, p, i, d, db) : 
        self.kp = p
        self.ki = i
        self.kd = d 
        if i != 0 and d != 0 :
            self.dband = db
        else:
            self.dband = 0
        self.out = 0 
        self.sum = 0
        self.lasterr = 0
        self.lastsp = 0

    def step(self, sp, fb) :
        err = sp - fb 

        P = err * self.kp

        self.sum += err 
        I = self.sum * self.ki

        D = self.kd * ((sp - self.lastsp) - (err - self.lasterr))
        self.lasterr = err  
        self.lastsp = sp 

        delta = P + I + D 
        if (abs(delta) > self.dband) :
            self.out += delta 

        if self.out > 32767 :
            self.out = 32767
        elif self.out < -32768 : 
            self.out = -32768

        return round(self.out)

def impulse(steps) :
    ar = numpy.array([0,1,0])
    ar.resize((steps,))
    return ar

def do_test(p, i, d, db, sp) :
    if not PID_INT64.configure(p, i, d, db, 16, True) :
        print ("Configuration ERROR!")    
    ref = refpid(p, i, d, db) 
    refdata = numpy.array([], dtype=int)
    dutdata = numpy.array([], dtype=int)
    refdata = numpy.resize(refdata, sp.shape)
    dutdata = numpy.resize(dutdata, sp.shape)
    refout = 0
    dutout = 0
    for i, point in enumerate(sp) : 
        refdata[i,] = refout
        dutdata[i,] = dutout
        refout = ref.step(point, refout)
        dutout = PID_INT64.step(point, dutout)

    return [refdata, dutdata]
    
def report_fail(p, i, d, db, sp, ref, test, err, magerr) : 
    print ("WARNING p={} i={} d={} db={} error: {}".format(p,i,d,db,magerr))
    cum = numpy.cumsum(err)
    plotname = "warning-p{}-i{}-d{}-db{}.png".format(p,i,d,db)
    plt.plot(sp, '', ref, '--', test, '', err, '*')
    plt.savefig(plotname)
    #plt.show()
    plt.close()
    
def reftest() :
    seed = datetime.time()
    seed = 0
    random.seed(seed)
    print ("Random seed:", seed)
    turns = 10000

    total = 0
    fails = 0
    best = 100
    worst = 0

    for i in range (turns) : 

        p = round(random.uniform(0, 2), 3)
        i = round(random.uniform(0, p), 3)
        d = round(random.uniform(0, i), 3)
        db = round(random.uniform(0, 32))

        steps = 100
        sp = impulse(steps) * round(random.uniform(-1,1) * 32767)

        (ref, test) = do_test(p, i, d, db, sp)

        err = numpy.abs(numpy.subtract(ref, test))
        swing = numpy.sum(numpy.abs(ref))
        if swing == 0: 
            continue

        magerr = numpy.sum(err) / swing**2

        if magerr > worst : 
            worst = magerr 

        if magerr < best : 
            best = magerr 

        total += 1
        if magerr > 0.001 : 
            fails += 1
            report_fail(p, i, d, db, sp, ref, test, err, magerr)

    print ("Total: {} Failures: {} Best: {} Worst: {}".format(total,fails,best,worst))

if __name__ == '__main__' : 
    reftest()
    
