#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
#from common import analyze_channels
#from fdint import parabolic as parabolic
from numpy.fft import rfft
from numpy import argmax, mean, diff, log, copy, arange
from matplotlib.mlab import find
from scipy.signal import fftconvolve, kaiser, decimate
from time import time
import scipy.io.wavfile as wav
from numpy import array_equal, polyfit, sqrt, mean, absolute, log10, arange
from scipy.stats import gmean


def load(filename):
    """
    Load a wave file and return the signal, sample rate and number of channels.
    Can be any format that libsndfile supports, like .wav, .flac, etc.
    """
    wave_file = Sndfile(filename, 'r')
    signal = wave_file.read_frames(wave_file.nframes)
    channels = wave_file.channels
    sample_rate = wave_file.samplerate
    return signal, sample_rate, channels


def analyze_channels(filename, function):
    """
    Given a filename, run the given analyzer function on each channel of the
    file
    """
    signal, sample_rate, channels = load(filename)
    print 'Analyzing "' + filename + '"...'

    if channels == 1:
        # Monaural
        function(signal, sample_rate)
    elif channels == 2:
        # Stereo
        if array_equal(signal[:, 0], signal[:, 1]):
            print '-- Left and Right channels are identical --'
            function(signal[:, 0], sample_rate)
        else:
            print '-- Left channel --'
            function(signal[:, 0], sample_rate)
            print '-- Right channel --'
            function(signal[:, 1], sample_rate)
    else:
        # Multi-channel
        for ch_no, channel in enumerate(signal.transpose()):
            print '-- Channel %d --' % (ch_no + 1)
            function(channel, sample_rate)


def rms_flat(a):
    """
    Return the root mean square of all the elements of *a*, flattened out.
    """
    return sqrt(mean(absolute(a)**2))


def dB(level):
    """
    Return a level in decibels.
    """
    return 20 * log10(level)


def spectral_flatness(spectrum):
    """
    The spectral flatness is calculated by dividing the geometric mean of
    the power spectrum by the arithmetic mean of the power spectrum
    I'm not sure if the spectrum should be squared first...
    """
    return gmean(spectrum)/mean(spectrum)

def freq_from_crossings(signal, fs):
    """Estimate frequency by counting zero crossings
    
    Pros: Fast, accurate (increasing with signal length).  Works well for long 
    low-noise sines, square, triangle, etc.
    
    Cons: Doesn't work if there are multiple zero crossings per cycle, 
    low-frequency baseline shift, noise, etc.
    
    """
    # Find all indices right before a rising-edge zero crossing
    indices = find((signal[1:] >= 0) & (signal[:-1] < 0))
    
    # Naive (Measures 1000.185 Hz for 1000 Hz, for instance)
    #crossings = indices
    
    # More accurate, using linear interpolation to find intersample
    # zero-crossings (Measures 1000.000129 Hz for 1000 Hz, for instance)
    crossings = [i - signal[i] / (signal[i+1] - signal[i]) for i in indices]
    
    # Some other interpolation based on neighboring points might be better. Spline, cubic, whatever
    
    return fs / mean(diff(crossings))


def parabolic(f, x):
    """
    Quadratic interpolation for estimating the true position of an
    inter-sample maximum when nearby samples are known.
    f is a vector and x is an index for that vector.
    Returns (vx, vy), the coordinates of the vertex of a parabola that goes
    through point x and its two neighbors.
    Example:
    Defining a vector f with a local maximum at index 3 (= 6), find local
    maximum if points 2, 3, and 4 actually defined a parabola.
    In [3]: f = [2, 3, 1, 6, 4, 2, 3, 1]
    In [4]: parabolic(f, argmax(f))
    Out[4]: (3.2142857142857144, 6.1607142857142856)
    """
    xv = 1/2. * (f[x-1] - f[x+1]) / (f[x-1] - 2 * f[x] + f[x+1]) + x
    yv = f[x] - 1/4. * (f[x-1] - f[x+1]) * (xv - x)
    return (xv, yv)


def parabolic_polyfit(f, x, n):
    """
    Use the built-in polyfit() function to find the peak of a parabola
    f is a vector and x is an index for that vector.
    n is the number of samples of the curve used to fit the parabola.
    """
    a, b, c = polyfit(arange(x-n//2, x+n//2+1), f[x-n//2:x+n//2+1], 2)
    xv = -0.5 * b/a
    yv = a * xv**2 + b * xv + c
    return (xv, yv)





def freq_from_fft(signal, fs):
    """Estimate frequency from peak of FFT
    
    Pros: Accurate, usually even more so than zero crossing counter 
    (1000.000004 Hz for 1000 Hz, for instance).  Due to parabolic 
    interpolation being a very good fit for windowed log FFT peaks?
    https://ccrma.stanford.edu/~jos/sasp/Quadratic_Interpolation_Spectral_Peaks.html
    Accuracy also increases with signal length
    
    Cons: Doesn't find the right value if harmonics are stronger than
    fundamental, which is common.
    
    """
    N = len(signal)
    
    # Compute Fourier transform of windowed signal
    windowed = signal * kaiser(N, 100)
    f = rfft(windowed)
    # Find the peak and interpolate to get a more accurate peak
    i_peak = argmax(abs(f)) # Just use this value for less-accurate result
    i_interp = parabolic(log(abs(f)), i_peak)[0]
    print str(fs * i_interp / N)
    # Convert to equivalent frequency
    return fs * i_interp / N # Hz


def freq_from_autocorr(signal, fs):
    """Estimate frequency using autocorrelation
    
    Pros: Best method for finding the true fundamental of any repeating wave, 
    even with strong harmonics or completely missing fundamental
    
    Cons: Not as accurate, doesn't work for inharmonic things like musical 
    instruments, this implementation has trouble with finding the true peak
    
    """
    # Calculate autocorrelation (same thing as convolution, but with one input
    # reversed in time), and throw away the negative lags
    signal -= mean(signal) # Remove DC offset
    corr = fftconvolve(signal, signal[::-1], mode='full')
    corr = corr[len(corr)/2:]
    
    # Find the first low point
    d = diff(corr)
    start = find(d > 0)[0]
    
    # Find the next peak after the low point (other than 0 lag).  This bit is 
    # not reliable for long signals, due to the desired peak occurring between 
    # samples, and other peaks appearing higher.
    i_peak = argmax(corr[start:]) + start
    i_interp = parabolic(corr, i_peak)[0]
    print str(fs / i_interp)
    return fs / i_interp
    


def freq_from_hps(signal, fs):
    """Estimate frequency using harmonic product spectrum
    
    Low frequency noise piles up and overwhelms the desired peaks
    """
    N = len(signal)
    signal -= mean(signal) # Remove DC offset
    
    # Compute Fourier transform of windowed signal
    windowed = signal * kaiser(N, 100)
    
    # Get spectrum
    X = log(abs(rfft(windowed)))
    
    # Downsample sum logs of spectra instead of multiplying
    hps = copy(X)
    for h in arange(2, 9): # TODO: choose a smarter upper limit
        dec = decimate(X, h)
        hps[:len(dec)] += dec
    
    # Find the peak and interpolate to get a more accurate peak
    i_peak = argmax(hps[:len(dec)])
    i_interp = parabolic(hps, i_peak)[0]
    print str(fs * i_interp / N)
    # Convert to equivalent frequency
    return fs * i_interp / N # Hz



fs, signal=wav.read("la-note.wav")
print signal.shape
print signal[:,1]




freq_from_fft(signal[:,1], fs)
freq_from_hps(signal[:,1], fs)
freq_from_autocorr(signal[:,1], fs)
























