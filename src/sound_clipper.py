#!/usr/bin/python3
#
# Copyright © 2017 jared <jared@jared-devstation>
#

import sys, os, math
import wave, struct

IN_DIR = './long_sounds'
OUT_DIR = './samples'
INTERVAL = 50000
counter = 0

for fname in os.listdir(IN_DIR):
    if fname[len(fname)-4:len(fname)] == '.wav':
        current_file = wave.open(IN_DIR + '/' + fname, 'r')
        length = current_file.getnframes()
        for i in range (0, math.floor(length/INTERVAL)):
            counter+=1
            print(i)
            print("running")
            working = wave.open(OUT_DIR + '/' + fname[0:len(fname)-4] + '_s' + str(counter) + '.wav', 'w') # open the sample file
            working.setparams(current_file.getparams())
            working.setnframes(0)
            curr_data = current_file.readframes(INTERVAL)
            working.writeframes(curr_data) # save the working frames to the temp file
            working.close()


