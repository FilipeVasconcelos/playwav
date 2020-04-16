#!/bin/bash

while true;
do
    read -rsn1 input
    if [ "$input" = "a" ]; then
        mplayer "doN_O3.wav"
    fi
    if [ "$input" = "q" ]; then
        mplayer "réN_O3.wav"
    fi
    if [ "$input" = "w" ]; then
        mplayer "miN_O3.wav"
    fi
    if [ "$input" = "z" ]; then
        mplayer "faN_O3.wav"
    fi
    if [ "$input" = "s" ]; then
        mplayer "solN_O3.wav"
    fi
    if [ "$input" = "x" ]; then
        mplayer "laN_O3.wav"
    fi
    if [ "$input" = "e" ]; then
        mplayer "siN_O3.wav"
    fi
    if [ "$input" = "d" ]; then
        mplayer "doN_O4.wav"
    fi
done 
