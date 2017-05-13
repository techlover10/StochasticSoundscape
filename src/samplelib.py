#!/usr/bin/python3
#
# Copyright © 2017 jared <jared@jared-devstation>
#

import librosa
import wave, struct
import json
import sys, os, math, random
from analyze import Analysis
import settings
from samplearr import SampleArr

class SampleLib:
    def __init__(self, dir, analyzeall=True):
        self.directory = dir
        self.lib = {}
        if analyzeall:
            for fname in os.listdir(self.directory):
                if fname.endswith('.wav'):
                    sys.stdout.write('\r' + (' '*int(os.popen('stty size', 'r').read().split()[1])))
                    sys.stdout.write('\r' + "classifying " + fname)
                    sys.stdout.flush()
                    classifier = str(Analysis.sound_analyze(os.path.abspath('../data/samples/' + fname), settings.ANALYSIS_MODE))
                    if classifier in self.lib:
                        self.lib[classifier].append(fname)
                    else:
                        self.lib[classifier] = [fname]

            data = json.dumps(self.lib)
            open(os.path.abspath('../data/samples/lib.json'), 'w').write(data)
        else:
            self.lib = json.loads(open(os.path.abspath('../data/samples/lib.json')).read())

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
        sample_choices = SampleArr(self.classifier_compare, limit=settings.SAMPLE_SELECTION_SIZE)
        for key in self.lib.keys():
            sample_choices.add(key)
        return random.choice(sample_choices.array)

    # Distance function on classifier keys
    @staticmethod
    def classifier_dist(c1, c2):
        if not settings.ANALYSIS_MODE == 'all':
            return math.fabs(float(c2) - float(c1))

        distance = 0
        c1_arr = c1.split(settings.DELIMITER)
        c2_arr = c2.split(settings.DELIMITER)
        for i in range (0, len(c1_arr)):
            distance += math.fabs(float(c1_arr[i]) - float(c2_arr[i]))

        return distance
        

    # Comparison function on classifier keys
    @staticmethod
    def classifier_compare(c1, c2):
        if not settings.ANALYSIS_MODE == 'all':
            if float(c1) > float(c2):
                return 1
            if float(c1) < float(c2):
                return -1
            return 0

        # First case: check number of greaters or less thans
        c1_arr = c1.split(settings.DELIMITER)
        c2_arr = c2.split(settings.DELIMITER)
        num_c1_greater = 0
        for i in range (0, len(c1_arr)):
            if float(c1_arr[i]) > float(c2_arr[i]):
                num_c1_greater += 1

        if num_c1_greater > len(c1)/2:
            return 1

        if num_c1_greater < len(c1)/2:
            return -1

        # Equal number: check magnitude
        c1_greater_dist = 0
        c2_greater_dist = 0
        for i in range (0, len(c1_arr)):
            if float(c1_arr[i]) > float(c2_arr[i]):
                c1_greater_dist += math.fabs(float(c1_arr[i]) > float(c2_arr[i]))
            else:
                c2_greater_dist += math.fabs(float(c1_arr[i]) > float(c2_arr[i]))

        if c1_greater_dist > c2_greater_dist:
            return 1
        elif c2_greater_dist > c1_greater_dist:
            return -1
        else:
            return random.choice([-1, 1])

        




                

