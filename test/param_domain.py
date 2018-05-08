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

def main() :
    kp = 1
    while FastPID.configure(kp-1,0,0,16,False) :
        print ('{} okay'.format(kp-1))
        kp *= 2
    
    
    print ('-------')
    kp = 1
    while FastPID.configure(kp,0,0,16,False) :
        print ('{} okay'.format(kp))
        kp /= 2

        
if __name__ == '__main__' :
    main()
