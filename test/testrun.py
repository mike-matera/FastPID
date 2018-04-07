import refpid
import numpy
import random
import os
import matplotlib.pyplot as plt
import math

class testrun : 

    def __init__(self, st, pid): 
        self.steps = st
        self.pid = pid
        
    def random(self) : 
        self.p = round(random.uniform(0, 1), 3)
        self.i = round(random.uniform(0, self.p), 3)
        self.d = round(random.uniform(0, self.i), 3)
        self.mag = round(random.uniform(-1,1) * 32767)

    def configure(self, p, i, d, mag) : 
        self.p = p;
        self.i = i; 
        self.d = d; 
        self.mag = mag; 

    def impulse(self, steps) :
        ar = numpy.array([0,0])
        #ar.resize((steps,))
        ar = numpy.resize([1], (steps,))
        ar[0] = 0
        ar[1] = 0
        return ar

    def run(self): 
        self.sp = self.impulse(self.steps) * self.mag
        if not self.pid.configure(self.p, self.i, self.d, 16, True) :
            print ("Configuration ERROR!")    
        ref = refpid.refpid(self.p, self.i, self.d) 
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
            dutout = self.pid.step(point, dutout)

        # Record result
        errf = numpy.square(numpy.subtract(self.refdata, self.dutdata))
        self.err = numpy.cumsum(errf) / numpy.arange(1, self.dutdata.size+1, dtype=float)
        self.chi2 = numpy.sum(errf) / self.dutdata.size
        return self.chi2
    
    def save(self) : 
        if not os.path.isdir('plots') :
            os.mkdir('plots')
        plotname = "plots/plot-p{}-i{}-d{}-mag{}-steps{}.png".format(self.p, self.i, self.d, self.mag, self.steps)
        print ("saving plot:", plotname)
        plt.plot(self.sp, '', self.refdata, '--', self.dutdata, '')
        plt.savefig(plotname)
        plt.close()

    def show(self):
        plt.plot(self.sp, '', self.refdata, '--', self.dutdata, '')
        plt.show()

