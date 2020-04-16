from scipy.io import wavfile
import numpy as np
import datetime
import argparse
import sys
from tools import argument,next_pow2
import matplotlib.pyplot as plt

def porte(amplitude,fenetre,ts,N):
    xe=np.zeros(N,dtype=np.complex_)
    #for k in range(-int(N/2),int(N/2)-1):
    for k in range(N):
        if k*ts > -fenetre*0.5 and k*ts < fenetre*0.5 : 
            xe[k]=amplitude
    return xe

def realexp(freq,ph,ts,N,a):
    tpi=2.*np.pi
    xe=np.zeros(N,dtype=np.complex_)
    for k in range(N):
        xe[k]=np.sin(freq*tpi*k*ts+ph)*np.exp(a*(k*ts))
    return xe

def cosinus(freq,ph,ts,N):
    tpi=2.*np.pi
    xe=np.zeros(N,dtype=np.complex_)
    #for k in range(-int(N/2),int(N/2)-1):
    for k in range(N):
        xe[k]=np.cos(freq*tpi*k*ts+ph)#*np.exp(-(k*ts)**2/0.25)
    return xe

def sinus(freq,ph,ts,N):
    tpi=2.*np.pi
    xe=np.zeros(N,dtype=np.complex_)
    #for k in range(-int(N/2),int(N/2)-1):
    for k in range(N):
        xe[k]=np.sin(freq*tpi*k*ts+ph)#*np.exp(-(k*ts)**2/0.25)
    return xe

def exp_comp(freq,ph,ts,N):
    tpi=2.*np.pi
    xe=np.zeros(N,dtype=np.complex_)
    for k in range(N):
        xe[k]=complex(np.cos(freq*tpi*k*ts+ph),np.sin(freq*tpi*k*ts+ph))#*np.exp(-(k*ts)**2/0.25)
    return xe

def main_parser():                                                                                                            
                                                                                                                              
    parser = argparse.ArgumentParser(description='')                                                                         
    parser.set_defaults(p=0)    
    parser.set_defaults(f_sampling=100)    
    parser.set_defaults(signal="cosine")    
    parser.add_argument('-p' ,'--n_sampling'  ,help='nombre de points du signal N=2^p)',dest="p")          
    parser.add_argument('-fs','--f_sampling'  ,help="fréquence d'échantillonage"       ,dest="f_sampling")          
    parser.add_argument('-s' ,'--signal'      ,help='signal needs data_signal'         ,dest="signal_type")  
    parser.add_argument('-d' ,'--data_signal' ,help='list of parameters)',nargs='+'    ,dest="data_signal")          
    parser.add_argument('-w' ,'--wave_file' ,help='wave filename',dest="wave_filename")          
                                                                                                                              
    if len(sys.argv)==1:                                                                                                      
        parser.print_help()                                                                                                   
        sys.exit(1)                                                                                                           
    args = parser.parse_args()                                                                                                
                                                                                                                              
    return args   

if __name__=="__main__":

    tpi=2.*np.pi

    path="./"                                                     
    xe_filename='xe.dat'
    fxe=open(path+xe_filename,'w')

    separator=60*"="
    now = datetime.datetime.now()
    print(separator)
    print("auteur : Filipe Vasconcelos ")
    print("ESME Sudria Lille ")
    print("v1. juin  2018")
    print("v2. avril 2020")
    print(separator)
    print(now.strftime("%Y-%m-%d %H:%M"))

    args = main_parser()
    signal_type = args.signal_type
    wave_filename = args.wave_filename


    if signal_type =="wav":

        fs, data = wavfile.read(path+wave_filename)
        ts=1./fs  
        p=next_pow2(len(data))
        N=2**p
        xe=np.zeros(N,dtype=np.complex_)
        print("INFO : number of sample points",N)
        print("INFO : sampling frequency (Hz)",fs)
        print("INFO : sampling period (s)",ts)
        print("INFO : signal duration (s)",ts*N)
        print("INFO : generate signal from wav file :",wave_filename)
        for k in range(len(data)):
            xe[k]=data[k]

        fxe.write("# "+str(N)+'\n')
        fxe.write("# "+str(fs)+'\n')
        for k in range(N):
            t=k*ts
            real=xe[k].real
            imag=xe[k].imag
            magn=abs(xe[k])
            phas=argument(real,imag)
            fxe.write('{:>19.15e} {:>19.15e} {:>19.15e} {:>19.15e} {:>19.15e}\n'.format(t,real,imag,magn,phas))
        fxe.close()

    else : 
        data_signal = args.data_signal
        p=int(args.p)
        N=2**p
        fs=float(args.f_sampling)
        ts=1./fs  
        print("INFO : number of sample points",N)
        print("INFO : sampling frequency (Hz)",fs)
        print("INFO : sampling period (s)",ts)
        print("INFO : signal duration (s)",ts*N)
        print("INFO : generate ",signal_type," signal ")
        print("INFO : data_signal : ",data_signal)
    
        if signal_type == "porte" :
            amplitude=float(data_signal[0])
            fenetre=float(data_signal[1])
            print("INFO : signal amplitude",amplitude)
            print("INFO : signal duration",fenetre)
            xe=porte(amplitude,fenetre,ts,N)

        if signal_type == "cosine" :
            freq=float(data_signal[0])
            phas=float(data_signal[1])*np.pi/180.
            print("INFO : signal frequency",freq)
            print("INFO : signal phase",phas)
            xe=cosinus(freq,phas,ts,N)
            print(xe)

        if signal_type == "sine" :
            freq=float(data_signal[0])
            phas=float(data_signal[1])*np.pi/180.
            print("INFO : signal frequency",freq)
            print("INFO : signal phase",phas)
            xe=sinus(freq,phas,ts,N)
        
        if signal_type == "expi" :
            freq=float(data_signal[0])
            phas=float(data_signal[1])*np.pi/180.
            print("INFO : signal frequency",freq)
            print("INFO : signal phase",phas)
            xe=exp_comp(freq,phas,ts,N)
        
        if signal_type == "realexp" :
            freq=float(data_signal[0])
            phas=float(data_signal[1])*np.pi/180.
            a=float(data_signal[2])
            print("INFO : signal frequency",freq)
            print("INFO : signal phase",phas)
            print("INFO : signal damping",a)
            xe=realexp(freq,phas,ts,N,a)


        fxe.write("# "+str(N)+'\n')
        fxe.write("# "+str(fs)+'\n')
        #for k in range(-int(N/2),int(N/2)):
        for k in range(N):
            t=k*ts
            real=xe[k].real
            imag=xe[k].imag
            magn=abs(xe[k])
            phas=argument(real,imag)
            fxe.write('{:>19.15e} {:>19.15e} {:>19.15e} {:>19.15e} {:>19.15e}\n'.format(t,real,imag,magn,phas))
        fxe.close()
        print("file "+path+xe_filename+" created")

    if True:
        t=np.linspace(0,ts*N,N)
#        plt.plot(t,xe.real)
#        plt.show()

        xs_tmp=np.zeros(N,dtype=np.int16)
        norm=2.0/np.sqrt(N)
        for k in range(N):
            xs_tmp[k]=100000*xe[k].real*norm
        wavfile.write(wave_filename,int(fs),xs_tmp)


