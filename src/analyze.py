#!/usr/bin/python3
#
# Copyright © 2017 jared <jared@jared-devstation>
#

import math
import sys, os
import wave, struct
import numpy
import librosa
from pydub import AudioSegment, scipy_effects
from PyTransitionMatrix.Markov import TransitionMatrix as tm
import settings
from multiprocessing import Pool

class Analysis:

    def __init__(self):
        self.pool = Pool(settings.THREADS, maxtasksperchild=1)

    def main(self):
        files_arr = []
        if not settings.FREQUENCY_SPLIT:
            for fname in os.listdir('../data/structural'):
                if fname.endswith('.wav') and not ('_low' in fname or '_mid' in fname or '_high' in fname):
                    files_arr.append(os.path.abspath('../data/structural/' + fname))
    
        else:
            for fname in os.listdir('../data/structural'):
                if fname.endswith('.wav'):
                    files_arr.append(os.path.abspath('../data/structural/' + fname))
        self.pool.map(Analysis.analyze, files_arr)
        self.pool.close()
        self.pool.join()

        return Analysis.master_combine()

    @staticmethod
    def analyze(fname):
        print('analyzing ' + fname)
        if settings.FREQUENCY_SPLIT:
            curr_file = AudioSegment.from_file(fname)
    
            low_seg = scipy_effects.low_pass_filter(curr_file, settings.LOW_FREQUENCY_LIM).export(fname + '_low.wav', 'wav')
            mid_seg = scipy_effects.band_pass_filter(curr_file, settings.LOW_FREQUENCY_LIM, settings.HIGH_FREQUENCY_LIM).export(fname + '_mid.wav', 'wav')
            high_seg = scipy_effects.high_pass_filter(curr_file, settings.HIGH_FREQUENCY_LIM).export(fname + '_high.wav', 'wav')

            seg_fnames = [fname + '_low.wav', fname + '_mid.wav', fname + '_high.wav']
    
            for seg in seg_fnames:
                Analysis.analyze_single(seg)
    
            os.remove(fname + '_low.wav')
            os.remove(fname + '_mid.wav')
            os.remove(fname + '_high.wav')
    
        else:
            analyze_single(fname)
    
    # Analyze a single sound file
    # Return the file with the frequency data
    @staticmethod
    def analyze_single(fname):
        print('analyze single: ' + fname)
        # Current file is the one we are iterating over
        current_file = wave.open(fname, 'r')
        length = current_file.getnframes()
        prev_classifier = None
        hash_dict = {}
    
        TEMP_NAME = (str(os.getpid())) +  'temp.wav'
        markov_data = tm(fname) # initialize markov object
        
        # Iterate over current file INTERVAL frames at a time
        pulse_loc = Analysis.pulse_detect(fname, settings.PULSE_TYPE)
        prev_point = 0
        for i in range (0, len(pulse_loc)-1):
            pulse_point = pulse_loc[i] * 1024 # 512 default hop length * halved librosa sample rate
            read_length = pulse_point - prev_point
            working = wave.open(TEMP_NAME, 'w') # open the temp file for writing
            working.setparams(current_file.getparams())
            working.setnframes(0)
            curr_data = current_file.readframes(read_length)
            working.writeframes(curr_data) # save the working frames to the temp file
            working.close()
            prev_point = pulse_point
    
            # Within current 10 frames, perform analysis + write to stochastic matrix
            # This is one of the parameters that can be changed
            classifier = Analysis.sound_analyze(TEMP_NAME, settings.ANALYSIS_MODE)
            
            # write the transition if there is a previous number
            if prev_classifier:
                markov_data.add_transition(prev_classifier, classifier)
    
            prev_classifier = classifier
    
        os.remove(TEMP_NAME)
        return markov_data.save() # save the associated data for that file

    # This function performs the analysis of any given sound.
    # Function can be modified as desired to analyze whatever
    # feature is desired.
    @staticmethod
    def sound_analyze(fname, mode):
        y, sr = librosa.load(fname) # load the temp file
        if mode == 'rolloff':
            feature = librosa.feature.spectral_rolloff(y=y, sr=sr)
            return math.floor(numpy.average(feature))
        elif mode == 'spectral_centroid':
            try:
                feature = librosa.feature.spectral_centroid(y=y, sr=sr)
            except:
                print(fname)
                exit()
            return math.floor(numpy.average(feature))
        elif mode == 'zero_crossing':
            ft = librosa.feature.zero_crossing_rate(y)
            return int(math.ceil(numpy.average(ft.transpose())*100))
        elif mode == 'all':
            rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
            rolloff_key = math.floor(numpy.average(rolloff))
            centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
            centroid_key = math.floor(numpy.average(centroid))
            crossing_rate = librosa.feature.zero_crossing_rate(y)
            crossing_rate_key = int(math.ceil(numpy.average(crossing_rate.transpose())*100))
    
            key = str(rolloff_key) + settings.DELIMITER + str(centroid_key) + settings.DELIMITER + str(crossing_rate_key)
            return key
            
    
    # This function uses Librosa's onset detection to find
    # impulses in the sound, and returns an array of positions
    # in frames
    @staticmethod
    def pulse_detect(fname, mode):
        y, sr = librosa.load(fname)
        if mode == 'onset':
            array = librosa.onset.onset_detect(y, sr)
            return array
        elif mode == 'beat':
            array = librosa.beat.beat_track(y,sr)[1]
            return array

    @staticmethod
    def master_combine():
        if not settings.FREQUENCY_SPLIT:
            markov_master = tm('master_data')
            for fname in os.listdir('../data/structural'):
                if fname.endswith('.json'):
                    markov_master.load_data('../data/structural' + fname)
            markov_master.save()
            return markov_master
        else:
            markov_master_low = tm('../data/generated_data/master_data_low')
            markov_master_mid = tm('../data/generated_data/master_data_mid')
            markov_master_high = tm('../data/generated_data/master_data_high')
            for fname in os.listdir('../data/structural'):
                if not '_norm' in fname:
                    if '_low' in fname:
                        markov_master_low.load_data('../data/structural/' + fname)
                    elif '_mid' in fname:
                        markov_master_mid.load_data('../data/structural/' + fname)
                    elif '_high' in fname:
                        markov_master_high.load_data('../data/structural/' + fname)
    
            markov_master_low.save()
            markov_master_mid.save()
            markov_master_high.save()
            return {"low": markov_master_low, "mid": markov_master_mid, "high": markov_master_high}

def data_gen():
    Analysis().main()

# Load existing data
def load_existing():
    if not settings.FREQUENCY_SPLIT:
        markov_master = tm()
        markov_master.load_data('../data/generated_data/master_data.json')
        return markov_master
    else:
        markov_master_low = tm()
        markov_master_mid = tm()
        markov_master_high = tm()
        markov_master_low.load_data('../data/generated_data/master_data_low.json')
        markov_master_mid.load_data('../data/generated_data/master_data_mid.json')
        markov_master_high.load_data('../data/generated_data/master_data_high.json')
        return {"low": markov_master_low, "mid": markov_master_mid, "high": markov_master_high}

