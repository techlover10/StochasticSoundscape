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
lib = SampleLib('./samples')

DURATION = 35 # desired soundscape duration in seconds
FILENAME = 'soundscape.wav' # output file name

markov_data.initialize_chain() # initialize data to follow chain
output = AudioSegment.empty()

# loop to generate audio based on transitions
while output.duration_seconds < DURATION:
    newsample = markov_data.get_next_outcome()
    audio.combine_samples(output, newsample)

output.export(FILENAME, format='wav')


