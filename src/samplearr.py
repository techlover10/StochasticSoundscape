#!/usr/bin/python3
#
# Copyright © 2017 jared <jared@jared-devstation>
#

# Class defines an array that is designed for managing
# similar samples and keeping them sorted.
# Requires a comparator.  For two items, 
# comparator(a, b) gives some measure of "distance".
# in our measurements.
class SampleArr:
    def __init__(self, target, comparator, limit=10):
        self.array = []
        self.target = target
        self.comparator = comparator
        self.limit = 10

    def add(self, item):
        if len(self.array) < self.limit:
            self.array.append(item)
            self.bubble(len(self.array)-1)
        else:
            if self.comparator(item, self.array[-1]) < 0:
                self.array[len(self.array)-1] = item
                self.bubble(len(self.array)-1)
    
    def bubble(self, index):
        curridx = index
        while curridx > 0:
            item = self.array[curridx]
            prev = self.array[curridx - 1]
            if self.comparator(item, self.target) < self.comparator(prev, self.target): # item is closer to target
                # swap
                self.array[curridx-1] = item
                self.array[curridx] = prev
            curridx -= 1
        

