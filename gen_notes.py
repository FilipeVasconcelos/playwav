# playing satie 
# date : 16-17 avril 2020
# author : fmv
import sys
import os 
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# ------------------------------------------------------------------------------
fs=float(44100) #Hz fréquence d'échantionnage
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

dureeData={"d4":(17,-3),"d3":(16.5,-3),"d2":(16,-6),"d1":(15,-5),"d0":(14,-10) }

# ------------------------------------------------------------------------------
def realexp(freq,ph,ts,N,a):
    tpi=2.*np.pi
    xe=np.zeros(N,dtype=np.complex_)
    for k in range(N):
        xe[k]=((k*ts)**0.08)*np.sin(freq*tpi*k*ts+ph)*np.exp(a*(k*ts))
    return xe

# ------------------------------------------------------------------------------
def extractInfoFromName(name):
    duree=name[-2:]
    octave=name[-3:-2]
    nc=len(name)-4
    key=name[:nc]
    return key,duree,int(octave)

# ------------------------------------------------------------------------------
def maxdureeNotes(notes):
    maxd="d0"
    for note in notes:
        k,d,o=extractInfoFromName(notes[0])
        if dureeData[d][0] > dureeData[maxd][0] :
            maxd=d
    return maxd

# ------------------------------------------------------------------------------
# name = keyo3dx
# key : si solD laD
# oi  : i = 0 à 9
# dx  : Durée x = "B" blanche ou "N" noire "C"
def genNote(notes,plotNote=False,writeWav=False,playWav=False):
    maxd=maxdureeNotes(notes)
    N=int(2**dureeData[maxd][0])
    xe=np.zeros(N,dtype=np.complex_)
    print(60*'=')
    print("INFO : number of sample points" ,N)
    print("INFO : sampling frequency (Hz)" ,fs)
    print("INFO : signal duration    (s)"  ,ts*N)
    notename=''
    for note in notes:
        notename+=note
        k,d,o=extractInfoFromName(note)
        phas=0.0
        a=dureeData[d][1]
        freq=key_freq[k]*octavesCoeff[o]
        print(60*'-')
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

# ------------------------------------------------------------------------------
if __name__ =="__main__":

    satieRythmique=[
           ["solO2dN"],
           ["siO2dC","reO3dC","faDO3dC"],
           ["reO2dN"],
           ["laO2dC","doDO3dC","faDO3dC"],
           ["solO2dN"],
           ["siO2dC","reO3dC","faDO3dC"],
           ["reO2dN"],
           ["laO2dC","doDO3dC","faDO3dC"]
          ]
    satieMelodie=[
            ["faDO4d1"],
            ["laO4d1"],
            ["solO4d1"],
            ["faDO4d1"],
            ["doDO4d1"],
            ["siO3d1"],
            ["doDO4d1"],
            ["reO4d1"],
            ["laO3d1"]]
    satie=[
        #-----------------------------------------
           ["solO2d1"],
           ["siO2d2","reO3d2","faDO3d2"],
        #-----------------------------------------
           ["reO2d1"],
           ["laO2d2","doDO3d2","faDO3d2"],
        #-----------------------------------------
           ["solO2d1"],
           ["siO2d2","reO3d2","faDO3d2"],
        #-----------------------------------------
           ["reO2d1"],
           ["laO2d2","doDO3d2","faDO3d2"],
        #-----------------------------------------
           ["solO2d1"],
           ["siO2d1","reO3d1","faDO3d1","faDO4d1"],
           ["siO2d1","reO3d1","faDO3d1","laO4d1"],
        #-----------------------------------------
           ["reO2d1","solO4d1"],
           ["laO2d1","doDO3d1","faDO3d1","faDO4d1"],
           ["laO2d1","doDO3d1","faDO3d1","doDO4d1"],
        #-----------------------------------------
           ["solO2d1","siO3d1"],
           ["siO2d1","reO3d1","faDO3d1","doDO4d1"],
           ["siO2d1","reO3d1","faDO3d1","reO4d1"],
           ["laO3d2","solO2d2"]
        #-----------------------------------------
          ]


    track=[["doDO3d3"]]
    track=satie
    trackname="satie.wav"

    # génération des notes (sur un set Python)
    k=0
    for note in set(tuple(i) for i in track) :
        #print(note)
        genNote(note,plotNote=False,writeWav=True)
        k+=1
    print(str(k)+" notes générés")

    notenamefiles=''
    # lecture
    for notes in track:
        notename=''
        for note  in notes:
            notename+=note
        notenamefile=notename+".wav"
        print(notenamefile)
        notenamefiles+=notenamefile+' '
        os.system("mplayer "+notenamefile+" > /dev/null 2>&1")    
    os.system("sox "+notenamefiles+trackname)


    
