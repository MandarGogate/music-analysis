import numpy as np
import scipy.io.wavfile as wav
from scipy.signal import spectrogram
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.ticker import FuncFormatter

samplerate, samples = wav.read('nto2.wav')

# the image appears between time points t1 and t2 (secs)
t1, t2 = 0, 14
# determine the corresponding indexes into the samples array
i1, i2 = int(t1 * samplerate), int(t2 * samplerate)
# calculate the spectrogram, Sxx, of the sum of the left and right channels
f, t, Sxx = spectrogram(np.sum(samples[i1:i2,:], axis=1), samplerate, nperseg=512, nfft=4096)
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