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
def analyze(fname, outfile, INTERVAL=50000):
    # Current file is the one we are iterating over
    current_file = wave.open(fname, 'r')
    length = current_file.getnframes()
    prev_rolloff = None
    hash_dict = {}
    
    # Iterate over current file 10 frames at a time
    for i in range (0, math.floor(length/INTERVAL)):
        working = wave.open('temp.wav', 'w') # open the temp file for writing
        working.setparams(current_file.getparams())
        working.setnframes(0)
        curr_data = current_file.readframes(INTERVAL)
        working.writeframes(curr_data) # save the working frames to the temp file
        working.close()

        # Within current 10 frames, perform analysis + write to stochastic matrix
        # This is one of the parameters that can be changed
        y, sr = librosa.load('temp.wav') # load the temp file
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        rolloff = math.floor(numpy.average(rolloff))
        
        # write the transition if there is a previous number
        if prev_rolloff:
            if prev_rolloff in hash_dict.keys():
                if rolloff in hash_dict[prev_rolloff]:
                    hash_dict[prev_rolloff][rolloff]+=1
                else:
                    hash_dict[prev_rolloff] = {}
                    hash_dict[prev_rolloff][rolloff]=1

            else:
                hash_dict[prev_rolloff] = {}
                hash_dict[prev_rolloff] = {}
                hash_dict[prev_rolloff][rolloff]=1

        prev_rolloff = rolloff

    return hash_dict

def normalize(hash_matrix):
    new_matrix = {}
    for prev_freq in hash_matrix.keys():
        curr_freq_data = hash_matrix[prev_freq]
        total = sum(curr_freq_data.values())
        new_dict = {}
        for key in curr_freq_data.keys():
            new_dict[key] = curr_freq_data[key]/total
        new_matrix[prev_freq] = new_dict

    return new_matrix

# Generate data based on every file in the 'data' folder
def data_gen(outfile):
    for fname in os.listdir('./data'):
        analyze(fname, outfile)
