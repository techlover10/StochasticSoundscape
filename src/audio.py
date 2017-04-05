#!/usr/bin/python3
#
# Copyright © 2017 jared <jared@jared-devstation>
#

from pydub import AudioSegment
import os

# combine two audio samples with a crossfade
def combine_samples(file1, file2, CROSSFADE_DUR):
    sample1 = AudioSegment.from_wav(file1)
    sample2 = AudioSegment.from_wave(file2)
    output = sample1.append(sample2, crossfade=CROSSFADE_DUR)
    file_out = output.export('outfile.wav', format='wav')
    return file_out

# add a sample to an existing wav
def add_sample(fname, samplefile, CROSSFADE_DUR=100):
    new_file = combine_samples(fname, samplefile, CROSSFADE_DUR)
    os.rename(fname, 'old_' + fname)
    os.rename(new_file, fname)

