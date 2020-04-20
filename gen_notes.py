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
AMPLITUDE=2**13 #PCM int16 MAX IS AMPLITUDE between -2**15 and 2**15 
# ------------------------------------------------------------------------------
key_freq={""    : 0.0,
          "do"  : 261.6,
          "doD" : 277.2, 
          "re"  : 293.7, 
          "reD" : 311.1, 
          "mi"  : 329.6, 
          "fa"  : 349.2, 
          "faD" : 370.0, 
          "sol" : 392.0, 
          "solD": 415.3, 
          "la"  : 440.0, 
          "sib" : 466.2, 
          "si"  : 493.9
          }
# ------------------------------------------------------------------------------
octavesCoeff=[0.125]
for i in range(1,10):
    octavesCoeff.append(octavesCoeff[-1]*2)
# ------------------------------------------------------------------------------
dureeData={"d4":(17,-3),"d3":(16.585,-2),"d2":(16,-4),"d1":(15,-6),"d0":(14,-10) } #originale
#dureeData={"d4":(16,-3),"d3":(15.585,-2),"d2":(15,-4),"d1":(14,-6),"d0":(13,-10) } # 2fois plus rapide 
# ------------------------------------------------------------------------------
def signal(freq,ph,ts,N,a,harmonics):
    tpi=2.*np.pi
    xe=np.zeros(N,dtype=np.complex_)
    for k in range(N):
        #xe[k]=((k*ts)**0.2)*np.sin(freq*tpi*k*ts+ph)*np.exp(a*(k*ts)) # original
        xetmp=0.0
        for harm in harmonics:
            xetmp+=harm[0]*np.sin(harm[1]*freq*tpi*k*ts+ph)
        xe[k]+=((k*ts)**0.2)*np.exp(a*(k*ts))*xetmp # enveloppe
    return xe
# ------------------------------------------------------------------------------
# name = keyo3dx
# key : si solD laD
# oi  : i = 0 à 9
# dx  : Durée x = "B" blanche ou "N" noire "C"
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
def genHarmonics(o):
    h=[]
    # (Pur)
    if False :
        for k in range(9):
            if k-o == 0 :
                h.append((1.0,1.0))
    
    # 1
    if False :
        for k in range(9):
            if k-o < 0 :
                a=1.0/(8.5*abs(k-o))
                b=1.0/(2*abs(k-o))
                if a > 1e-4 : h.append((a,b))
            elif k-o > 0 :
                a=1.0/(5.5*abs(k-o))
                b=2*abs(k-o)
                if a > 1e-4 : h.append((a,b))
            else:
                h.append((1.0,1.0))

    # 2
    if False :
        for k in range(9):
            if k-o > 0 :
                a=1.0/(3*abs(k-o))
                b=2*abs(k-o)
                if a > 1e-4 : h.append((a,b))
            elif k-o == 0 :
                h.append((1.0,1.0))

    # 3
    if False :
        for k in range(9):
            if k-o > 0 :
                a=1.0/(4*abs(k-o)**1.5)
                b=2*abs(k-o)
                if a > 1e-4 : h.append((a,b))
            elif k-o == 0 :
                h.append((1.0,1.0))

    #4 
    if False :
        for k in range(9):
            if k-o > 0 :
                a=1.0/(4*abs(k-o)**1.5)
                b=2*abs(k-o)
                if a > 1e-4 : h.append((a,b))
            elif k-o == 0 :
                h.append((1.0,1.0))

    #5 
    if False :
        for k in range(9):
            if k-o > 0 :
                a=1.0/(6.5*np.sqrt((k-o)))
                b=2*abs(k-o)
                if a > 1e-4 : h.append((a,b))
            elif k-o == 0 :
                h.append((1.0,1.0))
    
    #6 
    if False :
        for k in range(9):
            if k-o > 0 :
                a=1.0/(2*(k-o)**2)
                b=2*abs(k-o)
                if a > 1e-4 : h.append((a,b))
            elif k-o == 0 :
                h.append((1.0,1.0))
    # 7
    if True :
        for k in range(9):
            if k-o > 0 :
                a=1.0/(8*(k-o)**0.25)
                b=2*abs(k-o)
                if a > 1e-4 : h.append((a,b))
            elif k-o == 0 :
                h.append((1.0,1.0))

    for ele in h :
        print(ele)
    print("nombre d'harmoniques",len(h))
    return h
