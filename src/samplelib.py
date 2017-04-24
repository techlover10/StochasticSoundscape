#!/usr/bin/python3
#
# Copyright © 2017 jared <jared@jared-devstation>
#

import librosa
import wave, struct
import json
import sys, os, math, random
import analyze
import settings

class SampleLib:
    def __init__(self, dir, analyzeall=True):
        self.directory = dir
        self.lib = {}
        if analyzeall:
            for fname in os.listdir(self.directory):
                sys.stdout.write('\r')
                sys.stdout.write("classifying " + fname)
                sys.stdout.flush()
                if fname[len(fname)-4:len(fname)] == '.wav':
                    classifier = str(analyze.sound_analyze(os.path.abspath('samples/' + fname), settings.ANALYSIS_MODE))
                    if classifier in self.lib:
                        self.lib[classifier].append(fname)
                    else:
                        self.lib[classifier] = [fname]

            data = json.dumps(self.lib)
            open(os.path.abspath('samples/lib.json'), 'w').write(data)
        else:
            self.lib = json.loads(open(os.path.abspath('samples/lib.json')).read())

    def get_sample(self, classifier):
        if not settings.FREQUENCY_SPLIT:
            return self.get_single_sample(classifier)
        else:
            ret_sample = {}
            for band, target_classifier in classifier.items():
                ret_sample[band] = self.get_single_sample(target_classifier)
            return ret_sample


    # Given a classifier, returns the file name of a sample which most closely matches the classifier
    def get_single_sample(self, classifier):
        if classifier in self.lib:
            return random.choice(self.lib[classifier])
        else:
            classifier = float(classifier)
            close_floor = float(list(self.lib.keys())[0])
            close_ceil = float(list(self.lib.keys())[0])
            best_est = float(list(self.lib.keys())[0])
            best_delta = math.fabs(float(classifier) - best_est)
            for key in self.lib.keys():
                key = float(key)
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
        return random.choice(list(self.lib[str(int(best_est))]))


                

