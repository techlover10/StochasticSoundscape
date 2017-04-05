#!/usr/bin/python3
#
# Copyright © 2017 jared <jared@jared-devstation>
#

# Runs the main application.  Uses existing data to
# generate a new piece.

import analyze
from samplelib import SampleLib as slib
from pydub import AudioSegment
import audio

markov_data = analyze.data_gen()
lib = slib('./samples')

DURATION = 35 # desired soundscape duration in seconds
FILENAME = 'soundscape.wav' # output file name

markov_data.initialize_chain() # initialize data to follow chain

newsample = markov_data.get_next_outcome()
#print("selected sample: " + lib.get_sample(newsample))
output = AudioSegment.from_wav('samples/' + lib.get_sample(newsample))

# loop to generate audio based on transitions
while output.duration_seconds < DURATION:
    newsample = markov_data.get_next_outcome()
    #print("selected sample: " + lib.get_sample(newsample))
    output = audio.combine_samples(output, 'samples/' + lib.get_sample(newsample))
    #print("added sample")
    #print(output.duration_seconds)

output.export(FILENAME, format='wav')


