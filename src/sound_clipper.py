#!/usr/bin/python3
#
# Copyright © 2017 jared <jared@jared-devstation>
#

import sys, os, math
import wave, struct
import analyze
import settings, audio
import threading

IN_DIR = '../data/sound_clipper_sources'
OUT_DIR = '../data/samples'

def generate_sounds():
    for fname in os.listdir(IN_DIR):
        if fname.endswith('.wav') or fname.endswith('.mp3'):
            FileSplitter(fname).start()
    if settings.FREQUENCY_SPLIT:
        for fname in os.listdir(OUT_DIR):
            if fname.endswith('.wav') or fname.endswith('.mp3'):
                OutfileSplitter(fname).start()

class FileSplitter(threading.Thread):
    def __init__(self, fname):
        self.fname = fname
        threading.Thread.__init__ ( self )

    def run(self):
        self.split_single_file(self.fname)

    def split_single_file(self, fname):
        counter = 0
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

class OutfileSplitter(threading.Thread):
    def __init__(self, fname):
        self.fname = fname
        threading.Thread.__init__ ( self )

    def run(self):
        self.split_outfile(self.fname)

    def split_outfile(self, fname):
        audio.split_file(OUT_DIR + '/' + fname)
        os.remove(OUT_DIR + '/' + fname)


