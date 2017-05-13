#!/usr/bin/python3
#
# Copyright © 2017 jared <jared@jared-devstation>
#

# Class defines an array that is designed for managing
# similar samples and keeping them sorted.
# Requires a comparator.  For two items, 
# comparator(a, b) < 0 implies that a < b
# in our measurements.
class SampleArr:
    def __init__(self, comparator, limit=10):
        self.array = []
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
            if self.comparator(prev, item) > 0:
                # swap
                self.array[curridx-1] = item
                self.array[curridx] = prev
            curridx -= 1
        

