import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy.fftpack import fft
import numpy as np
 
rate, data = wav.read('nto2.wav')
 
fft_out = fft(data)
print fft_out
print fft_out.shape
#matplotlib inline
plt.plot(data, np.abs(fft_out[:,0]))
plt.show()