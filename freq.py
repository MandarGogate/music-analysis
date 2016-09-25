import numpy as np
import sounddevice as sd
from scipy.signal import fftconvolve, kaiser, decimate
from numpy.fft import rfft
from numpy import argmax, mean, diff, log, copy, arange
from scipy.io import wavfile
import scipy


def freq_from_fft(signal, fs):
    """Estimate frequency from peak of FFT
    Pros: Accurate, usually even more so than zero crossing counter 
    (1000.000004 Hz for 1000 Hz, for instance).  Due to parabolic 
    interpolation being a very good fit for windowed log FFT peaks?
    https://ccrma.stanford.edu/~jos/sasp/Quadratic_Interpolation_Spectral_Peaks.html
    Accuracy also increases with signal length
    """
    N = len(signal)
    # Compute Fourier transform of windowed signal
    windowed = signal * kaiser(N, 100)
    f = rfft(windowed)
    # Find the peak and interpolate to get a more accurate peak
    i_peak = argmax(abs(f)) # Just use this value for less-accurate result
    
    # Convert to equivalent frequency
    return fs * i_peak / N # Hz


rate , data  = scipy.io.wavfile.read('nto2.wav', mmap=False)
print data ,rate 
 
signal = np.array(data, dtype=float)
fourier = np.fft.fft(signal)

n = signal.size

frew = freq_from_fft(signal[:-1][0], n)
print frew
print fourier



timestep = 0.1
freq = np.fft.fftfreq(n, d=timestep)
freq
print abs(freq[0]-freq[1])

'''for i in range(1,222000,1000):
    print data[i]'''
