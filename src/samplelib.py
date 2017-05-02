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
                sys.stdout.write('\r' + (' '*int(os.popen('stty size', 'r').read().split()[1])))
                sys.stdout.write('\r' + "classifying " + fname)
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
            close_floor = list(self.lib.keys())[0]
            close_ceil = list(self.lib.keys())[0]
            best_est = list(self.lib.keys())[0]
            best_delta = self.classifier_dist(classifier, best_est)
            for key in self.lib.keys():
                if self.classifier_compare(key, classifier) < 0 and self.classifier_compare(key, close_floor) > 0:
                    close_floor = key
                elif self.classifier_compare(key, close_ceil) < 0:
                    close_ceil = key

                new_delta = self.classifier_dist(classifier, key) 
                if (new_delta < best_delta):
                    best_est = key
                    best_delta = new_delta

        return random.choice(list(self.lib[best_est]))

    # Distance function on classifier keys
    def classifier_dist(self, c1, c2):
        if not settings.ANALYSIS_MODE == 'all':
            return math.fabs(float(c2) - float(c1))

        distance = 0
        c1_arr = c1.split(settings.DELIMITER)
        c2_arr = c2.split(settings.DELIMITER)
        for i in range (0, len(c1_arr)):
            distance += math.fabs(float(c1_arr[i]) - float(c2_arr[i]))

        return distance
        

    # Comparison function on classifier keys
    def classifier_compare(self, c1, c2):
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

        




                

