from math import *
import numpy as np
import sounddevice as sd
import time
from matplotlib import pyplot as plt


samplerate = 44100
time = 3.0
frequency = 20
frequency2 = 440.5

# Generate time of samples between 0 and two seconds
samples = np.arange(samplerate * time) / samplerate
# Recall that a sinusoidal wave of frequency f has formula w(t) = A*sin(2*pi*f*t)
wave = 1000.00 * np.sin(2 * np.pi * frequency * samples)
wave2 = 1000.00 * np.sin(2 * np.pi * frequency2 * samples)


#sound in sec...
leninsec = len(wave)/samplerate
print leninsec

#plot a simple wave
plt.figure(1)
plt.xlim(0,samplerate)
plt.ylim(-1400,1400)
plt.title('Signal Wave...')
plt.plot(wave[1:samplerate])
plt.show()


# Convert it to wav format (16 bits)
wav_wave = np.array(wave, dtype=np.int16)
wav_wave2 = np.array(wave2, dtype=np.int16)
sd.play(wav_wave)
print wav_wave