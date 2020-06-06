#!/bin/bash

while true;
do
    read -rsn1 input
    if [ "$input" = "a" ]; then
        play "doN_O3.wav"
    fi
    if [ "$input" = "q" ]; then
        play "réN_O3.wav"
    fi
    if [ "$input" = "w" ]; then
        play "miN_O3.wav"
    fi
    if [ "$input" = "z" ]; then
        play "faN_O3.wav"
    fi
    if [ "$input" = "s" ]; then
        play "solN_O3.wav"
    fi
    if [ "$input" = "x" ]; then
        play "laN_O3.wav"
    fi
    if [ "$input" = "e" ]; then
        play "siN_O3.wav"
    fi
    if [ "$input" = "d" ]; then
        play "doN_O4.wav"
    fi
done 
