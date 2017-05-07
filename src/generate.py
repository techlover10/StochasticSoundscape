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
import settings
import sys, os
import util

def generate():

    if not os.path.isfile('../data/generated_data/master_data.json') and not os.path.isfile('../data/generated_data/master_data_low.json'):
        print("error: data file does not exist!  use 'runanalysis.py' to generate data file before running quickgen.")
        exit()
    if not os.path.isfile('../data/samples/lib.json'):
        print("error: sample directory has not been analyzed!  use 'libgen.py' to analyze samples before running quickgen.")
        exit()
    
    FILENAME = sys.argv[1] if len(sys.argv) > 1 else settings.FILENAME
    
    print()
    print("Generating soundscape...")
    markov_data = analyze.load_existing()
    lib = slib('../data/samples', analyzeall=False)
    
    if not settings.FREQUENCY_SPLIT:
        markov_data.initialize_chain() # initialize data to follow chain
        newsample = markov_data.get_next_outcome()
        output = AudioSegment.from_wav('../data/samples/' + lib.get_sample(newsample))
    else:
        output = {}
        newsample = {}
        for band, data in markov_data.items():
            data.initialize_chain()
            newsample[band] = data.get_next_outcome() 
        output_set = lib.get_sample(newsample)
        for band, sound in output_set.items():
            output[band] = AudioSegment.from_wav('../data/samples/' + sound)
    
    
    
    # loop to generate audio based on transitions
    curr_seconds = 0
    while curr_seconds < settings.DURATION:
        if not settings.FREQUENCY_SPLIT:
            newsample = markov_data.get_next_outcome()
            output = audio.combine_samples(output, '../data/samples/' + lib.get_sample(newsample), CROSSFADE_DUR=3)
            curr_seconds = output.duration_seconds
        else:
            for band, data in markov_data.items():
                data.initialize_chain()
                newsample[band] = data.get_next_outcome() 
            output_set = lib.get_sample(newsample)
            output_sounds = []
            for band, sound in output_set.items():
                output[band] = audio.combine_samples(output[band], ('../data/samples/' + sound))
            curr_seconds = min(output.values(), key=lambda sound: sound.duration_seconds).duration_seconds
    
    if settings.FREQUENCY_SPLIT:
        max_len = -1
        for i in output.values():
            if i.duration_seconds > max_len:
                max_len = i.duration_seconds
        
        util.debug_print(max_len)
        newfile = AudioSegment.silent(duration=max_len*1000, frame_rate=output['low'].frame_rate) # length in milliseconds
        for i in output.values():
            util.debug_print(i)
            newfile = newfile.overlay(i)
    
        #if settings.VERBOSE:
        #    for key, val in output.items():
        #        output[key].export(settings.FILENAME + key, format='wav')
    
        output = newfile
    
    print()
    output.export('../data/generated_sound/' + FILENAME, format='wav')
    print('file saved! ' + FILENAME)
    
