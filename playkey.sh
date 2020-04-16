#!/bin/bash

while true;
do
    read -rsn1 input
    if [ "$input" = "a" ]; then
        mplayer "doN.wav"
    fi
    if [ "$input" = "q" ]; then
        mplayer "réN.wav"
    fi
    if [ "$input" = "w" ]; then
        mplayer "miN.wav"
    fi
    if [ "$input" = "z" ]; then
        mplayer "faN.wav"
    fi
    if [ "$input" = "s" ]; then
        mplayer "solN.wav"
    fi
    if [ "$input" = "x" ]; then
        mplayer "laN.wav"
    fi
    if [ "$input" = "e" ]; then
        mplayer "siN.wav"
    fi
    if [ "$input" = "d" ]; then
        mplayer "doN1.wav"
    fi
done 
