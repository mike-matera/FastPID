
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
