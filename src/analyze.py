#!/usr/bin/python3
#
# Copyright © 2017 jared <jared@jared-devstation>
#

import math
import sys, os
import wave, struct
import numpy
import librosa

# Analyze a single sound file
def analyze(fname, outfile):
    # Current file is the one we are iterating over
    current_file = wave.open(fname, 'r')
    length = current_file.getnframes()
    
    # Iterate over current file 10 frames at a time
    for i in range (0, math.floor(length/100)):
        working = wave.open('temp.wav', 'w') # open the temp file for writing
        working.setparams(current_file.getparams())
        working.setnframes(0)
        curr_data = current_file.readframes(100)
        working.writeframes(curr_data) # save the working frames to the temp file
        working.close()

        # Within current 10 frames, perform analysis + write to stochastic matrix
        y, sr = librosa.load('temp.wav') # load the temp file
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        rolloff = numpy.average(rolloff)
        print(rolloff)


# Generate data based on every file in the 'data' folder
def data_gen(outfile):
    for fname in os.listdir('./data'):
        analyze(fname, outfile)
