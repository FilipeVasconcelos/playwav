#!/bin/bash
notes=("do" "doD" "ré" "réD" "mi" "fa" "faD" "sol" "solD" "la" "laD" "si")
freq=("523.3" "554.4" "587.3" "622.3" "659.3" "698.5" "740.0" "784.0" "830.6" "880.0" "932.3" "987.8")
n=${#notes[*]}
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
        python3 generate_1d_signal.py -p ${ktemps} -fs 44100 -s realexp -d ${freq[${i}]} 0 ${valtemps} -w ${notes[${i}]}${temps}.wav
    done
done