# ------------------------------------------------------------------------------
def genNote(notes,plotNote=False,writeWav=False,playWav=False,verbose=0):
    maxd=maxdureeNotes(notes)
    N=int(2**dureeData[maxd][0])
    xe=np.zeros(N,dtype=np.complex_)
    if verbose > 10 :
        print(60*'=')
        print("INFO : number of sample points" ,N)
        print("INFO : sampling frequency (Hz)" ,fs)
        print("INFO : signal duration    (s)"  ,ts*N)
    notename=''
    phas=0.0
    for knote,note in enumerate(notes):
        notename+=note
        k,d,o=extractInfoFromName(note)
        a=dureeData[d][1]
        freq=key_freq[k]*octavesCoeff[o]
        if verbose > 10 :
            print(60*'-')
            print("INFO : frequence key      (Hz)" ,freq)
            print("INFO : phase     key      ()"   ,phas)
            print("INFO : damping   key      (Hz)" ,a)
        xe+=signal(freq,phas,ts,N,a,genHarmonics(o))
        phas+=0.01
    if plotNote :
        t=np.linspace(0,ts*N,N)
        fig, ax = plt.subplots(1, 1)
        ax.plot(t,xe.real)
        ax.set_title(notes)
        ax.set_xlabel('time [s]')
        ax.set_ylabel('Amplitude ')
        plt.show()
    if writeWav :
        notenamefile=notename+".wav"
        xs=np.zeros(N,dtype=np.int16)
        for k in range(N):
            xs[k]=AMPLITUDE*xe[k].real
        wavfile.write(notenamefile,int(fs),xs)

