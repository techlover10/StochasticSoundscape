#!/usr/bin/python3
#
# Copyright © 2017 jared <jared@jared-devstation>
#

import math
import sys, os
import wave, struct
import numpy
import librosa
from PyTransitionMatrix.Markov import TransitionMatrix as tm

# Analyze a single sound file
# Return the file with the frequency data
def analyze(fname, INTERVAL=50000):
    # Current file is the one we are iterating over
    current_file = wave.open(fname, 'r')
    length = current_file.getnframes()
    prev_rolloff = None
    hash_dict = {}

    markov_data = tm(fname) # initialize markov object
    
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
            markov_data.add_transition(prev_rolloff, rolloff)

        prev_rolloff = rolloff

    return markov_data.save() # save the associated data for that file

# Generate data based on every file in the 'data' folder
def data_gen():
    markov_master = tm('master_data')
    for fname in os.listdir('./data'):
        curr_out_data = analyze(fname)
        markov_master.load_data(curr_out_data)

    markov_master.save()
