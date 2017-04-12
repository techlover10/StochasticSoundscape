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
import sys, os

if not os.path.isfile('master_data.mkv'):
    print("error: data file does not exist!  use 'runanalysis.py' to generate data file before running quickgen.")
    exit()
if not os.path.isfile('./samples/lib.json'):
    print("error: sample directory has not been analyzed!  use 'libgen.py' to analyze samples before running quickgen.")
    exit()

print("running quickgen")
markov_data = analyze.load_existing()
lib = slib('./samples', analyzeall=False)

DURATION = 60 # desired soundscape duration in seconds
FILENAME = 'soundscape.wav' # output file name

markov_data.initialize_chain() # initialize data to follow chain

newsample = markov_data.get_next_outcome()
#print("selected sample: " + lib.get_sample(newsample))
output = AudioSegment.from_wav('samples/' + lib.get_sample(newsample))

# loop to generate audio based on transitions
while output.duration_seconds < DURATION:
    newsample = markov_data.get_next_outcome()
    #print("selected sample: " + lib.get_sample(newsample))
    output = audio.combine_samples(output, 'samples/' + lib.get_sample(newsample), CROSSFADE_DUR=3)
    #print("added sample")
    #print(output.duration_seconds)

print()
print('file saved! ' + FILENAME)
output.export(FILENAME, format='wav')


