import numpy as N
import numpy as np
import wave
from scipy import signal
import scipy
from scipy.io import wavfile
from scipy import *
from scipy.io.wavfile import read
from scipy.fftpack import dst, idst

from scipy.fftpack import fft, fftshift,ifft
import matplotlib.pyplot as plt
import pylab
import struct


 
class SoundFile:
   def  __init__(self, signal):
       self.file = wave.open('test.wav', 'wb')
       self.signal = signal
       self.sr = 44100

   def write(self):
       self.file.setparams((1, 2, self.sr, 44100*4, 'NONE', 'noncompressed'))
       self.file.writeframes(self.signal)
       self.file.close()

# let's prepare signal
duration = 4 # seconds
samplerate = 44100 # Hz
samples = duration*samplerate
print(samples)
frequency = 440 # Hz
period = samplerate / float(frequency) # in sample points
omega = N.pi * 2 / period

xaxis = N.arange(int(period),dtype = N.float) * omega
ydata = 16384 * N.sin(xaxis)

signall = N.resize(ydata, (samples,))

ssignal = ''
for i in range(len(signall)):
   ssignal += wave.struct.pack('h',signall[i]) # transform to binary

f = SoundFile(ssignal)
f.write()
print 'file written'


frames , data = scipy.io.wavfile.read('test.wav');
print frames ,data[1], len(data)
duration = len(data) / float(frames)
print duration


bity = frames
data = data




# read audio samples
input_data = read("nto2.wav")
audio = input_data[1]
x=audio
y = fft(x)

freqs = np.fft.fftfreq(len(x[1:1024]))

print freqs[0:10]


# plot the first 1024 samples
plt.plot(audio[0:-1])
print (audio[45866:50010])
# label the axes
plt.ylabel("Amplitude")
plt.xlabel("Time")
# set the title  
plt.title("Sample Wav")
# display the plot
plt.show()

##
##
##
fs = 10e3
N = 1e5
amp = 2 * np.sqrt(2)
noise_power = 0.001 * fs / 2
time = np.arange(N) / fs
freq = np.linspace(1e3, 2e3, N)
x = amp * np.sin(2*np.pi*freq*time)
x += np.random.normal(scale=np.sqrt(noise_power), size=time.shape)

f, t, Sxx = signal.spectrogram(x, fs)
plt.pcolormesh(t, f, Sxx)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()















