#!/usr/bin/python3
#
# Copyright © 2017 jared <jared@jared-devstation>
#
# Settings for running the Stochastic Soundscape analysis
# and generation

# Set the duration for the output soundscape, in seconds
DURATION = 30

# Set the default file name for the soundscape
FILENAME = 'soundscape.wav'

# Set whether detailed prints show
VERBOSE = False

# Set number of threads assigned, default is 8
THREADS = 8

# -------------SOUND ANALYSIS SETTINGS---------------------
# Sounds can be analyzed based on a number of different features.
#
# 'all' performs all of the following analyses, and uses a 
# combination of them to determine similarity.
#
# 'rolloff' analyzes sounds based on spectral rolloff, a feature
# which is based on how much energy is in which frequency ranges
# for the sound.
# 
# 'spectral_centroid' analyzes the "center of mass" of a sound,
# which reflects the "brightness" of the sound.
#
# 'zero_crossing' measures the rate at which the sign of the 
# signal changes - that is, the rate at which the signal
# changes from positive to negative.

ANALYSIS_MODE = 'spectral_centroid'

# -------------PULSE DETECTION SETTINGS--------------------
# Sounds will be analyzed based on detecting spikes in the 
# sound - in order to both split soundscapes into musique concrete
# and to analyze data from soundscapes, the program will split
# sounds into samples to be analyzed.
#
# 'onset' finds spikes based on detected impulses in the sound,
# splitting according to this.
#
# 'beat' finds spikes based on detected impulses, along with
# some amount of inference based on the overall tempo of the 
# beats in the sound file.

PULSE_TYPE = 'onset'

# -------------FREQUENCY SEPARATION SETTINGS---------------
# Stochastic Soundscape is able to analyze sounds and separate
# samples by multiple bands.  This works by splitting the samples
# into low-frequency, mid-frequency, and high-frequency sounds for 
# analysis.  

# Enable or disable the analysis of samples by multiple bands
FREQUENCY_SPLIT = True

# Set the upper limit for the low-frequency band, in hz
LOW_FREQUENCY_LIM = 6000

# Set the lower limit for the high-frequency band, in hz
HIGH_FREQUENCY_LIM = 12000

########### DEV SETTINGS: USE CAUTION WHEN MODIFYING ###########

# Set the delimeter used to separate multiple features in 
# category keys
DELIMITER = ';'
