#!/usr/bin/env python
# coding: utf-8

debug = 0 # this will toggle printing if you want to debug

# Notebook doesn't require these first two lines, but if importing this script somewhere else,
# shebang and utf-8 encoding lines will tell command line to use python, etc.

'''burst.py

burst.py  - return burst information in a specified time window

Usage: 
    (b_time,b_strength) = burst(soundfile, start_time, end_time)

Arguments:
  soundfile   a soundfile to be analyzed.
  start_time   in seconds, start of chunk to be analyzed
  end_time      in seconds, end of the chunk
  
Assumption
    there is also a file soundfile
'''

# Authors: Keith Johnson (keithjohnson@berkeley.edu)
# 
# Copyright (c) 2015, The Regents of the University of California
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# * Neither the name of the University of California nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import numpy as np
import librosa




#-----------------------------
# This script uses the following functions from the ESPS library for speech processing
#   - hditem: get information from a wav or fea file header
#   - fft: spectral analysis, producing a single spectrum or a spectrogram
#   - melspec: convert an fft spectrum into a "Mel transformed" auditory spectrum
#   - pplain: print values from fea files (spectra) to plain text

# Read about these and other ESPS routines in the Berkeley Phonetics Machine 
# using the 'man' command.   For example:
#       > man fft 
# will show the manual page for the fft routine
#-------------------------

w_score = [0.0,0.0,0.0]
s_score = [0.0,0.0,0.0]
w_time = [0.0,0.0,0.0]
s_time = [0.0,0.0,0.0]

sr = 16000  # downsample to this rate
step_size = 0.005   # 5 ms between spectra

fmin = 300  # lowest frequency of interest
fmax = np.int(sr/2) # the nyquist frequency (sr/2)
n_fft = 1024  # number of FFT coefficients to compute
n_mels = 60  # number of MEL filter bands to calculate

# only need to do this once -- compute the mel frequency filter bank
mel_f = librosa.filters.mel(sr, n_fft=n_fft, n_mels=n_mels, fmin=fmin, fmax=fmax)

def usage():
    print("burst(): expected three arguments: sound_file, start_time, end_time")


# assigns -1 or 1 depending on if neg_peak or pos_peak has a greater magnitude/abs value
def polarity(data):
    neg_peak = 0
    pos_peak = 0
    
    for i in range(len(data)):
        if data[i] < neg_peak:
            neg_peak = data[i]
        if data[i] > pos_peak:
            pos_peak = data[i]
    if -neg_peak > pos_peak:
        return -1
    else:
        return 1
    
# return T or F for if 'j' is a peak or a valley
def is_peak(i,j,k):
    return ((i<j) & (j>k))

def is_valley(i,j,k):
    return ((i>j) & (j<k))

# define stop burst in waveform?
# loop over all the sample data and determine if current value is a peak or valley
def wave_burst(data,step,sr,pol):
    global w_score
    global w_time
    
    w_score[:] = [0.0,0.0,0.0]
    w_time[:] = [0.0,0.0,0.0]
    
    for loc in range(step,len(data)-2):
        if ((pol>0 and is_peak(data[loc],data[loc+1],data[loc+2])) or 
            (pol<0 and is_valley(data[loc],data[loc+1],data[loc+2]))):
                ave=0
                for i in range(step,1,-1):
                    ave += np.fabs(data[loc-i] - data[loc-(i+1)])
                ave /= step
                change = np.fabs(data[loc]-data[loc+1])/ave
                for i in range(3):
                    if change > w_score[i]:
                        if (i<2):
                            w_score[2] = w_score[1]
                            w_time[2] = w_time[1]
                        if (i<1):
                            w_score[1] = w_score[0]
                            w_time[1] = w_time[0]
                        w_score[i] = change
                        w_time[i] = float(loc+1)/sr
                        break
                        
# define burst in spectrogram.  Using librosa Mel filterbank spectrogram
def spec_burst (data, sr, step):
    global s_score 
    global s_time

    s_score[:] = [0,0,0]
    s_time[:] = [0,0,0]
 
    sgram = librosa.stft(data, n_fft=n_fft, hop_length=step, win_length=step)  # get the spectrogram
    melgram = np.log(mel_f.dot(np.abs(sgram))) # convolve the Mel filterbank over the spectrogram

    spec_diffs = np.sum(np.diff(melgram),axis=0)  # get summed difference between adjacent spectra

    for loc in range(len(spec_diffs)):
        for i in range(3):
            if spec_diffs[loc] > s_score[i]:
                if (i<2):
                    s_score[2] = s_score[1]
                    s_time[2] = s_time[1]
                if (i<1):
                    s_score[1] = s_score[0]
                    s_time[1] = s_time[0]
                s_score[i] = spec_diffs[loc]
                s_time[i] = float(loc+1)*step/sr
                break

def burst (soundfile, start_time, end_time):

    global sr
    
    if (start_time>end_time):
        usage()
        return(-1)
     
    step = np.int(step_size * sr)  # step_size as number of waveform samples
    # load in samples, resample to sr
    data, sr = librosa.load(soundfile, sr=sr, offset=start_time, duration=end_time-start_time) 
    
    pol = polarity(data)

    wave_burst(data,step,sr,pol) # looks for big jumps in waveform
    spec_burst(data,sr,step) # looks for big changes in spectrogram
        
    # candidate is a dictionary/dict that will have 0-3 entries depending on loop
    cand = {}

    # loop through the 3 values each in w_time and s_time, find the difference in time
    # if difference is less than 4 ms, 'w' becomes a candidate 0, 1, or 2
    for w in range(3):
        for s in range(3):
            if np.fabs(w_time[w] - s_time[s]) < 0.004: # burst
                cand[w]=s
    maxb = 0 
    loc = -1  
    
    for (w,s) in cand.items():  
        # burst score:  scale on s_score is a hack/approximation
        try:
            b = -1.814 + 0.618*np.log(w_score[w]) + 0.045*s_score[s]
        except:
            b = 0
        if (b>maxb): 
            maxb = b
            loc = w_time[w] + start_time
        if debug:
            print(b)
  
    return (loc,maxb)


if __name__ == "__main__":

    file = 'sx134.wav'
    (loc,maxb) = burst(file,2.169,2.248)
    print(loc,maxb)