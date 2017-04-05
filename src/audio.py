#!/usr/bin/python3
#
# Copyright © 2017 jared <jared@jared-devstation>
#

from pydub import AudioSegment
import os

# combine two audio samples with a crossfade
def combine_samples(acc, file2, CROSSFADE_DUR=100):
    sample2 = AudioSegment.from_wav(file2)
    output = acc.append(sample2, crossfade=CROSSFADE_DUR)
    return output

## add a sample to an existing wav
#def add_sample(fname, samplefile, CROSSFADE_DUR=100):
#    new_file = combine_samples(fname, samplefile, CROSSFADE_DUR)[0]
#    os.rename(fname, 'old_' + fname)
#    os.rename(new_file, fname)
#    return new_file[1]

