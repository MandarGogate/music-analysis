import matplotlib.pyplot as plt
import numpy as np
import scipy

import sys
import numpy
import struct
import warnings
from scipy.io import wavfile
t=1
t = np.arange(440*t)
_big_endian = True
#convert from bif ti little
with open("nto2.wav", "rb") as f:
    byte = f.read(1)
    while byte != "":
        # Do stuff with byte.
        byte = f.read(1)
        a = byte # for having more successive variables
        #b = a.decode('hex')
        #print repr(b)
        
        
        
#rate,data=scipy.io.wavfile.read('nto.wav')
#t = data
sp = np.fft.fft(np.sin(t))
freq = np.fft.fftfreq(t.shape[-1])
plt.plot(freq, sp.real, freq, sp.imag)
plt.show()

print t,freq,sp.real,sp