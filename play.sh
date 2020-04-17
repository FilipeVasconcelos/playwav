#!/bin/bash
tab=()
k=0
for note in $*
do
    tab[${k}]="${note}_O4.wav"
    k=$((k+1))
done

while [ 1 ]
do
    mplayer ${tab[*]}
done
