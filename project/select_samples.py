#!/usr/bin/python3
#
# Copyright © 2017 jared <jared@jared-devstation>
#

import csv, random
from collections import OrderedDict

STATE_ARR = {
        "Alabama",
        "Alaska",
        "Arizona",
        "Arkansas",
        "California",
        "Colorado",
        "Connecticut",
        "Delaware",
        "Florida",
        "Georgia",
        "Hawaii",
        "Idaho",
        "Illinois",
        "Indiana",
        "Iowa",
        "Kansas",
        "Kentucky",
        "Louisiana",
        "Maine",
        "Maryland",
        "Massachusetts",
        "Michigan",
        "Minnesota",
        "Mississippi",
        "Missouri",
        "Montana",
        "Nebraska",
        "Nevada",
        "New Hampshire",
        "New Jersey",
        "New Mexico",
        "New York",
        "North Carolina",
        "North Dakota",
        "Ohio",
        "Oklahoma",
        "Oregon",
        "Pennsylvania",
        "Rhode Island",
        "South Carolina",
        "South Dakota",
        "Tennessee",
        "Texas",
        "Utah",
        "Vermont",
        "Virginia",
        "Washington",
        "West Virginia",
        "Wisconsin",
        "Wyoming"
}

a = open('search.csv', 'r')
selection = csv.reader(a)
possibilities = {}
for state in STATE_ARR:
    possibilities[state] = []
# Note: Row 12 corresponds to the state
for row in selection:
    curr_state = row[12]
    if curr_state in possibilities.keys():
        possibilities[curr_state].append(row)

selections = {}
for state, opts in possibilities.items():
    if len(opts) <1:
        continue
    longest_dur = 0
    best_option = random.choice(opts)
    for opt in opts:
        try:
            dur = float(opt[27])
            if dur > longest_dur:
                best_option = opt
        except:
            continue
    selections[best_option[12]] = best_option

selections = OrderedDict(sorted(selections.items(), key=lambda t: str.lower(t[0])))
for state, selection in selections.items():
    #print(selection[0] + (' ') + selection[12] + (' ') + (selection[27]))
    print(selection[0])



