import numpy as np
from scikits.audiolab import Sndfile

f = Sndfile('nto2.wav', 'r')

# Sndfile instances can be queried for the audio file meta-data
fs = f.samplerate
nc = f.channels
enc = f.encoding
end = f.endianness

# Reading is straightfoward
data = f.read_frames(1000)
print f
# This reads the next 1000 frames, e.g. from 1000 to 2000, but as single precision
data_float = f.read_frames(1000, dtype=np.float32)