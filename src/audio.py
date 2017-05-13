#!/usr/bin/python3
#
# Copyright © 2017 jared <jared@jared-devstation>
#

from pydub import AudioSegment, scipy_effects, effects
import os
import settings, util

# combine two audio samples with a crossfade
def combine_samples(acc, file2, CROSSFADE_DUR=100):
    util.debug_print('combining ' + file2)
    sample2 = AudioSegment.from_wav(file2)
    output = acc.append(sample2, crossfade=CROSSFADE_DUR)
    output = effects.normalize(output)
    return output

# combine audio samples with crossfade, from within program
def combine_prog_samples(acc, nsamp, CROSSFADE_DUR=100):
    output = acc.append(nsamp, crossfade=CROSSFADE_DUR)
    return output

# split an audio file into low, mid, high bands
def split_file(fname):
    curr_file = AudioSegment.from_file(fname)
    low_seg = scipy_effects.low_pass_filter(curr_file, settings.LOW_FREQUENCY_LIM).export(fname + '_low.wav', 'wav')
    mid_seg = scipy_effects.band_pass_filter(curr_file, settings.LOW_FREQUENCY_LIM, settings.HIGH_FREQUENCY_LIM).export(fname + '_mid.wav', 'wav')
    high_seg = scipy_effects.high_pass_filter(curr_file, settings.HIGH_FREQUENCY_LIM).export(fname + '_high.wav', 'wav')

## add a sample to an existing wav
#def add_sample(fname, samplefile, CROSSFADE_DUR=100):
#    new_file = combine_samples(fname, samplefile, CROSSFADE_DUR)[0]
#    os.rename(fname, 'old_' + fname)
#    os.rename(new_file, fname)
#    return new_file[1]

