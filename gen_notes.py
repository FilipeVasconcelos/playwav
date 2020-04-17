import sys
import os 
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

fs=float(44100) #Hz
ts=1./fs
AMPLITUDE=10**5

key_freq={"do"  :261.6,
          "doD" :277.2, 
          "re"  :293.7, 
          "reD" :311.1, 
          "mi"  :329.6, 
          "fa"  :349.2, 
          "faD" :370.0, 
          "sol" :392.0, 
          "solD":415.3, 
          "la"  :440.0, 
          "sib" :466.2, 
          "si"  :493.9
          }
octavesCoeff=[0.125]
for i in range(1,10):
    octavesCoeff.append(octavesCoeff[-1]*2)

dureeData={ "dB":(16,-4),"dN":(15,-7.5),"dC":(15,-10) }

def realexp(freq,ph,ts,N,a):
    tpi=2.*np.pi
    xe=np.zeros(N,dtype=np.complex_)
    for k in range(N):
        xe[k]=np.sin(freq*tpi*k*ts+ph)*np.exp(a*(k*ts))
    return xe

def extractInfoFromName(name):
    duree=name[-2:]
    octave=name[-3:-2]
    nc=len(name)-4
    key=name[:nc]
    print(nc,len(name),name)
    return key,duree,int(octave)

def maxdureeNotes(notes):
    maxd="dC"
    for note in notes:
        k,d,o=extractInfoFromName(notes[0])
        if dureeData[d][0] > dureeData[maxd][0] :
            maxd=d
    return maxd

# name = keyo3dx
# key : si solD laD
# oi  : i = 0 à 9
# dx  : Durée x = "B" blanche ou "N" noire "C"
def genNote(notes,plotNote=False,writeWav=False,playWav=False):
    print("in genNote",len(notes)) 
    if len(notes) == 1 :
        k,d,o=extractInfoFromName(notes[0])
        N=2**dureeData[d][0]
        a=dureeData[d][1]
        freq=key_freq[k]*octavesCoeff[o]
        phas=0.0
        print("INFO : number of sample points" ,N)
        print("INFO : sampling frequency (Hz)" ,fs)
        print("INFO : signal duration    (s)"  ,ts*N)
        print("INFO : frequence key      (Hz)" ,freq)
        print("INFO : phase     key      ()"   ,phas)
        print("INFO : damping   key      (Hz)" ,a)
        xe=realexp(freq,phas,ts,N,a)
        if plotNote :
            t=np.linspace(0,ts*N,N)
            plt.plot(t,xe.real)
            plt.show()
        if writeWav :
            notenamefile=notes[0]+".wav"
            xs=np.zeros(N,dtype=np.int16)
            norm=2.0/np.sqrt(N)
            for k in range(N):
                xs[k]=AMPLITUDE*xe[k].real*norm
            wavfile.write(notenamefile,int(fs),xs)
            if playWav:
             os.system("mplayer "+notenamefile)    
    else:
        maxd=maxdureeNotes(notes)
        N=2**dureeData[maxd][0]
        a=dureeData[maxd][1]
        phas=0.0
        xe=np.zeros(N,dtype=np.complex_)
        print("INFO : number of sample points" ,N)
        print("INFO : sampling frequency (Hz)" ,fs)
        print("INFO : signal duration    (s)"  ,ts*N)
        notename=''
        for note in notes:
            notename+=note
            k,d,o=extractInfoFromName(note)
            freq=key_freq[k]*octavesCoeff[o]
            print("INFO : frequence key      (Hz)" ,freq)
            print("INFO : phase     key      ()"   ,phas)
            print("INFO : damping   key      (Hz)" ,a)
            xe+=realexp(freq,phas,ts,N,a)
        if plotNote :
            t=np.linspace(0,ts*N,N)
            plt.plot(t,xe.real)
            plt.show()
        if writeWav :
            notenamefile=notename+".wav"
            xs=np.zeros(N,dtype=np.int16)
            norm=2.0/np.sqrt(N)
            for k in range(N):
                xs[k]=AMPLITUDE*xe[k].real*norm
            wavfile.write(notenamefile,int(fs),xs)
            if playWav:
             os.system("mplayer "+notenamefile)    

def genAllNotes():
    #for octave in range(9):
    #   for note in notes_freq:
    pass

if __name__ =="__main__":

    p=16
    N=2**p
    fs=float(44100)
    ts=1./fs  
    satie=[
           ["solO2dN"],
           ["siO2dC","reO3dC","faDO3dC"],
           ["reO2dN"],
           ["laO2dC","doDO3dC","faDO3dC"],
           ["solO2dN"],
           ["siO2dC","reO3dC","faDO3dC"],
           ["reO2dN"],
           ["laO2dC","doDO3dC","faDO3dC"]
          ]
    satie2=[["faDO4dN"],["laO4dN"],["solO4dN"],["faDO4dN"],["doDO4dN"],["siO3dN"],["doDO4dN"],["reO4dN"],["laO3dB"]]
    satie=[
        #-----------------------------------------
           ["solO2dB"],
           ["siO2dB","reO3dB","faDO3dB"],
        #-----------------------------------------
           ["reO2dB"],
           ["laO2dB","doDO3dB","faDO3dB"],
        #-----------------------------------------
           ["solO2dB"],
           ["siO2dB","reO3dB","faDO3dB"],
        #-----------------------------------------
           ["reO2dB"],
           ["laO2dB","doDO3dB","faDO3dB"],
        #-----------------------------------------
           ["solO2dB"],
           ["siO2dB","reO3dB","faDO3dB","faDO4dN"],
           ["laO4dN"],
        #-----------------------------------------
           ["reO2dB","solO4dN"],
           ["laO2dB","doDO3dB","faDO3dB","faDO4dN"],
           ["doDO4dN"],
        #-----------------------------------------
           ["solO2dB","siO3dN"],
           ["siO2dB","reO3dB","faDO3dB","doDO4dN"],
           ["reO4dN"],
           ["laO3dB","solO2dB"]
        #-----------------------------------------
          ]
    # génération
    for note in satie :
        print(note)
        genNote(note,writeWav=True,playWav=True)
    # lecture
    for notes in satie:
        print(notes)
        notename=''
        for note  in notes:
            notename+=note
        notenamefile=notename+".wav"
        os.system("mplayer "+notenamefile)    



    
