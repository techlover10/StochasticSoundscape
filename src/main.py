#!/usr/bin/python3
#
# Copyright © 2017 jared <jared@jared-devstation>
#

# Runs the main application.  Uses existing data to
# generate a new piece.

import analyze
from samplelib import SampleLib as slib
from pydub import AudioSegment
import audio, generate
import util
import sys
import settings

markov_data = analyze.data_gen()

# Run the generate methods
generate.generate()
