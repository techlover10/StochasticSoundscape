#!/usr/bin/python3
#
# Copyright © 2017 jared <jared@jared-devstation>
#

import sys, os, math
import wave, struct
import analyze
import settings, audio

IN_DIR = '../data/sound_clipper_sources'
OUT_DIR = '../data/samples'
counter = 0

for fname in os.listdir(IN_DIR):
    if fname.endswith('.wav'):
        current_file = wave.open(IN_DIR + '/' + fname, 'r')
        pulse_loc = analyze.pulse_detect(IN_DIR + '/' + fname, settings.PULSE_TYPE)
        prev_point = 0
        for i in range (0, len(pulse_loc)):
            pulse_point = pulse_loc[i] * 1024 # 1024 = default hop length of 512 * sample rate which is halved
            read_length = pulse_point - prev_point
            counter+=1
            working = wave.open(OUT_DIR + '/' + fname[0:len(fname)-4] + '_s' + str(counter) + '.wav', 'w') # open the sample file
            working.setparams(current_file.getparams())
            working.setnframes(0)
            curr_data = current_file.readframes(read_length)
            working.writeframes(curr_data) # save the working frames to the temp file
            working.close()
            prev_point = pulse_point

if settings.FREQUENCY_SPLIT:
    for fname in os.listdir(OUT_DIR):
        if fname.endswith('wav'):
            audio.split_file(OUT_DIR + '/' + fname)
            os.remove(OUT_DIR + '/' + fname)


