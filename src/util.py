#!/usr/bin/python3
#
# Copyright © 2017 jared <jared@jared-devstation>
#
# Utilities for the program

import settings

def debug_print(string):
    if settings.VERBOSE:
        print(string)

