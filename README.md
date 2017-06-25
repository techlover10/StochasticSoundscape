# Stochastic Soundscape
Stochastic Soundscape program which probabilistically generates random soundscapes based on input data and a set of samples.

## Important notes
This program is only compatible with .wav files - future updates may extend compatibility to other audio files, but .wav is the most universal and for this reason I have restricted it to only recognize these files.  Those who wish to modify it to include compatibility with other files may do so at their own risk.  In this documentation, "any audio file" refers only to compatible .wav files.

**KNOWN ISSUE** - Throughout my use of this program I have occasionally encountered .wav files with corrupted metadata which WILL cause this program to freeze.  There is nothing I can do about this.  To use these files with Stochastic Soundscape, the following steps must be performed:
- Download [Audacity](http://www.audacityteam.org/) if you do not already have it.
- Open the file in Audacity
- Go to File -> Export and save the file again as a .wav file

The new .wav file should have proper metadata.  I have yet to find an explanation for this issue; if I find a better solution, this README will be updated.

## Dependencies
- Python 3.5
- [pydub](https://github.com/jiaaro/pydub)
- scipy
- [Librosa](http://nbviewer.jupyter.org/github/librosa/librosa/blob/master/examples/LibROSA%20demo.ipynb)
- ffmpeg (Linux library - for Ubuntu, this can be obtained with `sudo apt-get install ffmpeg`)
- (This program has only been tested on Ubuntu 16.04 - other platforms should be supported but have not been tested)

## Getting Started
Once the dependencies are installed, and the repository is cloned, you are ready to begin generating soundscapes!

To install on a standard Ubuntu distro, you should be able to run the following commands:
- `sudo apt-get install python3`
- `sudo pip3 install -r requirements.txt`
- `sudo apt-get install ffmpeg

To initialize the submodule dependencies, run the following:
`git submodule update --init --recursive`

### Usage
Stochastic Soundscape uses two types of source material, **structural** and **samples**.  **Structural** data is analyzed to generate the stochastic transition matrix from which the **samples** will be assembled.

#### Quick Start
Simply place structural material in the `data/structural` folder, and a collection of sound samples in the `data/samples/` folder (this works better with short samples).  Then, run ./main.py (on a Bash terminal) or `python3 main.py` (on any system with the proper dependencies installed, in theory - again, this is untested).

#### Sound Clipper
Don't have enough short samples?  No problem.  Stochastic Soundscape includes a script which allows samples to be generated from any longer source audio file.  Simply copy any audio files into the folder `data/sound_clipper_sources/` and run `./runclipper.py` (or `python3 runclipper.py`).  This will chop the audio into tiny samples and place them in the `samples/` folder.

#### Quickgen
`main.py` runs the structural analysis, the sample analysis, and the generation process.  Each of these can be run individually with `runanalysis.py`, `libgen.py`, and `quickgen.py`.  For example, if you've changed the sample set but you have not changed your data, you might wish to run `libgen.py` and `quickgen.py` to save time.

#### File Names
Both `quickgen.py` and `main.py` take one argument: a file name.  If the file name is not specified, it will default to whatever is set in `settings.py`.  Otherwise, the output file will be whatever is specified (so `./quickgen.py my-soundscape.wav` will generate a file called `my-soundscape.wav` in the generated_sound folder.


## Technical Details and Structure

### Analysis

The analysis occurs in `analyze.py`.  This contains all of the functions that analyze an audio file.  The function `sound_analyze` analyzes a sound file and returns a classifier key of some sort.  To modify how sounds are analyzed, this is the function that should be changed.  As long as this function returns a classifier which is a number of some sort, the program will continue to function.  I plan to eventually make this more general, such that any valid dictionary key will be accepted (for this, a comparator will have to be implemented for evaluating similarity of classifiers).

### Sound and Sample Library
`audio.py` contains all functions specifically for manipulating audio.  Currently, it only contains one function used to append a sample with a crossfade.  `samplelib.py` defines the object which manages the library of samples from which soundscapes are generated.  This manages both classifier comparison (the "similarity" evaluation mentioned earlier) and the dictionary of samples.

### Sound Clipper
`sound_clipper.py` is a standalone file which clips longer sounds into short samples for generative purposes.

### (EXPERIMENTAL) Endless Soundscapes
`endless.py` is a rough experiment in generating an endless soundscape based on the same stochastic process.  In its current implementation, it cannot handle buffering - for this reason, the resulting soundscape sounds choppy and disconnected.  I have not figured out the best way to implement this with a buffer in Python; when I do, this will be updated.

