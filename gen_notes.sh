#!/bin/bash
notes=("do" "doD" "ré" "réD" "mi" "fa" "faD" "sol" "solD" "la" "laD" "si")
freq=("523.3" "554.4" "587.3" "622.3" "659.3" "698.5" "740.0" "784.0" "830.6" "880.0" "932.3" "987.8")
octaves=("0.125" "0.25" "0.5" "1" "2" "4" "8" "16" "32" "64")
n=${#notes[*]}
for octave in 2 4 
do
    for temps in "N" "B"
    do
        if [ ${temps} == "B" ]
        then
            ktemps=16
            valtemps=-6
        else
            ktemps=15
            valtemps=-7.5
        fi
        for i in $(seq 0 $((n-1)))
        do
            echo ${i} ${notes[${i}]} ${note} ${temps}
            freqo=$(echo "scale=5;${freq[${i}]}*${octaves[${octave}]}"|bc)
            python3 generate_1d_signal.py -p ${ktemps} -fs 44100 -s realexp -d ${freqo} 0 ${valtemps} -w ${notes[${i}]}${temps}_O${octave}.wav
            mplayer ${notes[${i}]}${temps}_O${octave}.wav
        done
    done
done

