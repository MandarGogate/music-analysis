import numpy as np
import scipy.io.wavfile as wav
from scipy.signal import spectrogram
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.ticker import FuncFormatter
###################################
####PLOT WAVE SIGNAL ##############
###################################
import wave
import sys
import numpy as np
spf = wave.open('Python/nto2.wav','r')
wavsignal = spf.readframes(-1)
wavsignal = np.fromstring(wavsignal,'float')
wavfs = spf.getframerate()
###Make time of the plot with seconds
Time = np.linspace(0, len(wavsignal)/wavfs,num=len(wavsignal))
###Plot the signal wave
plt.figure(1)
plt.title('Signal Wave')
plt.plot(Time,wavsignal)
plt.show()


###################################
########END PLOT WAVE SIGNAL#######
###################################
samplerate, samples = wav.read('Python/nto2.wav')
print samples,samplerate
print "Samples", len(samples),'rate : ',samplerate
print 'Total length in seconds :' , ( float(len(samples))/samplerate )
totaltime =  float(len(samples))/samplerate
# the image appears between time points t1 and t2 (secs)
t1, t2 = 1, 20
# determine the corresponding indexes into the samples array
i1, i2 = int(t1 * samplerate), int(t2 * samplerate)
# calculate the spectrogram, Sxx, of the sum of the left and right channels
f, t, Sxx = spectrogram(np.sum(samples[i1:i2,:], axis=1),samplerate, nperseg=512,nfft=2048)
#print f,t,Sxx
print f[0:100]
print t[0:100]
vmax = Sxx.max()
vmin = vmax / 1.e5
plt.pcolormesh(t1 + t, f, Sxx, norm=LogNorm(vmin=vmin, vmax=vmax),
               cmap='YlGnBu_r')

ax = plt.gca()
ax.set_yscale('log')
ax.set_ylim(100, 22000)
ax.set_yticks([])

def seconds_to_minsec(t, pos):
    return '{:d}:{:02d}'.format(int(t // 60), int(t % 60))

xtick_formatter = FuncFormatter(seconds_to_minsec)
ax.xaxis.set_major_formatter(xtick_formatter)

ax.set_xlim(t1, t2)
plt.show()
print samples[2:]


##############################
#########
########
t = np.arange(400)
n = np.zeros((400,), dtype=complex)
n[40:60] = np.exp(1j*np.random.uniform(0, 2*np.pi, (20,)))
s = np.fft.ifft(n)
plt.plot(t, s.real, 'b-', t, s.imag, 'r--')

plt.legend(('real', 'imaginary'))

plt.show()