# ------------------------------------------------------------------------------
if __name__ =="__main__":

    satie_voix1=[
        #1----------------------------------------
           ["O0d1"],
           ["siO2d2","reO3d2","faDO3d2"],
        #2----------------------------------------
           ["O0d1"],
           ["laO2d2","doDO3d2","faDO3d2"],
        #3----------------------------------------
           ["O0d1"],
           ["siO2d2","reO3d2","faDO3d2"],
        #4----------------------------------------
           ["O0d1"],
           ["laO2d2","doDO3d2","faDO3d2"],
        #5----------------------------------------
           ["O0d1"],
           ["siO2d2","reO3d2","faDO3d2"],
        #6----------------------------------------
           ["O0d1"],
           ["laO2d2","doDO3d2","faDO3d2"],
        #7----------------------------------------
           ["O0d1"],
           ["siO2d2","reO3d2","faDO3d2"],
        #8----------------------------------------
           ["O0d1"],
           ["laO2d2","doDO3d2","faDO3d2"],
        #9----------------------------------------
           ["O0d1"],
           ["siO2d2","reO3d2","faDO3d2"],
        #10---------------------------------------
           ["O0d1"],
           ["laO2d2","doDO3d2","faDO3d2"],
        #11---------------------------------------
           ["O0d1"],
           ["siO2d2","reO3d2","faDO3d2"],
        #12---------------------------------------
           ["O0d1"],
           ["laO2d2","doDO3d2","faDO3d2"],
        #13---------------------------------------
           ["O0d1"],
           ["siO2d2","reO3d2","faDO3d2"],
        #14---------------------------------------
           ["O0d1"],
           ["laO2d2","doDO3d2","faDO3d2"],
        #15---------------------------------------
           ["O0d1"],
           ["siO2d2","reO3d2","faDO3d2"],
        #16---------------------------------------
           ["O0d1"],
           ["laO2d2","doDO3d2","faDO3d2"],
        #17---------------------------------------
           ["O0d1"],
           ["laO2d2","doDO3d2","faDO3d2"],
        #18---------------------------------------
           ["O0d1"],
           ["siO2d2","reO3d2","faDO3d2"],
        #19---------------------------------------
           ["O0d1"],
           ["laO2d2","faDO2d2"],
        #20---------------------------------------
           ["O0d1"],
           ["laO2d2","doDO3d2","faDO3d2"],
          ]
    satie_voix2=[
        #1----------------------------------------
           ["solO2d3"],
        #2----------------------------------------
           ["reO2d3"],
        #3----------------------------------------
           ["solO2d3"],
        #4----------------------------------------
           ["reO2d3"],
        #5----------------------------------------
           ["solO2d3"],
        #6----------------------------------------
           ["reO2d3"],
        #7----------------------------------------
           ["solO2d3"],
        #8----------------------------------------
           ["reO2d3"],
        #9----------------------------------------
           ["solO2d3"],
        #10---------------------------------------
           ["reO2d3"],
        #11---------------------------------------
           ["solO2d3"],
        #12---------------------------------------
           ["reO2d3"],
        #13---------------------------------------
           ["solO2d3"],
        #14---------------------------------------
           ["reO2d3"],
        #15---------------------------------------
           ["solO2d3"],
        #16---------------------------------------
           ["reO2d3"],
        #17---------------------------------------
           ["faDO2d3"],
        #18---------------------------------------
           ["siO1d3"],
        #17---------------------------------------
           ["miO2d3"],
        #18---------------------------------------
           ["miO2d3"]
          ]
    satie_voix3=[
        #1----------------------------------------
           ["O0d3"],
        #2----------------------------------------
           ["O0d3"],
        #3----------------------------------------
           ["O0d3"],
        #4----------------------------------------
           ["O0d3"],
        #5----------------------------------------
           ["O0d1"],
           ["faDO4d1"],
           ["laO4d1"],
        #6----------------------------------------
           ["solO4d1"],
           ["faDO4d1"],
           ["doDO4d1"],
        #7----------------------------------------
           ["siO3d1"],
           ["doDO4d1"],
           ["reO4d1"],
        #8----------------------------------------
           ["laO3d3"],
        #9----------------------------------------
           ["faDO3d3"],
        #10---------------------------------------
           ["faDO3d3"],
        #11---------------------------------------
           ["faDO3d3"],
        #12---------------------------------------
           ["faDO3d3"],
        #13---------------------------------------
           ["O0d1"],
           ["faDO4d1"],
           ["laO4d1"],
        #14---------------------------------------
           ["solO4d1"],
           ["faDO4d1"],
           ["doDO4d1"],
        #15---------------------------------------
           ["siO3d1"],
           ["doDO4d1"],
           ["reO4d1"],
        #16---------------------------------------
           ["laO3d3"],
        #17---------------------------------------
           ["doDO4d3"],
        #18---------------------------------------
           ["faDO4d3"],
        #19---------------------------------------
           ["miO3d3"],
        #20---------------------------------------
           ["miO3d3"],
          ]

    if True :
        Partition=[satie_voix1,satie_voix2,satie_voix3]
        playNote=False
        piecename="satie"
        tracknames=["satie_voix1","satie_voix2","satie_voix3"]

    frereJacques1=[
                  ["doO4d1"],
                  ["reO4d1"],
                  ["miO4d1"],
                  ["doO4d1"], 
                  ["doO4d1"],
                  ["reO4d1"],
                  ["miO4d1"],
                  ["doO4d1"],
                  ["miO4d1"],
                  ["faO4d1"],
                  ["solO4d2"],
                  ["miO4d1"],
                  ["faO4d1"],
                  ["solO4d2"],
                  ["O0d1"],
                  ["O0d1"],
                  ["O0d1"],
                  ]
    if False:
        Partition=[frereJacques1]
        playNote=False
        piecename="frereJacques"
        tracknames=["frereJacques1"]

    tracknamefiles=""
    for ktrack,track in enumerate(Partition):
        print(60*'=')
        print("Track : ",ktrack)
        print("Name  : "+tracknames[ktrack])
        print(60*'=')
        print(60*'-')
        print("Gen Keys ")
        print(60*'-')
        # ----------------------------------------
        # génération des notes (sur un set Python)
        # ----------------------------------------
        knote=0
        setNotes=set(tuple(i) for i in track)
        for note in setNotes :
            genNote(note,plotNote=False,writeWav=True,verbose=0)
            print(note)
        print("# Keys  : ",len(setNotes))
        notenamefiles=''
        # ----------------------------------------
        # lecture
        # ----------------------------------------
        print(60*'-')
        print("Gen Track ")
        print(60*'-')
        for notes in track:
            notename=''
            for note  in notes:
                notename+=note
            print(notename)
            notenamefile=notename+".wav"
            notenamefiles+=notenamefile+' '
            if playNote :
                os.system("play "+notenamefile+" vol 10dB > /dev/null 2>&1")  # jouer la note dans l'ordre
        os.system("sox "+notenamefiles+tracknames[ktrack]+'.wav')       # concatener les notes 
        tracknamefiles+=tracknames[ktrack]+".wav "+" "
    print(tracknamefiles)

    if len(Partition) > 1 : 
        os.system("sox -m "+tracknamefiles+piecename+'.wav')                # mixer les voix
        os.system("sox "+piecename+".wav "+" out.wav vol 12db bass +6")
    else:
        os.system("sox "+tracknames[0]+".wav "+" out.wav vol 12db bass +6")

    os.system("mv out.wav "+piecename+".wav") 
    print(60*'=')
    print("Play  : ")
    print(60*'=')
    os.system("play "+piecename+".wav")  # jouer tout le morceau 
    

    
