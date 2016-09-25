from Tkinter import *
import sounddevice as sd
#hfreq = sd.play(wav_wave)
import numpy as np
import scipy.fftpack as sf
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav


def sound(frequency): 
    sd.default.samplerate = 44100
    time = 4.0
    # Generate time of samples between 0 and two seconds
    samples = np.arange(44100 * time) / 44100.0
    # Recall that a sinusoidal wave of frequency f has formula w(t) = A*sin(2*pi*f*t)
    wave = 10000 * np.sin(2 * np.pi * frequency * samples)
    # Convert it to wav format (16 bits)
    wav_wave = np.array(wave, dtype=np.int16)
    print 'len of the wave is...',len(wav_wave)
    hfreq = sd.play(wav_wave)
    print  'The frequency is ,',frequency
    print samples, 'are the samples----len is ',len(samples)
    print 'Wave from ',str(wave) ,  type(wave)
    print wave[1:100]
    return wav_wave

def playwave(hfreq):
    sd.play(wav_wave)
    return wav_wave


def maxFrequency(X, F_sample, Low_cutoff=80, High_cutoff= 500):
        """ Searching presence of frequencies on a real signal using FFT
        Inputs
        =======
        X: 1-D numpy array, the real time domain audio signal (single channel time series)
        Low_cutoff: float, frequency components below this frequency will not pass the filter (physical frequency in unit of Hz)
        High_cutoff: float, frequency components above this frequency will not pass the filter (physical frequency in unit of Hz)
        F_sample: float, the sampling frequency of the signal (physical frequency in unit of Hz)
        """        
        M = X.size # let M be the length of the time series
        Spectrum = sf.rfft(X, n=M) 
        [Low_cutoff, High_cutoff, F_sample] = map(float, [Low_cutoff, High_cutoff, F_sample])

        #Convert cutoff frequencies into points on spectrum
        [Low_point, High_point] = map(lambda F: F/F_sample * M, [Low_cutoff, High_cutoff])

        maximumFrequency = np.where(Spectrum == np.max(Spectrum[Low_point : High_point])) # Calculating which frequency has max power.

        return maximumFrequency


fs, samples=wav.read("SONG.wav")
samplingRate = 440
hreq=440
wav_wave=sound(hreq)
freq = np.fft.fftfreq(wav_wave.shape[-1])
windows = samples[1,]
window =freq
fullAudio = wav_wave
voiceVector = []
for window in fullAudio: # Run a window of appropriate length across the audio file
    voiceVector.append (maxFrequency( window, samplingRate))
print voiceVector
    


print '^'*3

'''
wav_wave=sound(hreq)
t = np.arange(256)
print 't', t
sp = np.fft.fft(wav_wave)
print type(sp)
print sp[1:50]
print sp.shape
freq = np.fft.fftfreq(wav_wave.shape[-1])
plt.plot(freq, sp.real, freq, sp.imag)
plt.show()
'''
root = Tk() 
CA = Button(root, text = 'Play 232Hz', command = lambda: sound(440))
CB = Button(root, text = 'Play 220hz', command = lambda: sound(432))
CA.pack(),CB.pack()
root.mainloop()



