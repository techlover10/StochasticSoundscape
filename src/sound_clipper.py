#!/usr/bin/python3
#
# Copyright © 2017 jared <jared@jared-devstation>
#

import sys, os, math
import wave, struct
import analyze

INTERVAL = 2500 # Adjust this to change the sample length

IN_DIR = './long_sounds'
OUT_DIR = './samples'
counter = 0

for fname in os.listdir(IN_DIR):
    if fname[len(fname)-4:len(fname)] == '.wav':
        current_file = wave.open(IN_DIR + '/' + fname, 'r')
        pulse_loc = analyze.pulse_detect(IN_DIR + '/' + fname)
        prev_point = 0
        for pulse_point in pulse_loc:
            read_length = pulse_point - prev_point
            counter+=1
            working = wave.open(OUT_DIR + '/' + fname[0:len(fname)-4] + '_s' + str(counter) + '.wav', 'w') # open the sample file
            working.setparams(current_file.getparams())
            working.setnframes(0)
            curr_data = current_file.readframes(read_length)
            working.writeframes(curr_data) # save the working frames to the temp file
            working.close()
            prev_point = pulse_point


