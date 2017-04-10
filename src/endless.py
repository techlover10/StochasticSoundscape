#!/usr/bin/python3
#
# Copyright © 2017 jared <jared@jared-devstation>
#

# Runs the main application.  Uses existing data to
# generate a new piece.

import pygame
import analyze
import pydub
from pydub import AudioSegment
from pydub.playback import play
from samplelib import SampleLib as slib
import sys

print("running quickgen")
markov_data = analyze.load_existing()
lib = slib('./samples', analyzeall=False)

markov_data.initialize_chain() # initialize data to follow chain

newsample = markov_data.get_next_outcome()
#print("selected sample: " + lib.get_sample(newsample))
output = AudioSegment.from_wav('samples/' + lib.get_sample(newsample))

play(output)

# loop to generate audio based on transitions
while True:
    newsample = markov_data.get_next_outcome()
    #print("selected sample: " + lib.get_sample(newsample))
    output = AudioSegment.from_wav('samples/' + lib.get_sample(newsample))
    play(output)
    #print("added sample")
    #print(output.duration_seconds)



