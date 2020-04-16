#!/usr/bin/python3
import numpy as np
def next_pow2(N):
    if N == 0 :
        return
    return int(np.ceil(np.log2(N)))

def argument(x,y):
    if x == 0:
        if y > 0 :
            return  np.pi*0.5
        else:
            return -np.pi*0.5
    if x > 0 :
        return np.arctan(y/x)
    else :
        return np.arctan(y/x)-np.pi

if __name__=="__main__":

    print("testing block: tools" )

    for i in range(1,10):
        print(i,next_pow2(i))

