
class refpid : 
    def __init__(self, p, i, d, bits, sign) : 
        self.kp = p
        self.ki = i
        self.kd = d 
        self.sum = 0
        self.lasterr = 0
        self.lastsp = 0
        self.stepno = 0
        if bits == 16 : 
            self.max = 2 ** (bits-1) - 1
        else :
            self.max = 2 ** bits - 1
        if sign : 
            self.min = -2 ** (bits-1) 
        else:
            self.min = 0 

    def step(self, sp, fb) :
        err = sp - fb 

        P = err * self.kp

        if self.stepno > 0 : 
            self.sum += err * self.ki
            I = self.sum 

            D = self.kd * ((err - self.lasterr) - (sp - self.lastsp))
            self.lasterr = err  
            self.lastsp = sp 

        else:
            I = 0
            D = 0
            
        out = P + I + D 

        if out > self.max :
            out = self.max
        elif out < self.min : 
            out = self.min

        self.stepno += 1
        return round(out)
