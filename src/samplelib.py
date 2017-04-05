#!/usr/bin/python3
#
# Copyright © 2017 jared <jared@jared-devstation>
#

import librosa
import wave, struct
import sys, os, math, random
import analyze

class SampleLib:
    def __init__(self, dir):
        self.directory = dir
        self.lib = {}
        for fname in os.listdir(self.directory):
            if fname[len(fname)-4:len(fname)] == '.wav':
                classifier = analyze.sound_analyze(os.path.abspath('samples/' + fname))
                if classifier in self.lib:
                    self.lib[classifier].append(fname)
                else:
                    self.lib[classifier] = [fname]

    # Given a classifier, returns the file name of a sample which most closely matches the classifier
    def get_sample(self, classifier):
        if classifier in self.lib:
            return random.choice(self.lib[classifier])
        else:
            classifier = int(classifier)
            close_floor = int(list(self.lib.keys())[0])
            close_ceil = int(list(self.lib.keys())[0])
            best_est = int(list(self.lib.keys())[0])
            best_delta = math.fabs(int(classifier) - best_est)
            for key in self.lib.keys():
                key = int(key)
                if key < classifier and key > close_floor:
                    close_floor = key
                elif key < close_ceil:
                    close_ceil = key

                new_delta = math.fabs(classifier - key) 
                if (new_delta < best_delta):
                    best_est = key
                    best_delta = new_delta

        #print(classifier)
        #print(self.lib.keys())
        #print(best_est)
        #print(self.lib[best_est])
        return random.choice(list(self.lib[best_est]))


                

