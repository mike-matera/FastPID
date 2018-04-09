
class refpid : 
    def __init__(self, p, i, d, bits, sign) : 
        self.kp = p
        self.ki = i
        self.kd = d 
        self.out = 0 
        self.sum = 0
        self.lasterr = 0
        self.lastsp = 0
        self.stepno = 0
        if sign : 
            self.max = 2 ** (bits-1) - 1 
            self.min = -2 ** (bits-1) 
        else:
            self.max = 2 ** bits - 1
            self.min = 0 

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

        self.out += delta 

        if self.out > self.max :
            self.out = self.max
        elif self.out < self.min : 
            self.out = self.min

        self.stepno += 1
        return round(self.out)
